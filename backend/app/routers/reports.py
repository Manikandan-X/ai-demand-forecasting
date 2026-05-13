import pandas as pd

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.dataset import Dataset
from app.models.user import User

from app.core.dependencies import (
    get_current_user
)

from app.services.report_service import (
    generate_excel_report,
    generate_pdf_report
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/excel/{dataset_id}")
def export_excel_report(
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

    if dataset.file_path.endswith(".csv"):

        df = pd.read_csv(dataset.file_path)

    else:

        df = pd.read_excel(dataset.file_path)

    report_path = generate_excel_report(
        df,
        f"dataset_{dataset_id}.xlsx"
    )

    return FileResponse(
        path=report_path,
        filename=f"dataset_{dataset_id}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@router.get("/pdf/{dataset_id}")
def export_pdf_report(
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

    if dataset.file_path.endswith(".csv"):

        df = pd.read_csv(dataset.file_path)

    else:

        df = pd.read_excel(dataset.file_path)

    report_path = generate_pdf_report(
        df,
        f"dataset_{dataset_id}.pdf"
    )

    return FileResponse(
        path=report_path,
        filename=f"dataset_{dataset_id}.pdf",
        media_type="application/pdf"
    )