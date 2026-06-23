import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Customer Dashboard", layout="wide")

@st.cache_data
def load_data():
    
    rfm   = pd.read_csv("rfm_segments.csv")
    churn = pd.read_csv("churn_predictions.csv")
    return rfm, churn

rfm_df, churn_df = load_data()

st.title("👥 Customer Dashboard")
st.markdown("---")

# ── KPI Cards ──────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Customers",    f"{len(rfm_df):,}")
k2.metric("Champions",          f"{(rfm_df['Segment']=='Champions').sum():,}")
k3.metric("At Risk",            f"{(rfm_df['Segment']=='At Risk').sum():,}")
k4.metric("High Churn Risk",
          f"{(churn_df['Risk_Category']=='High Risk').sum():,}")

st.markdown("---")

# ── RFM Segments ───────────────────────────────────────────
st.subheader("Customer Segments (RFM)")

col1, col2 = st.columns(2)

with col1:
    seg_counts = rfm_df['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']
    fig_seg = px.pie(
        seg_counts, values='Count', names='Segment',
        title="Segment Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_seg, use_container_width=True)

with col2:
    seg_money = (rfm_df.groupby('Segment')['Monetary']
                 .mean().reset_index()
                 .sort_values('Monetary', ascending=True))
    fig_money = px.bar(
        seg_money, x='Monetary', y='Segment',
        orientation='h', title="Avg Spend per Segment",
        color_discrete_sequence=['#2196F3']
    )
    st.plotly_chart(fig_money, use_container_width=True)

# ── RFM Scatter ────────────────────────────────────────────
st.subheader("Recency vs Monetary by Segment")

fig_scatter = px.scatter(
    rfm_df, x='Recency', y='Monetary',
    color='Segment', size='Frequency',
    hover_data=['Customer ID'],
    title="Customer Map",
    color_discrete_sequence=px.colors.qualitative.Set1
)
fig_scatter.update_layout(height=450)
st.plotly_chart(fig_scatter, use_container_width=True)

# ── Churn Risk ─────────────────────────────────────────────
st.markdown("---")
st.subheader("Churn Risk Analysis")

col3, col4 = st.columns(2)

with col3:
    risk_counts = churn_df['Risk_Category'].value_counts().reset_index()
    risk_counts.columns = ['Risk', 'Count']
    color_map = {
        'High Risk'  : '#F44336',
        'Medium Risk': '#FF9800',
        'Low Risk'   : '#2196F3',
        'Safe'       : '#4CAF50'
    }
    fig_risk = px.bar(
        risk_counts, x='Risk', y='Count',
        title="Churn Risk Distribution",
        color='Risk', color_discrete_map=color_map
    )
    st.plotly_chart(fig_risk, use_container_width=True)

with col4:
    # High risk customers table
    st.markdown("**Top High Risk Customers**")
    high_risk = (churn_df[churn_df['Risk_Category'] == 'High Risk']
                 .sort_values('Monetary', ascending=False)
                 .head(10)[['Customer ID', 'Recency',
                             'Monetary', 'Churn_Probability']])
    high_risk['Churn_Probability'] = high_risk['Churn_Probability'].round(3)
    st.dataframe(high_risk, use_container_width=True, hide_index=True)