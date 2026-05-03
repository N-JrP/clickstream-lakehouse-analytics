import streamlit as st
import pandas as pd
from pathlib import Path


st.set_page_config(page_title="Clickstream Analytics", layout="wide")

st.title("📊 Clickstream Analytics Dashboard")

BASE_DIR = Path(__file__).resolve().parents[1]
gold_path = BASE_DIR / "data" / "gold"


def load_parquet(folder_path):
    files = list(folder_path.glob("*.parquet"))
    if not files:
        st.warning(f"No data found in {folder_path}")
        return pd.DataFrame()
    return pd.concat([pd.read_parquet(f) for f in files])


daily_pd = load_parquet(gold_path / "daily_kpis")
funnel_pd = load_parquet(gold_path / "funnel_metrics")
products_pd = load_parquet(gold_path / "product_metrics")


# --- KPIs ---
st.header("📅 Daily KPIs")

if not daily_pd.empty:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Events", int(daily_pd["total_events"].sum()))
    col2.metric("Active Users", int(daily_pd["active_users"].sum()))
    col3.metric("Sessions", int(daily_pd["sessions"].sum()))
    col4.metric("Revenue", round(daily_pd["total_revenue"].sum(), 2))

    st.dataframe(daily_pd)
else:
    st.warning("Daily KPI data not available")


# --- Funnel ---
st.header("🔄 Funnel Metrics")

if not funnel_pd.empty:
    # --- ORDER FIX (ADD THIS PART) ---
    order = ["page_view", "product_view", "add_to_cart", "checkout", "purchase"]

    funnel_pd["event_type"] = pd.Categorical(
        funnel_pd["event_type"], categories=order, ordered=True
    )

    funnel_pd = funnel_pd.sort_values("event_type")
    # --- END FIX ---

    st.bar_chart(
    	funnel_pd.set_index("event_type")[["event_count"]]
    )
else:
    st.warning("Funnel data not available")

# --- Products ---
st.header("🛍️ Top Products")

if not products_pd.empty:
    st.dataframe(products_pd.head(10))
else:
    st.warning("Product data not available")