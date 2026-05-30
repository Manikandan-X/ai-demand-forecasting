import os
import shutil
import uuid

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.dataset import Dataset
from app.models.user import User

from app.core.rbac import (
    admin_or_analyst_required,
    analyst_or_viewer_required
)

from app.services.dataset_service import (
    process_dataset
)

from app.utils.notification_utils import (
    create_notification
)

from app.routers.websocket import (
    send_dashboard_update
)

from app.utils.activity_logger import (
    log_user_activity
)
from app.utils.cache_utils import clear_dashboard_cache

router = APIRouter(
    prefix="/dataset",
    tags=["Dataset"]
)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ==========================
# UPLOAD DATASET
# ==========================
@router.post("/upload")
async def upload_dataset(

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        admin_or_analyst_required
    )
):

    try:

        allowed_extensions = [
            ".csv",
            ".xlsx"
        ]

        file_extension = os.path.splitext(
            file.filename
        )[1].lower()

        if (
            file_extension
            not in allowed_extensions
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only CSV and "
                    "Excel files allowed"
                )
            )

        # unique filename
        unique_filename = (
            f"{current_user.id}_"
            f"{uuid.uuid4()}_"
            f"{file.filename}"
        )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            unique_filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        dataset = Dataset(
            filename=file.filename,
            file_path=file_path,
            uploaded_by=current_user.id
        )

        db.add(dataset)

        db.commit()

        db.refresh(dataset)

        # activity log
        log_user_activity(
            db=db,
            user_id=current_user.id,
            action="DATASET_UPLOAD",
            details=(
                f"{dataset.filename} "
                f"uploaded"
            )
        )

        # dataset processing
        summary = process_dataset(
            file_path
        )
        
        #clear_dashboard_cache(current_user.id)

        # success notification
        await create_notification(
            db=db,
            title="Dataset Uploaded",
            message=(
                f"{dataset.filename} "
                f"uploaded successfully"
            ),
            user_id=current_user.id,
            notification_type="upload",
            is_admin=False
        )

        # realtime dashboard refresh
        await send_dashboard_update(
            user_id=current_user.id
        )

        return {
            "message":
            "Dataset uploaded successfully",

            "dataset_id":
            dataset.id,

            "filename":
            dataset.filename,

            "summary":
            summary
        }

    except HTTPException:
        raise

    except Exception as e:

        await create_notification(
            db=db,
            title="Upload Failed",
            message=(
                "Dataset upload failed"
            ),
            user_id=current_user.id,
            notification_type="upload",
            is_admin=False
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
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

    skip = (
        page - 1
    ) * limit

    query = db.query(
        Dataset
    )

    # non-admin only sees own
    if current_user.role != "super_admin":

        query = query.filter(
            Dataset.uploaded_by ==
            current_user.id
        )

    total = query.count()

    datasets = (
        query.order_by(
            Dataset.created_at.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "datasets": datasets
    }


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

    query = db.query(
        Dataset
    )

    if current_user.role != "super_admin":

        query = query.filter(
            Dataset.uploaded_by ==
            current_user.id
        )

    datasets = query.filter(
        Dataset.filename.ilike(
            f"%{keyword}%"
        )
    ).all()

    return datasets


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

    query = db.query(
        Dataset
    )

    if current_user.role != "super_admin":

        query = query.filter(
            Dataset.uploaded_by ==
            current_user.id
        )

    if start_date:

        query = query.filter(
            Dataset.created_at >=
            start_date
        )

    if end_date:

        query = query.filter(
            Dataset.created_at <=
            end_date
        )

    datasets = query.order_by(
        Dataset.created_at.desc()
    ).all()

    return datasets