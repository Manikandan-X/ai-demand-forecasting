from sqlalchemy.orm import Session

from app.models.notification import (
    Notification
)

from app.routers.websocket import (
    send_notification_to_clients
)


async def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str
):

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message
    )

    db.add(notification)

    db.commit()

    db.refresh(notification)

    await send_notification_to_clients(
        message
    )

    return notification