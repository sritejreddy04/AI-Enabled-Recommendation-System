import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def content_based_recommendations(
    data: pd.DataFrame,
    item_name: str,
    top_n: int = 10
):
    # 🔹 Keyword fallback
    matches = data[
        data["Name"].str.contains(item_name, case=False, na=False) |
        data["Tags"].str.contains(item_name, case=False, na=False)
    ]

    if matches.empty:
        return pd.DataFrame()

    # Use first best match as seed
    seed_index = matches.index[0]

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(data["Tags"])

    similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
    scores = list(enumerate(similarity[seed_index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    indices = [i[0] for i in scores[:top_n]]

    return data.iloc[indices][
        ["Name", "ReviewCount", "Brand", "ImageURL", "Rating"]
    ].reset_index(drop=True)