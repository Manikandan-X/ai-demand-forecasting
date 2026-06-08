from pydantic import BaseModel
from pydantic import validator

from typing import Optional
from datetime import datetime


class ApiKeyCreate(BaseModel):

    label: str
    scope: str = "read"
    expires_at: Optional[datetime] = None

    @validator("scope")
    def validate_scope(cls, v):
        allowed = ["read", "write", "admin"]
        if v not in allowed:
            raise ValueError(
                f"scope must be one of {allowed}"
            )
        return v


class ApiKeyResponse(BaseModel):

    id: int
    label: str
    key_prefix: str
    scope: str
    is_active: bool
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    usage_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# Returned ONLY on creation — raw key never stored
class ApiKeyCreatedResponse(BaseModel):

    id: int
    label: str
    key_prefix: str
    scope: str
    raw_key: str     # shown once, then lost
    created_at: datetime

    class Config:
        from_attributes = True