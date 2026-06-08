from sqlalchemy.orm import Session

from app.models.notification import (
    Notification
)


class NotificationService:

    @staticmethod
    def create_notification(

        db: Session,

        title: str,

        message: str,

        user_id: int = None,

        notification_type: str = "general",

        is_admin: bool = False
    ):

        notification = Notification(

            user_id=user_id,

            title=title,

            message=message,

            notification_type=
            notification_type,

            is_admin=is_admin
        )

        db.add(notification)

        db.commit()

        db.refresh(notification)

        return notification

    @staticmethod
    def get_notifications(

        db: Session,

        current_user
    ):

        query = db.query(
            Notification
        )

        if (
            current_user.role
            != "super_admin"
        ):

            query = query.filter(
                Notification.user_id
                ==
                current_user.id
            )

        return (

            query.order_by(
                Notification.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def mark_as_read(

        db: Session,

        notification_id: int,

        current_user
    ):

        notification = (
            db.query(
                Notification
            )
            .filter(
                Notification.id
                == notification_id
            )
            .first()
        )

        if not notification:

            return None

        if (
            current_user.role
            != "super_admin"
            and
            notification.user_id
            != current_user.id
        ):

            return None

        notification.is_read = True

        db.commit()

        return notification

    @staticmethod
    def delete_notification(

        db: Session,

        notification_id: int,

        current_user
    ):

        notification = (
            db.query(
                Notification
            )
            .filter(
                Notification.id
                == notification_id
            )
            .first()
        )

        if not notification:

            return False

        if (
            current_user.role
            != "super_admin"
            and
            notification.user_id
            != current_user.id
        ):

            return False

        db.delete(notification)

        db.commit()

        return True
    
    @staticmethod
    def get_unread_count(

        db: Session,

        current_user
    ):

        query = db.query(
            Notification
        ).filter(
            Notification.is_read == False
        )

        if (
            current_user.role
            != "super_admin"
        ):

            query = query.filter(
                Notification.user_id
                ==
                current_user.id
            )

        return {
            "unread_count":
            query.count()
        }


    @staticmethod
    def mark_all_as_read(

        db: Session,

        current_user
    ):

        query = db.query(
            Notification
        ).filter(
            Notification.is_read == False
        )

        if (
            current_user.role
            != "super_admin"
        ):

            query = query.filter(
                Notification.user_id
                ==
                current_user.id
            )

        notifications = query.all()

        for item in notifications:

            item.is_read = True

        db.commit()

        return {
            "message":
            "All notifications marked as read"
        }