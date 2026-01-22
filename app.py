import streamlit as st
from backend.recommender import (
    process_data,
    content_based_recommendation,
    get_top_rated_items,
    hybrid_recommendation
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Enabled Recommendation Engine",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return process_data("data/cleaned_data.csv")

data = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("User Profile")
user_id = st.sidebar.number_input(
    "Login with User ID (0 for Guest)",
    min_value=0,
    step=1,
    value=0
)

# ---------------- MAIN UI ----------------
st.title("🛒 AI-Enabled Recommendation Engine")

query = st.text_input(
    "Search for a product name or keyword to see similar items:"
)

# ---------------- LOGIC ----------------
if query:
    st.subheader(f"🔍 Results for '{query}'")
    results = content_based_recommendation(data, query)

elif user_id == 0:
    st.subheader("🔥 Recommended for You (Trending & Popular)")
    results = get_top_rated_items(data)

else:
    st.subheader(f"👋 Welcome Back, User {user_id}")
    results = hybrid_recommendation(data, user_id)

# ---------------- DISPLAY ----------------
if results.empty:
    st.warning("No products found.")
else:
    cols = st.columns(4)

    for i, row in enumerate(results.itertuples()):
        with cols[i % 4]:
            st.image(row.ImageURL)   # ✅ FIXED (NO width arg)
            st.markdown(f"**{row.Name}**")
            st.caption(row.Brand)
            st.write(f"⭐ {row.Rating} | 📝 {row.ReviewCount}")
