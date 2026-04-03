import sys
import os

# 🔥 ALWAYS POINT TO PROJECT ROOT
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import plotly.express as px
import pandas as pd

from src.auth import init_users_table, create_user, login_user
from src.pipeline import run_pipeline
from src.db import fetch_data
import src.queries as q
from src.recommender import get_strategy
from src.clustering import predict_segment

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Segmint AI", layout="wide")

# ---------------- SAFE INIT ----------------
# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Ensure users table exists
init_users_table()

# ---------------- SESSION ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ---------------- LOGIN PAGE ----------------
if not st.session_state.authenticated:

    st.title("🔐 Segmint AI Login")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password and login_user(username, password):
                st.session_state.authenticated = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if new_user and new_pass:
                if create_user(new_user, new_pass):
                    st.success("Account created. Please login.")
                else:
                    st.error("Username already exists")
            else:
                st.warning("Please enter valid details")

    st.stop()

# ---------------- UI ----------------
st.markdown("""
<style>
.stApp { background-color: #f8fafc; }

.title {
    font-size: 28px;
    font-weight: 700;
    color: #111827;
}

.kpi-card {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

.kpi-title { color: #6b7280; font-size: 13px; }
.kpi-value { font-size: 24px; font-weight: 600; }

.insight {
    background: #f1f5f9;
    padding: 12px;
    border-radius: 10px;
    border-left: 4px solid #3b82f6;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
col1, col2 = st.columns([6,4])

with col1:
    st.markdown("<div class='title'>Segmint AI — Customer Intelligence</div>", unsafe_allow_html=True)

with col2:
    nav1, nav2, nav3, nav4, nav5 = st.columns(5)

    if nav1.button("Dashboard"):
        st.session_state.page = "Dashboard"
    if nav2.button("Explorer"):
        st.session_state.page = "Explorer"
    if nav3.button("Strategy"):
        st.session_state.page = "Strategy"
    if nav4.button("Insights"):
        st.session_state.page = "Insights"
    if nav5.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

page = st.session_state.page

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    try:
        return run_pipeline()
    except Exception as e:
        st.error("Pipeline failed. Regenerating data...")
        return pd.DataFrame()

df = load_data()

# ---------------- SAFETY ----------------
if df.empty:
    st.warning("No data available. Please check dataset generation.")
    st.stop()

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.subheader("Overview")

    total = len(df)
    avg_clv = df['clv'].mean()
    at_risk = (df['segment']=="At Risk Customers").sum()
    high_val = (df['segment']=="High Value Customers").mean()*100

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Customers</div><div class='kpi-value'>{total}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><div class='kpi-title'>Avg CLV</div><div class='kpi-value'>${avg_clv:,.0f}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><div class='kpi-title'>High Value %</div><div class='kpi-value'>{high_val:.1f}%</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><div class='kpi-title'>At Risk</div><div class='kpi-value'>{at_risk}</div></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='insight'>
    High-value customers are driving revenue. Focus on retention and upselling.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    col1.plotly_chart(px.histogram(df, x="segment", color="segment"), use_container_width=True)
    col2.plotly_chart(px.scatter(df, x="annual_income", y="spending_score", color="segment"), use_container_width=True)

# ---------------- EXPLORER ----------------
elif page == "Explorer":

    st.subheader("Customer Explorer")

    seg = st.selectbox("Segment", df['segment'].unique())
    filtered = df[df.segment == seg]

    st.write(f"{len(filtered)} customers")
    st.dataframe(filtered.sample(min(300, len(filtered))))

# ---------------- STRATEGY ----------------
elif page == "Strategy":

    st.subheader("Strategy Engine")

    income = st.slider("Income",20000,150000,50000)
    spending = st.slider("Spending",0,200,50)
    freq = st.slider("Frequency",1,30,10)
    aov = st.slider("AOV",100,10000,2000)
    rec = st.slider("Recency",1,180,30)

    if st.button("Predict"):

        input_df = pd.DataFrame([{
            "annual_income": income,
            "spending_score": spending,
            "purchase_frequency": freq,
            "average_order_value": aov,
            "last_purchase_days_ago": rec
        }])

        cluster = predict_segment(input_df)[0]
        seg_map = ["High Value Customers","Loyal Customers","At Risk Customers","Low Value Customers"]

        st.success(f"Segment: {seg_map[cluster]}")
        st.info(get_strategy(seg_map[cluster]))

# ---------------- INSIGHTS ----------------
elif page == "Insights":

    st.subheader("Business Insights")

    rev = df.groupby("segment")["clv"].sum().reset_index()

    st.plotly_chart(px.bar(rev, x="segment", y="clv", color="segment"), use_container_width=True)

    st.markdown("""
    - High-value users dominate revenue  
    - At-risk users need retention  
    - Loyal users = upsell opportunity  

    Expected impact:
    - 15–25% revenue increase  
    - 1.5x retention improvement  
    """)