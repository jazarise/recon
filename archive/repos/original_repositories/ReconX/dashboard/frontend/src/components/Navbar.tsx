import { useLocation } from 'react-router-dom'
import { useAppStore } from '@/store'

const PAGE_NAMES: Record<string, string> = {
  '/':         'Dashboard',
  '/projects': 'Projects',
  '/assets':   'Assets',
  '/reports':  'Reports',
  '/logs':     'Live Logs',
  '/settings': 'Settings',
}

export function Navbar() {
  const location    = useLocation()
  const wsConnected = useAppStore((s) => s.wsConnected)
  const jobs        = useAppStore((s) => s.activeJobs)
  const pageName    = PAGE_NAMES[location.pathname] ?? 'ReconX'
  const runningCount = [...jobs.values()].filter((j) => j.status === 'running').length

  return (
    <header className="navbar">
      <div className="navbar-breadcrumb">
        <span>reconx</span>
        <span className="navbar-breadcrumb-sep">/</span>
        <span className="navbar-breadcrumb-current">{pageName.toLowerCase()}</span>
      </div>

      <div className="navbar-spacer" />

      {runningCount > 0 && (
        <div className="flex-center gap-8" style={{ marginRight: 8 }}>
          <div className="spinner" />
          <span style={{ fontSize: 12, color: 'var(--yellow)' }}>
            {runningCount} scan{runningCount > 1 ? 's' : ''} running
          </span>
        </div>
      )}

      <div className="navbar-status">
        <span
          className={`status-dot ${wsConnected ? '' : 'offline'}`}
          style={{ background: wsConnected ? 'var(--green)' : 'var(--text-muted)' }}
        />
        <span>{wsConnected ? 'Live' : 'Polling'}</span>
      </div>
    </header>
  )
}
