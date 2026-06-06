import { useState } from 'react'
import useSWR from 'swr'
import { fetchers, projectsApi } from '@/services/api'
import { useAppStore } from '@/store'
import { ProjectCard } from '@/components/ProjectCard'
import { Modal } from '@/components/Modal'
import type { CreateProjectRequest } from '@/types'

const EMPTY_FORM: CreateProjectRequest = {
  name: '', target: '', description: '', tags: [],
}

export default function Projects() {
  const { data: projects, isLoading, mutate } = useSWR('projects', fetchers.projects, { refreshInterval: 15000 })
  const [search,    setSearch]    = useState('')
  const [createOpen,setCreateOpen]= useState(false)
  const [form,      setForm]      = useState<CreateProjectRequest>(EMPTY_FORM)
  const [tagsInput, setTagsInput] = useState('')
  const [saving,    setSaving]    = useState(false)
  const { notify } = useAppStore()

  const filtered = (projects ?? []).filter((p) => {
    const q = search.toLowerCase()
    return (
      p.name.toLowerCase().includes(q) ||
      p.target.toLowerCase().includes(q) ||
      (p.description ?? '').toLowerCase().includes(q)
    )
  })

  const handleCreate = async () => {
    if (!form.name.trim() || !form.target.trim()) {
      notify('Name and target are required', 'error')
      return
    }
    setSaving(true)
    try {
      const tags = tagsInput.split(',').map((t) => t.trim()).filter(Boolean)
      await projectsApi.create({ ...form, tags })
      notify(`Project "${form.name}" created`, 'success')
      setCreateOpen(false)
      setForm(EMPTY_FORM)
      setTagsInput('')
      mutate()
    } catch (e) {
      notify(`Create failed: ${String(e)}`, 'error')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (name: string) => {
    try {
      await projectsApi.delete(name)
      notify(`Project "${name}" deleted`, 'info')
      mutate()
    } catch (e) {
      notify(`Delete failed: ${String(e)}`, 'error')
    }
  }

  return (
    <div className="page">
      <div className="page-header flex-between">
        <div>
          <div className="page-title">📁 Projects</div>
          <div className="page-subtitle">{(projects ?? []).length} project{(projects ?? []).length !== 1 ? 's' : ''}</div>
        </div>
        <button className="btn btn-primary" onClick={() => setCreateOpen(true)}>
          + New Project
        </button>
      </div>

      {/* Search */}
      <div className="search-bar">
        <div className="search-input-wrap">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            className="form-input"
            placeholder="Search projects…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        {search && (
          <span style={{ fontSize: 12, color: 'var(--text-dim)' }}>
            {filtered.length} result{filtered.length !== 1 ? 's' : ''}
          </span>
        )}
      </div>

      {isLoading ? (
        <div className="loading"><div className="spinner" /> Loading projects…</div>
      ) : filtered.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📁</div>
          <div className="empty-title">
            {search ? 'No projects match your search' : 'No projects yet'}
          </div>
          <div className="empty-sub">
            {!search && 'Create a project to start reconnaissance'}
          </div>
          {!search && (
            <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => setCreateOpen(true)}>
              + Create First Project
            </button>
          )}
        </div>
      ) : (
        <div className="projects-grid">
          {filtered.map((p) => (
            <ProjectCard
              key={p.name}
              project={p}
              onDelete={handleDelete}
              onRefresh={() => mutate()}
            />
          ))}
        </div>
      )}

      {/* Create modal */}
      <Modal
        open={createOpen}
        title="Create New Project"
        onClose={() => { setCreateOpen(false); setForm(EMPTY_FORM); setTagsInput('') }}
        footer={
          <>
            <button className="btn btn-secondary" onClick={() => setCreateOpen(false)}>
              Cancel
            </button>
            <button className="btn btn-primary" onClick={handleCreate} disabled={saving}>
              {saving ? '⏳ Creating…' : '+ Create Project'}
            </button>
          </>
        }
      >
        <div className="form-group">
          <label className="form-label">Project Name *</label>
          <input
            className="form-input"
            placeholder="my-target-recon"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label className="form-label">Target *</label>
          <input
            className="form-input"
            placeholder="example.com / 192.168.1.0/24"
            value={form.target}
            onChange={(e) => setForm({ ...form, target: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label className="form-label">Description</label>
          <textarea
            className="form-textarea"
            placeholder="Optional description…"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label className="form-label">Tags <span style={{ color: 'var(--text-muted)' }}>(comma-separated)</span></label>
          <input
            className="form-input"
            placeholder="bug-bounty, internal, web"
            value={tagsInput}
            onChange={(e) => setTagsInput(e.target.value)}
          />
        </div>
      </Modal>
    </div>
  )
}
