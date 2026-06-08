from fastapi import APIRouter
from fastapi import Depends

from fastapi import Request

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserLogin
)

from app.core.rate_limiter import (
    limiter
)

from app.core.dependencies import (
    get_current_user
)

from app.services.auth_service import (
    AuthService
)

auth_service = AuthService()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================
# REGISTER USER
# =========================
@router.post("/register")
def register_user(

    user: UserCreate,

    db: Session =
    Depends(get_db)
):

    return (
        AuthService
        .register_user(
            db=db,
            user=user
        )
    )


# =========================
# LOGIN USER
# =========================
@router.post("/login")
@limiter.limit(
    "10/minute"
)
def login_user(

    request: Request,

    user: UserLogin,

    db: Session =
    Depends(get_db)
):

    return (
        AuthService
        .login_user(
            db=db,
            user=user
        )
    )


# =========================
# CURRENT USER
# =========================
@router.get("/me")
def get_logged_in_user(

    current_user: User =
    Depends(
        get_current_user
    )
):

    return {

        "id":
        current_user.id,

        "name":
        current_user.name,

        "email":
        current_user.email,

        "role":
        current_user.role
    }