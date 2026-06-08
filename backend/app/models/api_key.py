from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from app.db.base import Base


class ApiKey(Base):

    __tablename__ = "api_keys"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Friendly label e.g. "SAP Prod Key"
    label = Column(
        String(150),
        nullable=False,
        index=True
    )

    # Hashed key stored in DB
    # Raw key shown only once on creation
    key_hash = Column(
        String(255),
        nullable=False,
        unique=True
    )

    # First 8 chars of raw key for display
    # e.g. "ek_live_"
    key_prefix = Column(
        String(20),
        nullable=False
    )

    # Scope: read | write | admin
    scope = Column(
        String(50),
        default="read"
    )

    # Whether this key is still usable
    is_active = Column(
        Boolean,
        default=True,
        index=True
    )

    # Optional expiry
    expires_at = Column(
        DateTime,
        nullable=True
    )

    last_used_at = Column(
        DateTime,
        nullable=True
    )

    # Tracks usage count
    usage_count = Column(
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