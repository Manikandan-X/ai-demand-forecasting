from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Float

from app.db.base import Base


class AlertSettings(Base):

    __tablename__ = "alert_settings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        unique=True,
        index=True
    )

    enable_forecast_alerts = Column(
        Boolean,
        default=True
    )

    enable_report_alerts = Column(
        Boolean,
        default=True
    )

    enable_threshold_alerts = Column(
        Boolean,
        default=True
    )

    enable_sales_drop_alerts = Column(
        Boolean,
        default=True
    )

    enable_sales_spike_alerts = Column(
        Boolean,
        default=True
    )

    enable_anomaly_alerts = Column(
        Boolean,
        default=True
    )

    sales_threshold = Column(
        Float,
        default=1000
    )