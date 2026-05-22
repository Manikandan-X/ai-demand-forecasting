from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

router = APIRouter()

connected_clients = []


@router.websocket("/ws/notifications")
async def websocket_notifications(
    websocket: WebSocket
):
    await websocket.accept()

    connected_clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        connected_clients.remove(websocket)


async def send_notification_to_clients(
    message: str
):
    disconnected = []

    for client in connected_clients:
        try:
            await client.send_json({
                "message": message
            })

        except Exception:
            disconnected.append(client)

    for client in disconnected:
        connected_clients.remove(client)