import pandas as pd
from .content_based import content_based_recommendation
from .collaborative_based import collaborative_filtering_recommendations

def hybrid_recommendation(
    data: pd.DataFrame,
    item_name: str,
    user_id: int,
    top_n: int = 10
):
    content_df = content_based_recommendation(data, item_name, top_n)
    collab_df = collaborative_filtering_recommendations(data, user_id, top_n)

    return (
        pd.concat([content_df, collab_df])
        .drop_duplicates()
        .head(top_n)
        .reset_index(drop=True)
    )