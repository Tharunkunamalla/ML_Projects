import streamlit as st
from utils import get_connection, run_query
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide", page_title="📊 PhonePe Dashboard")
st.title("📱 PhonePe Transaction Insights")

menu = [
    "Overview", "State-wise Analysis", "Aggregated Insurance", 
    "Top Users", "KPIs & Metrics", "Geo Visualization", "Download CSVs"
]
choice = st.sidebar.selectbox("🔎 Select Dashboard View", menu)

conn = get_connection()

#  Overview 
if choice == "Overview":
    st.header("💼 Aggregated Transaction Overview")

    year_df = run_query(conn, "SELECT DISTINCT Years FROM aggregated_transaction ORDER BY Years")
    selected_year = st.selectbox("Select Year", year_df["Years"], key="overview_year")

    chart_type = st.radio("📊 Select Chart Type", ["Bar", "Line", "Area"], horizontal=True)

    query = f"""
    SELECT States, SUM(Transaction_amount) AS Total_Amount, SUM(Transaction_count) AS Total_Count
    FROM aggregated_transaction
    WHERE Years = {selected_year}
    GROUP BY States
    ORDER BY Total_Amount DESC;
    """
    df = run_query(conn, query)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"💰 Transaction Amount - {selected_year}")
        if chart_type == "Bar":
            fig = px.bar(df, x='States', y='Total_Amount', title="Transaction Amount by State")
        elif chart_type == "Line":
            fig = px.line(df, x='States', y='Total_Amount', markers=True, title="Transaction Amount by State")
        else:
            fig = px.area(df, x='States', y='Total_Amount', title="Transaction Amount by State")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader(f"🔁 Transaction Count - {selected_year}")
        if chart_type == "Bar":
            fig = px.bar(df, x='States', y='Total_Count', color_discrete_sequence=['indianred'], title="Transaction Count by State")
        elif chart_type == "Line":
            fig = px.line(df, x='States', y='Total_Count', color_discrete_sequence=['indianred'], markers=True, title="Transaction Count by State")
        else:
            fig = px.area(df, x='States', y='Total_Count', color_discrete_sequence=['indianred'], title="Transaction Count by State")
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("🌳 Treemap View of Transaction Amount"):
        fig = px.treemap(df, path=['States'], values='Total_Amount', title=f"Treemap of Transaction Amount by State - {selected_year}")
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📉 Scatter Plot of Amount vs Count"):
        fig = px.scatter(df, x="Total_Count", y="Total_Amount", color="States",
                         title=f"Scatter Plot: Transaction Count vs Amount - {selected_year}",
                         size="Total_Amount", hover_name="States")
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📦 Boxplot of Transaction Amounts"):
        fig = px.box(df, y="Total_Amount", title="Boxplot of Transaction Amounts by State")
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("🔥 Heatmap: Quarter vs Year Transaction Amount"):
        heat_query = f"""
        SELECT Years, Quarter, SUM(Transaction_amount) AS Amount
        FROM aggregated_transaction
        WHERE Years <= {selected_year}
        GROUP BY Years, Quarter;
        """
        heat_df = run_query(conn, heat_query)
        pivot_df = heat_df.pivot(index="Years", columns="Quarter", values="Amount")
        fig = px.imshow(pivot_df, text_auto=True, aspect="auto", color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📈 National Yearly Transaction Trend"):
        trend_query = """
        SELECT Years, SUM(Transaction_amount) AS Amount
        FROM aggregated_transaction
        GROUP BY Years
        ORDER BY Years;
        """
        trend_df = run_query(conn, trend_query)
        fig = px.line(trend_df, x="Years", y="Amount", markers=True,
                      title="National Transaction Amount Over Years")
        st.plotly_chart(fig, use_container_width=True)

#  State-wise Analysis 
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

#  Aggregated Insurance 
elif choice == "Aggregated Insurance":
    st.header("🛡️ Insurance Insights")

    year_list = run_query(conn, "SELECT DISTINCT Years FROM aggregated_insurance ORDER BY Years")["Years"].tolist()
    selected_year = st.selectbox("📅 Select Year", year_list)

    state_list = run_query(conn, f"SELECT DISTINCT States FROM aggregated_insurance WHERE Years = {selected_year} ORDER BY States")["States"].tolist()
    selected_state = st.selectbox("📍 Select State", state_list)

    chart_type = st.radio("📊 Select Chart Type", ["Bar", "Pie", "Donut"], horizontal=True)

    q = f"""
    SELECT States, SUM(Insurance_amount) AS Total_Amount, SUM(Insurance_count) AS Total_Count
    FROM aggregated_insurance
    WHERE Years = {selected_year}
    GROUP BY States
    """
    df = run_query(conn, q)

    state_data = df[df["States"] == selected_state]
    st.subheader(f"📍 Insurance Summary for {selected_state}")
    st.dataframe(state_data)

    if chart_type == "Bar":
        fig = px.bar(df, x="States", y="Total_Amount", title=f"💰 Statewise Insurance Amounts - {selected_year}")
        st.plotly_chart(fig, use_container_width=True)
    elif chart_type == "Pie":
        fig = px.pie(df, values="Total_Amount", names="States", title=f"🟢 Insurance Amount Share by State - {selected_year}")
        st.plotly_chart(fig, use_container_width=True)
    elif chart_type == "Donut":
        fig = px.pie(df, values="Total_Amount", names="States", hole=0.4, title=f"🍩 Donut Chart - Insurance Share by State - {selected_year}")
        st.plotly_chart(fig, use_container_width=True)

#  Top Users 
elif choice == "Top Users":
    st.header("👥 Top Registered Users by State")

    # Fetch Top 10 States by Registered Users
    query = """
    SELECT States, SUM(RegisteredUser) AS Total_Users 
    FROM top_user 
    GROUP BY States 
    ORDER BY Total_Users DESC 
    LIMIT 10;
    """
    df = run_query(conn, query)

    # Display as Table and Chart
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📋 Top 10 States (Table)")
        st.dataframe(df)

    with col2:
        st.subheader("📊 Bar Chart View")
        fig = px.bar(df, x="States", y="Total_Users", text="Total_Users",
                     color="Total_Users", title="Top 10 States by Registered Users",
                     color_continuous_scale="viridis")
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📌 You can drill down by state using the State-wise Analysis tab for more details.")

#  KPIs 
elif choice == "KPIs & Metrics":
    st.header("📊 Key Performance Indicators")

    # === Current KPIs ===
    kpi1 = run_query(conn, "SELECT SUM(Transaction_amount) FROM aggregated_transaction").iloc[0, 0]
    kpi2 = run_query(conn, "SELECT SUM(Transaction_count) FROM aggregated_transaction").iloc[0, 0]
    kpi3 = run_query(conn, "SELECT SUM(RegisteredUser) FROM top_user").iloc[0, 0]

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Transaction Amount", f"₹ {kpi1:,}")
    col2.metric("🔁 Total Transactions", f"{kpi2:,}")
    col3.metric("📲 Total Registered Users", f"{kpi3:,}")

    st.markdown("### 📈 Yearly Growth Trends")

    # === Trend Graphs ===
    yearly = run_query(conn, """
        SELECT Years, 
               SUM(Transaction_amount) AS Amount, 
               SUM(Transaction_count) AS Count 
        FROM aggregated_transaction
        GROUP BY Years
        ORDER BY Years
    """)

    user_yearly = run_query(conn, """
        SELECT Years, SUM(RegisteredUser) AS Users 
        FROM top_user 
        GROUP BY Years
        ORDER BY Years
    """)

    fig1 = px.line(yearly, x="Years", y="Amount", markers=True, title="💰 Transaction Amount Over Years")
    fig2 = px.line(yearly, x="Years", y="Count", markers=True, title="🔁 Transaction Count Over Years")
    fig3 = px.line(user_yearly, x="Years", y="Users", markers=True, title="📲 Registered Users Over Years")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 🥧 Top 5 States by Transaction Amount")
    top_states = run_query(conn, """
        SELECT States, SUM(Transaction_amount) AS Amount
        FROM aggregated_transaction
        GROUP BY States
        ORDER BY Amount DESC
        LIMIT 5
    """)
    fig = px.pie(top_states, values="Amount", names="States", title="Top 5 States by Transaction Amount", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

#  Geo Map 
elif choice == "Geo Visualization":
    st.header("🗺️ Choropleth Map of Transaction Amounts")
    with open("streamlit_app/india_states.geojson", "r", encoding="utf-8") as f:
        india_states = json.load(f)

    geojson_key = "name"
    q = """
    SELECT States, SUM(Transaction_amount) AS Amount
    FROM aggregated_transaction
    GROUP BY States;
    """
    df = run_query(conn, q)

    df["States"] = df["States"].replace({
        "Andaman & Nicobar": "Andaman and Nicobar Islands",
        "Dadra and Nagar Haveli and Daman and Diu": "Dadra and Nagar Haveli and Daman and Diu",
        "Jammu & Kashmir": "Jammu and Kashmir",
        "Odisha": "Orissa"
    })

    fig = px.choropleth(
        df,
        geojson=india_states,
        locations="States",
        featureidkey=f"properties.{geojson_key}",
        color="Amount",
        color_continuous_scale="thermal",
        title="Statewise Transaction Amounts"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

    selected = st.selectbox("👇 Select a state for details", df["States"])
    if selected:
        st.subheader(f"📍 Transaction Info for {selected}")
        state_query = f"""
        SELECT Years, Quarter, SUM(Transaction_amount) AS Amount, SUM(Transaction_count) AS Count
        FROM aggregated_transaction
        WHERE States = '{selected}'
        GROUP BY Years, Quarter
        ORDER BY Years, Quarter;
        """
        state_df = run_query(conn, state_query)
        st.dataframe(state_df)
        fig = px.line(state_df, x="Years", y="Amount", color="Quarter", title=f"🧾 Yearly Transaction Trend - {selected}")
        st.plotly_chart(fig, use_container_width=True)

#  Download
elif choice == "Download CSVs":
    st.header("⬇️ Download Data as CSV")
    tables = [
        "aggregated_user", "aggregated_transaction", "aggregated_insurance",
        "map_user", "map_transaction", "map_insurance",
        "top_user", "top_transaction", "top_insurance"
    ]
    selected_table = st.selectbox("Select Table", tables)
    df = run_query(conn, f"SELECT * FROM {selected_table}")
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), file_name=f"{selected_table}.csv")
