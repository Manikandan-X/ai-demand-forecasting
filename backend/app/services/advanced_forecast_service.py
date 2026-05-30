import pandas as pd
import numpy as np

from prophet import Prophet

from sklearn.linear_model import (
    LinearRegression
)

from sklearn.tree import (
    DecisionTreeRegressor
)

from sklearn.ensemble import (
    RandomForestRegressor
)

from sklearn.metrics import (
    mean_absolute_error
)


class AdvancedForecastService:

    # =========================
    # PREPROCESS DATASET
    # =========================
    def preprocess_dataset(
        self,
        file_path
    ):

        if file_path.endswith(".csv"):

            df = pd.read_csv(
                file_path
            )

        else:

            df = pd.read_excel(
                file_path
            )

        df.columns = (
            df.columns
            .str.strip()
        )

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

        grouped_df = (
            df.groupby("Date")[
                "Total_Amount"
            ]
            .sum()
            .reset_index()
        )

        grouped_df = (
            grouped_df.rename(
                columns={
                    "Date":
                    "date",

                    "Total_Amount":
                    "sales"
                }
            )
        )

        return grouped_df

    # =========================
    # COMMON MODEL TRAINER
    # =========================
    def train_sklearn_model(
        self,
        df,
        model,
        model_name
    ):

        df = df.copy()

        df["index"] = np.arange(
            len(df)
        )

        X = df[["index"]]

        y = df["sales"]

        model.fit(X, y)

        future_index = np.arange(
            len(df),
            len(df) + 7
        ).reshape(-1, 1)

        predictions = model.predict(
            future_index
        )

        forecast_days = []

        for i, pred in enumerate(
            predictions
        ):

            forecast_days.append({
                "day":
                i + 1,

                "predicted_sales":
                round(
                    max(
                        0,
                        float(pred)
                    ),
                    2
                )
            })

        train_predictions = (
            model.predict(X)
        )

        error = (
            mean_absolute_error(
                y,
                train_predictions
            )
        )

        accuracy = max(
            0,
            100 - (
                error /
                y.mean()
            ) * 100
        )

        return {
            "model":
            model_name,

            "accuracy":
            round(
                float(accuracy),
                2
            ),

            "future_predictions":
            forecast_days
        }

    # =========================
    # LINEAR REGRESSION
    # =========================
    def train_linear_regression(
        self,
        df
    ):

        model = (
            LinearRegression()
        )

        return self.train_sklearn_model(
            df,
            model,
            "Linear Regression"
        )

    # =========================
    # DECISION TREE
    # =========================
    def train_decision_tree(
        self,
        df
    ):

        model = (
            DecisionTreeRegressor(
                random_state=42
            )
        )

        return self.train_sklearn_model(
            df,
            model,
            "Decision Tree"
        )

    # =========================
    # RANDOM FOREST
    # =========================
    def train_random_forest(
        self,
        df
    ):

        model = (
            RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )
        )

        return self.train_sklearn_model(
            df,
            model,
            "Random Forest"
        )

    # =========================
    # PROPHET MODEL
    # =========================
    def train_prophet(
        self,
        df
    ):

        prophet_df = (
            df.rename(
                columns={
                    "date":
                    "ds",

                    "sales":
                    "y"
                }
            )
        )

        model = Prophet()

        model.fit(
            prophet_df
        )

        future = (
            model
            .make_future_dataframe(
                periods=7
            )
        )

        forecast = (
            model.predict(
                future
            )
        )

        future_forecast = (
            forecast.tail(7)
        )

        predictions = []

        for i, row in enumerate(
            future_forecast
            .itertuples()
        ):

            predictions.append({
                "day":
                i + 1,

                "predicted_sales":
                round(
                    max(
                        0,
                        float(
                            row.yhat
                        )
                    ),
                    2
                )
            })

        predicted = (
            forecast["yhat"][
                :len(
                    prophet_df
                )
            ]
        )

        error = (
            mean_absolute_error(
                prophet_df["y"],
                predicted
            )
        )

        accuracy = max(
            0,
            100 - (
                error /
                prophet_df["y"]
                .mean()
            ) * 100
        )

        return {
            "model":
            "Prophet",

            "accuracy":
            round(
                float(
                    accuracy
                ),
                2
            ),

            "future_predictions":
            predictions
        }
        
    def detect_trend_and_seasonality(
        self,
        df
    ):

        df = df.copy()

        trend = "stable"

        seasonality_detected = False

        average_growth = 0

        # =========================
        # TREND DETECTION
        # =========================
        if len(df) > 1:

            growth = (
                df["sales"]
                .diff()
                .dropna()
            )

            average_growth = (
                growth.mean()
            )

            if average_growth > 0:

                trend = "increasing"

            elif average_growth < 0:

                trend = "decreasing"

        # =========================
        # SEASONALITY DETECTION
        # =========================
        if len(df) >= 14:

            weekly_pattern = (
                df["sales"]
                .rolling(7)
                .mean()
            )

            variability = (
                weekly_pattern
                .std()
            )

            if (
                variability
                and
                variability > 0
            ):

                seasonality_detected = True

        return {

            "trend":
            trend,

            "average_growth":
            round(
                float(
                    average_growth
                ),
                2
            ),

            "seasonality_detected":
            seasonality_detected
        }
        
    def detect_anomalies(
        self,
        df
    ):

        df = df.copy()

        anomalies = []

        # =========================
        # Z SCORE METHOD
        # =========================
        mean_sales = (
            df["sales"]
            .mean()
        )

        std_sales = (
            df["sales"]
            .std()
        )

        if std_sales == 0:

            return {
                "anomaly_count": 0,
                "anomalies": []
            }

        df["z_score"] = (

            df["sales"] -
            mean_sales

        ) / std_sales

        anomaly_rows = df[

            df["z_score"]
            .abs() > 2

        ]

        for row in anomaly_rows.itertuples():

            anomalies.append({

                "date":
                str(row.date.date()),

                "sales":
                round(
                    float(
                        row.sales
                    ),
                    2
                )
            })

        return {

            "anomaly_count":
            len(anomalies),

            "anomalies":
            anomalies
        }

    # =========================
    # MODEL COMPARISON
    # =========================
    def compare_models(
        self,
        file_path
    ):

        df = self.preprocess_dataset(
            file_path
        )

        results = [

            self.train_linear_regression(df),

            self.train_decision_tree(df),

            self.train_random_forest(df),

            self.train_prophet(df)
        ]

        best_model = max(
            results,
            key=lambda x:
            x["accuracy"]
        )

        seasonal_analysis = (
            self.detect_trend_and_seasonality(
                df
            )
        )
        
        anomaly_analysis = (
            self.detect_anomalies(
                df
            )
        )

        return {

            "best_model":
            best_model,

            "all_models":
            results,

            "seasonal_analysis":
            seasonal_analysis,
            
            "anomaly_analysis":
            anomaly_analysis
        }