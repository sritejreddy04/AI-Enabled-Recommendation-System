import pandas as pd

def rating_based_recommendations(data: pd.DataFrame, top_n: int = 10):
    avg = (
        data.groupby(["Name", "ReviewCount", "Brand", "ImageURL"])["Rating"]
        .mean()
        .reset_index()
    )

    return avg.sort_values("Rating", ascending=False).head(top_n).reset_index(drop=True)