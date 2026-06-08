from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from app.db.base import Base


class AutomationLog(Base):

    __tablename__ = "automation_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    job_name = Column(
        String(100),
        index=True
    )

    status = Column(
        String(50),
        index=True
    )

    message = Column(
        String(2000)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )