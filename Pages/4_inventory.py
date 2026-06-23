import os

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Inventory Dashboard", layout="wide")

@st.cache_data
def load_data():
    
    return pd.read_csv("inventory_optimization.csv")

inv_df = load_data()

st.title("📦 Inventory Dashboard")
st.markdown("---")

# ── KPI Cards ──────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Products",   f"{len(inv_df):,}")
k2.metric("Category A",       f"{(inv_df['ABC_Category']=='A').sum():,}")
k3.metric("Critical Stock",   f"{(inv_df['StockStatus']=='CRITICAL').sum():,}")
k4.metric("Reorder Now",      f"{(inv_df['StockStatus']=='REORDER NOW').sum():,}")

st.markdown("---")

# ── Sidebar Filter ─────────────────────────────────────────
st.sidebar.header("Filters")
abc_filter = st.sidebar.multiselect(
    "ABC Category", options=['A','B','C'], default=['A','B','C']
)
status_filter = st.sidebar.multiselect(
    "Stock Status",
    options=['CRITICAL','REORDER NOW','MONITOR','OK'],
    default=['CRITICAL','REORDER NOW','MONITOR','OK']
)

filtered = inv_df[
    (inv_df['ABC_Category'].isin(abc_filter)) &
    (inv_df['StockStatus'].isin(status_filter))
]

# ── ABC Analysis ───────────────────────────────────────────
st.subheader("ABC Analysis")

col1, col2 = st.columns(2)

with col1:
    abc_count = inv_df['ABC_Category'].value_counts().reset_index()
    abc_count.columns = ['Category', 'Count']
    fig_abc = px.pie(
        abc_count, values='Count', names='Category',
        title="Products by Category",
        color_discrete_sequence=['#2196F3','#FF9800','#4CAF50']
    )
    st.plotly_chart(fig_abc, use_container_width=True)

with col2:
    abc_rev = (inv_df.groupby('ABC_Category')['TotalRevenue']
               .sum().reset_index())
    fig_rev = px.bar(
        abc_rev, x='ABC_Category', y='TotalRevenue',
        title="Revenue by ABC Category",
        color='ABC_Category',
        color_discrete_sequence=['#2196F3','#FF9800','#4CAF50']
    )
    st.plotly_chart(fig_rev, use_container_width=True)

# ── Stock Status ───────────────────────────────────────────
st.subheader("Stock Status Overview")

status_colors = {
    'CRITICAL'   : '#F44336',
    'REORDER NOW': '#FF9800',
    'MONITOR'    : '#2196F3',
    'OK'         : '#4CAF50'
}

status_count = inv_df['StockStatus'].value_counts().reset_index()
status_count.columns = ['Status', 'Count']

fig_status = px.bar(
    status_count, x='Status', y='Count',
    title="Products by Stock Status",
    color='Status',
    color_discrete_map=status_colors
)
st.plotly_chart(fig_status, use_container_width=True)

# ── Urgent Orders Table ────────────────────────────────────
st.subheader("🚨 Urgent Orders Required")

urgent = filtered[
    filtered['StockStatus'].isin(['CRITICAL','REORDER NOW'])
].sort_values('TotalRevenue', ascending=False)

if len(urgent) > 0:
    display_cols = ['StockCode', 'ProductName', 'ABC_Category',
                    'StockStatus', 'CurrentStock',
                    'ReorderPoint', 'EOQ']
    st.dataframe(
        urgent[display_cols].head(20),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("Koi urgent order nahi hai!")

# ── Full Inventory Table ───────────────────────────────────
st.subheader("Full Inventory Table")
st.dataframe(
    filtered[['StockCode','ProductName','ABC_Category',
              'StockStatus','AvgDailyDemand',
              'SafetyStock','ReorderPoint','EOQ',
              'TotalRevenue']].head(50),
    use_container_width=True,
    hide_index=True
)