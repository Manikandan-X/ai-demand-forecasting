from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Index

from datetime import datetime

from app.db.base import Base


class AdminActivity(Base):

    __tablename__ = "admin_activities"
    
    __table_args__ = (

        Index(
            "idx_admin_activity_created",
            "created_at"
        ),

    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    activity = Column(
        String(1000)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )