import React, { useState, useEffect } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import GraphViewer from './components/GraphViewer';
import AttackSurface from './views/AttackSurface';
import AssetExplorer from './views/AssetExplorer';
import Scans from './views/Scans';

function Overview() {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [stats, setStats] = useState({ assets: 0, findings: 0, risk_score: 'A+' });
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8001/api/graph/attack-surface')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error("API Error", err));

    const ws = new WebSocket('ws://localhost:8001/ws');
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
      } catch (e) {}
    };
    return () => ws.close();
  }, []);

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
    <>
      <div className="sidebar glass-panel">
        <AttackSurface stats={stats} />
        {selectedNode && <AssetExplorer node={selectedNode} onClose={() => setSelectedNode(null)} />}
      </div>
      <div className="main-content">
        <GraphViewer graphData={graphData} onNodeClick={setSelectedNode} />
      </div>
    </>
  );
}

export default function App() {
  return (
    <div className="app-container" style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <nav style={{ padding: '1rem', background: '#1e1e1e', display: 'flex', gap: '1rem' }}>
        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>Overview</Link>
        <Link to="/scans" style={{ color: 'white', textDecoration: 'none' }}>Scans</Link>
      </nav>
      <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/scans" element={<Scans />} />
        </Routes>
      </div>
    </div>
  );
}
