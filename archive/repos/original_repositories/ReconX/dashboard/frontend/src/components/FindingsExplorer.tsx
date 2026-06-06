import { useState, useEffect } from "react";

export function FindingsExplorer() {
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    const fetchFindings = async () => {
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
    fetchFindings();
    const interval = setInterval(fetchFindings, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="card">
      <h2>Findings Explorer</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>Target</th>
            <th>Workflow</th>
            <th>Status</th>
            <th>Findings Count</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {history.filter(h => h.status === "completed").map((run, i) => (
            <tr key={i}>
              <td>{run.target}</td>
              <td>{run.workflow_name}</td>
              <td><span className={`badge ${run.status}`}>{run.status}</span></td>
              <td>{run.findings_count} findings</td>
              <td><button className="btn-small">View Details</button></td>
            </tr>
          ))}
          {history.filter(h => h.status === "completed").length === 0 && (
            <tr><td colSpan={5}>No completed workflows with findings yet.</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
