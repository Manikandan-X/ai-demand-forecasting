import pandas as pd


def generate_dashboard_data(file_path: str):

    if file_path.endswith(".csv"):

        df = pd.read_csv(file_path)

    else:

        df = pd.read_excel(file_path)

    total_sales = float(
        df["Total_Amount"].sum()
    )

    total_orders = int(len(df))

    top_products = (
        df.groupby("Product")["Total_Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .to_dict()
    )

    df["Date"] = pd.to_datetime(df["Date"])

    df["Month"] = df["Date"].dt.strftime("%Y-%m")

    monthly_sales = (
        df.groupby("Month")["Total_Amount"]
        .sum()
        .to_dict()
    )

    return {
        "total_sales": round(total_sales, 2),
        "total_orders": total_orders,
        "top_products": top_products,
        "monthly_sales": monthly_sales
    }