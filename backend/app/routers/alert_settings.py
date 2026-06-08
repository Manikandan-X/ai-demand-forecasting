from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.alert_settings import AlertSettings

from app.core.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/alert-settings",
    tags=["Alert Settings"]
)


@router.get("/")
def get_settings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    settings = (
        db.query(AlertSettings)
        .filter(
            AlertSettings.user_id ==
            current_user.id
        )
        .first()
    )

    return settings


@router.put("/")
def update_settings(
    enable_forecast_alerts: bool,
    enable_report_alerts: bool,
    enable_threshold_alerts: bool,
    sales_threshold: float,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    settings = (
        db.query(AlertSettings)
        .filter(
            AlertSettings.user_id ==
            current_user.id
        )
        .first()
    )

    if not settings:

        settings = AlertSettings(
            user_id=current_user.id
        )

        db.add(settings)

    settings.enable_forecast_alerts = (
        enable_forecast_alerts
    )

    settings.enable_report_alerts = (
        enable_report_alerts
    )

    settings.enable_threshold_alerts = (
        enable_threshold_alerts
    )

    settings.sales_threshold = (
        sales_threshold
    )

    db.commit()

    return {
        "message":
        "Alert settings updated"
    }