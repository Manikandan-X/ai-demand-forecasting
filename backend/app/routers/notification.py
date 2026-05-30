from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.notification import (
    Notification
)

from app.models.user import User

from app.core.rbac import (
    analyst_or_viewer_required
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# =========================
# GET ALL NOTIFICATIONS
# =========================
@router.get("/")
async def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    query = db.query(
        Notification
    )

    # super admin sees all
    if (
        current_user.role
        != "super_admin"
    ):

        query = query.filter(
            Notification.user_id
            == current_user.id
        )

    notifications = query.order_by(
        Notification.created_at.desc()
    ).all()

    return notifications


# =========================
# GET UNREAD COUNT
# =========================
@router.get("/unread-count")
async def unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    query = db.query(
        Notification
    ).filter(
        Notification.is_read == False
    )

    # super admin sees all
    if (
        current_user.role
        != "super_admin"
    ):

        query = query.filter(
            Notification.user_id
            == current_user.id
        )

    count = query.count()

    return {
        "unread_count":
        count
    }


# =========================
# MARK ALL AS READ
# =========================
@router.put("/mark-all/read")
async def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    query = db.query(
        Notification
    ).filter(
        Notification.is_read == False
    )

    # super admin sees all
    if (
        current_user.role
        != "super_admin"
    ):

        query = query.filter(
            Notification.user_id
            == current_user.id
        )

    notifications = query.all()

    for item in notifications:

        item.is_read = True

    db.commit()

    return {
        "message":
        "All notifications marked as read"
    }


# =========================
# MARK SINGLE AS READ
# =========================
@router.put(
    "/{notification_id}/read"
)
async def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    query = db.query(
        Notification
    ).filter(
        Notification.id
        == notification_id
    )

    # prevent other users
    # reading someone else's
    # notification
    if (
        current_user.role
        != "super_admin"
    ):

        query = query.filter(
            Notification.user_id
            == current_user.id
        )

    notification = query.first()

    if not notification:

        raise HTTPException(
            status_code=404,
            detail=(
                "Notification "
                "not found"
            )
        )

    notification.is_read = True

    db.commit()

    return {
        "message":
        "Notification marked as read"
    }