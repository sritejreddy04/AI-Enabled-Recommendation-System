import pandas as pd

def process_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Drop critical missing fields
    df = df.dropna(subset=["Name", "ImageURL", "Rating"])

    # Remove zero or negative ratings
    df = df[df["Rating"] > 0]

    # Ensure text columns exist and are strings
    for col in ["Name", "Brand", "Category", "Tags", "Description"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("").astype(str)

    return df.reset_index(drop=True)
