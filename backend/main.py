from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from schemas import RecommendRequest

from recommender.preprocess_data import process_data
from recommender.content_based import content_based_recommendation
from recommender.collaborative_based import collaborative_filtering_recommendations
from recommender.rating_based import get_top_rated_items
from recommender.hybrid import hybrid_recommendation
from recommender.user_history import get_user_history

# -------------------------------------------------
# FASTAPI APP
# -------------------------------------------------
app = FastAPI(title="AI Recommendation Engine")

# -------------------------------------------------
# CORS (FOR STREAMLIT)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# LOAD + PREPROCESS DATA (ONCE)
# -------------------------------------------------
raw_data = pd.read_csv("data/cleaned_data.csv")
data = process_data(raw_data)

# -------------------------------------------------
# MAIN RECOMMENDATION ENDPOINT
# -------------------------------------------------
@app.post("/recommend")
def recommend(req: RecommendRequest):
    if req.method == "rating":
        df = get_top_rated_items(data)

    elif req.method == "content":
        if not req.item_name:
            return []
        df = content_based_recommendation(data, req.item_name)

    elif req.method == "collaborative":
        if not req.user_id:
            return []
        df = collaborative_filtering_recommendations(data, req.user_id)

    elif req.method == "hybrid":
        if not req.item_name or not req.user_id:
            return []
        df = hybrid_recommendation(data, req.item_name, req.user_id)

    else:
        return []

    return df.to_dict(orient="records")

# -------------------------------------------------
# USER HISTORY ENDPOINT (REAL DATA)
# -------------------------------------------------
@app.get("/user-history/{user_id}")
def user_history(user_id: int):
    df = get_user_history(data, user_id)
    return df.to_dict(orient="records")
