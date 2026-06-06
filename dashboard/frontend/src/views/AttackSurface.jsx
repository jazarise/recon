import React from 'react';
import { Activity, ShieldAlert, Zap } from 'lucide-react';

export default function AttackSurface({ stats }) {
  return (
    <div>
      <h2>Attack Surface</h2>
      <div className="text-sm" style={{ marginBottom: '20px' }}>Real-time Recon Intelligence</div>
      
      <input type="text" className="search-bar" placeholder="Search graph..." />
      
      <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <div className="glass-panel metric-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Activity size={20} color="#3b82f6" />
            <span className="text-sm">Total Assets</span>
          </div>
          <div className="metric-value">{stats.assets || 0}</div>
        </div>
        
        <div className="glass-panel metric-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <ShieldAlert size={20} color="#ef4444" />
            <span className="text-sm">Critical Findings</span>
          </div>
          <div className="metric-value" style={{ color: '#ef4444' }}>{stats.findings || 0}</div>
        </div>

        <div className="glass-panel metric-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Zap size={20} color="#eab308" />
            <span className="text-sm">Risk Score</span>
          </div>
          <div className="metric-value" style={{ color: '#eab308' }}>{stats.risk_score || 'A+'}</div>
        </div>
      </div>
    </div>
  );
}
