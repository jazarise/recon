import React, { useState, useEffect } from 'react';

export default function Scans() {
  const [scans, setScans] = useState([]);
  const [target, setTarget] = useState('');
  const [workflow, setWorkflow] = useState('passive');

  useEffect(() => {
    fetch('http://localhost:8001/api/scans/')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
            setScans(data.data.scans || []);
        }
      })
      .catch(console.error);
  }, []);

  const handleLaunch = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8001/api/scans/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target, workflow })
      });
      const data = await res.json();
      if (data.success) {
        setScans([...scans, { id: data.data.scan_id, target, workflow, status: 'running' }]);
      } else {
        alert("Validation error: " + JSON.stringify(data.errors));
      }
    } catch (e) {
      alert("Error starting scan: " + e.message);
    }
  };

  return (
    <div style={{ padding: '2rem', color: 'white', width: '100%' }}>
      <h2>Scan Management</h2>
      
      <form onSubmit={handleLaunch} style={{ marginBottom: '2rem', display: 'flex', gap: '1rem' }}>
        <input 
          placeholder="Target (e.g. example.com)" 
          value={target} 
          onChange={e => setTarget(e.target.value)} 
          style={{ padding: '0.5rem', borderRadius: '4px' }}
        />
        <select value={workflow} onChange={e => setWorkflow(e.target.value)} style={{ padding: '0.5rem', borderRadius: '4px' }}>
            <option value="passive">Passive Recon</option>
            <option value="active">Active Scan</option>
        </select>
        <button type="submit" style={{ padding: '0.5rem 1rem', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Launch Scan
        </button>
      </form>

      <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #444' }}>
            <th style={{ padding: '0.5rem' }}>ID</th>
            <th style={{ padding: '0.5rem' }}>Target</th>
            <th style={{ padding: '0.5rem' }}>Workflow</th>
            <th style={{ padding: '0.5rem' }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {scans.map(scan => (
            <tr key={scan.id} style={{ borderBottom: '1px solid #333' }}>
              <td style={{ padding: '0.5rem' }}>{scan.id.split('-')[0]}...</td>
              <td style={{ padding: '0.5rem' }}>{scan.target}</td>
              <td style={{ padding: '0.5rem' }}>{scan.workflow}</td>
              <td style={{ padding: '0.5rem' }}>
                <span style={{ 
                    padding: '0.2rem 0.5rem', 
                    borderRadius: '999px', 
                    background: scan.status === 'running' ? '#eab308' : '#22c55e',
                    fontSize: '0.8rem'
                }}>
                    {scan.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
