import pandas as pd

from app.models.alert_settings import (
    AlertSettings
)

from app.services.notification_service import (
    NotificationService
)


class AlertService:

    @staticmethod
    def detect_sales_drop(df):

        if (
            "Total_Amount"
            not in df.columns
        ):
            return None

        values = (
            df["Total_Amount"]
            .tail(10)
            .tolist()
        )

        if len(values) < 5:
            return None

        first_half = (
            sum(values[:5]) / 5
        )

        second_half = (
            sum(values[-5:]) / 5
        )

        if second_half < (
            first_half * 0.8
        ):
            return (
                "Sales dropped by "
                "more than 20%"
            )

        return None

    @staticmethod
    def detect_sales_spike(df):

        if (
            "Total_Amount"
            not in df.columns
        ):
            return None

        values = (
            df["Total_Amount"]
            .tail(10)
            .tolist()
        )

        if len(values) < 5:
            return None

        first_half = (
            sum(values[:5]) / 5
        )

        second_half = (
            sum(values[-5:]) / 5
        )

        if second_half > (
            first_half * 1.3
        ):
            return (
                "Sales increased by "
                "more than 30%"
            )

        return None

    @staticmethod
    def detect_anomaly(df):

        if (
            "Total_Amount"
            not in df.columns
        ):
            return None

        mean = (
            df["Total_Amount"]
            .mean()
        )

        std = (
            df["Total_Amount"]
            .std()
        )

        latest = (
            df["Total_Amount"]
            .iloc[-1]
        )

        if abs(
            latest - mean
        ) > (
            2 * std
        ):
            return (
                "Possible sales "
                "anomaly detected"
            )

        return None

    @staticmethod
    def check_sales_threshold(

        db,
        user_id,
        total_sales

    ):

        settings = (
            db.query(AlertSettings)
            .filter(
                AlertSettings.user_id ==
                user_id
            )
            .first()
        )

        if not settings:
            return

        if not (
            settings.enable_threshold_alerts
        ):
            return

        if (
            total_sales >=
            settings.sales_threshold
        ):

            NotificationService.create_notification(

                db=db,

                user_id=user_id,

                title=
                "Sales Threshold Reached",

                message=
                f"Sales reached "
                f"{total_sales}",

                notification_type=
                "alert"
            )

    @staticmethod
    def process_dataset_alerts(

        db,
        user_id,
        df

    ):

        settings = (
            db.query(AlertSettings)
            .filter(
                AlertSettings.user_id ==
                user_id
            )
            .first()
        )

        if not settings:
            return

        # Sales Drop
        if (
            settings.enable_sales_drop_alerts
        ):

            drop_alert = (
                AlertService
                .detect_sales_drop(df)
            )

            if drop_alert:

                NotificationService.create_notification(

                    db=db,

                    user_id=user_id,

                    title="Sales Drop Alert",

                    message=drop_alert,

                    notification_type="alert"
                )

        # Sales Spike
        if (
            settings.enable_sales_spike_alerts
        ):

            spike_alert = (
                AlertService
                .detect_sales_spike(df)
            )

            if spike_alert:

                NotificationService.create_notification(

                    db=db,

                    user_id=user_id,

                    title="Sales Spike Alert",

                    message=spike_alert,

                    notification_type="alert"
                )

        # Anomaly
        if (
            settings.enable_anomaly_alerts
        ):

            anomaly_alert = (
                AlertService
                .detect_anomaly(df)
            )

            if anomaly_alert:

                NotificationService.create_notification(

                    db=db,

                    user_id=user_id,

                    title="Anomaly Detected",

                    message=anomaly_alert,

                    notification_type="alert"
                )

        # Threshold
        total_sales = 0

        if (
            "Total_Amount"
            in df.columns
        ):

            total_sales = float(
                df["Total_Amount"].sum()
            )

            AlertService.check_sales_threshold(

                db=db,

                user_id=user_id,

                total_sales=total_sales
            )