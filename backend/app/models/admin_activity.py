from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.db.base import Base


class AdminActivity(Base):

    __tablename__ = "admin_activities"

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