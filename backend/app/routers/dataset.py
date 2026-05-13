import os
import shutil

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException

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