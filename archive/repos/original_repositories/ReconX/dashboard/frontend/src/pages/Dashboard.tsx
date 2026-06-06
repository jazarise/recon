import { useState } from 'react'
import useSWR from 'swr'
import {
  AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
} from 'recharts'
import { fetchers, workflowsApi } from '@/services/api'
import { useAppStore } from '@/store'
import { StatCard } from '@/components/Badge'
import { ScanProgress } from '@/components/ScanProgress'
import { Badge, statusBadge } from '@/components/Badge'
import type { ScanProfile } from '@/types'
import { SCAN_PROFILES } from '@/types'

function fmt(iso: string | null) {
  if (!iso) return '—'
  return new Date(iso).toLocaleString('en-GB', { dateStyle: 'short', timeStyle: 'short' })
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: 'var(--bg3)', border: '1px solid var(--border2)',
      borderRadius: 6, padding: '8px 12px', fontSize: 12,
    }}>
      <div style={{ color: 'var(--text-dim)', marginBottom: 4 }}>{label}</div>
      {payload.map((p: any) => (
        <div key={p.name} style={{ color: p.color }}>{p.name}: {p.value}</div>
      ))}
    </div>
  )
}

export default function Dashboard() {
  const { data: projects, isLoading: loadProj } = useSWR('projects', fetchers.projects, { refreshInterval: 10000 })
  const { data: tasks,    isLoading: loadTask } = useSWR('tasks',    fetchers.tasks,    { refreshInterval: 5000 })
  const { data: reports,  isLoading: loadRep  } = useSWR('reports',  fetchers.reports,  { refreshInterval: 10000 })
  const { data: agents                         } = useSWR('agents',   fetchers.agents,   { refreshInterval: 30000 })

  const [target,   setTarget]   = useState('')
  const [projName, setProjName] = useState('')
  const [profile,  setProfile]  = useState<ScanProfile>('basic')
  const [scanning, setScanning] = useState(false)
  const { notify, startJob } = useAppStore()

  // Build mini scan history chart from tasks
  const chartData = (tasks ?? []).slice(0, 14).reverse().map((t, i) => ({
    name: `#${i + 1}`,
    completed: t.status === 'completed' ? 1 : 0,
    failed:    t.status === 'failed'    ? 1 : 0,
  }))

  // Scan type breakdown
  const profileCounts = (projects ?? []).reduce<Record<string, number>>((acc, _) => {
    acc['scanned'] = (acc['scanned'] || 0) + 1
    return acc
  }, {})

  const handleQuickScan = async () => {
    if (!target.trim()) { notify('Enter a target first', 'error'); return }
    const project = projName.trim() || `scan_${Date.now()}`
    setScanning(true)
    const wid = `qs-${Date.now()}`
    startJob({ workflowId: wid, target: target.trim(), profile, startedAt: new Date().toISOString() })
    try {
      await workflowsApi.run({ target: target.trim(), project, profile })
      notify(`Scan complete: ${target}`, 'success')
    } catch (e) {
      notify(`Scan failed: ${String(e)}`, 'error')
    } finally {
      setScanning(false)
    }
  }

  const runningJobs  = (tasks ?? []).filter((t) => t.status === 'running').length
  const completedJobs= (tasks ?? []).filter((t) => t.status === 'completed').length

  return (
    <div className="page">
      <div className="page-header">
        <div className="page-title">⬛ Dashboard</div>
        <div className="page-subtitle">Platform overview and quick scan launcher</div>
      </div>

      {/* Active scan progress banners */}
      <ScanProgress />

      {/* Stat cards */}
      <div className="stat-grid">
        <StatCard label="Projects"      value={(projects ?? []).length}  color="var(--blue)"   icon="📁" loading={loadProj} />
        <StatCard label="Reports"       value={(reports  ?? []).length}  color="var(--purple)" icon="📄" loading={loadRep}  />
        <StatCard label="Running Jobs"  value={runningJobs}              color="var(--yellow)" icon="▶"  loading={loadTask} />
        <StatCard label="Completed"     value={completedJobs}            color="var(--green)"  icon="✓"  loading={loadTask} />
        <StatCard label="Agents Ready"  value={(agents ?? []).length}    color="var(--orange)" icon="🤖" />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 28 }}>
        {/* Scan history chart */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Scan History</span>
            <span style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--text-dim)' }}>
              Last {chartData.length} jobs
            </span>
          </div>
          <div className="card-body" style={{ padding: '16px 16px 8px' }}>
            {chartData.length === 0 ? (
              <div className="empty-state" style={{ padding: '30px 0' }}>
                <div className="empty-title">No scan history yet</div>
              </div>
            ) : (
              <ResponsiveContainer width="100%" height={180}>
                <AreaChart data={chartData} margin={{ top: 4, right: 4, bottom: 0, left: -20 }}>
                  <defs>
                    <linearGradient id="gGreen" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#30d158" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#30d158" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="gRed" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#e53935" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#e53935" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                  <XAxis dataKey="name" tick={{ fill: 'var(--text-dim)', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: 'var(--text-dim)', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <Tooltip content={<CustomTooltip />} />
                  <Area type="monotone" dataKey="completed" stroke="#30d158" fill="url(#gGreen)" strokeWidth={2} name="Completed" />
                  <Area type="monotone" dataKey="failed"    stroke="#e53935" fill="url(#gRed)"   strokeWidth={2} name="Failed" />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Project status breakdown */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Project Status</span>
          </div>
          <div className="card-body" style={{ padding: '16px 16px 8px' }}>
            {(projects ?? []).length === 0 ? (
              <div className="empty-state" style={{ padding: '30px 0' }}>
                <div className="empty-title">No projects yet</div>
              </div>
            ) : (
              <ResponsiveContainer width="100%" height={180}>
                <BarChart
                  data={[
                    { name: 'New',     count: (projects ?? []).filter((p) => p.status === 'new').length },
                    { name: 'Scanned', count: (projects ?? []).filter((p) => p.status === 'scanned').length },
                    { name: 'Legacy',  count: (projects ?? []).filter((p) => p.status === 'legacy').length },
                  ]}
                  margin={{ top: 4, right: 4, bottom: 0, left: -20 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                  <XAxis dataKey="name" tick={{ fill: 'var(--text-dim)', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: 'var(--text-dim)', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="count" fill="var(--red)" radius={[3, 3, 0, 0]} name="Projects" />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {/* Quick Scan */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">🚀 Quick Scan</span>
          </div>
          <div className="card-body">
            <div className="form-group">
              <label className="form-label">Target</label>
              <input
                type="text"
                className="form-input"
                placeholder="example.com / 192.168.1.1"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleQuickScan()}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Project Name <span style={{ color: 'var(--text-muted)' }}>(optional)</span></label>
              <input
                type="text"
                className="form-input"
                placeholder="Auto-generated if empty"
                value={projName}
                onChange={(e) => setProjName(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Profile</label>
              <select
                className="form-select"
                value={profile}
                onChange={(e) => setProfile(e.target.value as ScanProfile)}
              >
                {SCAN_PROFILES.map((p) => (
                  <option key={p.value} value={p.value}>
                    {p.label} — {p.description} (~{p.estimated})
                  </option>
                ))}
              </select>
            </div>
            <button
              className="btn btn-primary"
              style={{ width: '100%' }}
              onClick={handleQuickScan}
              disabled={scanning || !target.trim()}
            >
              {scanning ? (
                <><div className="spinner" style={{ width: 12, height: 12 }} /> Running…</>
              ) : '▶ Launch Scan'}
            </button>
          </div>
        </div>

        {/* Recent tasks */}
        <div className="card">
          <div className="card-header">
            <span className="card-title">Recent Jobs</span>
            <span style={{ marginLeft: 'auto', fontSize: 11, color: 'var(--text-dim)' }}>
              {(tasks ?? []).length} total
            </span>
          </div>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Target</th>
                  <th>Status</th>
                  <th>Started</th>
                </tr>
              </thead>
              <tbody>
                {loadTask ? (
                  <tr><td colSpan={3}><div className="loading"><div className="spinner" /></div></td></tr>
                ) : (tasks ?? []).length === 0 ? (
                  <tr>
                    <td colSpan={3}>
                      <div className="empty-state" style={{ padding: '24px' }}>
                        <div className="empty-sub">No jobs yet</div>
                      </div>
                    </td>
                  </tr>
                ) : (
                  (tasks ?? []).slice(0, 8).map((t) => (
                    <tr key={t.workflow_id}>
                      <td className="mono" style={{ maxWidth: 140, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {t.target}
                      </td>
                      <td><Badge variant={statusBadge(t.status)}>{t.status}</Badge></td>
                      <td className="mono" style={{ fontSize: 11, color: 'var(--text-dim)' }}>
                        {fmt(t.started_at)}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}
