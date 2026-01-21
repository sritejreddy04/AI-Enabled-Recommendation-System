import streamlit as st
import requests

# -------------------------------------------------
# API URLs
# -------------------------------------------------
RECOMMEND_API = "http://127.0.0.1:8000/recommend"
HISTORY_API = "http://127.0.0.1:8000/user-history"

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI-Enabled Recommendation Engine",
    layout="wide"
)

# -------------------------------------------------
# CSS — UI POLISH ONLY (NO LOGIC CHANGES)
# -------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}

/* ---------- CARD ---------- */
.product-card {
    background: #111827;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 14px;
}

/* ---------- LEFT PANEL IMAGES ---------- */
.left-panel img {
    max-height: 120px;
    width: auto;
    margin: auto;
    display: block;
    object-fit: contain;
}

/* ---------- RIGHT PANEL IMAGES ---------- */
.right-panel img {
    height: 220px;
    width: 100%;
    object-fit: contain;
}

/* ---------- TEXT ---------- */
.product-title {
    font-weight: 600;
    margin-top: 8px;
    color: white;
}

.product-brand {
    color: #9ca3af;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LAYOUT
# -------------------------------------------------
left, right = st.columns([1, 3])

# =================================================
# LEFT PANEL — USER PROFILE + HISTORY
# =================================================
with left:
    st.subheader("User Profile")

    user_id = st.number_input(
        "Login with User ID (0 for Guest):",
        min_value=0,
        step=1,
        value=0
    )

    st.markdown("### 🕒 Your Recent Activity")

    if user_id == 0:
        st.info("Guest users have no past activity")
    else:
        try:
            res = requests.get(f"{HISTORY_API}/{user_id}", timeout=5)
            history = res.json() if res.status_code == 200 else []

            if history:
                st.markdown("<div class='left-panel'>", unsafe_allow_html=True)

                for item in history:
                    st.markdown("<div class='product-card'>", unsafe_allow_html=True)

                    if item.get("ImageURL"):
                        st.image(item["ImageURL"], width=140)

                    st.markdown(
                        f"<div class='product-title'>{item['Name']}</div>",
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"<div class='product-brand'>{item['Brand']} • ⭐ {item['Rating']}</div>",
                        unsafe_allow_html=True
                    )

                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No activity found for this user")

        except Exception as e:
            st.error(f"History API error: {e}")

# =================================================
# RIGHT PANEL — SEARCH + RECOMMENDATIONS
# =================================================
with right:
    st.title("AI-Enabled Recommendation Engine")

    search_query = st.text_input(
        "Search for a product name to see similar items:",
        placeholder="e.g. shampoo, hair color, nail polish"
    )

    search_clicked = st.button("Search")

    # -------------------------------------------------
    # PAYLOAD LOGIC (UNCHANGED)
    # -------------------------------------------------
    payload = None

    if search_clicked and search_query.strip():
        payload = {
            "method": "content",
            "item_name": search_query.strip()
        }

    elif user_id == 0:
        payload = {"method": "rating"}

    else:
        payload = {
            "method": "collaborative",
            "user_id": user_id
        }

    # -------------------------------------------------
    # API CALL
    # -------------------------------------------------
    results = []

    if payload:
        try:
            res = requests.post(RECOMMEND_API, json=payload, timeout=10)
            if res.status_code == 200:
                results = res.json()
        except Exception as e:
            st.error(f"Recommendation API error: {e}")

    # -------------------------------------------------
    # RESULTS DISPLAY
    # -------------------------------------------------
    if results:
        st.markdown("## 🎯 Recommended For You")
        st.markdown("<div class='right-panel'>", unsafe_allow_html=True)

        cols = st.columns(3)
        for i, item in enumerate(results):
            with cols[i % 3]:
                st.markdown("<div class='product-card'>", unsafe_allow_html=True)

                if item.get("ImageURL"):
                    st.image(item["ImageURL"], width=260)

                st.markdown(
                    f"<div class='product-title'>{item.get('Name')}</div>",
                    unsafe_allow_html=True
                )

                if item.get("Brand"):
                    st.markdown(
                        f"<div class='product-brand'>{item['Brand']}</div>",
                        unsafe_allow_html=True
                    )

                if item.get("Rating") and item["Rating"] > 0:
                    st.write(f"⭐ {round(item['Rating'], 2)}")

                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
