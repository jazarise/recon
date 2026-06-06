export function ExecutionMonitor({ events }: { events: any[] }) {
  // Extract only standard events
  const logEvents = events.filter(e => 
    ["workflow.started", "plugin_started", "plugin_progress", "plugin_completed", "plugin_failed", "workflow.completed"].includes(e.event)
  );

  return (
    <div className="card">
      <h2>Live Execution Monitor</h2>
      <div className="terminal">
        {logEvents.length === 0 && <div>Waiting for execution events...</div>}
        {logEvents.map((e, idx) => (
          <div key={idx} className="terminal-line">
            <span className="timestamp">[{new Date().toLocaleTimeString()}]</span>
            <span className={`event-type ${e.event.replace(".", "-")}`}> {e.event}</span>
            <span className="event-detail">
              {e.payload.workflow_name ? ` ${e.payload.workflow_name}` : ""}
              {e.payload.plugin ? ` ${e.payload.plugin}` : ""}
              {e.payload.target ? ` on ${e.payload.target}` : ""}
              {e.payload.message ? ` - ${e.payload.message}` : ""}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
