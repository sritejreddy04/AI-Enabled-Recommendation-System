import streamlit as st
import pandas as pd

from backend.recommender import (
    process_data,
    content_based_recommendation,
    collaborative_filtering_recommendations,
    get_top_rated_items,
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Enabled Recommendation System",
    layout="wide",
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_data.csv")
    return process_data(df)

data = load_data()

# ---------------- CSS ----------------
st.markdown("""
<style>
.card {
    background:#161b22;
    padding:12px;
    border-radius:12px;
    height:360px;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    box-shadow:0 4px 18px rgba(0,0,0,0.4);
}
.card img {
    width:100%;
    height:180px;
    object-fit:contain;
    background:white;
    border-radius:8px;
}
.title {
    font-size:14px;
    font-weight:600;
    color:white;
}
.meta {
    font-size:12px;
    color:#9ca3af;
}
.sidebar-card {
    background:#0d1117;
    padding:10px;
    border-radius:10px;
    margin-bottom:12px;
}
.sidebar-card img {
    width:100%;
    height:120px;
    object-fit:contain;
    background:white;
    border-radius:6px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("User Profile")

user_id = st.sidebar.number_input(
    "Login with User ID (0 for Guest)",
    min_value=0,
    step=1
)

# -------- SIDEBAR: BASED ON INTERESTS --------
if user_id > 0:
    st.sidebar.markdown("### ✨ Based on Your Interests")

    user_history = data[data["ID"] == user_id]

    if not user_history.empty:
        liked_item = user_history.iloc[-1:]

        for _, row in liked_item.iterrows():
            st.sidebar.markdown(f"""
            <div class="sidebar-card">
                <img src="{row['ImageURL']}">
                <div class="title">{row['Name']}</div>
                <div class="meta">⭐ {round(row['Rating'],2)}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.info("No liked products yet.")

# ---------------- MAIN UI ----------------
st.title("🛒 AI Enabled Recommendation System")
search_query = st.text_input("Search for a product name or keyword")

# ---------------- CARD RENDER (MAIN) ----------------
def render_cards(df, cols_count=4):
    if df.empty:
        st.info("No items to display.")
        return

    cols = st.columns(cols_count)
    for i, row in df.iterrows():
        with cols[i % cols_count]:
            st.markdown(f"""
            <div class="card">
                <img src="{row['ImageURL']}">
                <div>
                    <div class="title">{row['Name']}</div>
                    <div class="meta">Brand: {row['Brand']}</div>
                </div>
                <div class="meta">⭐ {round(row['Rating'],2)} | 📝 {row['ReviewCount']}</div>
            </div>
            """, unsafe_allow_html=True)

# ---------------- SEARCH MODE ----------------
if search_query.strip():
    st.subheader(f"🔍 Results for '{search_query}'")
    results = content_based_recommendation(data, search_query, top_n=12)
    render_cards(results)

# ---------------- RECOMMENDATION MODE ----------------
else:
    if user_id > 0:
        st.subheader("🤝 Users Like You Also Liked")

        cf_items = collaborative_filtering_recommendations(
            data=data,
            user_id=user_id,
            top_n=12
        )

        if cf_items.empty:
            cf_items = get_top_rated_items(data, top_n=12)

        if not user_history.empty:
            cf_items = cf_items[
                ~cf_items["Name"].isin(user_history["Name"])
            ]

        render_cards(cf_items.head(12))

    else:
        st.subheader("🔥 Top Rated Products")
        top_items = get_top_rated_items(data, top_n=12)
        render_cards(top_items)
