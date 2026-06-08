from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.core.dependencies import (
    get_current_user
)

from app.models.user import User

from app.schemas.user_management import (
    UserProfileUpdate,
    PasswordChange
)

from app.services.user_management_service import (
    UserManagementService
)
from app.core.rbac import (
    super_admin_required
)

router = APIRouter(
    prefix="/users",
    tags=["User Management"]
)

@router.get("/profile")
def get_profile(

    current_user: User =
    Depends(get_current_user)
):

    return (
        UserManagementService
        .get_profile(
            current_user
        )
    )
    
@router.put("/profile")
def update_profile(

    data: UserProfileUpdate,

    db: Session =
    Depends(get_db),

    current_user: User =
    Depends(get_current_user)
):

    return (
        UserManagementService
        .update_profile(
            db=db,
            current_user=current_user,
            name=data.name
        )
    )
    
@router.put("/change-password")
def change_password(

    data: PasswordChange,

    db: Session =
    Depends(get_db),

    current_user: User =
    Depends(get_current_user)
):

    return (
        UserManagementService
        .change_password(
            db=db,
            current_user=current_user,
            old_password=
            data.old_password,
            new_password=
            data.new_password
        )
    )
    
@router.get("/activity")
def user_activity(

    db: Session =
    Depends(get_db),

    current_user: User =
    Depends(get_current_user)
):

    return (
        UserManagementService
        .get_user_activity(
            db=db,
            current_user=current_user
        )
    )
    
@router.get("")
def list_users(

    db: Session =
    Depends(get_db),

    current_user =
    Depends(
        super_admin_required
    )
):

    return (
        UserManagementService
        .get_all_users(
            db=db
        )
    )
    
@router.patch("/{user_id}/status")
def update_user_status(

    user_id: int,

    is_active: bool,

    db: Session =
    Depends(get_db),

    current_user =
    Depends(
        super_admin_required
    )
):

    user = (
        UserManagementService
        .update_user_status(
            db=db,
            user_id=user_id,
            is_active=is_active
        )
    )

    if not user:

        return {
            "message":
            "User not found"
        }

    return {
        "message":
        "Status updated",
        "user_id":
        user.id,
        "is_active":
        user.is_active
    }