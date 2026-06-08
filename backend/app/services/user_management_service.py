from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.user import User

from app.models.user_activity import (
    UserActivity
)

from app.core.security import (
    verify_password,
    hash_password
)

from app.utils.activity_logger import (
    log_user_activity
)


class UserManagementService:

    @staticmethod
    def get_profile(
        current_user
    ):

        return {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "is_active": current_user.is_active
        }
        
    @staticmethod
    def update_profile(
        db: Session,
        current_user,
        name: str
    ):

        current_user.name = name

        db.commit()

        db.refresh(
            current_user
        )

        log_user_activity(
            db=db,
            user_id=current_user.id,
            action="PROFILE_UPDATED",
            details="Profile updated"
        )

        return {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "is_active": current_user.is_active
        }

    @staticmethod
    def change_password(
        db: Session,
        current_user,
        old_password: str,
        new_password: str
    ):

        valid = verify_password(
            old_password,
            current_user.password
        )

        if not valid:

            raise HTTPException(
                status_code=400,
                detail="Old password incorrect"
            )

        current_user.password = (
            hash_password(
                new_password
            )
        )

        db.commit()

        log_user_activity(
            db=db,
            user_id=current_user.id,
            action="PASSWORD_CHANGED",
            details="Password updated"
        )

        return {
            "message":
            "Password updated successfully"
        }

    @staticmethod
    def get_user_activity(
        db: Session,
        current_user
    ):

        return (

            db.query(
                UserActivity
            )

            .filter(
                UserActivity.user_id
                ==
                current_user.id
            )

            .order_by(
                UserActivity.created_at.desc()
            )

            .all()
        )
        
    @staticmethod
    def get_all_users(
        db: Session
    ):

        return (
            db.query(User)
            .order_by(User.id.desc())
            .all()
        )
        
    @staticmethod
    def update_user_status(
        db: Session,
        user_id: int,
        is_active: bool
    ):

        user = (
            db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )

        if not user:
            return None

        user.is_active = is_active

        db.commit()

        db.refresh(user)

        return user