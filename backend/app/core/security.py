from datetime import (
    datetime,
    timedelta
)

from jose import jwt
from passlib.context import (
    CryptContext
)

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

JWT_ISSUER = (
    "ai-demand-forecasting"
)

JWT_AUDIENCE = (
    "forecast-users"
)


def hash_password(
    password: str
):
    return pwd_context.hash(
        password
    )


def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = (
        datetime.utcnow()
        + timedelta(
            minutes=
            ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({
        "exp":
        expire,

        "iat":
        datetime.utcnow(),

        "iss":
        JWT_ISSUER,

        "aud":
        JWT_AUDIENCE,

        "type":
        "access"
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt