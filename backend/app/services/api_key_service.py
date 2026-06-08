import secrets
import hashlib

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.api_key import ApiKey
from app.schemas.api_key import ApiKeyCreate


class ApiKeyService:

    # ──────────────────────────────────────
    # CREATE — returns raw key once only
    # ──────────────────────────────────────
    @staticmethod
    def create_api_key(
        db: Session,
        data: ApiKeyCreate,
        user_id: int,
    ) -> dict:
        """
        Returns a dict with the ApiKey ORM object
        AND the plain-text raw_key (shown once).
        Store only the hash.
        """

        # Generate cryptographically secure key
        raw_key = "ek_" + secrets.token_urlsafe(32)

        key_hash = hashlib.sha256(
            raw_key.encode()
        ).hexdigest()

        key_prefix = raw_key[:12]   # e.g. "ek_abc12345"

        api_key = ApiKey(
            label=data.label,
            key_hash=key_hash,
            key_prefix=key_prefix,
            scope=data.scope,
            expires_at=data.expires_at,
            created_by=user_id,
        )

        db.add(api_key)
        db.commit()
        db.refresh(api_key)

        return {
            "api_key": api_key,
            "raw_key": raw_key,
        }

    # ──────────────────────────────────────
    # VALIDATE — used by auth middleware
    # ──────────────────────────────────────
    @staticmethod
    def validate_key(
        db: Session,
        raw_key: str,
    ) -> Optional[ApiKey]:
        """
        Returns the ApiKey record if the raw key
        is valid, active, and not expired.
        Also increments usage_count.
        """

        key_hash = hashlib.sha256(
            raw_key.encode()
        ).hexdigest()

        api_key = (
            db.query(ApiKey)
            .filter(ApiKey.key_hash == key_hash)
            .first()
        )

        if not api_key:
            return None

        if not api_key.is_active:
            return None

        if (
            api_key.expires_at
            and api_key.expires_at < datetime.utcnow()
        ):
            # Auto-deactivate expired key
            api_key.is_active = False
            db.commit()
            return None

        # Update usage tracking
        api_key.last_used_at = datetime.utcnow()
        api_key.usage_count += 1
        db.commit()

        return api_key

    # ──────────────────────────────────────
    # READ ALL
    # ──────────────────────────────────────
    @staticmethod
    def get_all_keys(
        db: Session,
    ) -> List[ApiKey]:

        return (
            db.query(ApiKey)
            .order_by(ApiKey.created_at.desc())
            .all()
        )

    # ──────────────────────────────────────
    # READ ONE
    # ──────────────────────────────────────
    @staticmethod
    def get_key(
        db: Session,
        key_id: int,
    ) -> Optional[ApiKey]:

        return (
            db.query(ApiKey)
            .filter(ApiKey.id == key_id)
            .first()
        )

    # ──────────────────────────────────────
    # REVOKE
    # ──────────────────────────────────────
    @staticmethod
    def revoke_key(
        db: Session,
        key_id: int,
    ) -> bool:

        api_key = ApiKeyService.get_key(
            db, key_id
        )

        if not api_key:
            return False

        api_key.is_active = False
        db.commit()

        return True

    # ──────────────────────────────────────
    # DELETE
    # ──────────────────────────────────────
    @staticmethod
    def delete_key(
        db: Session,
        key_id: int,
    ) -> bool:

        api_key = ApiKeyService.get_key(
            db, key_id
        )

        if not api_key:
            return False

        db.delete(api_key)
        db.commit()

        return True