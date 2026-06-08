from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.deps import get_db

from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast_history import ForecastHistory
from app.models.admin_activity import AdminActivity
from app.models.forecast import Forecast

from app.core.rbac import (
    super_admin_required
)

from app.core.dependencies import (
    get_current_user
)

from app.core.rbac import (
    super_admin_required
)

from app.core.admin_dependencies import (
    admin_required
)

from app.utils.activity_logger import (
    log_user_activity
)

from app.models.user_activity import (
    UserActivity
)

from app.services.automation_dashboard_service import (
    AutomationDashboardService
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ADMIN DASHBOARD
@router.get("/dashboard")
# @cache(expire=60)
async def admin_dashboard(
    db: Session = Depends(get_db),
    _: User = Depends(
    super_admin_required
    )
):

    total_users = db.query(User).count()

    total_datasets = db.query(
        Dataset
    ).count()

    total_forecasts = db.query(
        ForecastHistory
    ).count()

    recent_forecasts = db.query(
        ForecastHistory
    ).order_by(
        ForecastHistory.created_at.desc()
    ).limit(5).all()

    return {
        "total_users": total_users,
        "total_datasets": total_datasets,
        "total_forecasts": total_forecasts,
        "recent_forecasts": recent_forecasts
    }


# GET ALL USERS
@router.get("/users")
async def get_all_users(

    page: int = 1,

    limit: int = 20,

    db: Session = Depends(get_db),

    admin: User = Depends(
        super_admin_required
    )
):

    skip = (
        page - 1
    ) * limit

    total = db.query(
        User
    ).count()

    users = db.query(
        User
    ).offset(skip).limit(
        limit
    ).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "users": users
    }


# GET ALL DATASETS
@router.get("/datasets")
async def get_all_datasets(

    page: int = 1,

    limit: int = 20,

    db: Session = Depends(get_db),

    admin: User = Depends(
        super_admin_required
    )
):

    skip = (
        page - 1
    ) * limit

    query = db.query(
        Dataset
    )

    total = query.count()

    datasets = query.order_by(
        Dataset.created_at.desc()
    ).offset(skip).limit(
        limit
    ).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "datasets": datasets
    }


# GET FORECAST HISTORY
@router.get("/forecasts")
async def get_forecasts(

    page: int = 1,

    limit: int = 20,

    db: Session = Depends(get_db),

    admin: User = Depends(
        super_admin_required
    )
):

    skip = (
        page - 1
    ) * limit

    query = db.query(
        ForecastHistory
    )

    total = query.count()

    forecasts = query.order_by(
        ForecastHistory.created_at.desc()
    ).offset(skip).limit(
        limit
    ).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "forecasts": forecasts
    }

# GET REPORTS
@router.get("/reports")
async def get_reports(

    page: int = 1,

    limit: int = 20,

    db: Session = Depends(get_db),

    admin: User = Depends(
        super_admin_required
    )
):

    skip = (
        page - 1
    ) * limit

    query = db.query(
        ForecastHistory
    )

    total = query.count()

    reports = query.order_by(
        ForecastHistory.created_at.desc()
    ).offset(skip).limit(
        limit
    ).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "reports": reports
    }

# SYSTEM ANALYTICS
@router.get("/analytics")
# @cache(expire=60)
async def system_analytics(

    db: Session = Depends(get_db),

    admin: User = Depends(
        super_admin_required
    )
):

    total_users = db.query(
        User
    ).count()

    total_datasets = db.query(
        Dataset
    ).count()

    total_forecasts = db.query(
        ForecastHistory
    ).count()

    average_accuracy = db.query(
        func.avg(
            ForecastHistory.accuracy
        )
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
        "users":
        total_users,

        "datasets":
        total_datasets,

        "forecasts":
        total_forecasts,

        "average_accuracy":
        average_accuracy
    }
    
@router.delete("/users/{user_id}")
async def delete_user(

    user_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    admin_required(current_user)

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.id == current_user.id:

        raise HTTPException(
            status_code=400,
            detail="Admin cannot delete own account"
        )
    
    log_user_activity(
        db=db,
        user_id=current_user.id,
        action="USER_DELETED",
        details=(
            f"Deleted user "
            f"{user.email}"
        )
    )    

    db.delete(user)

    db.commit()

    return {
        "message":
        "User deleted successfully"
    }


@router.delete("/datasets/{dataset_id}")
async def delete_dataset(

    dataset_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    admin_required(current_user)

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

    # Delete forecasts first
    db.query(Forecast).filter(
        Forecast.dataset_id == dataset.id
    ).delete()

    log_user_activity(
        db=db,
        user_id=current_user.id,
        action="DATASET_DELETED",
        details=(
            f"Deleted dataset "
            f"{dataset.filename}"
        )
    )
    # Delete dataset
    db.delete(dataset)

    db.commit()

    return {
        "message":
        "Dataset deleted successfully"
    }
    
from pydantic import BaseModel


class RoleUpdate(
    BaseModel
):
    role: str


@router.put(
    "/users/{user_id}/role"
)
async def update_user_role(

    user_id: int,

    body: RoleUpdate,

    db: Session = Depends(
        get_db
    ),

    current_user: User =
    Depends(
        get_current_user
    )
):

    admin_required(current_user)

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if body.role not in [
        "super_admin",
        "analyst",
        "viewer"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    user.role = body.role
    
    log_user_activity(
        db=db,
        user_id=current_user.id,
        action="ROLE_UPDATED",
        details=(
            f"{user.email} "
            f"changed to "
            f"{body.role}"
        )
    )   

    db.commit()

    db.refresh(user)

    return {
        "message":
        f"User role updated to {body.role}"
    }
    
@router.get("/activity-logs")
# @cache(expire=60)
async def get_activity_logs(

    page: int = 1,

    limit: int = 20,

    action: str = None,

    user_id: int = None,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        super_admin_required
    )
):

    skip = (
        page - 1
    ) * limit

    query = db.query(
        UserActivity
    )

    if action:

        query = query.filter(
            UserActivity.action == action
        )

    if user_id:

        query = query.filter(
            UserActivity.user_id ==
            user_id
        )

    total = query.count()

    logs = query.order_by(
        UserActivity.created_at.desc()
    ).offset(skip).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "logs": logs
    }
    
@router.get("/system-monitoring")
# @cache(expire=60)
async def system_monitoring(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        super_admin_required
    )
):

    total_logs = db.query(
        UserActivity
    ).count()

    total_api_requests = db.query(
        UserActivity
    ).filter(
        UserActivity.action ==
        "API_REQUEST"
    ).count()

    total_forecasts = db.query(
        ForecastHistory
    ).count()

    total_users = db.query(
        User
    ).count()

    latest_activities = db.query(
        UserActivity
    ).order_by(
        UserActivity.created_at.desc()
    ).limit(10).all()

    return {
        "total_logs":
        total_logs,

        "total_api_requests":
        total_api_requests,

        "total_forecasts":
        total_forecasts,

        "total_users":
        total_users,

        "latest_activities":
        latest_activities
    }
    
# =========================
# AUTOMATION DASHBOARD
# =========================
@router.get(
    "/automation/stats"
)
def automation_stats():

    return (
        AutomationDashboardService
        .get_automation_stats()
    )