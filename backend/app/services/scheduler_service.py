from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from apscheduler.triggers.interval import (
    IntervalTrigger
)

from app.db.session import (
    SessionLocal
)

from app.services.automation_settings_service import (
    AutomationSettingsService
)

from app.services.schedule_service import (
    ScheduleService
)

from app.services.automation_service import (
    AutomationService
)

scheduler = BackgroundScheduler()


def start_scheduler():

    if scheduler.running:

        return

    db = SessionLocal()

    settings = (
        AutomationSettingsService
        .get_settings(db)
    )

    scheduler.add_job(

        AutomationService
        .run_daily_forecasts,

        IntervalTrigger(
            hours=
            settings
            .forecast_interval_hours
        ),

        id="daily_forecast"
    )

    scheduler.add_job(

        AutomationService
        .process_new_datasets,

        IntervalTrigger(
            minutes=
            settings
            .dataset_interval_minutes
        ),

        id="dataset_processing"
    )

    scheduler.add_job(

        AutomationService
        .generate_alerts,

        IntervalTrigger(
            minutes=
            settings
            .alert_interval_minutes
        ),

        id="alert_generation"
    )

    scheduler.start()

    db.close()


def stop_scheduler():

    if scheduler.running:

        scheduler.shutdown()