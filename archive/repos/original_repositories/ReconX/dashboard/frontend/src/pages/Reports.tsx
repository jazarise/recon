import { useState } from 'react'
import useSWR from 'swr'
import { fetchers } from '@/services/api'
import { Badge } from '@/components/Badge'
import type { Report } from '@/types'

type FormatFilter = 'all' | 'html' | 'md' | 'json' | 'csv'

const FORMAT_COLOR: Record<string, string> = {
  html: 'var(--blue)',
  md:   'var(--green)',
  json: 'var(--yellow)',
  csv:  'var(--orange)',
}

const FORMAT_BADGE: Record<string, 'blue' | 'green' | 'yellow' | 'orange' | 'dim'> = {
  html: 'blue', md: 'green', json: 'yellow', csv: 'orange',
}

function fmt(filename: string) {
  // Extract timestamp from filename: report_target_TIMESTAMP.ext
  const parts = filename.replace(/\.(html|md|json|csv)$/, '').split('_')
  const ts = parts[parts.length - 1]
  const num = parseInt(ts, 10)
  if (!isNaN(num) && num > 1e9) {
    return new Date(num * 1000).toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short' })
  }
  return ts
}

function getTarget(filename: string) {
  return filename.replace(/^report_/, '').replace(/_\d+\.(html|md|json|csv)$/, '').replace(/_/g, '.')
}

function groupByBase(reports: Report[]) {
  const groups: Map<string, Report[]> = new Map()
  for (const r of reports) {
    const base = r.filename.replace(/\.(html|md|json|csv)$/, '')
    if (!groups.has(base)) groups.set(base, [])
    groups.get(base)!.push(r)
  }
  return [...groups.entries()].map(([base, files]) => ({ base, files }))
}

export default function Reports() {
  const { data: reports, isLoading, mutate } = useSWR('reports', fetchers.reports, { refreshInterval: 15000 })
  const [filter, setFilter] = useState<FormatFilter>('all')
  const [search, setSearch] = useState('')

  const filtered = (reports ?? []).filter((r) => {
    const matchFormat = filter === 'all' || r.format === filter
    const matchSearch = !search || r.filename.toLowerCase().includes(search.toLowerCase())
    return matchFormat && matchSearch
  })

  const groups = groupByBase(filter === 'all' ? filtered : filtered)

  return (
    <div className="page">
      <div className="page-header flex-between">
        <div>
          <div className="page-title">📄 Reports</div>
          <div className="page-subtitle">{(reports ?? []).length} report file{(reports ?? []).length !== 1 ? 's' : ''}</div>
        </div>
        <button className="btn btn-secondary btn-sm" onClick={() => mutate()}>
          ↺ Refresh
        </button>
      </div>

      {/* Controls */}
      <div className="search-bar">
        <div className="search-input-wrap" style={{ flex: 2 }}>
          <span className="search-icon">🔍</span>
          <input
            type="text"
            className="form-input"
            placeholder="Search reports…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        {(['all', 'html', 'md', 'json', 'csv'] as FormatFilter[]).map((f) => (
          <button
            key={f}
            className={`btn btn-sm ${filter === f ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setFilter(f)}
          >
            {f.toUpperCase()}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="loading"><div className="spinner" /> Loading reports…</div>
      ) : filtered.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📄</div>
          <div className="empty-title">{search || filter !== 'all' ? 'No matching reports' : 'No reports yet'}</div>
          <div className="empty-sub">Reports are generated automatically after each scan</div>
        </div>
      ) : filter === 'all' ? (
        // Grouped view
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {groupByBase(filtered).map(({ base, files }) => (
            <div key={base} className="card">
              <div className="card-header">
                <span style={{ fontFamily: 'var(--mono)', fontSize: 13, color: 'var(--blue)' }}>
                  {getTarget(files[0]?.filename ?? base)}
                </span>
                <span style={{ marginLeft: 8, fontSize: 11, color: 'var(--text-dim)' }}>
                  {fmt(files[0]?.filename ?? '')}
                </span>
                <div style={{ marginLeft: 'auto', display: 'flex', gap: 6 }}>
                  {files.map((f) => (
                    <Badge key={f.filename} variant={FORMAT_BADGE[f.format] ?? 'dim'}>
                      {f.format}
                    </Badge>
                  ))}
                </div>
              </div>
              <div className="card-body" style={{ padding: '12px 20px' }}>
                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                  {files.map((f) => (
                    <a
                      key={f.filename}
                      href={`/api/v1/reports/${encodeURIComponent(f.filename)}`}
                      target="_blank"
                      rel="noreferrer"
                      className="btn btn-secondary btn-sm"
                      style={{ color: FORMAT_COLOR[f.format] ?? 'var(--text)' }}
                    >
                      ↓ {f.format.toUpperCase()}
                      <span style={{ color: 'var(--text-muted)', marginLeft: 4 }}>
                        {f.size_kb} KB
                      </span>
                    </a>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        // Flat list for filtered view
        <div className="card">
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Filename</th>
                  <th>Format</th>
                  <th>Size</th>
                  <th>Generated</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((r) => (
                  <tr key={r.filename}>
                    <td className="mono" style={{ fontSize: 12 }}>{r.filename}</td>
                    <td>
                      <Badge variant={FORMAT_BADGE[r.format] ?? 'dim'}>{r.format}</Badge>
                    </td>
                    <td className="mono" style={{ color: 'var(--text-dim)' }}>{r.size_kb} KB</td>
                    <td className="mono" style={{ color: 'var(--text-dim)', fontSize: 11 }}>
                      {fmt(r.filename)}
                    </td>
                    <td>
                      <a
                        href={`/api/v1/reports/${encodeURIComponent(r.filename)}`}
                        target="_blank"
                        rel="noreferrer"
                        className="btn btn-secondary btn-sm"
                      >
                        ↓ Open
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
