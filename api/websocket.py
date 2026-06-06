from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from core.event_bus import event_bus
import asyncio

router = APIRouter()
connected_clients = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

def broadcast_event(event_type: str, **kwargs):
    try:
        loop = asyncio.get_running_loop()
        for client in connected_clients:
            loop.create_task(client.send_json({"event": event_type, "data": kwargs}))
    except RuntimeError:
        pass # No running event loop

event_bus.subscribe("PluginStarted", lambda **kw: broadcast_event("PluginStarted", **kw))
event_bus.subscribe("FindingCreated", lambda **kw: broadcast_event("FindingCreated", **kw))
event_bus.subscribe("PluginFinished", lambda **kw: broadcast_event("PluginFinished", **kw))
event_bus.subscribe("ScanStarted", lambda **kw: broadcast_event("ScanStarted", **kw))
event_bus.subscribe("WorkflowCompleted", lambda **kw: broadcast_event("WorkflowCompleted", **kw))
