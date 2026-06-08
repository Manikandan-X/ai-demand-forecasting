from pydantic import BaseModel
from pydantic import HttpUrl
from pydantic import validator

from typing import Optional
from datetime import datetime


# ─────────────────────────────────────────
# REQUEST SCHEMAS
# ─────────────────────────────────────────

class IntegrationCreate(BaseModel):

    name: str
    integration_type: str   # erp | crm | ecommerce | custom
    base_url: str
    auth_type: str = "api_key"
    credentials: Optional[str] = None  # JSON string
    description: Optional[str] = None
    sync_direction: str = "both"
    sync_interval_minutes: int = 60

    @validator("integration_type")
    def validate_type(cls, v):
        allowed = ["erp", "crm", "ecommerce", "custom"]
        if v not in allowed:
            raise ValueError(
                f"integration_type must be one of {allowed}"
            )
        return v

    @validator("auth_type")
    def validate_auth(cls, v):
        allowed = ["api_key", "oauth2", "basic"]
        if v not in allowed:
            raise ValueError(
                f"auth_type must be one of {allowed}"
            )
        return v

    @validator("sync_direction")
    def validate_direction(cls, v):
        allowed = ["inbound", "outbound", "both"]
        if v not in allowed:
            raise ValueError(
                f"sync_direction must be one of {allowed}"
            )
        return v


class IntegrationUpdate(BaseModel):

    name: Optional[str] = None
    base_url: Optional[str] = None
    auth_type: Optional[str] = None
    credentials: Optional[str] = None
    description: Optional[str] = None
    sync_direction: Optional[str] = None
    sync_interval_minutes: Optional[int] = None
    status: Optional[str] = None


# ─────────────────────────────────────────
# RESPONSE SCHEMAS
# ─────────────────────────────────────────

class IntegrationResponse(BaseModel):

    id: int
    name: str
    integration_type: str
    base_url: str
    auth_type: str
    status: str
    description: Optional[str]
    sync_direction: str
    sync_interval_minutes: int
    last_synced_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IntegrationLogResponse(BaseModel):

    id: int
    integration_id: int
    action: str
    status: str
    message: Optional[str]
    records_synced: int
    created_at: datetime

    class Config:
        from_attributes = True


class TestConnectionResponse(BaseModel):

    success: bool
    message: str
    response_time_ms: Optional[float] = None