import { useState } from 'react'
import useSWR from 'swr'
import { fetchers, doctorApi, agentsApi } from '@/services/api'
import { Badge } from '@/components/Badge'
import type { DoctorCheck } from '@/types'

function doctorBadge(status: true | false | null) {
  if (status === true)  return 'green'
  if (status === false) return 'red'
  return 'yellow'
}
function doctorLabel(status: true | false | null) {
  if (status === true)  return 'PASS'
  if (status === false) return 'FAIL'
  return 'WARN'
}

export default function Settings() {
  const { data: agents }    = useSWR('agents',    fetchers.agents,    { revalidateOnFocus: false })
  const { data: workflows } = useSWR('workflows', fetchers.workflows, { revalidateOnFocus: false })

  const [doctorData, setDoctorData]   = useState<{ summary: any; checks: DoctorCheck[] } | null>(null)
  const [running,    setRunning]      = useState(false)
  const [tab,        setTab]          = useState<'config' | 'doctor' | 'plugins' | 'workflows'>('config')

  const runDoctor = async () => {
    setRunning(true)
    try {
      const result = await doctorApi.run()
      setDoctorData(result)
      setTab('doctor')
    } catch (e) {
      console.error(e)
    } finally {
      setRunning(false)
    }
  }

  const tabStyle = (t: string) => ({
    padding: '8px 18px',
    fontSize: 12,
    fontWeight: 600,
    letterSpacing: 0.5,
    cursor: 'pointer',
    borderRadius: 'var(--radius-sm)',
    border: 'none',
    fontFamily: 'var(--font)',
    background: tab === t ? 'var(--red-dim)' : 'transparent',
    color: tab === t ? 'var(--red)' : 'var(--text-dim)',
    transition: 'all .15s',
  })

  return (
    <div className="page">
      <div className="page-header flex-between">
        <div>
          <div className="page-title">⚙️ Settings</div>
          <div className="page-subtitle">Platform configuration and health diagnostics</div>
        </div>
        <button
          className="btn btn-primary"
          onClick={runDoctor}
          disabled={running}
        >
          {running ? <><div className="spinner" style={{ width: 12, height: 12 }} /> Running…</> : '🩺 Run Doctor'}
        </button>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 24, background: 'var(--bg2)', padding: 4, borderRadius: 'var(--radius)', border: '1px solid var(--border)', width: 'fit-content' }}>
        {(['config', 'doctor', 'plugins', 'workflows'] as const).map((t) => (
          <button key={t} style={tabStyle(t)} onClick={() => setTab(t)}>
            {t.charAt(0).toUpperCase() + t.slice(1)}
            {t === 'doctor' && doctorData && (
              <span style={{ marginLeft: 6 }}>
                {doctorData.summary.failed > 0
                  ? <Badge variant="red">{doctorData.summary.failed}</Badge>
                  : <Badge variant="green">✓</Badge>}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Config tab */}
      {tab === 'config' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div className="card">
            <div className="card-header"><span className="card-title">API Connection</span></div>
            <div className="card-body">
              {[
                ['API Base URL',     window.location.origin + '/api/v1'],
                ['WebSocket URL',    `ws://${window.location.host}/ws/events`],
                ['Dashboard Port',  window.location.port || '80'],
                ['React Build',     (import.meta as any).env?.MODE ?? 'production'],
              ].map(([label, value]) => (
                <div key={label} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border)', alignItems: 'center' }}>
                  <span style={{ color: 'var(--text-dim)', fontSize: 12 }}>{label}</span>
                  <span style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--blue)' }}>{value}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-header"><span className="card-title">Quick Links</span></div>
            <div className="card-body" style={{ display: 'flex', flexWrap: 'wrap', gap: 10 }}>
              {[
                ['/docs',           'API Docs (Swagger)'],
                ['/api/v1/doctor',  'Doctor JSON'],
                ['/api/v1/projects/', 'Projects API'],
                ['/api/v1/tasks/',  'Tasks API'],
                ['/api/v1/reports/', 'Reports API'],
              ].map(([href, label]) => (
                <a key={href} href={href} target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm">
                  {label} ↗
                </a>
              ))}
            </div>
          </div>

          <div className="card">
            <div className="card-header"><span className="card-title">Environment</span></div>
            <div className="card-body">
              <p style={{ color: 'var(--text-dim)', fontSize: 12, lineHeight: 2 }}>
                To configure API keys (OpenAI, Shodan, VirusTotal), edit{' '}
                <code style={{ fontFamily: 'var(--mono)', color: 'var(--blue)' }}>.env</code>{' '}
                in the ReconX root directory. The LLM analysis plugin automatically falls back
                to rule-based analysis if no API key is present.
              </p>
              <div style={{ marginTop: 12 }}>
                {['OPENAI_API_KEY', 'SHODAN_API_KEY', 'VIRUSTOTAL_API_KEY'].map((k) => (
                  <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid var(--border)' }}>
                    <span style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--text-dim)' }}>{k}</span>
                    <Badge variant="dim">not configured</Badge>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Doctor tab */}
      {tab === 'doctor' && (
        !doctorData ? (
          <div className="empty-state">
            <div className="empty-icon">🩺</div>
            <div className="empty-title">Doctor not run yet</div>
            <div className="empty-sub">Click "Run Doctor" to check system health</div>
            <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={runDoctor} disabled={running}>
              {running ? '⏳ Running…' : '🩺 Run Doctor'}
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {/* Summary */}
            <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
              {[
                { label: 'Passed', value: doctorData.summary.passed, color: 'var(--green)' },
                { label: 'Failed', value: doctorData.summary.failed, color: 'var(--red)' },
                { label: 'Warnings', value: doctorData.summary.warned, color: 'var(--yellow)' },
                { label: 'Total', value: doctorData.summary.total, color: 'var(--text)' },
              ].map((s) => (
                <div key={s.label} className="stat-card" style={{ minWidth: 100 }}>
                  <div className="stat-number" style={{ color: s.color, fontSize: 28 }}>{s.value}</div>
                  <div className="stat-label">{s.label}</div>
                </div>
              ))}
            </div>

            {/* Checks */}
            <div className="card">
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Check</th>
                      <th>Status</th>
                      <th>Detail</th>
                      <th>Fix</th>
                    </tr>
                  </thead>
                  <tbody>
                    {doctorData.checks.map((c, i) => (
                      <tr key={i}>
                        <td style={{ fontWeight: 600 }}>{c.name}</td>
                        <td><Badge variant={doctorBadge(c.status)}>{doctorLabel(c.status)}</Badge></td>
                        <td className="mono" style={{ fontSize: 11, maxWidth: 280, wordBreak: 'break-all' }}>{c.detail}</td>
                        <td style={{ fontSize: 11, color: 'var(--yellow)' }}>{c.fix ?? ''}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )
      )}

      {/* Plugins tab */}
      {tab === 'plugins' && (
        <div className="card">
          <div className="card-header">
            <span className="card-title">Registered Agents / Plugins</span>
            <span style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--text-dim)' }}>
              {(agents ?? []).length} loaded
            </span>
          </div>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr><th>Name</th><th>Status</th></tr>
              </thead>
              <tbody>
                {(agents ?? []).length === 0 ? (
                  <tr><td colSpan={2}><div className="loading"><div className="spinner" /></div></td></tr>
                ) : (
                  (agents ?? []).map((a) => (
                    <tr key={a.name}>
                      <td style={{ fontFamily: 'var(--mono)' }}>{a.name}</td>
                      <td><Badge variant="green">{a.status}</Badge></td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Workflows tab */}
      {tab === 'workflows' && (
        <div className="card">
          <div className="card-header"><span className="card-title">Available Workflows</span></div>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr><th>File</th><th>Name</th><th>Mode</th><th>Steps</th><th>Description</th></tr>
              </thead>
              <tbody>
                {(workflows ?? []).length === 0 ? (
                  <tr><td colSpan={5}><div className="loading"><div className="spinner" /></div></td></tr>
                ) : (
                  (workflows ?? []).map((w) => (
                    <tr key={w.file}>
                      <td className="mono" style={{ color: 'var(--blue)' }}>{w.file}</td>
                      <td style={{ fontWeight: 600 }}>{w.name}</td>
                      <td><Badge variant="dim">{w.mode}</Badge></td>
                      <td className="mono" style={{ color: 'var(--text-dim)' }}>{w.steps}</td>
                      <td style={{ color: 'var(--text-dim)', fontSize: 12 }}>{w.description}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
