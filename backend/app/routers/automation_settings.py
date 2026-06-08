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

from app.core.rbac import (
    super_admin_required
)

from app.models.user import (
    User
)

from app.services.automation_settings_service import (
    AutomationSettingsService
)

from app.services.scheduler_service import (
    stop_scheduler,
    start_scheduler
)

router = APIRouter(

    prefix="/automation-settings",

    tags=["Automation Settings"]
)


@router.get("/")
def get_settings(

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        super_admin_required
    )
):

    return (
        AutomationSettingsService
        .get_settings(db)
    )


@router.put("/")
def update_settings(

    forecast_enabled: bool,

    dataset_processing_enabled: bool,

    alerts_enabled: bool,

    forecast_interval_hours: int,

    dataset_interval_minutes: int,

    alert_interval_minutes: int,

    db: Session = Depends(
        get_db
    ),

    current_user: User = Depends(
        super_admin_required
    )
):

    return (
        AutomationSettingsService
        .update_settings(

            db=db,

            forecast_enabled=
            forecast_enabled,

            dataset_processing_enabled=
            dataset_processing_enabled,

            alerts_enabled=
            alerts_enabled,

            forecast_interval_hours=
            forecast_interval_hours,

            dataset_interval_minutes=
            dataset_interval_minutes,

            alert_interval_minutes=
            alert_interval_minutes
        )
    )
    
@router.post("/reload")
def reload_scheduler(

    current_user: User = Depends(
        super_admin_required
    )
):

    stop_scheduler()

    start_scheduler()

    return {
        "message":
        "Scheduler reloaded"
    }