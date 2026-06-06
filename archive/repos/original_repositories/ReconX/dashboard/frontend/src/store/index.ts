import { create } from 'zustand'
import type { LogEntry, WSEvent } from '@/types'

const MAX_LOGS = 500

interface ActiveJob {
  workflowId: string
  target: string
  profile: string
  startedAt: string
  status: 'running' | 'completed' | 'failed'
  steps: string[]
}

interface AppState {
  // WebSocket
  wsConnected: boolean
  setWsConnected: (v: boolean) => void

  // Live log stream
  logs: LogEntry[]
  addLog: (entry: LogEntry) => void
  clearLogs: () => void

  // Active scan jobs
  activeJobs: Map<string, ActiveJob>
  startJob: (job: Omit<ActiveJob, 'status' | 'steps'>) => void
  updateJob: (workflowId: string, patch: Partial<ActiveJob>) => void
  finishJob: (workflowId: string, status: 'completed' | 'failed') => void

  // Raw WS event handler (called by wsService subscription)
  handleWsEvent: (event: WSEvent) => void

  // Notifications (brief banner messages)
  notifications: { id: string; message: string; level: 'info' | 'success' | 'error' }[]
  notify: (message: string, level?: 'info' | 'success' | 'error') => void
  dismissNotification: (id: string) => void
}

export const useAppStore = create<AppState>((set, get) => ({
  // ── WebSocket ─────────────────────────────────────────────────────────────
  wsConnected: false,
  setWsConnected: (v) => set({ wsConnected: v }),

  // ── Logs ──────────────────────────────────────────────────────────────────
  logs: [],
  addLog: (entry) =>
    set((s) => ({
      logs: [...s.logs.slice(-(MAX_LOGS - 1)), entry],
    })),
  clearLogs: () => set({ logs: [] }),

  // ── Jobs ──────────────────────────────────────────────────────────────────
  activeJobs: new Map(),
  startJob: (job) =>
    set((s) => {
      const m = new Map(s.activeJobs)
      m.set(job.workflowId, { ...job, status: 'running', steps: [] })
      return { activeJobs: m }
    }),
  updateJob: (id, patch) =>
    set((s) => {
      const m = new Map(s.activeJobs)
      const existing = m.get(id)
      if (existing) m.set(id, { ...existing, ...patch })
      return { activeJobs: m }
    }),
  finishJob: (id, status) =>
    set((s) => {
      const m = new Map(s.activeJobs)
      const existing = m.get(id)
      if (existing) m.set(id, { ...existing, status })
      return { activeJobs: m }
    }),

  // ── WS event dispatcher ───────────────────────────────────────────────────
  handleWsEvent: (event) => {
    const { setWsConnected, finishJob } = get()
    const payload = event.payload ?? {}

    switch (event.event) {
      case 'ws.connected':
        setWsConnected(true)
        break
      case 'ws.disconnected':
      case 'ws.error':
        setWsConnected(false)
        break
      case 'workflow.completed': {
        const wid = (payload as { workflow_id?: string }).workflow_id
        if (wid) finishJob(wid, 'completed')
        break
      }
      case 'workflow.failed': {
        const wid = (payload as { workflow_id?: string }).workflow_id
        if (wid) finishJob(wid, 'failed')
        break
      }
    }
  },

  // ── Notifications ─────────────────────────────────────────────────────────
  notifications: [],
  notify: (message, level = 'info') => {
    const id = String(Date.now())
    set((s) => ({
      notifications: [...s.notifications, { id, message, level }],
    }))
    // Auto-dismiss after 4 s
    setTimeout(() => get().dismissNotification(id), 4000)
  },
  dismissNotification: (id) =>
    set((s) => ({
      notifications: s.notifications.filter((n) => n.id !== id),
    })),
}))
