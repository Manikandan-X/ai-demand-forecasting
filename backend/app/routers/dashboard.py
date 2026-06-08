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
from app.services.dashboard_manager_service import (
    DashboardManagerService
)

from app.core.rbac import (
    analyst_or_viewer_required
)




router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)
dashboard_manager = (
    DashboardManagerService()
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

    return await (
        dashboard_manager
        .dashboard_overview(
            db=db,
            current_user=current_user
        )
    )


# MONTHLY SALES TRENDS
@router.get("/monthly-sales")
# @cache(expire=60)
async def monthly_sales(
    dataset_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(analyst_or_viewer_required)
):

    return await (
        dashboard_manager
        .monthly_sales(
            dataset_id=dataset_id,
            db=db,
            current_user=current_user
        )
    )


# TOP PRODUCTS
@router.get("/top-products")
# @cache(expire=60)
async def top_products(
    dataset_id: int,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User =Depends(analyst_or_viewer_required)
):

    return await (
        dashboard_manager
        .top_products(
            dataset_id=dataset_id,
            limit=limit,
            db=db,
            current_user=current_user
        )
    )


# CATEGORY FILTER ANALYTICS
@router.get("/category-analysis")
# @cache(expire=60)
async def category_analysis(
    dataset_id: int,
    category: str = Query(None),

    db: Session = Depends(get_db),

    current_user: User = Depends(analyst_or_viewer_required)
):

    return await (
        dashboard_manager
        .category_analysis(
            dataset_id=dataset_id,
            category=category,
            db=db,
            current_user=current_user
        )
    )


# RECENT FORECAST ACTIVITY
@router.get("/recent-activities")
async def recent_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    return await (
        dashboard_manager
        .recent_activities(
            db=db,
            current_user=current_user
        )
    )


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

    return await (
        dashboard_manager
        .get_dashboard(
            dataset_id=dataset_id,
            region=region,
            category=category,
            start_date=start_date,
            end_date=end_date,
            db=db,
            current_user=current_user
        )
    )

    