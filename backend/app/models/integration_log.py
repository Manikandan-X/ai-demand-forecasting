from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from datetime import datetime

from app.db.base import Base


class IntegrationLog(Base):

    __tablename__ = "integration_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    integration_id = Column(
        Integer,
        ForeignKey("integrations.id"),
        nullable=False,
        index=True
    )

    # sync | push | pull | test
    action = Column(
        String(50),
        nullable=False
    )

    # SUCCESS | FAILED
    status = Column(
        String(20),
        nullable=False,
        index=True
    )

    # Human-readable result message
    message = Column(
        String(2000),
        nullable=True
    )

    # Number of records synced
    records_synced = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )