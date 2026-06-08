from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session

from typing import Optional, List

from app.db.deps import get_db
from app.core.rbac import super_admin_required

from app.schemas.integration import (
    IntegrationCreate,
    IntegrationUpdate,
    IntegrationResponse,
    IntegrationLogResponse,
    TestConnectionResponse,
)

from app.services.integration_service import (
    IntegrationService,
)


router = APIRouter(
    prefix="/integrations",
    tags=["Enterprise Integrations"],
)


# ──────────────────────────────────────────
# CREATE
# ──────────────────────────────────────────
@router.post(
    "",
    response_model=IntegrationResponse,
)
def create_integration(
    data: IntegrationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    return IntegrationService.create_integration(
        db=db,
        data=data,
        user_id=current_user.id,
    )


# ──────────────────────────────────────────
# LIST ALL
# ──────────────────────────────────────────
@router.get(
    "",
    response_model=List[IntegrationResponse],
)
def list_integrations(
    integration_type: Optional[str] = Query(
        None,
        description="Filter by type: erp|crm|ecommerce|custom"
    ),
    status: Optional[str] = Query(
        None,
        description="Filter by status: active|inactive|error"
    ),
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    return IntegrationService.get_all_integrations(
        db=db,
        integration_type=integration_type,
        status=status,
    )


# ──────────────────────────────────────────
# STATS
# ──────────────────────────────────────────
@router.get("/stats")
def get_integration_stats(
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    return IntegrationService.get_stats(db=db)


# ──────────────────────────────────────────
# GET ONE
# ──────────────────────────────────────────
@router.get(
    "/{integration_id}",
    response_model=IntegrationResponse,
)
def get_integration(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    integration = IntegrationService.get_integration(
        db=db,
        integration_id=integration_id,
    )

    if not integration:
        raise HTTPException(
            status_code=404,
            detail="Integration not found",
        )

    return integration


# ──────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────
@router.put(
    "/{integration_id}",
    response_model=IntegrationResponse,
)
def update_integration(
    integration_id: int,
    data: IntegrationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    updated = IntegrationService.update_integration(
        db=db,
        integration_id=integration_id,
        data=data,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Integration not found",
        )

    return updated


# ──────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────
@router.delete("/{integration_id}")
def delete_integration(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    deleted = IntegrationService.delete_integration(
        db=db,
        integration_id=integration_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Integration not found",
        )

    return {"message": "Integration deleted successfully"}


# ──────────────────────────────────────────
# TEST CONNECTION
# ──────────────────────────────────────────
@router.post(
    "/{integration_id}/test",
    response_model=TestConnectionResponse,
)
def test_connection(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    return IntegrationService.test_connection(
        db=db,
        integration_id=integration_id,
    )


# ──────────────────────────────────────────
# TRIGGER MANUAL SYNC
# ──────────────────────────────────────────
@router.post("/{integration_id}/sync")
def trigger_sync(
    integration_id: int,
    endpoint: str = Query(
        "/data",
        description="API endpoint path to pull data from"
    ),
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    return IntegrationService.trigger_sync(
        db=db,
        integration_id=integration_id,
        endpoint=endpoint,
    )


# ──────────────────────────────────────────
# GET LOGS
# ──────────────────────────────────────────
@router.get(
    "/{integration_id}/logs",
    response_model=List[IntegrationLogResponse],
)
def get_integration_logs(
    integration_id: int,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    return IntegrationService.get_logs(
        db=db,
        integration_id=integration_id,
        limit=limit,
    )