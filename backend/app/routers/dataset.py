import os
import shutil

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

from app.core.dependencies import get_current_user
from app.services.dataset_service import process_dataset

router = APIRouter(
    prefix="/dataset",
    tags=["Dataset"]
)

UPLOAD_FOLDER = "uploads"


@router.post("/upload")
def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    allowed_extensions = [
        ".csv",
        ".xlsx"
    ]

    file_extension = os.path.splitext(
        file.filename
    )[1]

    if file_extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files allowed"
        )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:

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
    
    summary = process_dataset(file_path)

    return {
        "message": "Dataset uploaded successfully",
        "dataset_id": dataset.id,
        "filename": dataset.filename,
        "summary": summary
    }
    
@router.get("/")
def get_datasets(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    skip = (page - 1) * limit

    datasets = db.query(
        Dataset
    ).filter(
        Dataset.uploaded_by ==
        current_user.id
    ).offset(skip).limit(limit).all()

    total = db.query(
        Dataset
    ).filter(
        Dataset.uploaded_by ==
        current_user.id
    ).count()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "datasets": datasets
    }
    
@router.get("/search/")
def search_datasets(
    keyword: str,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    datasets = db.query(
        Dataset
    ).filter(
        Dataset.uploaded_by ==
        current_user.id,

        Dataset.filename.ilike(
            f"%{keyword}%"
        )
    ).all()

    return datasets

@router.get("/filter/")
def filter_datasets(
    start_date: str = None,
    end_date: str = None,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    query = db.query(
        Dataset
    ).filter(
        Dataset.uploaded_by ==
        current_user.id
    )

    if start_date:

        query = query.filter(
            Dataset.created_at >= start_date
        )

    if end_date:

        query = query.filter(
            Dataset.created_at <= end_date
        )

    datasets = query.all()

    return datasets