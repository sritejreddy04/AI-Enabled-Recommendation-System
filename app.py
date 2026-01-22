import streamlit as st
from backend.recommender import *

st.set_page_config(
    page_title="AI-Enabled Recommendation Engine",
    layout="wide"
)

@st.cache_data(show_spinner=False)
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

# ---------------- MAIN ----------------
st.title("AI-Enabled Recommendation Engine")

query = st.text_input(
    "Search for a product name or keyword to see similar items:"
)

# ---------------- LOGIC ----------------
if query:
    st.subheader(f"🔍 Results for '{query}'")
    results = content_based_recommendation(data, query)

elif user_id == 0:
    st.subheader("🔥 Trending & Popular Products")
    results = get_top_rated_items(data)

else:
    st.subheader(f"👤 Personalized Recommendations for User {user_id}")
    results = hybrid_recommendation(data, user_id)

# ---------------- DISPLAY ----------------
cols = st.columns(4)

for i, row in enumerate(results.itertuples()):
    with cols[i % 4]:
        st.image(row.ImageURL, width="stretch")
        st.markdown(f"**{row.Name}**")
        st.caption(row.Brand)
        st.write(f"⭐ {row.Rating} | 📝 {row.ReviewCount}")
