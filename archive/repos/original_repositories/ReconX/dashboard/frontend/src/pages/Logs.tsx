import { useEffect, useRef, useState } from 'react'
import { useAppStore } from '@/store'
import type { LogLevel } from '@/types'

const LEVEL_OPTIONS: LogLevel[] = ['info', 'warn', 'error', 'debug']

function levelColor(level: LogLevel) {
  switch (level) {
    case 'error': return 'var(--red)'
    case 'warn':  return 'var(--yellow)'
    case 'info':  return 'var(--blue)'
    case 'debug': return 'var(--text-muted)'
  }
}

export default function Logs() {
  const logs        = useAppStore((s) => s.logs)
  const clearLogs   = useAppStore((s) => s.clearLogs)
  const wsConnected = useAppStore((s) => s.wsConnected)

  const [filter,     setFilter]     = useState<LogLevel | 'all'>('all')
  const [autoScroll, setAutoScroll] = useState(true)
  const [search,     setSearch]     = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (autoScroll && bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs, autoScroll])

  const filtered = logs.filter((l) => {
    const matchLevel  = filter === 'all' || l.level === filter
    const matchSearch = !search || l.message.toLowerCase().includes(search.toLowerCase()) ||
                        l.source.toLowerCase().includes(search.toLowerCase())
    return matchLevel && matchSearch
  })

  const counts = logs.reduce<Record<string, number>>((acc, l) => {
    acc[l.level] = (acc[l.level] ?? 0) + 1
    return acc
  }, {})

  return (
    <div className="page">
      <div className="page-header flex-between">
        <div>
          <div className="page-title">📋 Live Logs</div>
          <div className="page-subtitle">
            Real-time event stream via WebSocket
            {' · '}
            <span style={{ color: wsConnected ? 'var(--green)' : 'var(--red)' }}>
              {wsConnected ? '● Live' : '○ Disconnected'}
            </span>
          </div>
        </div>
        <div className="btn-group">
          <button
            className={`btn btn-sm ${autoScroll ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setAutoScroll((v) => !v)}
          >
            {autoScroll ? '⬇ Auto-scroll On' : '⬇ Auto-scroll Off'}
          </button>
          <button className="btn btn-secondary btn-sm" onClick={clearLogs}>
            Clear
          </button>
        </div>
      </div>

      {/* Level counters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 20, flexWrap: 'wrap' }}>
        {LEVEL_OPTIONS.map((l) => (
          <div
            key={l}
            style={{
              background: 'var(--bg2)',
              border: `1px solid ${filter === l ? levelColor(l) : 'var(--border)'}`,
              borderRadius: 'var(--radius)',
              padding: '8px 16px',
              cursor: 'pointer',
              transition: 'border-color .15s',
              textAlign: 'center',
              minWidth: 80,
            }}
            onClick={() => setFilter((prev) => (prev === l ? 'all' : l))}
          >
            <div style={{ fontSize: 20, fontWeight: 700, fontFamily: 'var(--mono)', color: levelColor(l) }}>
              {counts[l] ?? 0}
            </div>
            <div style={{ fontSize: 10, letterSpacing: 1.5, textTransform: 'uppercase', color: 'var(--text-dim)' }}>
              {l}
            </div>
          </div>
        ))}
        <div
          style={{
            background: 'var(--bg2)',
            border: `1px solid ${filter === 'all' ? 'var(--text-dim)' : 'var(--border)'}`,
            borderRadius: 'var(--radius)',
            padding: '8px 16px',
            cursor: 'pointer',
            textAlign: 'center',
            minWidth: 80,
          }}
          onClick={() => setFilter('all')}
        >
          <div style={{ fontSize: 20, fontWeight: 700, fontFamily: 'var(--mono)', color: 'var(--text)' }}>
            {logs.length}
          </div>
          <div style={{ fontSize: 10, letterSpacing: 1.5, textTransform: 'uppercase', color: 'var(--text-dim)' }}>
            total
          </div>
        </div>
      </div>

      {/* Search bar */}
      <div className="search-bar">
        <div className="search-input-wrap">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            className="form-input"
            placeholder="Filter log messages…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {/* Log viewer */}
      <div className="log-viewer">
        <div className="log-toolbar">
          <span style={{ fontSize: 11, color: 'var(--text-dim)' }}>
            Showing {filtered.length} / {logs.length} entries
          </span>
          {!wsConnected && (
            <span style={{ fontSize: 11, color: 'var(--yellow)', marginLeft: 12 }}>
              ⚠ WebSocket disconnected — reconnecting…
            </span>
          )}
        </div>
        <div className="log-body" id="log-body">
          {filtered.length === 0 ? (
            <div className="empty-state" style={{ padding: '40px' }}>
              <div className="empty-icon">📋</div>
              <div className="empty-title">
                {logs.length === 0 ? 'Waiting for events…' : 'No matching entries'}
              </div>
              <div className="empty-sub">
                {logs.length === 0 && 'Events will appear here in real time when a scan runs'}
              </div>
            </div>
          ) : (
            filtered.map((entry) => (
              <div key={entry.id} className={`log-line ${entry.level}`}>
                <span className="log-ts">
                  {new Date(entry.timestamp).toLocaleTimeString('en-GB', {
                    hour: '2-digit', minute: '2-digit', second: '2-digit',
                  })}
                </span>
                <span className={`log-level ${entry.level}`}>{entry.level}</span>
                <span className="log-msg">
                  <span style={{ color: 'var(--text-muted)', marginRight: 8 }}>
                    [{entry.source}]
                  </span>
                  {entry.message}
                </span>
              </div>
            ))
          )}
          <div ref={bottomRef} />
        </div>
      </div>
    </div>
  )
}
