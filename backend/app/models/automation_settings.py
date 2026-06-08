from sqlalchemy import (
    Column,
    Integer,
    Boolean
)

from app.db.base import Base


class AutomationSettings(Base):

    __tablename__ = (
        "automation_settings"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    forecast_enabled = Column(
        Boolean,
        default=True
    )

    dataset_processing_enabled = Column(
        Boolean,
        default=True
    )

    alerts_enabled = Column(
        Boolean,
        default=True
    )

    forecast_interval_hours = Column(
        Integer,
        default=24
    )

    dataset_interval_minutes = Column(
        Integer,
        default=30
    )

    alert_interval_minutes = Column(
        Integer,
        default=60
    )