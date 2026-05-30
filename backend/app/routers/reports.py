import pandas as pd

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import BackgroundTasks

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.dataset import Dataset
from app.models.user import User

from app.core.rbac import (
    analyst_or_viewer_required
)

from app.services.report_service import (
    generate_excel_report,
    generate_pdf_report
)

from app.utils.notification_utils import (
    create_notification
)

from app.utils.activity_logger import (
    log_user_activity
)

from app.routers.websocket import (
    send_dashboard_update
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# ==========================
# BACKGROUND TASK
# ==========================
def log_report_generation():

    print(
        "Report generated successfully"
    )


# ==========================
# EXPORT EXCEL REPORT
# ==========================
@router.get("/excel/{dataset_id}")
async def export_excel_report(

    dataset_id: int,

    background_tasks:
    BackgroundTasks,

    db: Session = Depends(
        get_db
    ),

    current_user: User =
    Depends(
        analyst_or_viewer_required
    )
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

    if dataset.file_path.endswith(
        ".csv"
    ):

        df = pd.read_csv(
            dataset.file_path
        )

    else:

        df = pd.read_excel(
            dataset.file_path
        )

    report_path = (
        generate_excel_report(
            df,
            f"dataset_{dataset_id}.xlsx"
        )
    )

    log_user_activity(
        db=db,
        user_id=current_user.id,
        action=
        "REPORT_EXCEL_DOWNLOAD",
        details=(
            f"Excel report "
            f"downloaded for "
            f"{dataset.filename}"
        )
    )

    await create_notification(
        db=db,
        title=
        "Report Generated",
        message=
        "Excel report generated successfully",
        user_id=
        current_user.id,
        notification_type=
        "report",
        is_admin=False
    )

    await send_dashboard_update(
        user_id=
        current_user.id
    )

    background_tasks.add_task(
        log_report_generation
    )

    return FileResponse(

        path=report_path,

        filename=(
            f"dataset_"
            f"{dataset_id}.xlsx"
        ),

        media_type=(
            "application/"
            "vnd.openxmlformats-"
            "officedocument."
            "spreadsheetml.sheet"
        )
    )


# ==========================
# EXPORT PDF REPORT
# ==========================
@router.get("/pdf/{dataset_id}")
async def export_pdf_report(

    dataset_id: int,

    background_tasks:
    BackgroundTasks,

    db: Session = Depends(
        get_db
    ),

    current_user: User =
    Depends(
        analyst_or_viewer_required
    )
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

    if dataset.file_path.endswith(
        ".csv"
    ):

        df = pd.read_csv(
            dataset.file_path
        )

    else:

        df = pd.read_excel(
            dataset.file_path
        )

    report_path = (
        generate_pdf_report(
            df,
            f"dataset_{dataset_id}.pdf"
        )
    )

    log_user_activity(
        db=db,
        user_id=current_user.id,
        action=
        "REPORT_PDF_DOWNLOAD",
        details=(
            f"PDF report "
            f"downloaded for "
            f"{dataset.filename}"
        )
    )

    await create_notification(
        db=db,
        title=
        "Report Generated",
        message=
        "PDF report generated successfully",
        user_id=
        current_user.id,
        notification_type=
        "report",
        is_admin=False
    )

    await send_dashboard_update(
        user_id=
        current_user.id
    )

    background_tasks.add_task(
        log_report_generation
    )

    return FileResponse(

        path=report_path,

        filename=(
            f"dataset_"
            f"{dataset_id}.pdf"
        ),

        media_type=
        "application/pdf"
    )