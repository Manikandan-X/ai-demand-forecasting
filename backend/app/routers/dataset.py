from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import Query
from fastapi import Request

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.user import User

from app.core.rate_limiter import (
    limiter
)

from app.core.rbac import (
    admin_or_analyst_required,
    analyst_or_viewer_required
)

from app.services.dataset_manager_service import (
    DatasetManagerService
)

router = APIRouter(
    prefix="/dataset",
    tags=["Dataset"]
)

dataset_manager = (
    DatasetManagerService()
)


# ==========================
# UPLOAD DATASET
# ==========================
@router.post("/upload")
@limiter.limit(
    "20/minute"
)
async def upload_dataset(

    request: Request,

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_or_analyst_required
    )
):

    return await (
        dataset_manager
        .upload_dataset(
            file=file,
            db=db,
            current_user=current_user
        )
    )


# ==========================
# GET DATASETS
# ==========================
@router.get("/")
def get_datasets(

    page: int = Query(
        1,
        ge=1
    ),

    limit: int = Query(
        5,
        ge=1,
        le=100
    ),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    return (
        dataset_manager
        .get_datasets(
            db=db,
            current_user=current_user,
            page=page,
            limit=limit
        )
    )


# ==========================
# SEARCH DATASET
# ==========================
@router.get("/search/")
def search_datasets(

    keyword: str,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    return (
        dataset_manager
        .search_datasets(
            db=db,
            current_user=current_user,
            keyword=keyword
        )
    )


# ==========================
# FILTER DATASET
# ==========================
@router.get("/filter/")
def filter_datasets(

    start_date: str = None,

    end_date: str = None,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        analyst_or_viewer_required
    )
):

    return (
        dataset_manager
        .filter_datasets(
            db=db,
            current_user=current_user,
            start_date=start_date,
            end_date=end_date
        )
    )