import { useAppStore } from '@/store'
import { Badge, statusBadge } from './Badge'

export function ScanProgress() {
  const jobs = useAppStore((s) => s.activeJobs)
  const active = [...jobs.values()]

  if (active.length === 0) return null

  return (
    <div style={{ marginBottom: 24 }}>
      {active.map((job) => (
        <div key={job.workflowId} className="card" style={{ marginBottom: 12 }}>
          <div className="card-header">
            <span className="card-title" style={{ fontSize: 11 }}>
              {job.status === 'running' ? '▶' : job.status === 'completed' ? '✓' : '✗'} Scan
            </span>
            <span
              className="mono"
              style={{ fontSize: 12, color: 'var(--blue)', marginLeft: 8 }}
            >
              {job.target}
            </span>
            <div style={{ marginLeft: 'auto' }}>
              <Badge variant={statusBadge(job.status)}>{job.status}</Badge>
            </div>
          </div>
          <div className="card-body" style={{ padding: '12px 20px' }}>
            {job.status === 'running' && (
              <div className="progress-bar" style={{ marginBottom: 10 }}>
                <div
                  className="progress-fill"
                  style={{
                    width: '100%',
                    background:
                      'linear-gradient(90deg, var(--red) 0%, var(--orange) 50%, var(--red) 100%)',
                    backgroundSize: '200% 100%',
                    animation: 'shimmer 1.5s linear infinite',
                  }}
                />
              </div>
            )}
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              {job.steps.map((step, i) => (
                <div
                  key={i}
                  className="badge badge-dim mono"
                  style={{ fontSize: 10 }}
                >
                  {step}
                </div>
              ))}
            </div>
            <div
              style={{
                fontSize: 11,
                color: 'var(--text-muted)',
                marginTop: 8,
                fontFamily: 'var(--mono)',
              }}
            >
              Started: {new Date(job.startedAt).toLocaleTimeString()} · Profile:{' '}
              {job.profile}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
