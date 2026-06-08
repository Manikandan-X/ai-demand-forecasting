from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Index

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.base import Base


class UserActivity(Base):

    __tablename__ = "user_activity_logs"
    
    __table_args__ = (

        Index(
            "idx_activity_user_created",
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

    action = Column(
        String(255),
        nullable=False,
        index=True
    )

    details = Column(
        String(1000),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    user = relationship(
        "User"
    )