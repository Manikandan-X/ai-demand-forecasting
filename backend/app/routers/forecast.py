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

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)


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

    forecast_data = generate_forecast(
        dataset.file_path
    )

    for prediction in forecast_data[
        "future_predictions"
    ]:

        forecast = Forecast(
            dataset_id=dataset.id,
            predicted_value=prediction[
                "predicted_sales"
            ],
            prediction_date=f"Day {prediction['day']}"
        )

        db.add(forecast)

    db.commit()

    return {
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "forecast": forecast_data
    }