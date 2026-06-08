from app.db.session import SessionLocal

from app.models.dataset import (
    Dataset
)

from app.services.dataset_service import (
    process_dataset
)


def auto_process_datasets():

    db = SessionLocal()

    try:

        datasets = (
            db.query(
                Dataset
            )
            .all()
        )

        for dataset in datasets:

            process_dataset(
                dataset.file_path
            )

        print(
            "Dataset automation completed"
        )

    finally:

        db.close()