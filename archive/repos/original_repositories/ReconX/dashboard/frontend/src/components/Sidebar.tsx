import { NavLink, useLocation } from 'react-router-dom'
import { useAppStore } from '@/store'

interface NavEntry {
  to: string
  icon: string
  label: string
  section?: string
}

const NAV: NavEntry[] = [
  { to: '/',         icon: '⬛', label: 'Dashboard',  section: 'Main' },
  { to: '/projects', icon: '📁', label: 'Projects',   section: 'Main' },
  { to: '/assets',   icon: '🔍', label: 'Assets',     section: 'Intelligence' },
  { to: '/reports',  icon: '📄', label: 'Reports',    section: 'Intelligence' },
  { to: '/logs',     icon: '📋', label: 'Live Logs',  section: 'System' },
  { to: '/settings', icon: '⚙️', label: 'Settings',   section: 'System' },
]

export function Sidebar() {
  const location   = useLocation()
  const wsConnected = useAppStore((s) => s.wsConnected)

  let lastSection = ''

  return (
    <aside className="sidebar">
      {/* Logo */}
      <NavLink to="/" className="sidebar-logo" style={{ textDecoration: 'none' }}>
        <div>
          <div className="sidebar-logo-text">RECONX</div>
          <div className="sidebar-logo-sub">Recon Platform</div>
        </div>
      </NavLink>

      {/* Nav */}
      <nav className="sidebar-nav">
        {NAV.map((item) => {
          const showSection = item.section && item.section !== lastSection
          if (showSection) lastSection = item.section!
          const isActive =
            item.to === '/'
              ? location.pathname === '/'
              : location.pathname.startsWith(item.to)

          return (
            <div key={item.to}>
              {showSection && (
                <div className="nav-section-label">{item.section}</div>
              )}
              <NavLink
                to={item.to}
                className={`nav-item ${isActive ? 'active' : ''}`}
                style={{ textDecoration: 'none' }}
              >
                <span className="nav-item-icon">{item.icon}</span>
                <span>{item.label}</span>
              </NavLink>
            </div>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <div
          className="sidebar-version flex-center gap-8"
          style={{ marginBottom: 6 }}
        >
          <span
            className="status-dot"
            style={{ background: wsConnected ? 'var(--green)' : 'var(--red)' }}
          />
          <span style={{ color: wsConnected ? 'var(--green)' : 'var(--red)' }}>
            {wsConnected ? 'Live' : 'Offline'}
          </span>
        </div>
        <div className="sidebar-version">v1.0.0 · ReconX</div>
      </div>
    </aside>
  )
}
