import pandas as pd
from .content_based import content_based_recommendation
from .collaborative_based import collaborative_filtering_recommendations

def hybrid_recommendation(
    data: pd.DataFrame,
    item_name: str,
    user_id: int,
    top_n: int = 10
):
    cb = content_based_recommendation(data, item_name, top_n)
    cf = collaborative_filtering_recommendations(data, user_id, top_n)

    hybrid = pd.concat([cb, cf]).drop_duplicates(subset='Name')
    return hybrid.head(top_n).reset_index(drop=True)
