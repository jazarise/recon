import { useState } from 'react'
import type { Project, ScanProfile } from '@/types'
import { SCAN_PROFILES } from '@/types'
import { workflowsApi } from '@/services/api'
import { useAppStore } from '@/store'
import { Badge, statusBadge } from './Badge'
import { Modal } from './Modal'

interface ProjectCardProps {
  project: Project
  onDelete: (name: string) => void
  onRefresh: () => void
}

function fmt(iso: string | null) {
  if (!iso) return 'never'
  return new Date(iso).toLocaleDateString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
  })
}

export function ProjectCard({ project, onDelete, onRefresh }: ProjectCardProps) {
  const [scanOpen, setScanOpen]   = useState(false)
  const [profile,  setProfile]    = useState<ScanProfile>('basic')
  const [scanning, setScanning]   = useState(false)
  const { notify, startJob }      = useAppStore()

  const handleScan = async () => {
    setScanning(true)
    const id = `${project.name}-${Date.now()}`
    startJob({
      workflowId: id,
      target:     project.target,
      profile,
      startedAt:  new Date().toISOString(),
    })
    try {
      await workflowsApi.run({
        target:  project.target,
        project: project.name,
        profile,
      })
      notify(`Scan complete: ${project.name}`, 'success')
      onRefresh()
    } catch (err) {
      notify(`Scan failed: ${String(err)}`, 'error')
    } finally {
      setScanning(false)
      setScanOpen(false)
    }
  }

  return (
    <>
      <div className="project-card">
        {/* Status strip */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
          <Badge variant={statusBadge(project.status)}>{project.status}</Badge>
          <span style={{ fontSize: 11, color: 'var(--text-muted)', fontFamily: 'var(--mono)' }}>
            {project.scan_count} scan{project.scan_count !== 1 ? 's' : ''}
          </span>
        </div>

        <div className="project-name">{project.display_name || project.name}</div>
        <div className="project-target">{project.target}</div>

        {project.description && (
          <p style={{ fontSize: 12, color: 'var(--text-dim)', marginBottom: 10 }}>
            {project.description}
          </p>
        )}

        <div className="project-meta">
          <div className="project-meta-item">
            <span>📅</span>
            <span>Created: {fmt(project.created_at)}</span>
          </div>
          <div className="project-meta-item">
            <span>🔄</span>
            <span>Last scan: {fmt(project.last_scan)}</span>
          </div>
        </div>

        {project.tags.length > 0 && (
          <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap', marginBottom: 14 }}>
            {project.tags.map((t) => (
              <span key={t} className="tag">{t}</span>
            ))}
          </div>
        )}

        <div className="project-actions">
          <button
            className="btn btn-primary btn-sm"
            onClick={() => setScanOpen(true)}
            disabled={scanning}
          >
            {scanning ? '⏳ Scanning…' : '▶ Scan'}
          </button>
          <button
            className="btn btn-secondary btn-sm"
            onClick={() => window.open(`/api/v1/findings/?project=${project.name}`, '_blank')}
          >
            Assets
          </button>
          <button
            className="btn btn-danger btn-sm"
            onClick={() => {
              if (confirm(`Delete project "${project.name}"? This cannot be undone.`))
                onDelete(project.name)
            }}
          >
            Delete
          </button>
        </div>
      </div>

      {/* Scan modal */}
      <Modal
        open={scanOpen}
        title={`Launch Scan — ${project.name}`}
        onClose={() => setScanOpen(false)}
        footer={
          <>
            <button className="btn btn-secondary" onClick={() => setScanOpen(false)}>
              Cancel
            </button>
            <button
              className="btn btn-primary"
              onClick={handleScan}
              disabled={scanning}
            >
              {scanning ? '⏳ Running…' : '▶ Start Scan'}
            </button>
          </>
        }
      >
        <p style={{ color: 'var(--text-dim)', fontSize: 13, marginBottom: 16 }}>
          Target: <span className="mono text-blue">{project.target}</span>
        </p>

        <div className="form-group">
          <label className="form-label">Scan Profile</label>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {SCAN_PROFILES.map((p) => (
              <label
                key={p.value}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                  padding: '10px 14px',
                  background: profile === p.value ? 'var(--red-dim)' : 'var(--bg3)',
                  border: `1px solid ${profile === p.value ? 'var(--red)' : 'var(--border)'}`,
                  borderRadius: 'var(--radius-sm)',
                  cursor: 'pointer',
                  transition: 'all .15s',
                }}
              >
                <input
                  type="radio"
                  name="profile"
                  value={p.value}
                  checked={profile === p.value}
                  onChange={() => setProfile(p.value)}
                  style={{ accentColor: 'var(--red)' }}
                />
                <div>
                  <div style={{ fontWeight: 700, fontSize: 13 }}>{p.label}</div>
                  <div style={{ fontSize: 11, color: 'var(--text-dim)' }}>
                    {p.description} · ~{p.estimated}
                  </div>
                </div>
              </label>
            ))}
          </div>
        </div>
      </Modal>
    </>
  )
}
