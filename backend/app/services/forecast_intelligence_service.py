import json
import numpy as np

from sqlalchemy.orm import Session

from app.models.forecast_history import (
    ForecastHistory
)


class ForecastIntelligenceService:

    @staticmethod
    def model_comparison(

        db: Session,
        dataset_id: int
    ):

        history = (

            db.query(
                ForecastHistory
            )

            .filter(
                ForecastHistory.dataset_id
                ==
                dataset_id
            )

            .all()
        )

        comparison = []

        for item in history:

            comparison.append({

                "model":
                item.model_name,

                "accuracy":
                item.accuracy,

                "created_at":
                item.created_at
            })

        comparison.sort(
            key=lambda x:
            x["accuracy"]
            if x["accuracy"]
            else 999999
        )

        return comparison

    @staticmethod
    def accuracy_trends(

        db: Session,
        dataset_id: int
    ):

        history = (

            db.query(
                ForecastHistory
            )

            .filter(
                ForecastHistory.dataset_id
                ==
                dataset_id
            )

            .order_by(
                ForecastHistory.created_at
            )

            .all()
        )

        return [

            {
                "date":
                item.created_at,

                "model":
                item.model_name,

                "accuracy":
                item.accuracy
            }

            for item in history
        ]

    @staticmethod
    def forecast_confidence(
        db: Session,
        dataset_id: int
    ):

        histories = (
            db.query(
                ForecastHistory
            )
            .filter(
                ForecastHistory.dataset_id
                ==
                dataset_id
            )
            .all()
            
        )
        for h in histories:
                print(
                    "MODEL:",
                    h.model_name,
                    "ACCURACY:",
                    h.accuracy
                )

        if not histories:

            return {
                "confidence_score": 0
            }

        accuracies = [
            h.accuracy
            for h in histories
            if h.accuracy is not None
        ]

        if not accuracies:

            return {
                "confidence_score": 0
            }

        return {
            "confidence_score":
            round(
                max(accuracies),
                2
            )
        }

    @staticmethod
    def historical_comparison(

        db: Session,
        dataset_id: int
    ):

        history = (

            db.query(
                ForecastHistory
            )

            .filter(
                ForecastHistory.dataset_id
                ==
                dataset_id
            )

            .order_by(
                ForecastHistory.created_at.desc()
            )

            .limit(10)

            .all()
        )

        results = []

        for item in history:

            forecast = []

            try:

                forecast = json.loads(
                    item.forecast_result
                )

            except:

                pass

            results.append({

                "model":
                item.model_name,

                "accuracy":
                item.accuracy,

                "forecast":
                forecast,

                "created_at":
                item.created_at
            })

        return results

    @staticmethod
    def business_recommendations(

        db: Session,
        dataset_id: int
    ):

        confidence = (
            ForecastIntelligenceService
            .forecast_confidence(
                db,
                dataset_id
            )
        )

        score = confidence[
            "confidence_score"
        ]

        recommendations = []

        if score >= 85:

            recommendations.append(
                "Increase inventory planning based on forecast demand."
            )

        elif score >= 70:

            recommendations.append(
                "Maintain current stock levels and monitor demand."
            )

        else:

            recommendations.append(
                "Forecast uncertainty is high. Review data quality before making purchasing decisions."
            )

        return {

            "confidence_score":
            score,

            "recommendations":
            recommendations
        }