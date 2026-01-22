import pandas as pd

def get_top_rated_items(
    data: pd.DataFrame,
    top_n: int = 12
) -> pd.DataFrame:

    return (
        data
        .sort_values(["Rating", "ReviewCount"], ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
