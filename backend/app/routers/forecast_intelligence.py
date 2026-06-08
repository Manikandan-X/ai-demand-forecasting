from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.dataset import Dataset
from app.models.user import User

from app.core.rbac import (
    analyst_or_viewer_required
)

from app.services.forecast_intelligence_service import (
    ForecastIntelligenceService
)

router = APIRouter(
    prefix="/forecast-intelligence",
    tags=["Forecast Intelligence"]
)


# ==========================================
# DATASET ACCESS CHECK
# ==========================================
def validate_dataset(

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


# ==========================================
# MODEL COMPARISON
# ==========================================
@router.get(
    "/model-comparison/{dataset_id}"
)
def model_comparison(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    validate_dataset(
        db,
        dataset_id,
        current_user
    )

    return {

        "dataset_id":
        dataset_id,

        "comparison":
        (
            ForecastIntelligenceService
            .model_comparison(
                db,
                dataset_id
            )
        )
    }


# ==========================================
# ACCURACY TRENDS
# ==========================================
@router.get(
    "/accuracy-trends/{dataset_id}"
)
def accuracy_trends(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    validate_dataset(
        db,
        dataset_id,
        current_user
    )

    return {

        "dataset_id":
        dataset_id,

        "trends":
        (
            ForecastIntelligenceService
            .accuracy_trends(
                db,
                dataset_id
            )
        )
    }


# ==========================================
# HISTORICAL FORECASTS
# ==========================================
@router.get(
    "/historical-comparison/{dataset_id}"
)
def historical_comparison(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    validate_dataset(
        db,
        dataset_id,
        current_user
    )

    return {

        "dataset_id":
        dataset_id,

        "history":
        (
            ForecastIntelligenceService
            .historical_comparison(
                db,
                dataset_id
            )
        )
    }


# ==========================================
# CONFIDENCE SCORE
# ==========================================
@router.get(
    "/confidence-score/{dataset_id}"
)
def confidence_score(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    validate_dataset(
        db,
        dataset_id,
        current_user
    )

    return {

        "dataset_id":
        dataset_id,

        "confidence":
        (
            ForecastIntelligenceService
            .forecast_confidence(
                db,
                dataset_id
            )
        )
    }


# ==========================================
# BUSINESS RECOMMENDATIONS
# ==========================================
@router.get(
    "/recommendations/{dataset_id}"
)
def business_recommendations(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    validate_dataset(
        db,
        dataset_id,
        current_user
    )

    return {

        "dataset_id":
        dataset_id,

        "recommendations":
        (
            ForecastIntelligenceService
            .business_recommendations(
                db,
                dataset_id
            )
        )
    }


# ==========================================
# COMPLETE DASHBOARD DATA
# ==========================================
@router.get(
    "/dashboard/{dataset_id}"
)
def forecast_dashboard(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    validate_dataset(
        db,
        dataset_id,
        current_user
    )

    return {

        "dataset_id":
        dataset_id,

        "model_comparison":
        (
            ForecastIntelligenceService
            .model_comparison(
                db,
                dataset_id
            )
        ),

        "accuracy_trends":
        (
            ForecastIntelligenceService
            .accuracy_trends(
                db,
                dataset_id
            )
        ),

        "confidence":
        (
            ForecastIntelligenceService
            .forecast_confidence(
                db,
                dataset_id
            )
        ),

        "recommendations":
        (
            ForecastIntelligenceService
            .business_recommendations(
                db,
                dataset_id
            )
        )
    }