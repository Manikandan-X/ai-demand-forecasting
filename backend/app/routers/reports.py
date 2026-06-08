from fastapi import APIRouter
from fastapi import Depends
from fastapi import BackgroundTasks

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.user import User

from app.core.rbac import (
    analyst_or_viewer_required
)

from app.services.report_service import (
    ReportService
)

from app.services.notification_service import (
    NotificationService
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

report_service = ReportService()


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

    report_path = await (
        report_service
        .export_excel_report(
            db=db,
            dataset_id=dataset_id,
            current_user=current_user
        )
    )

    NotificationService.create_notification(

        db=db,

        title="Report Ready",

        message=f"Excel report generated",

        user_id=current_user.id,

        notification_type="report"
    )
    
    background_tasks.add_task(
        log_report_generation
    )

    return FileResponse(

        path=report_path,

        filename=
        f"dataset_{dataset_id}.xlsx",

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

    report_path = await (
        report_service
        .export_pdf_report(
            db=db,
            dataset_id=dataset_id,
            current_user=current_user
        )
    )

    NotificationService.create_notification(

        db=db,

        title="Report Ready",

        message=f"PDF report generated",

        user_id=current_user.id,

        notification_type="report"
    )
    
    background_tasks.add_task(
        log_report_generation
    )

    return FileResponse(

        path=report_path,

        filename=
        f"dataset_{dataset_id}.pdf",

        media_type=
        "application/pdf"
    )