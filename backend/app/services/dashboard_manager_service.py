from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

import pandas as pd

from app.models.dataset import Dataset
from app.models.forecast_history import (
    ForecastHistory
)
from app.models.user import User

from app.services.dashboard_service import (
    generate_dashboard_data
)
from app.services.alert_service import (
    AlertService
)

from app.services.forecast_intelligence_service import (
    ForecastIntelligenceService
)

class DashboardManagerService:

    def get_dataset(
        self,
        db: Session,
        dataset_id: int,
        current_user
    ):

        dataset = (
            db.query(Dataset)
            .filter(
                Dataset.id ==
                dataset_id
            )
            .first()
        )

        if not dataset:

            raise HTTPException(
                status_code=404,
                detail="Dataset not found"
            )

        if (
            current_user.role
            != "super_admin"
            and
            dataset.uploaded_by
            != current_user.id
        ):

            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return dataset

    async def dashboard_overview(
        self,
        db: Session,
        current_user
    ):

        total_datasets = db.query(
            Dataset
        ).filter(
            Dataset.uploaded_by ==
            current_user.id
        ).count()

        total_forecasts = db.query(
            ForecastHistory
        ).filter(
            ForecastHistory.user_id ==
            current_user.id
        ).count()

        average_accuracy = db.query(
            func.avg(
                ForecastHistory.accuracy
            )
        ).filter(
            ForecastHistory.user_id ==
            current_user.id
        ).scalar()

        if average_accuracy:

            average_accuracy = round(
                float(
                    average_accuracy
                ),
                2
            )

        else:

            average_accuracy = 0

        return {
            "total_datasets":
            total_datasets,

            "total_forecasts":
            total_forecasts,

            "average_accuracy":
            average_accuracy
        }

    async def monthly_sales(
        self,
        dataset_id,
        db,
        current_user
    ):

        dataset = self.get_dataset(
            db=db,
            dataset_id=dataset_id,
            current_user=current_user
        )

        df = pd.read_csv(
            dataset.file_path
        )

        df.columns = (
            df.columns.str.strip()
        )

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d-%m-%Y"
        )

        df["Month"] = df[
            "Date"
        ].dt.strftime("%Y-%m")

        monthly_sales = (
            df.groupby(
                "Month"
            )[
                "Total_Amount"
            ]
            .sum()
        )

        return [
            {
                "month":
                month,

                "sales":
                float(sales)
            }
            for month, sales
            in monthly_sales.items()
        ]

    async def top_products(
        self,
        dataset_id,
        limit,
        db,
        current_user
    ):

        dataset = self.get_dataset(
            db=db,
            dataset_id=dataset_id,
            current_user=current_user
        )

        df = pd.read_csv(
            dataset.file_path
        )

        df.columns = (
            df.columns.str.strip()
        )

        top_products = (
            df.groupby(
                "Product"
            )[
                "Total_Amount"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(limit)
        )

        return [
            {
                "product":
                product,

                "sales":
                float(sales)
            }
            for product, sales
            in top_products.items()
        ]

    async def category_analysis(
        self,
        dataset_id,
        category,
        db,
        current_user
    ):

        dataset = self.get_dataset(
            db=db,
            dataset_id=dataset_id,
            current_user=current_user
        )

        df = pd.read_csv(
            dataset.file_path
        )

        df.columns = (
            df.columns.str.strip()
        )

        if category:

            df = df[
                df["Category"]
                == category
            ]

        grouped = (
            df.groupby(
                "Category"
            )[
                "Total_Amount"
            ]
            .sum()
        )

        return [
            {
                "category":
                cat,

                "sales":
                float(amount)
            }
            for cat, amount
            in grouped.items()
        ]

    async def recent_activities(
        self,
        db,
        current_user
    ):

        activities = (
            db.query(
                ForecastHistory.id,
                ForecastHistory.dataset_id,
                ForecastHistory.model_name,
                ForecastHistory.accuracy,
                ForecastHistory.created_at
            )
            .filter(
                ForecastHistory.user_id
                ==
                current_user.id
            )
            .order_by(
                ForecastHistory
                .created_at.desc()
            )
            .limit(10)
            .all()
        )

        return [
            {
                "id":
                activity.id,

                "dataset_id":
                activity.dataset_id,

                "model_name":
                activity.model_name,

                "accuracy":
                activity.accuracy,

                "created_at":
                activity.created_at
            }
            for activity
            in activities
        ]

    async def get_dashboard(
        self,
        dataset_id,
        region,
        category,
        start_date,
        end_date,
        db,
        current_user
    ):

        dataset = self.get_dataset(
            db=db,
            dataset_id=dataset_id,
            current_user=current_user
        )

        df = pd.read_csv(
            dataset.file_path
        )

        AlertService.process_dataset_alerts(
            db=db,
            user_id=current_user.id,
            df=df
        )
        dashboard_data = (
            generate_dashboard_data(
                file_path=
                dataset.file_path,

                region=region,

                category=category,

                start_date=
                start_date,

                end_date=
                end_date
            )
        )

        confidence = (
            ForecastIntelligenceService
            .forecast_confidence(
                db,
                dataset.id
            )
        )

        dashboard_data[
            "confidence_score"
        ] = confidence[
            "confidence_score"
        ]
        return {
            "dataset_id":
            dataset.id,

            "filename":
            dataset.filename,

            "analytics":
            dashboard_data,
            
            "forecast_confidence":
            confidence
        }