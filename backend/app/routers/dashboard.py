import pandas as pd

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.dataset import Dataset
from app.models.forecast_history import (
    ForecastHistory
)

from app.models.user import User

from app.core.dependencies import (
    get_current_user
)
from app.services.dashboard_service import (
    generate_dashboard_data
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# DASHBOARD OVERVIEW
@router.get("/overview")
async def dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    total_datasets = db.query(
        Dataset
    ).filter(
        Dataset.uploaded_by ==
        current_user.id
    ).count()

    total_forecasts = db.query(
        ForecastHistory
    ).filter(
        ForecastHistory.user_id ==
        current_user.id
    ).count()

    forecasts = db.query(
        ForecastHistory
    ).filter(
        ForecastHistory.user_id ==
        current_user.id
    ).all()

    accuracy_list = []

    for item in forecasts:

        if item.accuracy:

            accuracy_list.append(
                item.accuracy
            )

    average_accuracy = 0

    if accuracy_list:

        average_accuracy = round(
            sum(accuracy_list)
            /
            len(accuracy_list),
            2
        )

    return {
        "total_datasets": total_datasets,
        "total_forecasts": total_forecasts,
        "average_accuracy": average_accuracy
    }


# MONTHLY SALES TRENDS
@router.get("/monthly-sales")
async def monthly_sales(
    dataset_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    dataset = db.query(
        Dataset
    ).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    df = pd.read_csv(
        dataset.file_path
    )

    df.columns = df.columns.str.strip()

    df["Date"] = pd.to_datetime(
        df["Date"],
        format="%d-%m-%Y"
    )

    df["Month"] = df[
        "Date"
    ].dt.strftime("%Y-%m")

    monthly_sales = df.groupby(
        "Month"
    )["Total_Amount"].sum()

    results = []

    for month, sales in monthly_sales.items():

        results.append({
            "month": month,
            "sales": float(sales)
        })

    return results


# TOP PRODUCTS
@router.get("/top-products")
async def top_products(
    dataset_id: int,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    dataset = db.query(
        Dataset
    ).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    df = pd.read_csv(
        dataset.file_path
    )

    df.columns = df.columns.str.strip()

    top_products = df.groupby(
        "Product"
    )["Total_Amount"].sum()

    top_products = top_products.sort_values(
        ascending=False
    ).head(limit)

    results = []

    for product, sales in top_products.items():

        results.append({
            "product": product,
            "sales": float(sales)
        })

    return results


# CATEGORY FILTER ANALYTICS
@router.get("/category-analysis")
async def category_analysis(
    dataset_id: int,
    category: str = Query(None),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    dataset = db.query(
        Dataset
    ).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    df = pd.read_csv(
        dataset.file_path
    )

    df.columns = df.columns.str.strip()

    if category:

        df = df[
            df["Category"] == category
        ]

    grouped = df.groupby(
        "Category"
    )["Total_Amount"].sum()

    results = []

    for cat, amount in grouped.items():

        results.append({
            "category": cat,
            "sales": float(amount)
        })

    return results


# RECENT FORECAST ACTIVITY
@router.get("/recent-activities")
async def recent_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    activities = db.query(
        ForecastHistory
    ).filter(
        ForecastHistory.user_id ==
        current_user.id
    ).order_by(
        ForecastHistory.created_at.desc()
    ).limit(10).all()

    return activities


@router.get("/{dataset_id}")
async def get_dashboard(
    dataset_id: int,

    region: str = Query(None),

    category: str = Query(None),

    start_date: str = Query(None),

    end_date: str = Query(None),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    dashboard_data = generate_dashboard_data(
        file_path=dataset.file_path,
        region=region,
        category=category,
        start_date=start_date,
        end_date=end_date
    )

    return {
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "analytics": dashboard_data
    }