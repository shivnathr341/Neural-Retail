import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# ── Data load ──────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(BASE_DIR, "Online Retail Cleaned.csv"),
                     parse_dates=['InvoiceDate'])
    daily = pd.read_csv(os.path.join(BASE_DIR,  "daily_sales.csv"),
                        parse_dates=['InvoiceDate'])

    # Yeh 3 lines add karo
    df['Month']   = df['InvoiceDate'].dt.month
    df['Hour']    = df['InvoiceDate'].dt.hour
    df['Weekday'] = df['InvoiceDate'].dt.day_name()

    return df, daily

df, daily_sales = load_data()

# ── Header ─────────────────────────────────────────────────
st.title("📊 Sales Dashboard")
st.markdown("---")

# ── Sidebar Filters ────────────────────────────────────────
st.sidebar.header("Filters")

min_date = df['InvoiceDate'].min().date()
max_date = df['InvoiceDate'].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

countries = ['All'] + sorted(df['Country'].unique().tolist())
selected_country = st.sidebar.selectbox("Country", countries)

# Filter apply karo
mask = (df['InvoiceDate'].dt.date >= date_range[0]) & \
       (df['InvoiceDate'].dt.date <= date_range[1])
filtered = df[mask]

if selected_country != 'All':
    filtered = filtered[filtered['Country'] == selected_country]

# ── KPI Cards ──────────────────────────────────────────────
st.subheader("Key Metrics")
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Revenue",
          f"£{filtered['Total Price'].sum():,.0f}")
k2.metric("Total Orders",
          f"{filtered['Invoice'].nunique():,}")
k3.metric("Unique Customers",
          f"{filtered['Customer ID'].nunique():,}")
k4.metric("Avg Order Value",
          f"£{filtered['Total Price'].mean():,.2f}")

st.markdown("---")

# ── Revenue Trend ──────────────────────────────────────────
st.subheader("Revenue Trend")

daily_filtered = daily_sales[
    (daily_sales['InvoiceDate'].dt.date >= date_range[0]) &
    (daily_sales['InvoiceDate'].dt.date <= date_range[1])
]

fig_trend = px.line(
    daily_filtered,
    x='InvoiceDate',
    y='Revenue',
    title="Daily Revenue",
    color_discrete_sequence=['#2196F3']
)
fig_trend.update_layout(height=350)
st.plotly_chart(fig_trend, use_container_width=True)

# ── Monthly + Hourly ───────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    monthly = filtered.groupby('Month')['Total Price'].sum().reset_index()
    fig_Month = px.bar(
        monthly, x='Month', y='Total Price',
        title="Monthly Revenue",
        color_discrete_sequence=['#2196F3']
    )
    st.plotly_chart(fig_Month, use_container_width=True)

with col2:
    hourly = filtered.groupby('Hour')['Total Price'].sum().reset_index()
    fig_hour = px.bar(
        hourly, x='Hour', y='Total Price',
        title="Revenue by Hour",
        color_discrete_sequence=['#FF5722']
    )
    st.plotly_chart(fig_hour, use_container_width=True)

# ── Top Products + Countries ───────────────────────────────
col3, col4 = st.columns(2)

with col3:
    top_products = (filtered.groupby('Description')['Total Price']
                    .sum().nlargest(10).reset_index())
    fig_prod = px.bar(
        top_products, x='Total Price', y='Description',
        orientation='h', title="Top 10 Products",
        color_discrete_sequence=['#4CAF50']
    )
    fig_prod.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_prod, use_container_width=True)

with col4:
    country_rev = (filtered[filtered['Country'] != 'United Kingdom']
                   .groupby('Country')['Total Price']
                   .sum().nlargest(10).reset_index())
    fig_country = px.bar(
        country_rev, x='Total Price', y='Country',
        orientation='h', title="Top 10 Countries (excl. UK)",
        color_discrete_sequence=['#9C27B0']
    )
    fig_country.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_country, use_container_width=True)