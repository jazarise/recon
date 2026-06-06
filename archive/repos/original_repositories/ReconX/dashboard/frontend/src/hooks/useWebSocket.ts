import { useEffect } from 'react'
import { wsService } from '@/services/websocket'
import { useAppStore } from '@/store'

export function useWebSocket() {
  const { handleWsEvent, addLog } = useAppStore()

  useEffect(() => {
    wsService.connect()

    const unsubEvent = wsService.subscribe(handleWsEvent)
    const unsubLog   = wsService.subscribeLog(addLog)

    return () => {
      unsubEvent()
      unsubLog()
      wsService.disconnect()
    }
  }, [handleWsEvent, addLog])

  return { connected: wsService.connected }
}
