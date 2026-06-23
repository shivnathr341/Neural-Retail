import streamlit as st

st.set_page_config(
    page_title = "NeuralRetail Dashboard",
    page_icon  = "🛒",
    layout     = "wide"
)

st.title("🛒 NeuralRetail Analytics Dashboard")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("📊 **Sales Dashboard**\n\nRevenue trends, top products, country analysis")
with col2:
    st.success("👥 **Customer Dashboard**\n\nRFM segments, churn risk, customer value")
with col3:
    st.warning("📈 **Forecast Dashboard**\n\nDemand forecasting, future sales prediction")
with col4:
    st.error("📦 **Inventory Dashboard**\n\nStock status, reorder alerts, ABC analysis")

st.markdown("---")
st.markdown("**Select page from Slidebar**")