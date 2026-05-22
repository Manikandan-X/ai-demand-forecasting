import pandas as pd
import numpy as np

from prophet import Prophet

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


class AdvancedForecastService:

    # PREPROCESS DATASET
    def preprocess_dataset(self, file_path):

        df = pd.read_csv(file_path)

        # CLEAN COLUMN NAMES
        df.columns = df.columns.str.strip()

        # CONVERT DATE
        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d-%m-%Y"
        )

        # GROUP SALES BY DATE
        grouped_df = df.groupby("Date")[
            "Total_Amount"
        ].sum().reset_index()

        grouped_df = grouped_df.rename(columns={
            "Date": "date",
            "Total_Amount": "sales"
        })

        return grouped_df

    # LINEAR REGRESSION MODEL
    def train_linear_regression(self, df):

        df = df.copy()

        df["index"] = np.arange(len(df))

        X = df[["index"]]

        y = df["sales"]

        model = LinearRegression()

        model.fit(X, y)

        future_index = np.arange(
            len(df),
            len(df) + 7
        ).reshape(-1, 1)

        predictions = model.predict(
            future_index
        )

        forecast_days = []

        for i, pred in enumerate(predictions):

            forecast_days.append({
                "day": i + 1,
                "predicted_sales": round(max(0, float(pred)), 2)
            })

        train_predictions = model.predict(X)

        error = mean_absolute_error(
            y,
            train_predictions
        )

        accuracy = max(
            0,
            100 - error / y.mean() * 100
        )

        return {
            "model": "Linear Regression",
            "accuracy": round(float(accuracy), 2),
            "future_predictions": forecast_days
        }

    # PROPHET MODEL
    def train_prophet(self, df):

        prophet_df = df.rename(columns={
            "date": "ds",
            "sales": "y"
        })

        model = Prophet()

        model.fit(prophet_df)

        future = model.make_future_dataframe(
            periods=7
        )

        forecast = model.predict(future)

        future_forecast = forecast.tail(7)

        predictions = []

        for i, row in enumerate(
            future_forecast.itertuples()
        ):

            predictions.append({
                "day": i + 1,
                "predicted_sales": round(
                    max(0, float(row.yhat)),
                    2
                )
            })

        predicted = forecast["yhat"][
            :len(prophet_df)
        ]

        error = mean_absolute_error(
            prophet_df["y"],
            predicted
        )

        accuracy = max(
            0,
            100 - error / prophet_df["y"].mean() * 100
        )

        return {
            "model": "Prophet",
            "accuracy": round(float(accuracy), 2),
            "future_predictions": predictions
        }

    # MODEL COMPARISON
    def compare_models(self, file_path):

        df = self.preprocess_dataset(
            file_path
        )

        linear_result = self.train_linear_regression(df)

        prophet_result = self.train_prophet(df)

        if (
            linear_result["accuracy"]
            >
            prophet_result["accuracy"]
        ):

            best_model = linear_result

        else:

            best_model = prophet_result

        return {
            "best_model": best_model,
            "linear_regression": linear_result,
            "prophet": prophet_result
        }