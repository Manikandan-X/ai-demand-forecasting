from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.user import User
from app.models.dataset import Dataset
from app.models.forecast_history import ForecastHistory
from app.models.admin_activity import AdminActivity
from app.models.forecast import Forecast

from app.core.admin_dependencies import (
    admin_required
)

from app.core.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ADMIN DASHBOARD
@router.get("/dashboard")
async def admin_dashboard(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
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
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):

    users = db.query(User).all()

    return users


# GET ALL DATASETS
@router.get("/datasets")
async def get_all_datasets(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):

    datasets = db.query(
        Dataset
    ).order_by(
        Dataset.created_at.desc()
    ).all()

    return datasets


# GET FORECAST HISTORY
@router.get("/forecasts")
async def get_forecasts(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):

    forecasts = db.query(
        ForecastHistory
    ).order_by(
        ForecastHistory.created_at.desc()
    ).all()

    return forecasts


# GET REPORTS
@router.get("/reports")
async def get_reports(

    db: Session = Depends(get_db),

    admin: User = Depends(
        admin_required
    )
):

    reports = db.query(
        ForecastHistory
    ).order_by(
        ForecastHistory.created_at.desc()
    ).all()

    return reports

# SYSTEM ANALYTICS
@router.get("/analytics")
async def system_analytics(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)
):

    total_users = db.query(User).count()

    total_datasets = db.query(
        Dataset
    ).count()

    total_forecasts = db.query(
        ForecastHistory
    ).count()

    avg_accuracy = db.query(
        ForecastHistory
    ).all()

    accuracy_list = []

    for item in avg_accuracy:

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
        "users": total_users,
        "datasets": total_datasets,
        "forecasts": total_forecasts,
        "average_accuracy": average_accuracy
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
        "admin",
        "user"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    user.role = body.role

    db.commit()

    db.refresh(user)

    return {
        "message":
        f"User role updated to {body.role}"
    }