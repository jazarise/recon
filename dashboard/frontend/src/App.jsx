import React, { useState, useEffect } from 'react';
import GraphViewer from './components/GraphViewer';
import AttackSurface from './views/AttackSurface';
import AssetExplorer from './views/AssetExplorer';

export default function App() {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [stats, setStats] = useState({ assets: 0, findings: 0, risk_score: 'A+' });
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    // Initial fetch
    fetch('http://localhost:8000/api/graph/attack-surface')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error("API Error", err));

    // Connect WebSocket for live events
    const ws = new WebSocket('ws://localhost:8000/ws');
    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.event === 'node.added') {
            setGraphData(prev => ({
                ...prev,
                nodes: [...prev.nodes, msg.data]
            }));
            setStats(prev => ({...prev, assets: prev.assets + 1}));
        }
      } catch (e) {
        console.error(e);
      }
    };
    return () => ws.close();
  }, []);

  // Generate some dummy data to show immediately
  useEffect(() => {
     setGraphData({
        nodes: [
            { id: '1', label: 'example.com', group: 'domain', val: 5 },
            { id: '2', label: 'api.example.com', group: 'subdomain', val: 3 },
            { id: '3', label: '104.16.10.5', group: 'ip', val: 3 },
            { id: '4', label: 'CVE-2024-XXXX', group: 'vuln', val: 8, color: '#ef4444' }
        ],
        edges: [
            { source: '1', target: '2' },
            { source: '2', target: '3' },
            { source: '3', target: '4' }
        ]
     });
  }, []);

  return (
    <div className="app-container">
      <div className="sidebar glass-panel">
        <AttackSurface stats={stats} />
        {selectedNode && <AssetExplorer node={selectedNode} onClose={() => setSelectedNode(null)} />}
      </div>
      
      <div className="main-content">
        <GraphViewer graphData={graphData} onNodeClick={setSelectedNode} />
      </div>
    </div>
  );
}
