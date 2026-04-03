import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.express as px
import pandas as pd

from src.pipeline import run_pipeline
from src.db import fetch_data
import src.queries as q
from src.recommender import get_strategy
from src.clustering import predict_segment
from src.auth import create_user, login_user

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Customer Intelligence", layout="wide")

# ---------------- SESSION ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ---------------- LOGIN PAGE ----------------
if not st.session_state.authenticated:

    st.title("🔐 Customer Intelligence Login")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.authenticated = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if create_user(new_user, new_pass):
                st.success("Account created. Please login.")
            else:
                st.error("Username already exists")

    st.stop()

# ---------------- LIGHT UI ----------------
st.markdown("""
<style>
.stApp { background-color: #f8fafc; }

.title {
    font-size: 30px;
    font-weight: 700;
    color: #111827;
}

.stButton > button {
    background-color: #e5e7eb;
    color: #111827;
    border-radius: 8px;
}

.kpi-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

.kpi-title { color: #6b7280; }
.kpi-value { font-size: 26px; font-weight: 600; color: #111827; }

.insight {
    background: #f1f5f9;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #3b82f6;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
col1, col2 = st.columns([6,4])

with col1:
    st.markdown("<div class='title'>Customer Intelligence</div>", unsafe_allow_html=True)

with col2:
    nav1, nav2, nav3, nav4, nav5 = st.columns(5)

    with nav1:
        if st.button("Dashboard"):
            st.session_state.page = "Dashboard"
    with nav2:
        if st.button("Explorer"):
            st.session_state.page = "Explorer"
    with nav3:
        if st.button("Strategy"):
            st.session_state.page = "Strategy"
    with nav4:
        if st.button("Insights"):
            st.session_state.page = "Insights"
    with nav5:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

page = st.session_state.page

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return run_pipeline()

df = load_data()

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.markdown("### Overview")

    total = fetch_data(q.TOTAL_CUSTOMERS)['total'][0]
    avg_clv = fetch_data(q.AVG_CLV)['avg_clv'][0]
    at_risk = fetch_data(q.AT_RISK)['count'][0]
    high_val = (df['segment']=="High Value Customers").mean()*100

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Customers</div><div class='kpi-value'>{total}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><div class='kpi-title'>Avg CLV</div><div class='kpi-value'>${avg_clv:,.0f}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><div class='kpi-title'>High Value %</div><div class='kpi-value'>{high_val:.1f}%</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><div class='kpi-title'>At Risk</div><div class='kpi-value'>{at_risk}</div></div>", unsafe_allow_html=True)

    # -------- INSIGHT --------
    st.markdown(f"""
    <div class='insight'>
    <b>Insight:</b> Your dataset shows segmentation across multiple behavioral groups.
    Focus on high-value users for revenue and re-engage at-risk customers.
    </div>
    """, unsafe_allow_html=True)

    # -------- CHARTS --------
    st.markdown("### Segmentation Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(df, x="segment", color="segment")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(df,
                         x="annual_income",
                         y="spending_score",
                         color="segment")
        st.plotly_chart(fig, use_container_width=True)

    # -------- CONCLUSION --------
    st.markdown("""
    ### Business Conclusion

    - High Value Customers drive revenue  
    - Loyal Customers ensure stability  
    - At Risk Customers need retention  
    - Low Value Customers need engagement  

    👉 Focus: retention + upselling = max ROI
    """)

# ---------------- EXPLORER ----------------
elif page == "Explorer":

    st.markdown("### Customer Explorer")

    seg = st.selectbox("Segment", df['segment'].unique())
    income = st.slider("Income Range", 20000,150000,(30000,100000))

    filtered = df[(df.segment==seg)&
                  (df.annual_income>=income[0])&
                  (df.annual_income<=income[1])]

    st.write(f"Showing {len(filtered)} customers")
    st.dataframe(filtered.sample(300))

# ---------------- STRATEGY ----------------
elif page == "Strategy":

    st.markdown("### Strategy Engine")

    income = st.slider("Income",20000,150000,50000)
    spending = st.slider("Spending Score",0,200,50)
    freq = st.slider("Frequency",1,30,10)
    aov = st.slider("AOV",100,10000,2000)
    rec = st.slider("Recency",1,180,30)

    if st.button("Predict Segment"):

        input_df = pd.DataFrame([{
            "annual_income": income,
            "spending_score": spending,
            "purchase_frequency": freq,
            "average_order_value": aov,
            "last_purchase_days_ago": rec
        }])

        cluster = predict_segment(input_df)[0]

        seg_map = ["High Value Customers","Loyal Customers","At Risk Customers","Low Value Customers"]
        seg = seg_map[cluster]

        st.success(f"Segment: {seg}")
        st.info(get_strategy(seg))

# ---------------- INSIGHTS ----------------
elif page == "Insights":

    st.markdown("### Business Insights")

    rev = fetch_data(q.SEGMENT_REVENUE)

    fig = px.bar(rev, x="segment", y="revenue", color="segment")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### Strategic Insights

    - Revenue concentrated in high-value customers  
    - At-risk users require re-engagement  
    - Loyal customers ideal for upselling  

    ### Expected Impact

    - 15–25% revenue increase  
    - 1.5x retention improvement  
    """)