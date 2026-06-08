from pydantic import BaseModel
from pydantic import EmailStr


class UserProfileUpdate(
    BaseModel
):
    name: str


class PasswordChange(
    BaseModel
):
    old_password: str

    new_password: str


class UserProfileResponse(
    BaseModel
):
    id: int

    name: str

    email: EmailStr

    role: str

    is_active: bool

    class Config:
        from_attributes = True