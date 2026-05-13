import pandas as pd


def process_dataset(file_path: str):

    if file_path.endswith(".csv"):

        df = pd.read_csv(file_path)

    elif file_path.endswith(".xlsx"):

        df = pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format")

    original_rows = len(df)

    duplicate_count = df.duplicated().sum()

    missing_values = df.isnull().sum().to_dict()

    df = df.drop_duplicates()

    df = df.ffill()

    cleaned_rows = len(df)

    columns = list(df.columns)

    dataset_summary = {
        "original_rows": original_rows,
        "cleaned_rows": cleaned_rows,
        "duplicate_rows_removed": int(duplicate_count),
        "columns": columns,
        "missing_values": missing_values
    }

    return dataset_summary