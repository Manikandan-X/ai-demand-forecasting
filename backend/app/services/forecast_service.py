import pandas as pd

from sklearn.linear_model import LinearRegression

from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_absolute_error

import numpy as np


def generate_forecast(file_path: str):

    if file_path.endswith(".csv"):

        df = pd.read_csv(file_path)

    else:

        df = pd.read_excel(file_path)

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date")

    df["Day_Number"] = np.arange(len(df))

    X = df[["Day_Number"]]

    y = df["Total_Amount"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = LinearRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = mean_absolute_error(
        y_test,
        predictions
    )

    future_days = np.array(
        range(len(df), len(df) + 7)
    ).reshape(-1, 1)

    future_predictions = model.predict(
        future_days
    )

    forecast_results = []

    for i, prediction in enumerate(future_predictions):

        forecast_results.append({
            "day": i + 1,
            "predicted_sales": round(
                max(float(prediction),0),
                2
            )
        })

    return {
        "forecast_accuracy_mae": round(
            float(accuracy),
            2
        ),
        "future_predictions": forecast_results
    }