from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Index

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.base import Base


class Notification(Base):

    __tablename__ = "notifications"
    
    __table_args__ = (

        Index(
            "idx_notification_user_read",
            "user_id",
            "is_read"
        ),

        Index(
            "idx_notification_user_created",
            "user_id",
            "created_at"
        ),

    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    title = Column(
        String(255)
    )

    message = Column(
        String(1000)
    )

    notification_type = Column(
        String(100),
        default="general",
        index=True
    )

    is_admin = Column(
        Boolean,
        default=False,
        index=True
    )

    is_read = Column(
        Boolean,
        default=False,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    user = relationship(
        "User",
        back_populates="notifications"
    )