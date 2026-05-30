import json

from sqlalchemy.orm import Session

from app.models.forecast_history import (
    ForecastHistory
)

from app.services.advanced_forecast_service import (
    AdvancedForecastService
)


class ModelRetrainingService:

    def retrain_model(
        self,
        db: Session,
        dataset,
        current_user
    ):

        service = (
            AdvancedForecastService()
        )

        results = (
            service.compare_models(
                dataset.file_path
            )
        )

        best_model = (
            results[
                "best_model"
            ]
        )

        history = (
            ForecastHistory(
                user_id=
                current_user.id,

                dataset_id=
                dataset.id,

                model_name=
                best_model[
                    "model"
                ],

                accuracy=
                best_model[
                    "accuracy"
                ],

                forecast_result=
                json.dumps(
                    best_model[
                        "future_predictions"
                    ]
                )
            )
        )

        db.add(history)

        db.commit()

        return results