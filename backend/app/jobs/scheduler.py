from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from app.jobs.dataset_jobs import (
    auto_process_datasets
)

from app.jobs.forecast_jobs import (
    run_scheduled_forecasts
)

scheduler = (
    BackgroundScheduler()
)

scheduler.add_job(

    auto_process_datasets,

    "interval",

    minutes=30,

    id="dataset_processor"
)

scheduler.add_job(

    run_scheduled_forecasts,

    "interval",

    hours=1,

    id="forecast_scheduler"
)