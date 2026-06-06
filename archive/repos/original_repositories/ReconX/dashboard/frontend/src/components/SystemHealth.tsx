export function SystemHealth({ wsStatus, events }: { wsStatus: string, events: any[] }) {
  const activeWorkflows = events.filter(e => e.event === "workflow.started").length 
    - events.filter(e => e.event === "workflow.completed" || e.event === "workflow.failed").length;

  return (
    <div className="card">
      <h2>System Health</h2>
      <div className="metrics-grid">
        <div className="metric-box">
          <h3>WebSocket</h3>
          <p className={wsStatus === "Connected" ? "text-success" : "text-error"}>{wsStatus}</p>
        </div>
        <div className="metric-box">
          <h3>Active Workflows</h3>
          <p>{Math.max(0, activeWorkflows)}</p>
        </div>
        <div className="metric-box">
          <h3>API Status</h3>
          <p className="text-success">Online</p>
        </div>
        <div className="metric-box">
          <h3>Total Events</h3>
          <p>{events.length}</p>
        </div>
      </div>
    </div>
  );
}
