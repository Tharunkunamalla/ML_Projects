import streamlit as st
from utils import get_connection, run_query
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="📊 PhonePe Dashboard")
st.title("📱 PhonePe Transaction Insights")

menu = ["Overview", "State-wise Analysis", "Aggregated Insurance", "Top Users"]
choice = st.sidebar.selectbox("🔎 Select Dashboard View", menu)

conn = get_connection()

if choice == "Overview":
    st.header("💼 Aggregated Transaction Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        q1 = """
        SELECT States, SUM(Transaction_amount) AS Total_Amount
        FROM aggregated_transaction
        GROUP BY States
        ORDER BY Total_Amount DESC
        """
        df1 = run_query(conn, q1)
        fig1 = px.bar(df1, x='States', y='Total_Amount', title="Statewise Transaction Amount", height=450)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        q2 = """
        SELECT States, SUM(Transaction_count) AS Total_Count
        FROM aggregated_transaction
        GROUP BY States
        ORDER BY Total_Count DESC
        """
        df2 = run_query(conn, q2)
        fig2 = px.bar(df2, x='States', y='Total_Count', title="Statewise Transaction Count", color_discrete_sequence=['red'])
        st.plotly_chart(fig2, use_container_width=True)

elif choice == "State-wise Analysis":
    st.header("🌍 Detailed State-wise Analysis")
    states_df = run_query(conn, "SELECT DISTINCT States FROM aggregated_transaction")
    state = st.selectbox("Select State", states_df["States"])

    q = f"""
    SELECT Years, Quarter, SUM(Transaction_amount) AS Amount, SUM(Transaction_count) AS Count
    FROM aggregated_transaction
    WHERE States = '{state}'
    GROUP BY Years, Quarter
    ORDER BY Years, Quarter;
    """
    df = run_query(conn, q)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Year-Quarter Transaction Amount")
        fig = px.bar(df, x="Quarter", y="Amount", color="Years", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📊 Year-Quarter Transaction Count")
        fig2 = px.bar(df, x="Quarter", y="Count", color="Years", barmode="group")
        st.plotly_chart(fig2, use_container_width=True)

elif choice == "Aggregated Insurance":
    st.header("🛡️ Insurance Insights")
    q = """
    SELECT Insurance_type, SUM(Insurance_amount) AS Total_Amount, SUM(Insurance_count) AS Total_Count
    FROM aggregated_insurance
    GROUP BY Insurance_type
    ORDER BY Total_Amount DESC;
    """
    df = run_query(conn, q)
    st.dataframe(df)
    fig = px.pie(df, names='Insurance_type', values='Total_Amount', title='Insurance Type Share')
    st.plotly_chart(fig, use_container_width=True)

elif choice == "Top Users":
    st.header("👥 Top Registered Users by State")
    q = "SELECT States, SUM(RegisteredUser) AS Total_Users FROM top_user GROUP BY States ORDER BY Total_Users DESC LIMIT 10;"
    df = run_query(conn, q)
    st.bar_chart(df.set_index("States"))