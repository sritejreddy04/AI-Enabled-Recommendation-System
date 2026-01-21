import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def collaborative_filtering_recommendations(
    data: pd.DataFrame,
    target_user_id: int,
    top_n: int = 10
):
    user_item_matrix = data.pivot_table(
        index="ID",
        columns="ProdID",
        values="Rating",
        aggfunc="mean"
    ).fillna(0)

    if target_user_id not in user_item_matrix.index:
        return pd.DataFrame()

    similarity_matrix = cosine_similarity(user_item_matrix)
    target_idx = user_item_matrix.index.get_loc(target_user_id)

    similarity_scores = similarity_matrix[target_idx]
    similar_users = similarity_scores.argsort()[::-1][1:]

    recommended_items = []
    for idx in similar_users:
        user_ratings = user_item_matrix.iloc[idx]
        mask = (user_ratings != 0) & (user_item_matrix.iloc[target_idx] == 0)
        recommended_items.extend(user_item_matrix.columns[mask][:top_n])

    recommended_items = list(set(recommended_items))[:top_n]

    return (
        data[data["ProdID"].isin(recommended_items)]
        [["Name", "ReviewCount", "Brand", "ImageURL", "Rating"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )