from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.db.base import Base


class AutomationSchedule(Base):

    __tablename__ = (
        "automation_schedules"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    job_name = Column(
        String(100),
        unique=True,
        index=True
    )

    interval_minutes = Column(
        Integer,
        nullable=False
    )