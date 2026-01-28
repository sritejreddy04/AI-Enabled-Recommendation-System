import pandas as pd

def content_based_recommendation(data: pd.DataFrame, query: str, top_n: int = 12):
    query = query.lower().strip()

    results = data[
        data["Name"].str.lower().str.contains(query, na=False)
        | data["Category"].str.lower().str.contains(query, na=False)
        | data["Tags"].str.lower().str.contains(query, na=False)
    ]

    if results.empty:
        return pd.DataFrame()

    return (
        results.groupby(["Name", "Brand", "ImageURL"])
        .agg(
            Rating=("Rating", "mean"),
            ReviewCount=("Rating", "count"),
        )
        .reset_index()
        .sort_values(["Rating", "ReviewCount"], ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
