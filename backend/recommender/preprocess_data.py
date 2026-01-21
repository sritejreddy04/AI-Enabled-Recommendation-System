import pandas as pd
import numpy as np

def process_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    # -----------------------------
    # SAFE NUMERIC CONVERSIONS
    # -----------------------------
    data["ID"] = pd.to_numeric(data["ID"], errors="coerce")
    data["ProdID"] = pd.to_numeric(data["ProdID"], errors="coerce")

    # ONLY drop rows where ID or ProdID is missing
    data = data.dropna(subset=["ID", "ProdID"])

    # Convert to int AFTER cleaning
    data["ID"] = data["ID"].astype(int)
    data["ProdID"] = data["ProdID"].astype(int)

    # -----------------------------
    # RATINGS
    # -----------------------------
    data["Rating"] = (
        pd.to_numeric(data["Rating"], errors="coerce")
        .fillna(0)
    )

    # -----------------------------
    # TEXT COLUMNS (SAFE)
    # -----------------------------
    text_cols = [
        "Name",
        "Brand",
        "Category",
        "Tags",
        "Description",
        "ImageURL"
    ]

    for col in text_cols:
        if col in data.columns:
            data[col] = data[col].fillna("").astype(str)

    return data
