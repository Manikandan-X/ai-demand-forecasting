from sqlalchemy.orm import Session

from app.services.automation_settings_service import (
    AutomationSettingsService
)

from app.models.automation_log import (
    AutomationLog
)

from app.services.automation_service import (
    AutomationService
)


class AdminAutomationService:

    @staticmethod
    def get_dashboard(

        db: Session
    ):

        settings = (
            AutomationSettingsService
            .get_settings(db)
        )

        logs = (

            db.query(
                AutomationLog
            )

            .order_by(
                AutomationLog.created_at.desc()
            )

            .limit(20)

            .all()
        )

        return {

            "automation_status": {

                "forecast_enabled":
                settings.forecast_enabled,

                "dataset_processing_enabled":
                settings.dataset_processing_enabled,

                "alerts_enabled":
                settings.alerts_enabled
            },

            "intervals": {

                "forecast_interval_hours":
                settings.forecast_interval_hours,

                "dataset_interval_minutes":
                settings.dataset_interval_minutes,

                "alert_interval_minutes":
                settings.alert_interval_minutes
            },

            "statistics": {

                "forecasts_generated":
                AutomationService
                .forecasts_generated,

                "datasets_processed":
                AutomationService
                .datasets_processed,

                "alerts_generated":
                AutomationService
                .alerts_generated
            },

            "recent_logs":
            logs
        }