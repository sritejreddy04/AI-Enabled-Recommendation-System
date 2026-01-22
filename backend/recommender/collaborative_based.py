import pandas as pd
import numpy as np

def collaborative_filtering_recommendations(
    data: pd.DataFrame,
    user_id: int,
    top_n: int = 12
) -> pd.DataFrame:

    # Deterministic randomness per user
    np.random.seed(user_id)

    sampled = data.sample(
        n=min(len(data), top_n * 3),
        random_state=user_id
    )

    return (
        sampled
        .sort_values(["Rating", "ReviewCount"], ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
