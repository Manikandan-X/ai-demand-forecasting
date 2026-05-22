from sqlalchemy.orm import Session

from app.models.notification import (
    Notification
)

from app.routers.websocket import (
    send_notification_to_clients
)


async def create_notification(
    db: Session,
    title: str,
    message: str,
    user_id: int = None,
    notification_type: str = "general",
    is_admin: bool = False
):

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        is_admin=is_admin
    )

    db.add(notification)

    db.commit()

    db.refresh(notification)

    await send_notification_to_clients(
        message
    )

    return notification