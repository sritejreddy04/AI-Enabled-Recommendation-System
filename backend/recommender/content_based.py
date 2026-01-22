import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def content_based_recommendation(
    data: pd.DataFrame,
    query: str,
    top_n: int = 12
) -> pd.DataFrame:

    if not query:
        return pd.DataFrame()

    query = query.lower().strip()

    combined_text = (
        data["Name"] + " " +
        data["Category"] + " " +
        data["Tags"] + " " +
        data["Description"]
    ).str.lower()

    # FIX: no regex warning
    mask = combined_text.str.contains(query, regex=False, na=False)
    matched = data[mask]

    if matched.empty:
        return pd.DataFrame()

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(combined_text)

    idx = matched.index[0]
    similarity = cosine_similarity(
        tfidf_matrix[idx], tfidf_matrix
    ).flatten()

    top_indices = similarity.argsort()[::-1][1:top_n + 1]

    return data.iloc[top_indices].reset_index(drop=True)
