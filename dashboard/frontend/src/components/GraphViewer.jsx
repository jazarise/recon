import React, { useRef, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

export default function GraphViewer({ graphData, onNodeClick }) {
  const fgRef = useRef();

  const handleNodeClick = useCallback(node => {
    onNodeClick(node);
    // Center the camera on the node
    fgRef.current.centerAt(node.x, node.y, 1000);
    fgRef.current.zoom(4, 2000);
  }, [onNodeClick]);

  return (
    <div className="graph-container" style={{ width: '100%', height: '100%' }}>
      <ForceGraph2D
        ref={fgRef}
        graphData={graphData}
        nodeLabel="label"
        nodeAutoColorBy="group"
        nodeRelSize={6}
        onNodeClick={handleNodeClick}
        linkDirectionalArrowLength={3.5}
        linkDirectionalArrowRelPos={1}
        backgroundColor="#0b0f19"
        nodeCanvasObject={(node, ctx, globalScale) => {
          const label = node.label;
          const fontSize = 12/globalScale;
          ctx.font = `${fontSize}px Sans-Serif`;
          ctx.fillStyle = node.color || '#3b82f6';
          ctx.beginPath();
          ctx.arc(node.x, node.y, node.val || 4, 0, 2 * Math.PI, false);
          ctx.fill();
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillStyle = 'white';
          ctx.fillText(label, node.x, node.y + (node.val || 4) + fontSize);
        }}
      />
    </div>
  );
}
