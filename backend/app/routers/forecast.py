import json
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.dataset import Dataset
from app.models.forecast import Forecast
from app.models.user import User

from app.core.dependencies import get_current_user

from app.services.forecast_service import (
    generate_forecast
)
from app.models.forecast_history import ForecastHistory

from app.services.advanced_forecast_service import (
    AdvancedForecastService
)
from app.utils.notification_utils import (
    create_notification
)

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)


@router.get("/history")
def get_forecast_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    history = db.query(ForecastHistory)\
        .filter(ForecastHistory.user_id == current_user.id)\
        .order_by(ForecastHistory.created_at.desc())\
        .all()

    return [
        {
            "id": h.id,
            "dataset_id": h.dataset_id,
            "model": h.model_name,
            "accuracy": h.accuracy,
            "created_at": h.created_at,
            "forecast_result": h.forecast_result
        }
        for h in history
    ]
    
    
@router.get("/summary")
def forecast_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    total_forecasts = db.query(Forecast)\
        .join(Dataset)\
        .filter(Dataset.user_id == current_user.id)\
        .count()

    total_history = db.query(ForecastHistory)\
        .filter(ForecastHistory.user_id == current_user.id)\
        .count()

    latest = db.query(ForecastHistory)\
        .filter(ForecastHistory.user_id == current_user.id)\
        .order_by(ForecastHistory.created_at.desc())\
        .first()

    return {
        "total_forecasts": total_forecasts,
        "total_history": total_history,
        "latest_model": latest.model_name if latest else None,
        "latest_accuracy": latest.accuracy if latest else None
    }


    
@router.get("/advanced/{dataset_id}")
async def advanced_forecast(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    service = AdvancedForecastService()

    results = service.compare_models(
        dataset.file_path
    )

    best_model = results["best_model"]

    history = ForecastHistory(
        user_id=current_user.id,
        dataset_id=dataset.id,
        model_name=best_model["model"],
        accuracy=best_model["accuracy"],
         forecast_result=json.dumps(best_model["future_predictions"])
    )

    db.add(history)

    db.commit()
    
    await create_notification(
        db=db,
        title="Forecast Completed",
        message="Forecast generation is completed",
        user_id=current_user.id,
        notification_type="forecast",
        is_admin=True
    )

    return {
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "model_comparison": results,
        "best_model": results["best_model"]
    }


@router.get("/{dataset_id}")
def forecast_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    forecast_data = generate_forecast(dataset.file_path)

    # SAVE INDIVIDUAL FORECAST ROWS
    for prediction in forecast_data["future_predictions"]:

        forecast = Forecast(
            dataset_id=dataset.id,
            predicted_value=prediction["predicted_sales"],
            prediction_date=f"Day {prediction['day']}",
            model_used="Linear Regression"
        )

        db.add(forecast)

    # SAVE HISTORY (IMPORTANT FIX)
    history = ForecastHistory(
        user_id=current_user.id,
        dataset_id=dataset.id,
        model_name="Linear Regression",
        accuracy=forecast_data["forecast_accuracy_mae"],
        forecast_result=json.dumps(forecast_data["future_predictions"])  # FIX
    )

    db.add(history)

    db.commit()

    return {
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "forecast": forecast_data
    }
