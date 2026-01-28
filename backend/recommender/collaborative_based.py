import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def collaborative_filtering_recommendations(
    data: pd.DataFrame, user_id: int, top_n: int = 12
):
    if user_id not in data["ID"].values:
        return pd.DataFrame()

    matrix = data.pivot_table(
        index="ID", columns="ProdID", values="Rating", fill_value=0
    )

    if user_id not in matrix.index:
        return pd.DataFrame()

    similarity = cosine_similarity(matrix)
    idx = list(matrix.index).index(user_id)

    similar_users = similarity[idx].argsort()[::-1][1:6]

    recommended = matrix.iloc[similar_users].mean().sort_values(ascending=False)

    prod_ids = recommended.head(top_n).index.tolist()

    return (
        data[data["ProdID"].isin(prod_ids)]
        .groupby(["Name", "Brand", "ImageURL"])
        .agg(
            Rating=("Rating", "mean"),
            ReviewCount=("Rating", "count"),
        )
        .reset_index()
        .sort_values(["Rating", "ReviewCount"], ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
