from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.user import User

from app.core.rbac import (
    analyst_or_viewer_required
)

from app.services.notification_service import (
    NotificationService
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

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    return (
        NotificationService
        .get_notifications(
            db=db,
            current_user=current_user
        )
    )


# =========================
# GET UNREAD COUNT
# =========================
@router.get("/unread-count")
async def unread_count(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    return (
        NotificationService
        .get_unread_count(
            db=db,
            current_user=current_user
        )
    )


# =========================
# MARK ALL AS READ
# =========================
@router.put("/mark-all/read")
async def mark_all_read(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    return (
        NotificationService
        .mark_all_as_read(
            db=db,
            current_user=current_user
        )
    )


# =========================
# MARK SINGLE AS READ
# =========================
@router.put(
    "/{notification_id}/read"
)
async def mark_as_read(

    notification_id: int,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    result = (
        NotificationService
        .mark_as_read(
            db=db,
            notification_id=
            notification_id,
            current_user=
            current_user
        )
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail=
            "Notification not found"
        )

    return {
        "message":
        "Notification marked as read"
    }