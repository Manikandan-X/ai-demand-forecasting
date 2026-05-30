import time

from jose import jwt
from jose import JWTError

from starlette.middleware.base import (
    BaseHTTPMiddleware
)

from sqlalchemy.orm import Session

from app.db.session import (
    SessionLocal
)

from app.models.user import User

from app.utils.activity_logger import (
    log_user_activity
)

from app.core.config import (
    SECRET_KEY,
    ALGORITHM
)


EXCLUDED_PATHS = [

    "/docs",

    "/redoc",

    "/openapi.json",

    "/",

]


class ApiMonitoringMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):

        path = request.url.path

        if (
            path in EXCLUDED_PATHS
            or path.startswith("/ws")
            or path.startswith("/test")
        ):

            return await call_next(
                request
            )

        start_time = time.time()

        response = await call_next(
            request
        )

        process_time = round(
            (
                time.time()
                - start_time
            ) * 1000,
            2
        )

        user_id = None

        try:

            auth_header = request.headers.get(
                "authorization"
            )

            if auth_header:

                token = auth_header.replace(
                    "Bearer ",
                    ""
                )

                payload = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=[ALGORITHM]
                )

                email = payload.get(
                    "sub"
                )

                if email:

                    db: Session = (
                        SessionLocal()
                    )

                    user = db.query(
                        User
                    ).filter(
                        User.email == email
                    ).first()

                    if user:

                        user_id = user.id

        except JWTError:
            pass

        except Exception:
            pass

        finally:
            try:
                db.close()
            except:
                pass

        db = SessionLocal()

        try:

            log_user_activity(
                db=db,
                user_id=user_id,
                action="API_REQUEST",
                details=(
                    f"{request.method} "
                    f"{path} | "
                    f"{response.status_code} | "
                    f"{process_time}ms"
                )
            )

        finally:
            db.close()

        return response