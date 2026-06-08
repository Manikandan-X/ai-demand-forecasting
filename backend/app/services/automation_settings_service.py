from sqlalchemy.orm import Session

from app.models.automation_settings import (
    AutomationSettings
)


class AutomationSettingsService:

    @staticmethod
    def get_settings(
        db: Session
    ):

        settings = (
            db.query(
                AutomationSettings
            )
            .first()
        )

        if not settings:

            settings = (
                AutomationSettings()
            )

            db.add(settings)

            db.commit()

            db.refresh(settings)

        return settings

    @staticmethod
    def update_settings(

        db: Session,

        forecast_enabled: bool,

        dataset_processing_enabled: bool,

        alerts_enabled: bool,

        forecast_interval_hours: int,

        dataset_interval_minutes: int,

        alert_interval_minutes: int
    ):

        settings = (
            AutomationSettingsService
            .get_settings(db)
        )

        settings.forecast_enabled = (
            forecast_enabled
        )

        settings.dataset_processing_enabled = (
            dataset_processing_enabled
        )

        settings.alerts_enabled = (
            alerts_enabled
        )

        settings.forecast_interval_hours = (
            forecast_interval_hours
        )

        settings.dataset_interval_minutes = (
            dataset_interval_minutes
        )

        settings.alert_interval_minutes = (
            alert_interval_minutes
        )

        db.commit()

        db.refresh(settings)

        return settings