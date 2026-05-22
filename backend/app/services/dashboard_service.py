import pandas as pd


def generate_dashboard_data(
    file_path,
    region=None,
    category=None,
    start_date=None,
    end_date=None
):

    # =========================
    # LOAD FILE
    # =========================
    if file_path.endswith(".csv"):

        df = pd.read_csv(file_path)

    else:

        df = pd.read_excel(file_path)

    # =========================
    # DATE COLUMN FORMAT
    # =========================
    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    # =========================
    # REGION FILTER
    # =========================
    if (
        region and
        "Region" in df.columns
    ):

        df = df[
            df["Region"] == region
        ]

    # =========================
    # CATEGORY FILTER
    # =========================
    if (
        category and
        "Category" in df.columns
    ):

        df = df[
            df["Category"] == category
        ]

    # =========================
    # DATE RANGE FILTER
    # =========================
    if "Date" in df.columns:

        if start_date:
            df = df[df["Date"] >= pd.to_datetime(start_date)]

        if end_date:
            df = df[df["Date"] <= pd.to_datetime(end_date)]

    # =========================
    # ANALYTICS
    # =========================
    total_sales = 0

    if "Total_Amount" in df.columns:

        total_sales = float(
            df["Total_Amount"]
            .sum()
        )

    total_orders = int(
        len(df)
    )

    top_products = {}

    if "Product" in df.columns:

        top_products = (
            df["Product"]
            .value_counts()
            .head(5)
            .astype(int)
            .to_dict()
        )

    # =========================
    # MONTHLY SALES
    # =========================
    monthly_sales = {}

    if (
        "Date" in df.columns
        and
        "Total_Amount"
        in df.columns
    ):

        grouped_sales = (
            df.groupby(
                df["Date"]
                .dt.strftime("%Y-%m")
            )[
                "Total_Amount"
            ]
            .sum()
        )

        monthly_sales = {

            str(month):
            float(sales)

            for month, sales in
            grouped_sales.items()

        }

    # =========================
    # FILTER OPTIONS
    # =========================
    regions = []

    if "Region" in df.columns:

        regions = sorted(
            df["Region"]
            .dropna()
            .unique()
            .tolist()
        )

    categories = []

    if "Category" in df.columns:

        categories = sorted(
            df["Category"]
            .dropna()
            .unique()
            .tolist()
        )

    return {

        "total_sales":
        total_sales,

        "total_orders":
        total_orders,

        "top_products":
        top_products,

        "monthly_sales":
        monthly_sales,

        # dropdown values
        "regions":
        regions,

        "categories":
        categories
    }