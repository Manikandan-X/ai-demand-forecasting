import json
import hmac
import hashlib
import requests

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.webhook import Webhook, WebhookLog
from app.schemas.webhook import (
    WebhookCreate,
    WebhookUpdate,
)


class WebhookService:

    # ──────────────────────────────────────
    # CREATE
    # ──────────────────────────────────────
    @staticmethod
    def create_webhook(
        db: Session,
        data: WebhookCreate,
        user_id: int,
    ) -> Webhook:

        webhook = Webhook(
            name=data.name,
            target_url=data.target_url,
            # store events as comma-separated string
            events=",".join(data.events),
            secret=data.secret,
            is_active=data.is_active,
            created_by=user_id,
        )

        db.add(webhook)
        db.commit()
        db.refresh(webhook)

        return webhook

    # ──────────────────────────────────────
    # READ ALL
    # ──────────────────────────────────────
    @staticmethod
    def get_all_webhooks(
        db: Session,
        active_only: bool = False,
    ) -> List[Webhook]:

        query = db.query(Webhook)

        if active_only:
            query = query.filter(
                Webhook.is_active == True
            )

        return (
            query
            .order_by(Webhook.created_at.desc())
            .all()
        )

    # ──────────────────────────────────────
    # READ ONE
    # ──────────────────────────────────────
    @staticmethod
    def get_webhook(
        db: Session,
        webhook_id: int,
    ) -> Optional[Webhook]:

        return (
            db.query(Webhook)
            .filter(Webhook.id == webhook_id)
            .first()
        )

    # ──────────────────────────────────────
    # UPDATE
    # ──────────────────────────────────────
    @staticmethod
    def update_webhook(
        db: Session,
        webhook_id: int,
        data: WebhookUpdate,
    ) -> Optional[Webhook]:

        webhook = WebhookService.get_webhook(
            db, webhook_id
        )

        if not webhook:
            return None

        update_data = data.dict(exclude_unset=True)

        if "events" in update_data:
            update_data["events"] = ",".join(
                update_data["events"]
            )

        for field, value in update_data.items():
            setattr(webhook, field, value)

        webhook.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(webhook)

        return webhook

    # ──────────────────────────────────────
    # DELETE
    # ──────────────────────────────────────
    @staticmethod
    def delete_webhook(
        db: Session,
        webhook_id: int,
    ) -> bool:

        webhook = WebhookService.get_webhook(
            db, webhook_id
        )

        if not webhook:
            return False

        db.delete(webhook)
        db.commit()

        return True

    # ──────────────────────────────────────
    # FIRE EVENT  ← called from other services
    # ──────────────────────────────────────
    @staticmethod
    def fire_event(
        db: Session,
        event: str,
        payload: dict,
    ):
        """
        Call this from AutomationService,
        ForecastService, etc. to notify all
        subscribed active webhooks.

        Example:
            WebhookService.fire_event(
                db=db,
                event="forecast.completed",
                payload={"dataset_id": 3, ...}
            )
        """

        webhooks = (
            db.query(Webhook)
            .filter(Webhook.is_active == True)
            .all()
        )

        for webhook in webhooks:

            subscribed_events = [
                e.strip()
                for e in webhook.events.split(",")
                if e.strip()
            ]

            if event not in subscribed_events:
                continue

            WebhookService._deliver(
                db=db,
                webhook=webhook,
                event=event,
                payload=payload,
            )

    # ──────────────────────────────────────
    # TEST DELIVERY
    # ──────────────────────────────────────
    @staticmethod
    def test_webhook(
        db: Session,
        webhook_id: int,
    ) -> dict:

        webhook = WebhookService.get_webhook(
            db, webhook_id
        )

        if not webhook:
            return {
                "success": False,
                "message": "Webhook not found"
            }

        result = WebhookService._deliver(
            db=db,
            webhook=webhook,
            event="webhook.test",
            payload={
                "message": "Test delivery from "
                           "AI Demand Forecasting",
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

        return result

    # ──────────────────────────────────────
    # LOGS
    # ──────────────────────────────────────
    @staticmethod
    def get_logs(
        db: Session,
        webhook_id: int,
        limit: int = 50,
    ) -> List[WebhookLog]:

        return (
            db.query(WebhookLog)
            .filter(
                WebhookLog.webhook_id == webhook_id
            )
            .order_by(WebhookLog.triggered_at.desc())
            .limit(limit)
            .all()
        )

    # ──────────────────────────────────────
    # PRIVATE — actual HTTP delivery
    # ──────────────────────────────────────
    @staticmethod
    def _deliver(
        db: Session,
        webhook: Webhook,
        event: str,
        payload: dict,
    ) -> dict:

        body = json.dumps(
            {
                "event": event,
                "timestamp": (
                    datetime.utcnow().isoformat()
                ),
                "data": payload,
            }
        )

        headers = {
            "Content-Type": "application/json",
            "X-Event-Type": event,
        }

        # HMAC signature header
        if webhook.secret:
            sig = hmac.new(
                webhook.secret.encode(),
                body.encode(),
                hashlib.sha256,
            ).hexdigest()
            headers["X-Signature-SHA256"] = (
                f"sha256={sig}"
            )

        status = "success"
        response_code = None
        response_body = None

        try:

            resp = requests.post(
                webhook.target_url,
                data=body,
                headers=headers,
                timeout=10,
            )

            response_code = resp.status_code
            response_body = resp.text[:500]

            success = resp.status_code < 400

            if success:
                webhook.failure_count = 0
            else:
                webhook.failure_count += 1
                status = "failed"

            webhook.last_response_code = (
                resp.status_code
            )
            webhook.last_triggered_at = (
                datetime.utcnow()
            )

            # Auto-disable after 5 consecutive failures
            if webhook.failure_count >= 5:
                webhook.is_active = False

            db.commit()

        except Exception as e:

            status = "failed"
            response_body = str(e)[:500]
            webhook.failure_count += 1

            if webhook.failure_count >= 5:
                webhook.is_active = False

            db.commit()

        # Save delivery log
        log = WebhookLog(
            webhook_id=webhook.id,
            event=event,
            payload=body[:2000],
            response_code=response_code,
            response_body=response_body,
            status=status,
        )

        db.add(log)
        db.commit()

        return {
            "success": status == "success",
            "response_code": response_code,
            "message": (
                f"Delivered to {webhook.target_url}"
                if status == "success"
                else f"Delivery failed: {response_body}"
            ),
        }