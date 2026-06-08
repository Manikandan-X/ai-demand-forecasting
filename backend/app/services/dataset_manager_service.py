import os
import shutil
import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.dataset import Dataset

from app.services.dataset_service import (
    process_dataset
)

from app.services.notification_service import (
    NotificationService
)

from app.routers.websocket import (
    send_dashboard_update
)

from app.utils.activity_logger import (
    log_user_activity
)


class DatasetManagerService:

    def __init__(self):

        self.upload_folder = "uploads"

        os.makedirs(
            self.upload_folder,
            exist_ok=True
        )

        self.allowed_extensions = [
            ".csv",
            ".xlsx"
        ]

        self.allowed_content_types = [
            "text/csv",

            "application/csv",

            "application/vnd.ms-excel",

            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ]

    def validate_file(
        self,
        file
    ):

        file_extension = (
            os.path.splitext(
                file.filename
            )[1]
            .lower()
        )

        if (
            file_extension
            not in
            self.allowed_extensions
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only CSV and "
                    "Excel files allowed"
                )
            )

        if (
            file.content_type
            not in
            self.allowed_content_types
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid file type"
                )
            )

    def save_uploaded_file(
        self,
        file,
        current_user
    ):

        unique_filename = (
            f"{current_user.id}_"
            f"{uuid.uuid4()}_"
            f"{file.filename}"
        )

        file_path = os.path.join(
            self.upload_folder,
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

        return file_path

    async def upload_dataset(
        self,
        file,
        db: Session,
        current_user
    ):

        try:

            self.validate_file(
                file
            )
            
            file.file.seek(
                0,
                2
            )

            file_size = (
                file.file.tell()
            )

            file.file.seek(0)

            max_size = (
                25 * 1024 * 1024
            )

            if file_size > max_size:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "File size exceeds "
                        "25MB limit"
                    )
                )

            file_path = (
                self.save_uploaded_file(
                    file=file,
                    current_user=current_user
                )
            )

            dataset = Dataset(
                filename=file.filename,

                file_path=file_path,

                uploaded_by=current_user.id
            )

            db.add(dataset)

            db.commit()

            db.refresh(dataset)

            log_user_activity(
                db=db,

                user_id=current_user.id,

                action="DATASET_UPLOAD",

                details=(
                    f"{dataset.filename} "
                    f"uploaded"
                )
            )

            summary = (
                process_dataset(
                    file_path
                )
            )

            NotificationService.create_notification(
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

            NotificationService.create_notification(
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
            
    def get_datasets(

        self,

        db: Session,

        current_user,

        page: int,

        limit: int
    ):

        skip = (
            page - 1
        ) * limit

        query = db.query(
            Dataset
        )

        if (
            current_user.role
            != "super_admin"
        ):

            query = query.filter(
                Dataset.uploaded_by
                ==
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

            "page":
            page,

            "limit":
            limit,

            "total":
            total,

            "datasets":
            datasets
        }
        
    def search_datasets(

        self,

        db: Session,

        current_user,

        keyword: str
    ):

        query = db.query(
            Dataset
        )

        if (
            current_user.role
            != "super_admin"
        ):

            query = query.filter(
                Dataset.uploaded_by
                ==
                current_user.id
            )

        return query.filter(
            Dataset.filename.ilike(
                f"%{keyword}%"
            )
        ).all()
        
    def filter_datasets(

        self,

        db: Session,

        current_user,

        start_date=None,

        end_date=None
    ):

        query = db.query(
            Dataset
        )

        if (
            current_user.role
            != "super_admin"
        ):

            query = query.filter(
                Dataset.uploaded_by
                ==
                current_user.id
            )

        if start_date:

            query = query.filter(
                Dataset.created_at
                >= start_date
            )

        if end_date:

            query = query.filter(
                Dataset.created_at
                <= end_date
            )

        return (
            query.order_by(
                Dataset.created_at.desc()
            )
            .all()
        )