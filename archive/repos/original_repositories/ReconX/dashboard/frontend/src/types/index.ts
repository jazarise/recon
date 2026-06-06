// ── API Entity Types ──────────────────────────────────────────────────────────

export interface Project {
  name: string
  display_name: string
  target: string
  description: string
  tags: string[]
  created_at: string | null
  last_scan: string | null
  scan_count: number
  status: 'new' | 'scanned' | 'legacy' | string
}

export interface Asset {
  id: number
  type: 'ip' | 'subdomain' | 'domain' | 'url' | 'cidr' | 'asn' | string
  value: string
  tags: string[]
  first_seen: string | null
}

export interface Service {
  port: number
  protocol: string
  service_name: string
  banner?: string
}

export interface Task {
  workflow_id: string
  target: string
  status: 'completed' | 'failed' | 'running' | string
  started_at: string | null
  completed_at: string | null
  step_count: number
}

export interface Report {
  filename: string
  format: 'md' | 'json' | 'csv' | 'html' | string
  size_kb: number
  path: string
}

export interface Agent {
  name: string
  status: 'ready' | 'running' | 'error' | string
}

export interface Workflow {
  file: string
  name: string
  description: string
  mode: string
  steps: number
}

export interface DoctorCheck {
  name: string
  status: true | false | null
  detail: string
  fix: string | null
  category: string
}

export interface DoctorResult {
  summary: { passed: number; failed: number; warned: number; total: number }
  checks: DoctorCheck[]
}

export interface FindingsResponse {
  project: string
  count: number
  assets: Asset[]
}

// ── WebSocket Event Types ─────────────────────────────────────────────────────

export type LogLevel = 'info' | 'warn' | 'error' | 'debug'

export interface WSEvent {
  event: string
  payload?: Record<string, unknown>
  timestamp?: string
}

export interface LogEntry {
  id: string
  level: LogLevel
  message: string
  source: string
  timestamp: string
}

// ── UI State Types ────────────────────────────────────────────────────────────

export interface ScanRequest {
  target: string
  project: string
  profile: 'basic' | 'medium' | 'deep'
}

export interface CreateProjectRequest {
  name: string
  target: string
  description: string
  tags: string[]
}

export type ScanProfile = 'basic' | 'medium' | 'deep'

export interface ProfileOption {
  value: ScanProfile
  label: string
  description: string
  estimated: string
}

export const SCAN_PROFILES: ProfileOption[] = [
  { value: 'basic',  label: 'Basic',  description: 'Passive DNS + HTTP probe', estimated: '5–15 min' },
  { value: 'medium', label: 'Medium', description: 'Port scan + LLM analysis',  estimated: '15–60 min' },
  { value: 'deep',   label: 'Deep',   description: 'Full-depth intelligence',   estimated: '1–6+ hrs' },
]
