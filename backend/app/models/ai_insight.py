from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Index

from datetime import datetime

from app.db.base import Base


class AIInsight(Base):

    __tablename__ = "ai_insights"

    __table_args__ = (

        Index(
            "idx_ai_dataset_type",
            "dataset_id",
            "insight_type"
        ),

    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    dataset_id = Column(
        Integer,
        ForeignKey("datasets.id"),
        index=True
    )

    insight_type = Column(
        String(100),
        index=True
    )

    title = Column(
        String(255)
    )

    description = Column(
        String(2000)
    )

    priority = Column(
        String(50),
        default="MEDIUM"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )