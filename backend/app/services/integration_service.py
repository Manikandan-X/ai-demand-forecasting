import json
import time
import requests

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.integration import Integration
from app.models.integration_log import IntegrationLog

from app.schemas.integration import (
    IntegrationCreate,
    IntegrationUpdate,
    TestConnectionResponse,
)


class IntegrationService:

    # ──────────────────────────────────────
    # CREATE
    # ──────────────────────────────────────
    @staticmethod
    def create_integration(
        db: Session,
        data: IntegrationCreate,
        user_id: int
    ) -> Integration:

        integration = Integration(
            name=data.name,
            integration_type=data.integration_type,
            base_url=data.base_url,
            auth_type=data.auth_type,
            credentials=data.credentials,
            description=data.description,
            sync_direction=data.sync_direction,
            sync_interval_minutes=data.sync_interval_minutes,
            status="inactive",
            created_by=user_id,
        )

        db.add(integration)
        db.commit()
        db.refresh(integration)

        return integration

    # ──────────────────────────────────────
    # READ ALL
    # ──────────────────────────────────────
    @staticmethod
    def get_all_integrations(
        db: Session,
        integration_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Integration]:

        query = db.query(Integration)

        if integration_type:
            query = query.filter(
                Integration.integration_type
                == integration_type
            )

        if status:
            query = query.filter(
                Integration.status == status
            )

        return (
            query
            .order_by(Integration.created_at.desc())
            .all()
        )

    # ──────────────────────────────────────
    # READ ONE
    # ──────────────────────────────────────
    @staticmethod
    def get_integration(
        db: Session,
        integration_id: int
    ) -> Optional[Integration]:

        return (
            db.query(Integration)
            .filter(Integration.id == integration_id)
            .first()
        )

    # ──────────────────────────────────────
    # UPDATE
    # ──────────────────────────────────────
    @staticmethod
    def update_integration(
        db: Session,
        integration_id: int,
        data: IntegrationUpdate,
    ) -> Optional[Integration]:

        integration = (
            IntegrationService.get_integration(
                db, integration_id
            )
        )

        if not integration:
            return None

        update_data = data.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(integration, field, value)

        integration.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(integration)

        return integration

    # ──────────────────────────────────────
    # DELETE
    # ──────────────────────────────────────
    @staticmethod
    def delete_integration(
        db: Session,
        integration_id: int
    ) -> bool:

        integration = (
            IntegrationService.get_integration(
                db, integration_id
            )
        )

        if not integration:
            return False

        db.delete(integration)
        db.commit()

        return True

    # ──────────────────────────────────────
    # TEST CONNECTION
    # ──────────────────────────────────────
    @staticmethod
    def test_connection(
        db: Session,
        integration_id: int,
    ) -> TestConnectionResponse:

        integration = (
            IntegrationService.get_integration(
                db, integration_id
            )
        )

        if not integration:
            return TestConnectionResponse(
                success=False,
                message="Integration not found"
            )

        try:

            headers = {}

            # Build auth headers based on auth_type
            if (
                integration.auth_type == "api_key"
                and integration.credentials
            ):
                try:
                    creds = json.loads(
                        integration.credentials
                    )
                    api_key = creds.get("api_key", "")
                    headers["Authorization"] = (
                        f"Bearer {api_key}"
                    )
                except Exception:
                    pass

            elif (
                integration.auth_type == "basic"
                and integration.credentials
            ):
                try:
                    creds = json.loads(
                        integration.credentials
                    )
                    import base64
                    token = base64.b64encode(
                        f"{creds.get('username','')}:"
                        f"{creds.get('password','')}".encode()
                    ).decode()
                    headers["Authorization"] = (
                        f"Basic {token}"
                    )
                except Exception:
                    pass

            start = time.time()

            response = requests.get(
                integration.base_url,
                headers=headers,
                timeout=10,
            )

            elapsed_ms = round(
                (time.time() - start) * 1000, 2
            )

            success = response.status_code < 400

            # Update integration status
            integration.status = (
                "active" if success else "error"
            )
            db.commit()

            # Log the test
            IntegrationService._log(
                db=db,
                integration_id=integration_id,
                action="test",
                status="SUCCESS" if success else "FAILED",
                message=(
                    f"HTTP {response.status_code} "
                    f"in {elapsed_ms}ms"
                ),
            )

            return TestConnectionResponse(
                success=success,
                message=(
                    f"Connected successfully "
                    f"(HTTP {response.status_code})"
                    if success
                    else f"Connection failed "
                         f"(HTTP {response.status_code})"
                ),
                response_time_ms=elapsed_ms,
            )

        except requests.exceptions.ConnectionError:

            integration.status = "error"
            db.commit()

            IntegrationService._log(
                db=db,
                integration_id=integration_id,
                action="test",
                status="FAILED",
                message="Connection refused / DNS failure",
            )

            return TestConnectionResponse(
                success=False,
                message="Could not reach the endpoint. "
                        "Check the base URL.",
            )

        except requests.exceptions.Timeout:

            integration.status = "error"
            db.commit()

            IntegrationService._log(
                db=db,
                integration_id=integration_id,
                action="test",
                status="FAILED",
                message="Request timed out (10s)",
            )

            return TestConnectionResponse(
                success=False,
                message="Connection timed out.",
            )

        except Exception as e:

            integration.status = "error"
            db.commit()

            IntegrationService._log(
                db=db,
                integration_id=integration_id,
                action="test",
                status="FAILED",
                message=str(e),
            )

            return TestConnectionResponse(
                success=False,
                message=f"Unexpected error: {str(e)}",
            )

    # ──────────────────────────────────────
    # MANUAL SYNC (inbound data pull)
    # ──────────────────────────────────────
    @staticmethod
    def trigger_sync(
        db: Session,
        integration_id: int,
        endpoint: str = "/data",
    ) -> dict:

        integration = (
            IntegrationService.get_integration(
                db, integration_id
            )
        )

        if not integration:
            return {
                "success": False,
                "message": "Integration not found"
            }

        if integration.status != "active":
            return {
                "success": False,
                "message": (
                    "Integration is not active. "
                    "Test the connection first."
                )
            }

        try:

            headers = (
                IntegrationService._build_headers(
                    integration
                )
            )

            url = (
                integration.base_url.rstrip("/")
                + endpoint
            )

            response = requests.get(
                url,
                headers=headers,
                timeout=30,
            )

            records = 0

            try:
                payload = response.json()
                if isinstance(payload, list):
                    records = len(payload)
                elif isinstance(payload, dict):
                    records = len(
                        payload.get("data", [])
                        or payload.get("results", [])
                        or payload.get("items", [])
                    )
            except Exception:
                pass

            success = response.status_code < 400

            integration.last_synced_at = (
                datetime.utcnow()
            )
            integration.status = (
                "active" if success else "error"
            )
            db.commit()

            IntegrationService._log(
                db=db,
                integration_id=integration_id,
                action="sync",
                status="SUCCESS" if success else "FAILED",
                message=(
                    f"Synced {records} record(s) "
                    f"via {endpoint}"
                ),
                records_synced=records,
            )

            return {
                "success": success,
                "records_synced": records,
                "message": (
                    f"Sync completed — "
                    f"{records} record(s) received"
                    if success
                    else f"Sync failed "
                         f"(HTTP {response.status_code})"
                ),
            }

        except Exception as e:

            IntegrationService._log(
                db=db,
                integration_id=integration_id,
                action="sync",
                status="FAILED",
                message=str(e),
            )

            return {
                "success": False,
                "message": f"Sync error: {str(e)}"
            }

    # ──────────────────────────────────────
    # LOGS
    # ──────────────────────────────────────
    @staticmethod
    def get_logs(
        db: Session,
        integration_id: int,
        limit: int = 50,
    ) -> List[IntegrationLog]:

        return (
            db.query(IntegrationLog)
            .filter(
                IntegrationLog.integration_id
                == integration_id
            )
            .order_by(IntegrationLog.created_at.desc())
            .limit(limit)
            .all()
        )

    # ──────────────────────────────────────
    # STATS SUMMARY
    # ──────────────────────────────────────
    @staticmethod
    def get_stats(db: Session) -> dict:

        total = db.query(Integration).count()

        active = (
            db.query(Integration)
            .filter(Integration.status == "active")
            .count()
        )

        error = (
            db.query(Integration)
            .filter(Integration.status == "error")
            .count()
        )

        by_type = {}
        for row in db.query(Integration).all():
            t = row.integration_type
            by_type[t] = by_type.get(t, 0) + 1

        return {
            "total": total,
            "active": active,
            "inactive": total - active - error,
            "error": error,
            "by_type": by_type,
        }

    # ──────────────────────────────────────
    # PRIVATE HELPERS
    # ──────────────────────────────────────
    @staticmethod
    def _build_headers(
        integration: Integration
    ) -> dict:

        headers = {}

        if (
            integration.auth_type == "api_key"
            and integration.credentials
        ):
            try:
                creds = json.loads(
                    integration.credentials
                )
                api_key = creds.get("api_key", "")
                headers["Authorization"] = (
                    f"Bearer {api_key}"
                )
            except Exception:
                pass

        elif (
            integration.auth_type == "basic"
            and integration.credentials
        ):
            try:
                import base64
                creds = json.loads(
                    integration.credentials
                )
                token = base64.b64encode(
                    f"{creds.get('username','')}:"
                    f"{creds.get('password','')}".encode()
                ).decode()
                headers["Authorization"] = (
                    f"Basic {token}"
                )
            except Exception:
                pass

        return headers

    @staticmethod
    def _log(
        db: Session,
        integration_id: int,
        action: str,
        status: str,
        message: str,
        records_synced: int = 0,
    ):

        log = IntegrationLog(
            integration_id=integration_id,
            action=action,
            status=status,
            message=message,
            records_synced=records_synced,
        )

        db.add(log)
        db.commit()