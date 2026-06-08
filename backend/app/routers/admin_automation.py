from fastapi import (
    APIRouter,
    Depends
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

from app.core.rbac import (
    super_admin_required
)

from app.services.admin_automation_service import (
    AdminAutomationService
)



router = APIRouter(

    prefix="/admin/automation",

    tags=["Admin Automation"]
)


@router.get("/dashboard")
def automation_dashboard(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        super_admin_required
    )
):

    return (
        AdminAutomationService
        .get_dashboard(db)
    )
    
