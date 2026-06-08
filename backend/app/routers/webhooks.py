from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session

from typing import List

from app.db.deps import get_db
from app.core.rbac import super_admin_required

from app.schemas.webhook import (
    WebhookCreate,
    WebhookUpdate,
    WebhookResponse,
    WebhookLogResponse,
    WebhookTestResponse,
    SUPPORTED_EVENTS,
)

from app.services.webhook_service import (
    WebhookService,
)


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
)


# ──────────────────────────────────────────
# SUPPORTED EVENTS LIST
# ──────────────────────────────────────────
@router.get("/events")
def list_supported_events(
    current_user=Depends(super_admin_required),
):
    """Returns all event names that can trigger webhooks."""
    return {"events": SUPPORTED_EVENTS}


# ──────────────────────────────────────────
# CREATE
# ──────────────────────────────────────────
@router.post(
    "",
    response_model=WebhookResponse,
)
def create_webhook(
    data: WebhookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    return WebhookService.create_webhook(
        db=db,
        data=data,
        user_id=current_user.id,
    )


# ──────────────────────────────────────────
# LIST ALL
# ──────────────────────────────────────────
@router.get(
    "",
    response_model=List[WebhookResponse],
)
def list_webhooks(
    active_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    return WebhookService.get_all_webhooks(
        db=db,
        active_only=active_only,
    )


# ──────────────────────────────────────────
# GET ONE
# ──────────────────────────────────────────
@router.get(
    "/{webhook_id}",
    response_model=WebhookResponse,
)
def get_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    webhook = WebhookService.get_webhook(
        db=db,
        webhook_id=webhook_id,
    )

    if not webhook:
        raise HTTPException(
            status_code=404,
            detail="Webhook not found",
        )

    return webhook


# ──────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────
@router.put(
    "/{webhook_id}",
    response_model=WebhookResponse,
)
def update_webhook(
    webhook_id: int,
    data: WebhookUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    updated = WebhookService.update_webhook(
        db=db,
        webhook_id=webhook_id,
        data=data,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Webhook not found",
        )

    return updated


# ──────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────
@router.delete("/{webhook_id}")
def delete_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    deleted = WebhookService.delete_webhook(
        db=db,
        webhook_id=webhook_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Webhook not found",
        )

    return {"message": "Webhook deleted successfully"}


# ──────────────────────────────────────────
# TEST DELIVERY
# ──────────────────────────────────────────
@router.post(
    "/{webhook_id}/test",
    response_model=WebhookTestResponse,
)
def test_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    result = WebhookService.test_webhook(
        db=db,
        webhook_id=webhook_id,
    )

    return WebhookTestResponse(**result)


# ──────────────────────────────────────────
# GET DELIVERY LOGS
# ──────────────────────────────────────────
@router.get(
    "/{webhook_id}/logs",
    response_model=List[WebhookLogResponse],
)
def get_webhook_logs(
    webhook_id: int,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    return WebhookService.get_logs(
        db=db,
        webhook_id=webhook_id,
        limit=limit,
    )