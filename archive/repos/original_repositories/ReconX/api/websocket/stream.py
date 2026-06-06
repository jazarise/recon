"""ReconX WebSocket event stream."""

import asyncio
import json
from typing import Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()
_connections: Set[WebSocket] = set()


async def broadcast_event(data: dict):
    """Broadcast a JSON event to all connected WebSocket clients."""
    if not _connections:
        return
    msg = json.dumps(data)
    dead: Set[WebSocket] = set()
    for ws in list(_connections):
        try:
            await ws.send_text(msg)
        except Exception:
            dead.add(ws)
    _connections.difference_update(dead)


@router.websocket("/events")
async def ws_events(websocket: WebSocket):
    await websocket.accept()
    _connections.add(websocket)
    try:
        while True:
            # Keep connection alive — client sends pings
            await asyncio.sleep(30)
            await websocket.send_text(json.dumps({"event": "ping"}))
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        _connections.discard(websocket)
