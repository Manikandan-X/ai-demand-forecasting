import json

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.models.forecast import Forecast
from app.models.forecast_history import (
    ForecastHistory
)

from app.services.forecast_service import (
    generate_forecast
)

from app.services.model_retraining_service import (
    ModelRetrainingService
)

from app.utils.activity_logger import (
    log_user_activity
)

from app.services.notification_service import (
    NotificationService
)

from app.routers.websocket import (
    send_dashboard_update
)


class ForecastManagerService:

    def __init__(self):

        self.retrainer = (
            ModelRetrainingService()
        )

    def get_dataset(

        self,

        db: Session,

        dataset_id: int,

        current_user
    ):

        dataset = (

            db.query(
                Dataset
            )

            .filter(
                Dataset.id ==
                dataset_id
            )

            .first()
        )

        if not dataset:

            raise HTTPException(
                status_code=404,
                detail="Dataset not found"
            )

        if (
            current_user.role
            != "super_admin"
            and
            dataset.uploaded_by
            != current_user.id
        ):

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return dataset
    
    async def generate_normal_forecast(

        self,

        db: Session,

        dataset_id: int,

        current_user
    ):

        dataset = self.get_dataset(
            db,
            dataset_id,
            current_user
        )

        try:

            forecast_data = generate_forecast(
                dataset.file_path
            )

        except Exception as e:

            NotificationService.create_notification(

                db=db,

                title="Forecast Failed",

                message=str(e),

                user_id=current_user.id,

                notification_type="error"
            )

            raise

        for prediction in (
            forecast_data[
                "future_predictions"
            ]
        ):

            db.add(

                Forecast(

                    dataset_id=
                    dataset.id,

                    predicted_value=
                    prediction[
                        "predicted_sales"
                    ],

                    prediction_date=
                    f"Day {prediction['day']}",

                    model_used=
                    "Linear Regression"
                )
            )
            print("FORECAST DATA =", forecast_data)

        history = ForecastHistory(

            user_id=current_user.id,

            dataset_id=dataset.id,

            model_name="Linear Regression",

            accuracy=
            forecast_data[
                "forecast_accuracy_mae"
            ],

            confidence_score=
            forecast_data[
                "confidence_score"
            ],

            forecast_result=
            json.dumps(
                forecast_data[
                    "future_predictions"
                ]
            )
        )

        db.add(history)

        db.commit()

        log_user_activity(

            db=db,

            user_id=
            current_user.id,

            action=
            "FORECAST_GENERATED",

            details=
            f"Forecast generated for "
            f"{dataset.filename}"
        )

        NotificationService.create_notification(

            db=db,

            title=
            "Forecast Completed",

            message=
            "Forecast generation completed",

            user_id=
            current_user.id,

            notification_type=
            "forecast",

            is_admin=False
        )

        await send_dashboard_update(
            user_id=current_user.id
        )

        return {

            "dataset_id":
            dataset.id,

            "filename":
            dataset.filename,

            "forecast":
            forecast_data
        }
        
    async def generate_advanced_forecast(

        self,

        db: Session,

        dataset_id: int,

        current_user
    ):

        dataset = self.get_dataset(
            db,
            dataset_id,
            current_user
        )

        results = (
            self.retrainer
            .retrain_model(
                db=db,
                dataset=dataset,
                current_user=current_user
            )
        )

        log_user_activity(

            db=db,

            user_id=
            current_user.id,

            action=
            "ADVANCED_FORECAST_GENERATED",

            details=
            f"Advanced forecast generated "
            f"for {dataset.filename}"
        )

        NotificationService.create_notification(

            db=db,

            title=
            "Forecast Completed",

            message=
            "Advanced forecast completed",

            user_id=
            current_user.id,

            notification_type=
            "forecast",

            is_admin=False
        )

        await send_dashboard_update(
            user_id=current_user.id
        )

        return {

            "dataset_id":
            dataset.id,

            "filename":
            dataset.filename,

            "model_comparison":
            results,

            "best_model":
            results["best_model"]
        }