from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.dataset import Dataset
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


@router.get("/{dataset_id}")
def get_dashboard(
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

    dashboard_data = generate_dashboard_data(
        dataset.file_path
    )

    return {
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "analytics": dashboard_data
    }