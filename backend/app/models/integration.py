from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from datetime import datetime

from app.db.base import Base


class Integration(Base):

    __tablename__ = "integrations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # e.g. "SAP ERP", "Salesforce CRM",
    # "Shopify", "Oracle ERP", "Custom API"
    name = Column(
        String(150),
        nullable=False,
        index=True
    )

    # erp | crm | ecommerce | custom
    integration_type = Column(
        String(50),
        nullable=False,
        index=True
    )

    # Base URL of the external system
    base_url = Column(
        String(500),
        nullable=False
    )

    # Auth type: api_key | oauth2 | basic
    auth_type = Column(
        String(50),
        default="api_key"
    )

    # Encrypted credential storage (JSON string)
    # e.g. {"api_key": "xxx"}
    # or   {"client_id": "x", "client_secret": "y"}
    credentials = Column(
        Text,
        nullable=True
    )

    # active | inactive | error
    status = Column(
        String(50),
        default="inactive",
        index=True
    )

    # Optional description / notes
    description = Column(
        String(500),
        nullable=True
    )

    # Sync direction: inbound | outbound | both
    sync_direction = Column(
        String(20),
        default="both"
    )

    # How often to sync (minutes), 0 = manual only
    sync_interval_minutes = Column(
        Integer,
        default=60
    )

    last_synced_at = Column(
        DateTime,
        nullable=True
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