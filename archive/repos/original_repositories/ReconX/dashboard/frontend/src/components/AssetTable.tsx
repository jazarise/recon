import { useState, useMemo } from 'react'
import type { Asset } from '@/types'
import { Badge, assetTypeBadge } from './Badge'

interface AssetTableProps {
  assets: Asset[]
  loading?: boolean
}

type SortKey = 'type' | 'value' | 'first_seen'
type SortDir = 'asc' | 'desc'

const TYPE_OPTIONS = ['all', 'ip', 'subdomain', 'domain', 'url', 'cidr', 'asn']

export function AssetTable({ assets, loading }: AssetTableProps) {
  const [search,    setSearch]    = useState('')
  const [typeFilter,setTypeFilter]= useState('all')
  const [sortKey,   setSortKey]   = useState<SortKey>('type')
  const [sortDir,   setSortDir]   = useState<SortDir>('asc')
  const [page,      setPage]      = useState(0)
  const PAGE_SIZE = 50

  const filtered = useMemo(() => {
    let rows = assets
    if (typeFilter !== 'all') rows = rows.filter((a) => a.type === typeFilter)
    if (search) {
      const q = search.toLowerCase()
      rows = rows.filter(
        (a) => a.value.toLowerCase().includes(q) || a.tags.some((t) => t.toLowerCase().includes(q)),
      )
    }
    rows = [...rows].sort((a, b) => {
      let va = a[sortKey] ?? ''
      let vb = b[sortKey] ?? ''
      if (va < vb) return sortDir === 'asc' ? -1 : 1
      if (va > vb) return sortDir === 'asc' ?  1 : -1
      return 0
    })
    return rows
  }, [assets, search, typeFilter, sortKey, sortDir])

  const pages    = Math.ceil(filtered.length / PAGE_SIZE)
  const pageData = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE)

  const toggleSort = (key: SortKey) => {
    if (sortKey === key) setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    else { setSortKey(key); setSortDir('asc') }
    setPage(0)
  }

  const SortIcon = ({ k }: { k: SortKey }) =>
    sortKey === k ? (
      <span style={{ marginLeft: 4, opacity: 0.7 }}>
        {sortDir === 'asc' ? '↑' : '↓'}
      </span>
    ) : (
      <span style={{ marginLeft: 4, opacity: 0.2 }}>↕</span>
    )

  return (
    <div>
      {/* Controls */}
      <div className="search-bar">
        <div className="search-input-wrap" style={{ flex: 2 }}>
          <span className="search-icon">🔍</span>
          <input
            type="text"
            className="form-input"
            placeholder="Search assets…"
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(0) }}
          />
        </div>
        <select
          className="form-select"
          value={typeFilter}
          onChange={(e) => { setTypeFilter(e.target.value); setPage(0) }}
          style={{ width: 140 }}
        >
          {TYPE_OPTIONS.map((t) => (
            <option key={t} value={t}>
              {t === 'all' ? 'All types' : t}
            </option>
          ))}
        </select>
        <span style={{ fontSize: 12, color: 'var(--text-dim)', whiteSpace: 'nowrap' }}>
          {filtered.length} asset{filtered.length !== 1 ? 's' : ''}
        </span>
      </div>

      {/* Table */}
      <div className="card">
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th
                  style={{ cursor: 'pointer', userSelect: 'none' }}
                  onClick={() => toggleSort('type')}
                >
                  Type <SortIcon k="type" />
                </th>
                <th
                  style={{ cursor: 'pointer', userSelect: 'none' }}
                  onClick={() => toggleSort('value')}
                >
                  Value <SortIcon k="value" />
                </th>
                <th>Tags</th>
                <th
                  style={{ cursor: 'pointer', userSelect: 'none' }}
                  onClick={() => toggleSort('first_seen')}
                >
                  First Seen <SortIcon k="first_seen" />
                </th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={4}>
                    <div className="loading"><div className="spinner" /> Loading assets…</div>
                  </td>
                </tr>
              ) : pageData.length === 0 ? (
                <tr>
                  <td colSpan={4}>
                    <div className="empty-state">
                      <div className="empty-icon">🔍</div>
                      <div className="empty-title">No assets found</div>
                      <div className="empty-sub">Run a scan to populate the asset database</div>
                    </div>
                  </td>
                </tr>
              ) : (
                pageData.map((a) => (
                  <tr key={a.id}>
                    <td>
                      <Badge variant={assetTypeBadge(a.type)}>{a.type}</Badge>
                    </td>
                    <td className="mono" style={{ wordBreak: 'break-all' }}>
                      {a.value}
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                        {(a.tags ?? []).map((t) => (
                          <span key={t} className="tag">{t}</span>
                        ))}
                      </div>
                    </td>
                    <td className="mono" style={{ whiteSpace: 'nowrap', color: 'var(--text-dim)' }}>
                      {a.first_seen ? new Date(a.first_seen).toLocaleDateString() : '—'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {pages > 1 && (
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 8,
              padding: '12px 16px',
              borderTop: '1px solid var(--border)',
            }}
          >
            <button
              className="btn btn-ghost btn-sm"
              onClick={() => setPage((p) => Math.max(0, p - 1))}
              disabled={page === 0}
            >
              ‹ Prev
            </button>
            <span style={{ fontSize: 12, color: 'var(--text-dim)' }}>
              {page + 1} / {pages}
            </span>
            <button
              className="btn btn-ghost btn-sm"
              onClick={() => setPage((p) => Math.min(pages - 1, p + 1))}
              disabled={page >= pages - 1}
            >
              Next ›
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
