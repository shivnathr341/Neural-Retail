import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Forecast Dashboard", layout="wide")

@st.cache_data
def load_data():
    
    daily   = pd.read_csv("daily_sales.csv",
                          parse_dates=['InvoiceDate'])
    forecast = pd.read_csv("future_forecast.csv",
                           parse_dates=['Date'])
    return daily, forecast

daily_sales, forecast_df = load_data()

st.title("📈 Forecast Dashboard")
st.markdown("---")

# ── KPI Cards ──────────────────────────────────────────────
next30 = forecast_df.head(30)
k1, k2, k3 = st.columns(3)
k1.metric("Forecast (Next 30 Days)",
          f"£{next30['Forecast'].sum():,.0f}")
k2.metric("Avg Daily Forecast",
          f"£{next30['Forecast'].mean():,.0f}")
k3.metric("Peak Day Forecast",
          f"£{next30['Forecast'].max():,.0f}")

st.markdown("---")

# ── Forecast Plot ──────────────────────────────────────────
st.subheader("Revenue Forecast")

days = st.slider("Forecast Days", min_value=7,
                 max_value=60, value=30, step=7)

fig = go.Figure()

# Actual data — last 90 days
actual_tail = daily_sales.tail(90)
fig.add_trace(go.Scatter(
    x=actual_tail['InvoiceDate'],
    y=actual_tail['Revenue'],
    name='Actual Revenue',
    line=dict(color='#2196F3', width=2)
))

# Forecast
fc = forecast_df.head(days)
fig.add_trace(go.Scatter(
    x=fc['Date'], y=fc['Forecast'],
    name='Forecast',
    line=dict(color='#FF5722', width=2, dash='dash')
))

# Confidence interval
fig.add_trace(go.Scatter(
    x=pd.concat([fc['Date'], fc['Date'][::-1]]),
    y=pd.concat([fc['Upper_Bound'], fc['Lower_Bound'][::-1]]),
    fill='toself',
    fillcolor='rgba(255,87,34,0.15)',
    line=dict(color='rgba(255,255,255,0)'),
    name='Confidence Interval'
))

fig.update_layout(
    title=f"Revenue Forecast — Next {days} Days",
    xaxis_title="Date",
    yaxis_title="Revenue (£)",
    height=450,
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

# ── Forecast Table ─────────────────────────────────────────
st.subheader("Forecast Details")
display_fc = forecast_df.head(days).copy()
display_fc['Date']        = display_fc['Date'].dt.strftime('%Y-%m-%d')
display_fc['Forecast']    = display_fc['Forecast'].round(2)
display_fc['Lower_Bound'] = display_fc['Lower_Bound'].round(2)
display_fc['Upper_Bound'] = display_fc['Upper_Bound'].round(2)
st.dataframe(display_fc, use_container_width=True, hide_index=True)