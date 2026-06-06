import { useState } from 'react'
import useSWR from 'swr'
import { fetchers, findingsApi } from '@/services/api'
import { AssetTable } from '@/components/AssetTable'

export default function Assets() {
  const { data: projects } = useSWR('projects', fetchers.projects)
  const [selected, setSelected] = useState('')

  const projectName = selected || (projects?.[0]?.name ?? '')

  const { data: assets, isLoading } = useSWR(
    projectName ? `findings/${projectName}` : null,
    () => findingsApi.list(projectName).then((r) => r.assets),
    { refreshInterval: 20000 },
  )

  // Counts by type
  const typeCounts = (assets ?? []).reduce<Record<string, number>>((acc, a) => {
    acc[a.type] = (acc[a.type] ?? 0) + 1
    return acc
  }, {})

  return (
    <div className="page">
      <div className="page-header flex-between">
        <div>
          <div className="page-title">🔍 Assets</div>
          <div className="page-subtitle">Correlated intelligence from scan results</div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <label className="form-label" style={{ margin: 0 }}>Project:</label>
          <select
            className="form-select"
            value={selected || projectName}
            onChange={(e) => setSelected(e.target.value)}
            style={{ width: 200 }}
          >
            {(projects ?? []).length === 0 ? (
              <option value="">No projects</option>
            ) : (
              (projects ?? []).map((p) => (
                <option key={p.name} value={p.name}>
                  {p.name} — {p.target}
                </option>
              ))
            )}
          </select>
        </div>
      </div>

      {/* Mini type summary */}
      {Object.keys(typeCounts).length > 0 && (
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 20 }}>
          {Object.entries(typeCounts).map(([type, count]) => (
            <div
              key={type}
              style={{
                background: 'var(--bg2)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius)',
                padding: '10px 16px',
                textAlign: 'center',
                minWidth: 90,
              }}
            >
              <div style={{ fontSize: 22, fontWeight: 700, fontFamily: 'var(--mono)', color: 'var(--blue)' }}>
                {count}
              </div>
              <div style={{ fontSize: 10, letterSpacing: 1, textTransform: 'uppercase', color: 'var(--text-dim)' }}>
                {type}
              </div>
            </div>
          ))}
        </div>
      )}

      {!projectName ? (
        <div className="empty-state">
          <div className="empty-icon">📁</div>
          <div className="empty-title">No projects found</div>
          <div className="empty-sub">Create a project first, then run a scan</div>
        </div>
      ) : (
        <AssetTable assets={assets ?? []} loading={isLoading} />
      )}
    </div>
  )
}
