import type {
  Project, CreateProjectRequest,
  FindingsResponse, Task, Report, Agent, Workflow,
  DoctorResult, ScanRequest,
} from '@/types'

const BASE = '/api/v1'

async function req<T>(
  path: string,
  opts: RequestInit = {},
): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...opts.headers },
    ...opts,
  })
  if (!res.ok) {
    const err = await res.text().catch(() => 'Unknown error')
    throw new Error(`API ${res.status}: ${err}`)
  }
  return res.json() as Promise<T>
}

// ── Projects ──────────────────────────────────────────────────────────────────
export const projectsApi = {
  list:   () => req<{ projects: Project[] }>('/projects/'),
  get:    (name: string) => req<Project>(`/projects/${encodeURIComponent(name)}`),
  create: (data: CreateProjectRequest) =>
    req<{ status: string; project: Project }>('/projects/', { method: 'POST', body: JSON.stringify(data) }),
  delete: (name: string) =>
    req<{ status: string }>(`/projects/${encodeURIComponent(name)}`, { method: 'DELETE' }),
}

// ── Workflows ─────────────────────────────────────────────────────────────────
export const workflowsApi = {
  list: () => req<{ workflows: Workflow[] }>('/workflows/'),
  run:  (data: ScanRequest) =>
    req<{ status: string; workflow_id: string; result: unknown }>(
      '/workflows/run',
      { method: 'POST', body: JSON.stringify(data) },
    ),
}

// ── Findings / Assets ─────────────────────────────────────────────────────────
export const findingsApi = {
  list: (project: string, asset_type?: string, limit = 200) => {
    const params = new URLSearchParams({ project, limit: String(limit) })
    if (asset_type) params.set('asset_type', asset_type)
    return req<FindingsResponse>(`/findings/?${params}`)
  },
}

// ── Tasks ─────────────────────────────────────────────────────────────────────
export const tasksApi = {
  list: () => req<{ count: number; tasks: Task[] }>('/tasks/'),
}

// ── Reports ───────────────────────────────────────────────────────────────────
export const reportsApi = {
  list:    () => req<{ count: number; reports: Report[] }>('/reports/'),
  content: (filename: string) =>
    req<{ filename: string; content: string }>(`/reports/${encodeURIComponent(filename)}`),
}

// ── Agents ────────────────────────────────────────────────────────────────────
export const agentsApi = {
  list: () => req<{ count: number; agents: Agent[] }>('/agents/'),
}

// ── Doctor ────────────────────────────────────────────────────────────────────
export const doctorApi = {
  run: () => req<DoctorResult>('/doctor'),
}

// ── SWR fetchers (stable references for useSWR) ───────────────────────────────
export const fetchers = {
  projects:  () => projectsApi.list().then((r) => r.projects),
  tasks:     () => tasksApi.list().then((r) => r.tasks),
  reports:   () => reportsApi.list().then((r) => r.reports),
  agents:    () => agentsApi.list().then((r) => r.agents),
  workflows: () => workflowsApi.list().then((r) => r.workflows),
  findings:  (project: string) => findingsApi.list(project).then((r) => r.assets),
}
