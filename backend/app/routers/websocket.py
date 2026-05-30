from collections import defaultdict

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect


router = APIRouter()


class ConnectionManager:

    def __init__(self):

        self.active_connections = (
            defaultdict(list)
        )

    # =========================
    # CONNECT
    # =========================
    async def connect(

        self,

        websocket: WebSocket,

        user_id: int
    ):

        await websocket.accept()

        self.active_connections[
            user_id
        ].append(websocket)

    # =========================
    # DISCONNECT
    # =========================
    def disconnect(

        self,

        websocket: WebSocket,

        user_id: int
    ):

        if (
            user_id
            not in self.active_connections
        ):

            return

        if websocket in self.active_connections[
            user_id
        ]:

            self.active_connections[
                user_id
            ].remove(websocket)

        # remove empty key
        if not self.active_connections[
            user_id
        ]:

            del self.active_connections[
                user_id
            ]

    # =========================
    # SEND TO USER
    # =========================
    async def send_to_user(

        self,

        user_id: int,

        payload: dict
    ):

        if (
            user_id
            not in self.active_connections
        ):

            return

        disconnected = []

        for ws in self.active_connections[
            user_id
        ]:

            try:

                await ws.send_json(
                    payload
                )

            except Exception:

                disconnected.append(
                    ws
                )

        for ws in disconnected:

            self.disconnect(
                ws,
                user_id
            )

    # =========================
    # BROADCAST
    # =========================
    async def broadcast(

        self,

        payload: dict
    ):

        disconnected = []

        for (
            user_id,
            sockets
        ) in list(
            self.active_connections.items()
        ):

            for ws in sockets:

                try:

                    await ws.send_json(
                        payload
                    )

                except Exception:

                    disconnected.append(
                        (
                            ws,
                            user_id
                        )
                    )

        for (
            ws,
            user_id
        ) in disconnected:

            self.disconnect(
                ws,
                user_id
            )


manager = ConnectionManager()


# =========================
# NOTIFICATION SOCKET
# =========================
@router.websocket(
    "/ws/notifications/{user_id}"
)
async def websocket_notifications(

    websocket: WebSocket,

    user_id: int
):

    await manager.connect(
        websocket,
        user_id
    )

    try:

        while True:

            # keep connection alive
            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(
            websocket,
            user_id
        )

    except Exception:

        manager.disconnect(
            websocket,
            user_id
        )


# =========================
# SEND NOTIFICATION
# =========================
async def send_notification_to_clients(

    message: str,

    user_id: int = None
):

    payload = {

        "type":
        "notification",

        "message":
        message
    }

    if user_id is not None:

        await manager.send_to_user(
            user_id,
            payload
        )

    else:

        await manager.broadcast(
            payload
        )


# =========================
# SEND DASHBOARD UPDATE
# =========================
async def send_dashboard_update(

    user_id: int = None
):

    payload = {

        "type":
        "dashboard_update",

        "message":
        "refresh_dashboard"
    }

    if user_id is not None:

        await manager.send_to_user(
            user_id,
            payload
        )

    else:

        await manager.broadcast(
            payload
        )