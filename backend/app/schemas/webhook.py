from pydantic import BaseModel
from pydantic import validator

from typing import Optional, List
from datetime import datetime


# ─────────────────────────────────────────
# SUPPORTED EVENTS (single source of truth)
# ─────────────────────────────────────────

SUPPORTED_EVENTS = [
    "forecast.completed",
    "forecast.failed",
    "dataset.uploaded",
    "dataset.processed",
    "alert.generated",
    "integration.synced",
    "automation.job_completed",
]


# ─────────────────────────────────────────
# REQUEST SCHEMAS
# ─────────────────────────────────────────

class WebhookCreate(BaseModel):

    name: str
    target_url: str
    events: List[str]
    secret: Optional[str] = None
    is_active: bool = True

    @validator("events")
    def validate_events(cls, v):
        for event in v:
            if event not in SUPPORTED_EVENTS:
                raise ValueError(
                    f"Unsupported event '{event}'. "
                    f"Supported: {SUPPORTED_EVENTS}"
                )
        return v


class WebhookUpdate(BaseModel):

    name: Optional[str] = None
    target_url: Optional[str] = None
    events: Optional[List[str]] = None
    secret: Optional[str] = None
    is_active: Optional[bool] = None


# ─────────────────────────────────────────
# RESPONSE SCHEMAS
# ─────────────────────────────────────────

class WebhookResponse(BaseModel):

    id: int
    name: str
    target_url: str
    events: str          # stored as comma-separated string
    is_active: bool
    last_response_code: Optional[int]
    last_triggered_at: Optional[datetime]
    failure_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class WebhookLogResponse(BaseModel):

    id: int
    webhook_id: int
    event: str
    payload: Optional[str]
    response_code: Optional[int]
    response_body: Optional[str]
    status: str
    triggered_at: datetime

    class Config:
        from_attributes = True


class WebhookTestResponse(BaseModel):

    success: bool
    message: str
    response_code: Optional[int] = None