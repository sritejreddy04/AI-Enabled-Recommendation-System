import pandas as pd
from .collaborative_based import collaborative_filtering_recommendations
from .rating_based import get_top_rated_items

def hybrid_recommendation(
    data: pd.DataFrame,
    user_id: int,
    top_n: int = 12
) -> pd.DataFrame:

    if user_id <= 0:
        return get_top_rated_items(data, top_n)

    collab = collaborative_filtering_recommendations(data, user_id, top_n)
    popular = get_top_rated_items(data, top_n)

    merged = (
        pd.concat([collab, popular])
        .drop_duplicates(subset="Name")
        .head(top_n)
        .reset_index(drop=True)
    )

    return merged
