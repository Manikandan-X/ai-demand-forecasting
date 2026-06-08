from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.core.rbac import (
    super_admin_required
)

from app.services.automation_log_service import (
    AutomationLogService
)

router = APIRouter(

    prefix="/automation",

    tags=["Automation"]
)


@router.get("/logs")
def get_logs(

    db: Session =
    Depends(get_db),

    current_user =
    Depends(
        super_admin_required
    )
):

    return (
        AutomationLogService
        .get_logs(db)
    )