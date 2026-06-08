from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from datetime import datetime

from app.db.base import Base


class Webhook(Base):

    __tablename__ = "webhooks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Human-readable name
    name = Column(
        String(150),
        nullable=False,
        index=True
    )

    # URL that receives the POST payload
    target_url = Column(
        String(500),
        nullable=False
    )

    # Comma-separated events this webhook fires on
    # e.g. "forecast.completed,dataset.uploaded,alert.generated"
    events = Column(
        String(500),
        nullable=False
    )

    # HMAC secret for payload signing (optional)
    secret = Column(
        String(255),
        nullable=True
    )

    # active | inactive
    is_active = Column(
        Boolean,
        default=True,
        index=True
    )

    # Last HTTP response code received
    last_response_code = Column(
        Integer,
        nullable=True
    )

    # Timestamp of last successful delivery
    last_triggered_at = Column(
        DateTime,
        nullable=True
    )

    # Count of consecutive failures
    failure_count = Column(
        Integer,
        default=0
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class WebhookLog(Base):

    __tablename__ = "webhook_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    webhook_id = Column(
        Integer,
        ForeignKey("webhooks.id"),
        nullable=False,
        index=True
    )

    event = Column(
        String(100),
        nullable=False
    )

    # JSON payload that was sent
    payload = Column(
        Text,
        nullable=True
    )

    # HTTP response code from target
    response_code = Column(
        Integer,
        nullable=True
    )

    # Response body snippet
    response_body = Column(
        String(1000),
        nullable=True
    )

    # success | failed
    status = Column(
        String(20),
        default="success",
        index=True
    )

    triggered_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )