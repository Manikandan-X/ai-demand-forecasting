import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.dataset import Dataset
from app.models.forecast import Forecast
from app.models.forecast_history import (
    ForecastHistory
)
from app.models.user import User

from app.services.forecast_service import (
    generate_forecast
)

from app.services.advanced_forecast_service import (
    AdvancedForecastService
)

from app.utils.notification_utils import (
    create_notification
)

from app.routers.websocket import (
    send_dashboard_update
)

from app.core.rbac import (
    admin_or_analyst_required,
    analyst_or_viewer_required
)

from app.utils.activity_logger import (
    log_user_activity
)
from app.utils.cache_utils import clear_dashboard_cache

from app.services.model_retraining_service import (
    ModelRetrainingService
)

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
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
            h.created_at,

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

    dataset = (
        db.query(
            Dataset.id,
            Dataset.filename,
            Dataset.file_path
        )
        .filter(
            Dataset.id == dataset_id,
            Dataset.uploaded_by ==
            current_user.id
        )
        .first()
    )

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    # ownership check
    if (
        current_user.role
        != "super_admin"
        and
        dataset.uploaded_by
        != current_user.id
    ):

        raise HTTPException(
            status_code=403,
            detail=(
                "Access denied"
            )
        )

    retrainer = (
        ModelRetrainingService()
    )

    results = (
        retrainer.retrain_model(
            db=db,
            dataset=dataset,
            current_user=current_user
        )
    )

    best_model = results[
        "best_model"
    ]

    history = ForecastHistory(
        user_id=current_user.id,

        dataset_id=dataset.id,

        model_name=best_model[
            "model"
        ],

        accuracy=best_model[
            "accuracy"
        ],

        forecast_result=json.dumps(
            best_model[
                "future_predictions"
            ]
        )
    )

    db.add(history)

    db.commit()

    log_user_activity(
        db=db,

        user_id=current_user.id,

        action=(
            "ADVANCED_FORECAST_GENERATED"
        ),

        details=(
            f"Advanced forecast "
            f"generated for "
            f"{dataset.filename}"
        )
    )
    
    #clear_dashboard_cache(current_user.id)

    await create_notification(
        db=db,

        title="Forecast Completed",

        message=(
            "Advanced forecast "
            "completed"
        ),

        user_id=current_user.id,

        notification_type="forecast",

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

    dataset = (
        db.query(
            Dataset.id,
            Dataset.filename,
            Dataset.file_path
        )
        .filter(
            Dataset.id == dataset_id,
            Dataset.uploaded_by ==
            current_user.id
        )
        .first()
    )

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    # ownership check
    if (
        current_user.role
        != "super_admin"
        and
        dataset.uploaded_by
        != current_user.id
    ):

        raise HTTPException(
            status_code=403,
            detail=(
                "Access denied"
            )
        )

    retrainer = (
        ModelRetrainingService()
    )

    retrained_result = (
        retrainer.retrain_model(
            db=db,
            dataset=dataset,
            current_user=current_user
        )
    )

    forecast_data = (
        generate_forecast(
            dataset.file_path
        )
    )

    # save predictions
    for prediction in (
        forecast_data[
            "future_predictions"
        ]
    ):

        forecast = Forecast(
            dataset_id=dataset.id,

            predicted_value=
            prediction[
                "predicted_sales"
            ],

            prediction_date=(
                f"Day "
                f"{prediction['day']}"
            ),

            model_used=
            "Linear Regression"
        )

        db.add(forecast)

    history = ForecastHistory(
        user_id=current_user.id,

        dataset_id=dataset.id,

        model_name=
        "Linear Regression",

        accuracy=forecast_data[
            "forecast_accuracy_mae"
        ],

        forecast_result=json.dumps(
            forecast_data[
                "future_predictions"
            ]
        )
    )

    db.add(history)

    db.commit()

    log_user_activity(
        db=db,

        user_id=current_user.id,

        action=
        "FORECAST_GENERATED",

        details=(
            f"Forecast generated "
            f"for "
            f"{dataset.filename}"
        )
    )
    
    #clear_dashboard_cache(current_user.id)

    await create_notification(
        db=db,

        title=
        "Forecast Completed",

        message=(
            "Forecast generation "
            "completed"
        ),

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