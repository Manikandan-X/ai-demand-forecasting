from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.dataset import Dataset
from app.models.forecast import Forecast
from app.models.forecast_history import (
    ForecastHistory
)
from app.models.user import User

from app.core.rbac import (
    admin_or_analyst_required,
    analyst_or_viewer_required
)

from app.services.forecast_manager_service import (
    ForecastManagerService
)

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)

forecast_manager = (
    ForecastManagerService()
)


# ==========================
# HISTORY
# ==========================
@router.get("/history")
def get_forecast_history(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    query = db.query(
        ForecastHistory.id,
        ForecastHistory.dataset_id,
        ForecastHistory.model_name,
        ForecastHistory.accuracy,
        ForecastHistory.created_at
    )

    if current_user.role != "super_admin":

        query = query.filter(
            ForecastHistory.user_id ==
            current_user.id
        )

    history = query.order_by(
        ForecastHistory.created_at.desc()
    ).all()

    return [
        {
            "id":
            h.id,

            "dataset_id":
            h.dataset_id,

            "model":
            h.model_name,

            "accuracy":
            h.accuracy,

            "created_at":
            h.created_at
        }
        for h in history
    ]


# ==========================
# SUMMARY
# ==========================
@router.get("/summary")
def forecast_summary(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    dataset_query = db.query(
        Dataset
    )

    history_query = db.query(
        ForecastHistory
    )

    if current_user.role != "super_admin":

        dataset_query = dataset_query.filter(
            Dataset.uploaded_by ==
            current_user.id
        )

        history_query = history_query.filter(
            ForecastHistory.user_id ==
            current_user.id
        )

    dataset_ids = [
        row[0]
        for row in dataset_query.with_entities(
            Dataset.id
        ).all()
    ]

    total_forecasts = db.query(
        Forecast
    ).filter(
        Forecast.dataset_id.in_(
            dataset_ids
        )
    ).count()

    total_history = (
        history_query.count()
    )

    latest = (
        history_query
        .with_entities(
            ForecastHistory.model_name,
            ForecastHistory.accuracy
        )
        .order_by(
            ForecastHistory.created_at.desc()
        )
        .first()
    )

    return {
        "total_forecasts":
        total_forecasts,

        "total_history":
        total_history,

        "latest_model":
        (
            latest.model_name
            if latest
            else None
        ),

        "latest_accuracy":
        (
            latest.accuracy
            if latest
            else None
        )
    }


# ==========================
# ADVANCED FORECAST
# ==========================
@router.get("/advanced/{dataset_id}")
async def advanced_forecast(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_or_analyst_required
    )
):

    return await (
        forecast_manager
        .generate_advanced_forecast(
            db=db,
            dataset_id=dataset_id,
            current_user=current_user
        )
    )


# ==========================
# NORMAL FORECAST
# ==========================
@router.get("/{dataset_id}")
async def forecast_dataset(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_or_analyst_required
    )
):

    return await (
        forecast_manager
        .generate_normal_forecast(
            db=db,
            dataset_id=dataset_id,
            current_user=current_user
        )
    )