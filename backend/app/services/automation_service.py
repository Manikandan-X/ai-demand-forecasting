import json

import pandas as pd

from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.models.dataset import Dataset

from app.models.forecast_history import (
    ForecastHistory
)

from app.services.advanced_forecast_service import (
    AdvancedForecastService
)

from app.services.notification_service import (
    NotificationService
)

from app.services.alert_service import (
    AlertService
)

from app.services.dataset_service import (
    process_dataset
)

from app.services.automation_log_service import (
    AutomationLogService
)

from app.services.automation_settings_service import (
    AutomationSettingsService
)
from app.services.webhook_service import WebhookService

class AutomationService:

    forecasts_generated = 0

    alerts_generated = 0

    datasets_processed = 0

    # ==========================
    # DAILY FORECAST AUTOMATION
    # ==========================
    @staticmethod
    def run_daily_forecasts():

        db: Session = SessionLocal()
        
        settings = (
            AutomationSettingsService
            .get_settings(db)
        )

        if not settings.forecast_enabled:

            print(
                "Forecast automation disabled"
            )

            return

        try:

            AutomationService.forecasts_generated = 0

            datasets = db.query(
                Dataset
            ).all()

            forecast_service = (
                AdvancedForecastService()
            )

            for dataset in datasets:

                try:

                    results = (
                        forecast_service
                        .compare_models(
                            dataset.file_path
                        )
                    )

                    best_model = (
                        results["best_model"]
                    )

                    history = ForecastHistory(

                        user_id=
                        dataset.uploaded_by,

                        dataset_id=
                        dataset.id,

                        model_name=
                        best_model["model"],

                        accuracy=
                        best_model["accuracy"],

                        forecast_result=
                        json.dumps(
                            best_model[
                                "future_predictions"
                            ]
                        )
                    )

                    db.add(history)

                    NotificationService.create_notification(

                        db=db,

                        title=
                        "Forecast Completed",

                        message=
                        (
                            f"Forecast generated "
                            f"for dataset "
                            f"{dataset.filename}"
                        ),

                        user_id=
                        dataset.uploaded_by,

                        notification_type=
                        "forecast",

                        is_admin=False
                    )

                    AutomationService.forecasts_generated += 1

                except Exception as e:

                    AutomationLogService.create_log(

                        db=db,

                        job_name=
                        "Daily Forecast",

                        status=
                        "FAILED",

                        message=str(e)
                    )

                    print(
                        f"Forecast failed "
                        f"for dataset "
                        f"{dataset.id}: "
                        f"{e}"
                    )

            db.commit()
            
            
            WebhookService.fire_event(
                db=db,
                event="forecast.completed",
                payload={
                    "forecasts_generated": AutomationService.forecasts_generated
                },
            )

            AutomationLogService.create_log(

                db=db,

                job_name=
                "Daily Forecast",

                status=
                "SUCCESS",

                message=
                (
                    f"{AutomationService.forecasts_generated} "
                    f"forecasts generated"
                )
            )

            NotificationService.create_notification(

                db=db,

                title=
                "Automation Job Completed",

                message=
                (
                    f"{AutomationService.forecasts_generated} "
                    f"forecast(s) generated"
                ),

                notification_type=
                "automation",

                is_admin=True
            )

            db.commit()

            print(
                f"Automated forecasts completed "
                f"({AutomationService.forecasts_generated})"
            )

        finally:

            db.close()

    # ==========================
    # DATASET PROCESSING JOB
    # ==========================
    @staticmethod
    def process_new_datasets():

        db: Session = SessionLocal()
        
        settings = (
            AutomationSettingsService
            .get_settings(db)
        )

        if (
            not settings
            .dataset_processing_enabled
        ):

            print(
                "Dataset automation disabled"
            )

            return

        try:

            AutomationService.datasets_processed = 0

            datasets = db.query(
                Dataset
            ).all()

            for dataset in datasets:

                try:

                    process_dataset(
                        dataset.file_path
                    )

                    NotificationService.create_notification(

                        db=db,

                        title=
                        "Dataset Processed",

                        message=
                        (
                            f"{dataset.filename} "
                            f"processed automatically"
                        ),

                        user_id=
                        dataset.uploaded_by,

                        notification_type=
                        "automation",

                        is_admin=False
                    )

                    AutomationService.datasets_processed += 1

                except Exception as e:

                    AutomationLogService.create_log(

                        db=db,

                        job_name=
                        "Dataset Processing",

                        status=
                        "FAILED",

                        message=str(e)
                    )

                    print(
                        f"Dataset processing "
                        f"failed for "
                        f"{dataset.id}: "
                        f"{e}"
                    )

            AutomationLogService.create_log(

                db=db,

                job_name=
                "Dataset Processing",

                status=
                "SUCCESS",

                message=
                (
                    f"{AutomationService.datasets_processed} "
                    f"datasets processed"
                )
            )

            NotificationService.create_notification(

                db=db,

                title=
                "Dataset Processing Completed",

                message=
                (
                    f"{AutomationService.datasets_processed} "
                    f"dataset(s) processed"
                ),

                notification_type=
                "automation",

                is_admin=True
            )

            db.commit()
            
            WebhookService.fire_event(
                db=db,
                event="dataset.processed",
                payload={
                    "datasets_processed": AutomationService.datasets_processed
                },
            )

            print(
                f"Processed "
                f"{AutomationService.datasets_processed} "
                f"datasets"
            )

        finally:

            db.close()

    # ==========================
    # ALERT GENERATION JOB
    # ==========================
    @staticmethod
    def generate_alerts():

        db: Session = SessionLocal()
        
        settings = (
            AutomationSettingsService
            .get_settings(db)
        )

        if not settings.alerts_enabled:

            print(
                "Alert automation disabled"
            )

            return

        try:

            AutomationService.alerts_generated = 0

            datasets = db.query(
                Dataset
            ).all()

            for dataset in datasets:

                try:

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

                    alerts = []

                    drop_alert = (
                        AlertService
                        .detect_sales_drop(df)
                    )

                    if drop_alert:

                        alerts.append(
                            drop_alert
                        )

                    spike_alert = (
                        AlertService
                        .detect_sales_spike(df)
                    )

                    if spike_alert:

                        alerts.append(
                            spike_alert
                        )

                    anomaly_alert = (
                        AlertService
                        .detect_anomaly(df)
                    )

                    if anomaly_alert:

                        alerts.append(
                            anomaly_alert
                        )

                    for alert in alerts:

                        NotificationService.create_notification(

                            db=db,

                            title=
                            "Business Alert",

                            message=
                            (
                                f"{alert} "
                                f"({dataset.filename})"
                            ),

                            user_id=
                            dataset.uploaded_by,

                            notification_type=
                            "alert",

                            is_admin=False
                        )

                        AutomationService.alerts_generated += 1

                except Exception as e:

                    AutomationLogService.create_log(

                        db=db,

                        job_name=
                        "Alert Engine",

                        status=
                        "FAILED",

                        message=str(e)
                    )

                    print(
                        f"Alert engine error: "
                        f"{e}"
                    )

            AutomationLogService.create_log(

                db=db,

                job_name=
                "Alert Engine",

                status=
                "SUCCESS",

                message=
                (
                    f"{AutomationService.alerts_generated} "
                    f"alerts generated"
                )
            )

            NotificationService.create_notification(

                db=db,

                title=
                "Alert Job Completed",

                message=
                (
                    f"{AutomationService.alerts_generated} "
                    f"alert(s) generated"
                ),

                notification_type=
                "automation",

                is_admin=True
            )

            db.commit()
            
            WebhookService.fire_event(
                db=db,
                event="alert.generated",
                payload={
                    "alerts_generated": AutomationService.alerts_generated
                },
            )

            print(
                f"Alert generation completed "
                f"({AutomationService.alerts_generated})"
            )

        finally:

            db.close()