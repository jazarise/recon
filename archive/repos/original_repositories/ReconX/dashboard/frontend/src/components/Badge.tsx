import type { CSSProperties } from 'react'

// ── Badge ─────────────────────────────────────────────────────────────────────
type BadgeVariant = 'red' | 'green' | 'yellow' | 'blue' | 'purple' | 'orange' | 'dim'

interface BadgeProps {
  children: React.ReactNode
  variant?: BadgeVariant
  style?: CSSProperties
}

export function Badge({ children, variant = 'dim', style }: BadgeProps) {
  return (
    <span className={`badge badge-${variant}`} style={style}>
      {children}
    </span>
  )
}

export function statusBadge(status: string) {
  const s = status.toLowerCase()
  if (s === 'completed' || s === 'scanned' || s === 'ready') return 'green'
  if (s === 'running')                                        return 'yellow'
  if (s === 'failed' || s === 'error')                       return 'red'
  if (s === 'new')                                           return 'blue'
  return 'dim'
}

export function riskBadge(level: string): BadgeVariant {
  switch (level?.toUpperCase()) {
    case 'CRITICAL': return 'red'
    case 'HIGH':     return 'orange'
    case 'MEDIUM':   return 'yellow'
    case 'LOW':      return 'green'
    default:         return 'dim'
  }
}

export function assetTypeBadge(type: string): BadgeVariant {
  switch (type) {
    case 'ip':        return 'orange'
    case 'subdomain': return 'blue'
    case 'domain':    return 'purple'
    case 'url':       return 'green'
    case 'cidr':      return 'yellow'
    default:          return 'dim'
  }
}

// ── StatCard ──────────────────────────────────────────────────────────────────
interface StatCardProps {
  label: string
  value: number | string
  color?: string
  icon?: string
  onClick?: () => void
  loading?: boolean
}

export function StatCard({ label, value, color = 'var(--blue)', icon, onClick, loading }: StatCardProps) {
  return (
    <div
      className="stat-card"
      style={{
        '--stat-color': color,
        '--accent-top': color,
        cursor: onClick ? 'pointer' : 'default',
      } as CSSProperties}
      onClick={onClick}
    >
      {icon && (
        <div style={{ fontSize: 22, marginBottom: 8, opacity: 0.7 }}>{icon}</div>
      )}
      <div className="stat-number" style={{ color }}>
        {loading ? '—' : value}
      </div>
      <div className="stat-label">{label}</div>
    </div>
  )
}

// ── WorkflowStatus ────────────────────────────────────────────────────────────
interface WorkflowStatusProps {
  status: string
  steps?: number
}

export function WorkflowStatus({ status, steps }: WorkflowStatusProps) {
  return (
    <div className="flex-center gap-8">
      <Badge variant={statusBadge(status)}>{status}</Badge>
      {steps !== undefined && (
        <span style={{ fontSize: 11, color: 'var(--text-dim)' }}>{steps} steps</span>
      )}
    </div>
  )
}
