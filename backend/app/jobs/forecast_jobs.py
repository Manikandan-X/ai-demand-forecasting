from app.db.session import SessionLocal

from app.models.dataset import (
    Dataset
)

from app.services.advanced_forecast_service import (
    AdvancedForecastService
)


def run_scheduled_forecasts():

    db = SessionLocal()

    try:

        service = (
            AdvancedForecastService()
        )

        datasets = (
            db.query(
                Dataset
            )
            .all()
        )

        for dataset in datasets:

            service.compare_models(
                dataset.file_path
            )

        print(
            "Forecast automation completed"
        )

    finally:

        db.close()