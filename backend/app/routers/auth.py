from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserLogin
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.core.dependencies import (
    get_current_user
)

from app.utils.activity_logger import (
    log_user_activity
)

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
    db: Session = Depends(get_db)
):

    existing_user = db.query(
        User
    ).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail=(
                "Email already "
                "registered"
            )
        )

    hashed_password = (
        hash_password(
            user.password
        )
    )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,

        # default role
        role="viewer"
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    log_user_activity(
        db=db,
        user_id=new_user.id,
        action="REGISTER",
        details=(
            "User account "
            "created"
        )
    )

    return {
        "message":
        "User registered successfully"
    }


# =========================
# LOGIN USER
# =========================
@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(
        User
    ).filter(
        User.email == user.email
    ).first()

    if not existing_user:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid email "
                "or password"
            )
        )

    valid_password = (
        verify_password(
            user.password,
            existing_user.password
        )
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid email "
                "or password"
            )
        )

    access_token = (
        create_access_token(
            data={
                "sub":
                existing_user.email
            }
        )
    )

    log_user_activity(
        db=db,
        user_id=existing_user.id,
        action="LOGIN",
        details=(
            "User logged in"
        )
    )

    return {

        "access_token":
        access_token,

        "token_type":
        "bearer",

        "user": {

            "id":
            existing_user.id,

            "name":
            existing_user.name,

            "email":
            existing_user.email,

            "role":
            existing_user.role
        }
    }


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