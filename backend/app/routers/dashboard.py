import pandas as pd

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import func
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

from app.core.rbac import (
    analyst_or_viewer_required
)




router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# DASHBOARD OVERVIEW
@router.get("/overview")
# @cache(expire=60)
async def dashboard_overview(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
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

    average_accuracy = db.query(
        func.avg(
            ForecastHistory.accuracy
        )
    ).filter(
        ForecastHistory.user_id ==
        current_user.id
    ).scalar()

    if average_accuracy:

        average_accuracy = round(
            float(
                average_accuracy
            ),
            2
        )

    else:

        average_accuracy = 0

    return {
        "total_datasets":
        total_datasets,

        "total_forecasts":
        total_forecasts,

        "average_accuracy":
        average_accuracy
    }


# MONTHLY SALES TRENDS
@router.get("/monthly-sales")
# @cache(expire=60)
async def monthly_sales(
    dataset_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(analyst_or_viewer_required)
):

    dataset = db.query(
        Dataset
    ).filter(
        Dataset.id ==
        dataset_id,

        Dataset.uploaded_by ==
        current_user.id
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
# @cache(expire=60)
async def top_products(
    dataset_id: int,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User =Depends(analyst_or_viewer_required)
):

    dataset = db.query(
        Dataset
    ).filter(
        Dataset.id ==
        dataset_id,

        Dataset.uploaded_by ==
        current_user.id
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
# @cache(expire=60)
async def category_analysis(
    dataset_id: int,
    category: str = Query(None),

    db: Session = Depends(get_db),

    current_user: User = Depends(analyst_or_viewer_required)
):

    dataset = db.query(
        Dataset
    ).filter(
        Dataset.id ==
        dataset_id,

        Dataset.uploaded_by ==
        current_user.id
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
        analyst_or_viewer_required
    )
):

    activities = (
        db.query(
            ForecastHistory.id,
            ForecastHistory.dataset_id,
            ForecastHistory.model_name,
            ForecastHistory.accuracy,
            ForecastHistory.created_at
        )
        .filter(
            ForecastHistory.user_id ==
            current_user.id
        )
        .order_by(
            ForecastHistory.created_at.desc()
        )
        .limit(10)
        .all()
    )

    return [
        {
            "id": activity.id,
            "dataset_id":
            activity.dataset_id,

            "model_name":
            activity.model_name,

            "accuracy":
            activity.accuracy,

            "created_at":
            activity.created_at
        }
        for activity in activities
    ]


@router.get("/search")
async def global_search(

    search: str = Query(None),

    type: str = Query(None),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    if not search:

        return []

    search = search.strip()

    results = []

    # =========================
    # DATASET SEARCH
    # =========================
    if type == "dataset":

        query = db.query(
            Dataset
        ).filter(
            Dataset.uploaded_by ==
            current_user.id
        )

        if search.isdigit():

            query = query.filter(
                Dataset.id ==
                int(search)
            )

        else:

            query = query.filter(
                Dataset.filename.ilike(
                    f"%{search}%"
                )
            )

        datasets = query.all()

        for item in datasets:

            results.append({
                "id":
                item.id,

                "name":
                item.filename,

                "type":
                "dataset"
            })

    # =========================
    # FORECAST SEARCH
    # =========================
    elif type == "forecast":

        query = db.query(
            ForecastHistory
        ).filter(
            ForecastHistory.user_id ==
            current_user.id
        )

        if search.isdigit():

            query = query.filter(
                ForecastHistory.id ==
                int(search)
            )

        else:

            query = query.filter(
                ForecastHistory.model_name.ilike(
                    f"%{search}%"
                )
            )

        forecasts = query.all()

        for item in forecasts:

            results.append({
                "id":
                item.id,

                "name":
                item.model_name,

                "type":
                "forecast"
            })

    # =========================
    # USER SEARCH
    # =========================
    elif type == "user":

        query = db.query(User)

        if search.isdigit():

            query = query.filter(
                User.id ==
                int(search)
            )

        else:

            query = query.filter(
                User.name.ilike(
                    f"%{search}%"
                )
            )

        users = query.all()

        for item in users:

            results.append({
                "id":
                item.id,

                "name":
                item.name,

                "type":
                "user"
            })

    # =========================
    # REPORT SEARCH
    # =========================
    elif type == "report":

        query = db.query(
            Dataset
        ).filter(
            Dataset.uploaded_by ==
            current_user.id
        )

        if search.isdigit():

            query = query.filter(
                Dataset.id ==
                int(search)
            )

        else:

            query = query.filter(
                Dataset.filename.ilike(
                    f"%{search}%"
                )
            )

        reports = query.all()

        for item in reports:

            results.append({
                "id":
                item.id,

                "name":
                item.filename,

                "type":
                "report",

                "excel_url":
                f"/reports/excel/{item.id}",

                "pdf_url":
                f"/reports/pdf/{item.id}"
            })

    return results
                
@router.get("/{dataset_id}")
async def get_dashboard(

    dataset_id: int,

    region: str = Query(None),

    category: str = Query(None),

    start_date: str = Query(None),

    end_date: str = Query(None),
    
    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    # =========================
    # CHECK DATASET
    # =========================
    dataset = db.query(
        Dataset
    ).filter(

        Dataset.id ==
        dataset_id,

        Dataset.uploaded_by ==
        current_user.id

    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    # =========================
    # GENERATE DASHBOARD DATA
    # =========================
    dashboard_data = generate_dashboard_data(

        file_path=dataset.file_path,

        region=region,

        category=category,

        start_date=start_date,

        end_date=end_date
    )
    
    
    # =========================
    # RESPONSE
    # =========================
    return {

        "dataset_id":
        dataset.id,

        "filename":
        dataset.filename,

        "analytics":
        dashboard_data
    }

    