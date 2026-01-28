import pandas as pd

def get_top_rated_items(data: pd.DataFrame, top_n: int = 10):
    avg = (
        data.groupby(['Name', 'Brand', 'ImageURL', 'ReviewCount'])['Rating']
        .mean()
        .reset_index()
    )

    avg = avg.sort_values(
        by=['Rating', 'ReviewCount'],
        ascending=[False, False]
    )

    return avg.head(top_n).reset_index(drop=True)
