from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.dataset import Dataset
from app.models.user import User

from app.core.rbac import (
    analyst_or_viewer_required,
    admin_or_analyst_required
)

from app.services.ai_insight_service import (
    AIInsightService
)

router = APIRouter(
    prefix="/ai",
    tags=["AI Insights"]
)


# ==========================================
# PRODUCT DEMAND RECOMMENDATIONS
# ==========================================
@router.get(
    "/recommendations/{dataset_id}"
)
def get_recommendations(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    dataset = (
        db.query(Dataset)
        .filter(
            Dataset.id == dataset_id
        )
        .first()
    )

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    if (
        current_user.role != "super_admin"
        and
        dataset.uploaded_by
        != current_user.id
    ):

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    recommendations = (
        AIInsightService
        .generate_product_recommendations(
            db=db,
            dataset_id=dataset_id
        )
    )

    return {
        "dataset_id": dataset_id,
        "recommendations":
        recommendations
    }


# ==========================================
# CUSTOMER BUYING BEHAVIOR
# ==========================================
@router.get(
    "/customer-behavior/{dataset_id}"
)
def customer_behavior(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    dataset = (
        db.query(Dataset)
        .filter(
            Dataset.id == dataset_id
        )
        .first()
    )

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    if (
        current_user.role != "super_admin"
        and
        dataset.uploaded_by
        != current_user.id
    ):

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    analysis = (
        AIInsightService
        .customer_behavior_analysis(
            db=db,
            dataset_id=dataset_id
        )
    )

    return {
        "dataset_id":
        dataset_id,

        "customers":
        analysis
    }


# ==========================================
# DEMAND SPIKE PREDICTION
# ==========================================
@router.get(
    "/demand-spikes/{dataset_id}"
)
def demand_spikes(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    dataset = (
        db.query(Dataset)
        .filter(
            Dataset.id == dataset_id
        )
        .first()
    )

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    if (
        current_user.role != "super_admin"
        and
        dataset.uploaded_by
        != current_user.id
    ):

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    spikes = (
        AIInsightService
        .predict_demand_spikes(
            db=db,
            dataset_id=dataset_id
        )
    )

    return {
        "dataset_id":
        dataset_id,

        "spikes":
        spikes
    }


# ==========================================
# LOW STOCK PREDICTION
# ==========================================
@router.get(
    "/low-stock/{dataset_id}"
)
def low_stock_prediction(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    recommendations = (
        AIInsightService
        .generate_product_recommendations(
            db=db,
            dataset_id=dataset_id
        )
    )

    risky_products = [

        item

        for item in recommendations

        if item["priority"] == "HIGH"
    ]

    return {

        "dataset_id":
        dataset_id,

        "high_risk_products":
        risky_products
    }


# ==========================================
# INVENTORY OPTIMIZATION
# ==========================================
@router.get(
    "/inventory-optimization/{dataset_id}"
)
def inventory_optimization(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    suggestions = (
        AIInsightService
        .inventory_suggestions(
            db=db,
            dataset_id=dataset_id
        )
    )

    return {

        "dataset_id":
        dataset_id,

        "suggestions":
        suggestions
    }


# ==========================================
# GENERATE + SAVE INSIGHTS
# ==========================================
@router.post(
    "/generate/{dataset_id}"
)
def generate_ai_insights(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_or_analyst_required
    )
):

    recommendations = (
        AIInsightService
        .generate_product_recommendations(
            db=db,
            dataset_id=dataset_id
        )
    )

    created = 0

    for item in recommendations:

        AIInsightService.save_insight(

            db=db,

            dataset_id=
            dataset_id,

            insight_type=
            "DEMAND_RECOMMENDATION",

            title=
            item["product"],

            description=
            item["recommendation"],

            priority=
            item["priority"]
        )

        created += 1

    AIInsightService.create_ai_notification(

        db=db,

        user_id=
        current_user.id,

        title=
        "AI Insights Generated",

        message=
        f"{created} AI insights created"
    )

    return {

        "message":
        "AI insights generated successfully",

        "insights_created":
        created
    }