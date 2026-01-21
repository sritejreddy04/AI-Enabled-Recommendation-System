import pandas as pd

def get_user_history(data: pd.DataFrame, user_id: int, limit: int = 5):
    user_id = int(user_id)  # 🔴 critical

    history = data.loc[data["ID"] == user_id]

    if history.empty:
        return pd.DataFrame()

    history = (
        history
        .sort_values("Rating", ascending=False)
        .drop_duplicates(subset=["ProdID"])
        .head(limit)
    )

    return history[["Name", "Brand", "Rating", "ImageURL"]].reset_index(drop=True)
