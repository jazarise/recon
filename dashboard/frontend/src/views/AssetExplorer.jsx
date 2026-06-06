import React from 'react';
import { X, Server, Globe, Hash } from 'lucide-react';

export default function AssetExplorer({ node, onClose }) {
  if (!node) return null;

  return (
    <div className="glass-panel" style={{ marginTop: '20px', padding: '15px', position: 'relative' }}>
      <button 
        onClick={onClose} 
        style={{ position: 'absolute', top: '10px', right: '10px', background: 'none', border: 'none', color: 'white', cursor: 'pointer' }}
      >
        <X size={18} />
      </button>
      
      <h3 style={{ marginBottom: '10px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '10px' }}>Asset Details</h3>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Hash size={16} color="#94a3b8" />
          <span className="text-sm">ID:</span>
          <span style={{ fontSize: '0.875rem' }}>{node.id}</span>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Globe size={16} color="#94a3b8" />
          <span className="text-sm">Value:</span>
          <span style={{ fontSize: '0.875rem', fontWeight: 'bold' }}>{node.label}</span>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Server size={16} color="#94a3b8" />
          <span className="text-sm">Type:</span>
          <span style={{ fontSize: '0.75rem', padding: '2px 8px', borderRadius: '12px', background: 'rgba(59, 130, 246, 0.2)', color: '#3b82f6' }}>
            {node.group?.toUpperCase() || 'UNKNOWN'}
          </span>
        </div>
      </div>
      
      {node.color === '#ef4444' && (
         <div style={{ marginTop: '15px', padding: '10px', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
            <h4 style={{ color: '#ef4444', marginBottom: '5px' }}>Critical Finding</h4>
            <div className="text-sm">This node has been flagged with a critical severity exposure. Immediate attention required.</div>
         </div>
      )}
    </div>
  );
}
