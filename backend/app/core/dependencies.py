from jose import (
    JWTError,
    jwt
)

from fastapi import (
    Depends,
    HTTPException
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from sqlalchemy.orm import (
    Session
)

from app.db.deps import (
    get_db
)

from app.models.user import (
    User
)

from app.core.config import (
    SECRET_KEY,
    ALGORITHM
)

security = HTTPBearer()

JWT_ISSUER = (
    "ai-demand-forecasting"
)

JWT_AUDIENCE = (
    "forecast-users"
)


def get_current_user(

    credentials:
    HTTPAuthorizationCredentials
    = Depends(security),

    db: Session =
    Depends(get_db)
):

    token = (
        credentials.credentials
    )

    credentials_exception = (
        HTTPException(
            status_code=401,
            detail=(
                "Could not validate "
                "credentials"
            )
        )
    )

    try:

        payload = jwt.decode(
            token,

            SECRET_KEY,

            algorithms=[
                ALGORITHM
            ],

            audience=
            JWT_AUDIENCE
        )

        issuer = payload.get(
            "iss"
        )

        token_type = payload.get(
            "type"
        )

        email = payload.get(
            "sub"
        )

        if (
            issuer !=
            JWT_ISSUER
        ):

            raise (
                credentials_exception
            )

        if (
            token_type
            != "access"
        ):

            raise (
                credentials_exception
            )

        if not email:

            raise (
                credentials_exception
            )

    except JWTError:

        raise (
            credentials_exception
        )

    user = db.query(
        User
    ).filter(
        User.email ==
        email
    ).first()

    if user is None:

        raise (
            credentials_exception
        )

    return user