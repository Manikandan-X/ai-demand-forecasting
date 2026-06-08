from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from typing import List

from app.db.deps import get_db
from app.core.rbac import super_admin_required

from app.schemas.api_key import (
    ApiKeyCreate,
    ApiKeyResponse,
    ApiKeyCreatedResponse,
)

from app.services.api_key_service import (
    ApiKeyService,
)


router = APIRouter(
    prefix="/api-keys",
    tags=["API Key Management"],
)


# ──────────────────────────────────────────
# CREATE — raw key shown once
# ──────────────────────────────────────────
@router.post(
    "",
    response_model=ApiKeyCreatedResponse,
)
def create_api_key(
    data: ApiKeyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    """
    Creates a new API key.
    The raw key is returned ONCE — store it securely.
    Only the prefix is visible afterwards.
    """
    result = ApiKeyService.create_api_key(
        db=db,
        data=data,
        user_id=current_user.id,
    )

    api_key = result["api_key"]
    raw_key = result["raw_key"]

    return ApiKeyCreatedResponse(
        id=api_key.id,
        label=api_key.label,
        key_prefix=api_key.key_prefix,
        scope=api_key.scope,
        raw_key=raw_key,
        created_at=api_key.created_at,
    )


# ──────────────────────────────────────────
# LIST ALL
# ──────────────────────────────────────────
@router.get(
    "",
    response_model=List[ApiKeyResponse],
)
def list_api_keys(
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    return ApiKeyService.get_all_keys(db=db)


# ──────────────────────────────────────────
# GET ONE
# ──────────────────────────────────────────
@router.get(
    "/{key_id}",
    response_model=ApiKeyResponse,
)
def get_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    key = ApiKeyService.get_key(
        db=db,
        key_id=key_id,
    )

    if not key:
        raise HTTPException(
            status_code=404,
            detail="API key not found",
        )

    return key


# ──────────────────────────────────────────
# REVOKE (soft disable)
# ──────────────────────────────────────────
@router.patch("/{key_id}/revoke")
def revoke_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    revoked = ApiKeyService.revoke_key(
        db=db,
        key_id=key_id,
    )

    if not revoked:
        raise HTTPException(
            status_code=404,
            detail="API key not found",
        )

    return {"message": "API key revoked successfully"}


# ──────────────────────────────────────────
# DELETE (permanent)
# ──────────────────────────────────────────
@router.delete("/{key_id}")
def delete_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(super_admin_required),
):
    deleted = ApiKeyService.delete_key(
        db=db,
        key_id=key_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="API key not found",
        )

    return {"message": "API key deleted successfully"}