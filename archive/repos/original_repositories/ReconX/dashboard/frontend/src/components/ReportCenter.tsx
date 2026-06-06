import { useState, useEffect } from "react";

export function ReportCenter() {
  const [reports, setReports] = useState<any[]>([]);

  const fetchReports = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/reports");
      if (res.ok) {
        const data = await res.json();
        setReports(data.reports);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchReports();
    const interval = setInterval(fetchReports, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="card">
      <h2>Report Center</h2>
      <div className="report-grid">
        {reports.length === 0 ? <p>No reports generated yet.</p> : null}
        {reports.map((report, i) => (
          <div key={i} className="report-card">
            <h3>{report.name}</h3>
            <p>Size: {(report.size / 1024).toFixed(2)} KB</p>
            <p>Created: {new Date(report.created_at * 1000).toLocaleString()}</p>
            <a 
              href={`http://127.0.0.1:8000/api/v1/reports/${report.name}`} 
              target="_blank" 
              rel="noreferrer"
              className="btn-download"
            >
              Download Report
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
