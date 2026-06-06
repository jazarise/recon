import type { WSEvent, LogEntry, LogLevel } from '@/types'

type EventHandler = (event: WSEvent) => void
type LogHandler   = (entry: LogEntry) => void

class WebSocketService {
  private ws: WebSocket | null = null
  private handlers: Set<EventHandler> = new Set()
  private logHandlers: Set<LogHandler> = new Set()
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private reconnectDelay = 2000
  private shouldConnect = false
  private _connected = false

  get connected() { return this._connected }

  connect() {
    this.shouldConnect = true
    this._connect()
  }

  disconnect() {
    this.shouldConnect = false
    this._cleanup()
  }

  subscribe(handler: EventHandler): () => void {
    this.handlers.add(handler)
    return () => this.handlers.delete(handler)
  }

  subscribeLog(handler: LogHandler): () => void {
    this.logHandlers.add(handler)
    return () => this.logHandlers.delete(handler)
  }

  private _connect() {
    if (this.ws?.readyState === WebSocket.OPEN) return

    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const host  = window.location.host
    const url   = `${proto}://${host}/ws/events`

    try {
      this.ws = new WebSocket(url)

      this.ws.onopen = () => {
        this._connected = true
        this.reconnectDelay = 2000
        this._emit({ event: 'ws.connected' })
        this._log('info', 'WebSocket connected', 'ws')
      }

      this.ws.onclose = () => {
        this._connected = false
        this._emit({ event: 'ws.disconnected' })
        if (this.shouldConnect) this._scheduleReconnect()
      }

      this.ws.onerror = () => {
        this._connected = false
        this._emit({ event: 'ws.error' })
      }

      this.ws.onmessage = (ev: MessageEvent<string>) => {
        try {
          const data = JSON.parse(ev.data) as WSEvent
          if (data.event === 'ping') return
          this._emit(data)
          this._toLog(data)
        } catch {
          // ignore unparseable frames
        }
      }
    } catch {
      this._scheduleReconnect()
    }
  }

  private _cleanup() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    if (this.ws) {
      this.ws.onclose = null
      this.ws.close()
      this.ws = null
    }
    this._connected = false
  }

  private _scheduleReconnect() {
    if (this.reconnectTimer) return
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null
      if (this.shouldConnect) this._connect()
    }, this.reconnectDelay)
    this.reconnectDelay = Math.min(this.reconnectDelay * 1.5, 15000)
  }

  private _emit(event: WSEvent) {
    this.handlers.forEach((h) => {
      try { h(event) } catch {}
    })
  }

  private _log(level: LogLevel, message: string, source: string) {
    const entry: LogEntry = {
      id:        crypto.randomUUID ? crypto.randomUUID() : String(Date.now()),
      level,
      message,
      source,
      timestamp: new Date().toISOString(),
    }
    this.logHandlers.forEach((h) => {
      try { h(entry) } catch {}
    })
  }

  private _toLog(event: WSEvent) {
    const payload = event.payload ?? {}
    let level: LogLevel = 'info'
    let msg = event.event

    if (event.event.includes('fail') || event.event.includes('error')) level = 'error'
    else if (event.event.includes('warn')) level = 'warn'
    else if (event.event.includes('start')) level = 'debug'

    const plugin = (payload as Record<string, unknown>).plugin as string | undefined
    const target = (payload as Record<string, unknown>).target as string | undefined
    const error  = (payload as Record<string, unknown>).error  as string | undefined

    if (plugin)  msg += ` [${plugin}]`
    if (target)  msg += ` → ${target}`
    if (error)   msg += `: ${error}`

    this._log(level, msg, plugin ?? 'orchestrator')
  }
}

export const wsService = new WebSocketService()
