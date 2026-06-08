from app.services.automation_service import (
    AutomationService
)


class AutomationDashboardService:

    @staticmethod
    def get_automation_stats():

        return {

            "forecasts_generated":
            AutomationService.forecasts_generated,

            "datasets_processed":
            AutomationService.datasets_processed,

            "alerts_generated":
            AutomationService.alerts_generated
        }