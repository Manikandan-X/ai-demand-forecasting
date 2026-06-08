import pandas as pd

from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.models.ai_insight import AIInsight

from app.services.notification_service import (
    NotificationService
)


class AIInsightService:

    # ==========================
    # LOAD DATASET
    # ==========================
    @staticmethod
    def load_dataset(

        db: Session,

        dataset_id: int
    ):

        dataset = (

            db.query(
                Dataset
            )

            .filter(
                Dataset.id == dataset_id
            )

            .first()
        )

        if not dataset:

            return None

        if dataset.file_path.endswith(".csv"):

            df = pd.read_csv(
                dataset.file_path
            )

        else:

            df = pd.read_excel(
                dataset.file_path
            )

        return dataset, df

    # ==========================
    # PRODUCT RECOMMENDATIONS
    # ==========================
    @staticmethod
    def generate_product_recommendations(

        db: Session,

        dataset_id: int
    ):

        result = (
            AIInsightService
            .load_dataset(
                db,
                dataset_id
            )
        )

        if not result:

            return []

        dataset, df = result

        grouped = (

            df.groupby(
                "Product"
            )["Quantity"]

            .sum()

            .sort_values(
                ascending=False
            )

            .head(10)
        )

        insights = []

        for product, quantity in grouped.items():

            priority = (
                "HIGH"
                if quantity > grouped.mean()
                else "MEDIUM"
            )

            recommendation = (
                "Increase Stock"
            )

            insights.append({

                "product":
                product,

                "total_quantity":
                int(quantity),

                "recommendation":
                recommendation,

                "priority":
                priority
            })

        return insights

    # ==========================
    # CUSTOMER ANALYSIS
    # ==========================
    @staticmethod
    def customer_behavior_analysis(

        db: Session,

        dataset_id: int
    ):

        result = (
            AIInsightService
            .load_dataset(
                db,
                dataset_id
            )
        )

        if not result:

            return []

        dataset, df = result

        grouped = (

            df.groupby(
                "Customer"
            )

            .agg({

                "Total_Amount":
                "sum",

                "Invoice_ID":
                "count"
            })

            .reset_index()
        )

        results = []

        for _, row in grouped.iterrows():

            total_spent = float(
                row["Total_Amount"]
            )

            purchases = int(
                row["Invoice_ID"]
            )

            if total_spent > 50000:

                segment = "VIP"

            elif total_spent > 10000:

                segment = "Regular"

            else:

                segment = "Occasional"

            results.append({

                "customer":
                row["Customer"],

                "total_spent":
                round(
                    total_spent,
                    2
                ),

                "purchase_count":
                purchases,

                "segment":
                segment
            })

        return sorted(

            results,

            key=lambda x:
            x["total_spent"],

            reverse=True
        )

    # ==========================
    # DEMAND SPIKES
    # ==========================
    @staticmethod
    def predict_demand_spikes(

        db: Session,

        dataset_id: int
    ):

        result = (
            AIInsightService
            .load_dataset(
                db,
                dataset_id
            )
        )

        if not result:

            return []

        dataset, df = result

        grouped = (

            df.groupby(
                "Product"
            )["Total_Amount"]

            .mean()

            .reset_index()
        )

        spikes = []

        for _, row in grouped.iterrows():

            avg_sales = float(
                row["Total_Amount"]
            )

            predicted_sales = (
                avg_sales * 1.6
            )

            spike = (
                predicted_sales >
                avg_sales * 1.5
            )

            spikes.append({

                "product":
                row["Product"],

                "average_sales":
                round(
                    avg_sales,
                    2
                ),

                "predicted_sales":
                round(
                    predicted_sales,
                    2
                ),

                "spike_detected":
                spike
            })

        return spikes

    # ==========================
    # INVENTORY OPTIMIZATION
    # ==========================
    @staticmethod
    def inventory_suggestions(

        db: Session,

        dataset_id: int
    ):

        result = (
            AIInsightService
            .load_dataset(
                db,
                dataset_id
            )
        )

        if not result:

            return []

        dataset, df = result

        grouped = (

            df.groupby(
                "Product"
            )["Quantity"]

            .mean()

            .reset_index()
        )

        suggestions = []

        for _, row in grouped.iterrows():

            recommended = int(
                row["Quantity"] * 1.25
            )

            suggestions.append({

                "product":
                row["Product"],

                "recommended_stock":
                recommended
            })

        return suggestions

    # ==========================
    # SAVE INSIGHT
    # ==========================
    @staticmethod
    def save_insight(

        db: Session,

        dataset_id: int,

        insight_type: str,

        title: str,

        description: str,

        priority: str = "MEDIUM"
    ):

        insight = AIInsight(

            dataset_id=
            dataset_id,

            insight_type=
            insight_type,

            title=
            title,

            description=
            description,

            priority=
            priority
        )

        db.add(insight)

        db.commit()

        db.refresh(insight)

        return insight

    # ==========================
    # AI NOTIFICATION
    # ==========================
    @staticmethod
    def create_ai_notification(

        db: Session,

        user_id: int,

        title: str,

        message: str
    ):

        NotificationService.create_notification(

            db=db,

            title=title,

            message=message,

            user_id=user_id,

            notification_type="ai",

            is_admin=False
        )