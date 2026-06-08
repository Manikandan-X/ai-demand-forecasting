import pandas as pd
import numpy as np

# =========================
# SIMPLE IN-MEMORY CACHE
# =========================
_DATASET_CACHE = {}


def load_dataset(file_path: str):
    """
    Load dataset once and reuse from memory
    """

    if file_path in _DATASET_CACHE:
        return _DATASET_CACHE[file_path]

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # standard cleanup ONCE
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    _DATASET_CACHE[file_path] = df

    return df


def generate_dashboard_data(
    file_path,
    region=None,
    category=None,
    start_date=None,
    end_date=None
):

    # =========================
    # LOAD FROM CACHE
    # =========================
    df = load_dataset(file_path)

    # avoid modifying cached df directly
    df = df.copy(deep=False)

    # =========================
    # FILTERS (FAST PIPELINE)
    # =========================
    if (
        region and
        "Region" in df.columns
    ):
        df = df[
            df["Region"] == region
        ]

    if (
        category and
        "Category" in df.columns
    ):
        df = df[
            df["Category"] == category
        ]

    if "Date" in df.columns:

        if start_date:
            start_date = pd.to_datetime(
                start_date
            )

            df = df[
                df["Date"] >= start_date
            ]

        if end_date:
            end_date = pd.to_datetime(
                end_date
            )

            df = df[
                df["Date"] <= end_date
            ]

    # =========================
    # TOTAL SALES
    # =========================
    total_sales = 0

    if "Total_Amount" in df.columns:
        total_sales = float(
            df["Total_Amount"].sum()
        )

    total_orders = len(df)

    # =========================
    # TOP PRODUCTS
    # =========================
    top_products = {}

    if (
        "Product" in df.columns and
        "Total_Amount" in df.columns
    ):

        top_products = (
            df.groupby(
                "Product",
                observed=True
            )[
                "Total_Amount"
            ]
            .sum()
            .nlargest(5)
            .astype(float)
            .to_dict()
        )

    # =========================
    # MONTHLY SALES
    # =========================
    monthly_sales = {}

    if (
        "Date" in df.columns and
        "Total_Amount" in df.columns
    ):

        grouped = (
            df.groupby(
                df["Date"]
                .dt.strftime("%Y-%m")
            )[
                "Total_Amount"
            ]
            .sum()
        )

        monthly_sales = {
            month: float(sales)
            for month, sales
            in grouped.items()
        }

    # =========================
    # AI TREND DETECTION
    # =========================
    trend = "stable"

    values = list(
        monthly_sales.values()
    )

    if len(values) >= 2:

        midpoint = (
            len(values) // 2
        )

        first_half = np.mean(
            values[:midpoint]
        )

        second_half = np.mean(
            values[midpoint:]
        )

        if (
            second_half >
            first_half * 1.05
        ):
            trend = "up"

        elif (
            second_half <
            first_half * 0.95
        ):
            trend = "down"

        else:
            trend = "stable"

    # =========================
    # ANOMALY DETECTION
    # =========================
    anomalies = []

    if len(values) > 2:

        mean = np.mean(values)
        std = np.std(values)

        for (
            month,
            sales
        ) in monthly_sales.items():

            if abs(
                sales - mean
            ) > (
                2 * std
            ):

                anomalies.append({
                    "month": month,
                    "sales": float(sales)
                })

    # =========================
    # NEXT MONTH FORECAST
    # =========================
    forecast_next_month = None

    if len(values) >= 2:

        growth_rate = (
            values[-1]
            - values[0]
        ) / max(
            values[0],
            1
        )

        forecast_next_month = (
            values[-1]
            * (
                1 + growth_rate
            )
        )

    # =========================
    # DROPDOWN VALUES
    # =========================
    regions = []
    categories = []

    if "Region" in df.columns:

        regions = (
            df["Region"]
            .dropna()
            .unique()
            .tolist()
        )

        regions.sort()

    if "Category" in df.columns:

        categories = (
            df["Category"]
            .dropna()
            .unique()
            .tolist()
        )

        categories.sort()

        # =========================
        # GROWTH PERCENTAGE
        # =========================

        growth_percentage = 0

        if len(values) >= 2:

            first_value = values[0]
            last_value = values[-1]

            if first_value > 0:

                growth_percentage = round(
                    (
                        (last_value - first_value)
                        /
                        first_value
                    ) * 100,
                    2
                )
    # =========================
    # RESPONSE
    # =========================
    return {
        "total_sales":
        total_sales,

        "total_orders":
        total_orders,

        "top_products":
        top_products,

        "monthly_sales":
        monthly_sales,

        "regions":
        regions,

        "categories":
        categories,
        
        "growth_percentage":
        growth_percentage,

        # AI ANALYTICS
        "trend":
        trend,

        "anomalies":
        anomalies,

        "forecast_next_month":
        forecast_next_month
        
        
    }