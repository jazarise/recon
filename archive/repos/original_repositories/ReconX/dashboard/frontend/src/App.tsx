import { lazy, Suspense, useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Sidebar } from '@/components/Sidebar'
import { Navbar }  from '@/components/Navbar'
import { useWebSocket } from '@/hooks/useWebSocket'
import { useAppStore } from '@/store'
import '@/styles/globals.css'

// Lazy-load pages for code-splitting
const Dashboard = lazy(() => import('@/pages/Dashboard'))
const Projects  = lazy(() => import('@/pages/Projects'))
const Assets    = lazy(() => import('@/pages/Assets'))
const Reports   = lazy(() => import('@/pages/Reports'))
const Logs      = lazy(() => import('@/pages/Logs'))
const Settings  = lazy(() => import('@/pages/Settings'))

function PageLoader() {
  return (
    <div className="loading" style={{ paddingTop: 80 }}>
      <div className="spinner" />
      <span>Loading…</span>
    </div>
  )
}

function NotificationToast() {
  const notifications     = useAppStore((s) => s.notifications)
  const dismissNotification = useAppStore((s) => s.dismissNotification)

  if (notifications.length === 0) return null

  return (
    <div
      style={{
        position: 'fixed',
        bottom: 24,
        right: 24,
        zIndex: 2000,
        display: 'flex',
        flexDirection: 'column',
        gap: 8,
        maxWidth: 360,
      }}
    >
      {notifications.map((n) => (
        <div
          key={n.id}
          style={{
            background: 'var(--bg2)',
            border: `1px solid ${
              n.level === 'success' ? 'rgba(48,209,88,.4)'
              : n.level === 'error' ? 'rgba(229,57,53,.4)'
              : 'var(--border2)'
            }`,
            borderRadius: 'var(--radius)',
            padding: '12px 16px',
            boxShadow: '0 8px 32px rgba(0,0,0,.5)',
            display: 'flex',
            alignItems: 'flex-start',
            gap: 10,
            animation: 'slideUp .2s ease',
          }}
        >
          <span style={{ fontSize: 16, flexShrink: 0, marginTop: 1 }}>
            {n.level === 'success' ? '✓' : n.level === 'error' ? '✗' : 'ℹ'}
          </span>
          <span style={{
            fontSize: 13,
            color: n.level === 'success' ? 'var(--green)'
                 : n.level === 'error'   ? 'var(--red)'
                 : 'var(--text)',
            flex: 1,
          }}>
            {n.message}
          </span>
          <button
            onClick={() => dismissNotification(n.id)}
            style={{
              background: 'none', border: 'none', color: 'var(--text-dim)',
              cursor: 'pointer', fontSize: 16, lineHeight: 1, padding: 0, flexShrink: 0,
            }}
          >
            ×
          </button>
        </div>
      ))}
    </div>
  )
}

function AppLayout() {
  useWebSocket()

  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Navbar />
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/"         element={<Dashboard />} />
            <Route path="/projects" element={<Projects  />} />
            <Route path="/assets"   element={<Assets    />} />
            <Route path="/reports"  element={<Reports   />} />
            <Route path="/logs"     element={<Logs      />} />
            <Route path="/settings" element={<Settings  />} />
            <Route path="*"         element={
              <div className="page">
                <div className="empty-state" style={{ paddingTop: 80 }}>
                  <div className="empty-icon">404</div>
                  <div className="empty-title">Page not found</div>
                </div>
              </div>
            } />
          </Routes>
        </Suspense>
      </div>
      <NotificationToast />
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  )
}
