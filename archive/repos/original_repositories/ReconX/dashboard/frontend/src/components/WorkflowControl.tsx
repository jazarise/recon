import { useState, useEffect } from "react";

export function WorkflowControl({ events }: { events: any[] }) {
  const [history, setHistory] = useState<any[]>([]);
  const [target, setTarget] = useState("google.com");
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/workflows/history");
      if (res.ok) {
        const data = await res.json();
        setHistory(data.history);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [events]);

  const launchGolden = async () => {
    setLoading(true);
    try {
      await fetch("http://127.0.0.1:8000/api/v1/workflows/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target, workflow: "golden" })
      });
      setTimeout(fetchHistory, 1000);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Workflow Control Panel</h2>
      <div className="input-group">
        <input 
          value={target} 
          onChange={(e) => setTarget(e.target.value)} 
          placeholder="Target Domain/IP" 
        />
        <button onClick={launchGolden} disabled={loading}>
          Launch Golden Workflow
        </button>
      </div>

      <table className="data-table">
        <thead>
          <tr>
            <th>Workflow ID</th>
            <th>Name</th>
            <th>Target</th>
            <th>Status</th>
            <th>Findings</th>
          </tr>
        </thead>
        <tbody>
          {history.length === 0 ? <tr><td colSpan={5}>No history</td></tr> : null}
          {history.map((run, i) => (
            <tr key={i}>
              <td>{run.workflow_id.slice(0, 8)}...</td>
              <td>{run.workflow_name}</td>
              <td>{run.target}</td>
              <td><span className={`badge ${run.status}`}>{run.status.toUpperCase()}</span></td>
              <td>{run.findings_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
