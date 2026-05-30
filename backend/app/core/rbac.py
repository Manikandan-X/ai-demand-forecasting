from fastapi import Depends
from fastapi import HTTPException

from app.core.dependencies import (
    get_current_user
)

from app.models.user import User


class Roles:

    SUPER_ADMIN = "super_admin"

    ANALYST = "analyst"

    VIEWER = "viewer"


def require_roles(
    allowed_roles: list[str]
):

    def role_checker(

        current_user: User = Depends(
            get_current_user
        )
    ):

        # super admin bypass
        if current_user.role == (
            Roles.SUPER_ADMIN
        ):
            return current_user

        if (
            current_user.role
            not in allowed_roles
        ):

            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return role_checker


# ==========================
# READY TO USE DEPENDENCIES
# ==========================

super_admin_required = (
    require_roles([
        Roles.SUPER_ADMIN
    ])
)

analyst_required = (
    require_roles([
        Roles.ANALYST
    ])
)

viewer_required = (
    require_roles([
        Roles.VIEWER
    ])
)

analyst_or_viewer_required = (
    require_roles([
        Roles.ANALYST,
        Roles.VIEWER
    ])
)

admin_or_analyst_required = (
    require_roles([
        Roles.SUPER_ADMIN,
        Roles.ANALYST
    ])
)