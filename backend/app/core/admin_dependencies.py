from fastapi import Depends
from fastapi import HTTPException

from app.core.dependencies import get_current_user

from app.models.user import User


def admin_required(
    current_user: User = Depends(
        get_current_user
    )
):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user