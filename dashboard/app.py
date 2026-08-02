import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.express as px
import pandas as pd
from sqlalchemy import text
from db.connection import get_engine
from db.queries import (
    get_total_revenue,
    get_total_orders,
    get_total_profit,
    get_average_order_value,
    get_revenue_by_month,
    get_revenue_by_region,
    get_top_products,
    get_revenue_by_category,
    get_revenue_by_subcategory,
    get_revenue_by_segment,
    get_shipmode_breakdown,
    get_top_customers
)

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Title ─────────────────────────────────────────────────────
st.title("📊 Sales Analytics Dashboard")
st.markdown("Real-time sales insights powered by PostgreSQL & Python")
st.divider()

# ── KPI Cards ─────────────────────────────────────────────────
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"${get_total_revenue():,}"
    )

with col2:
    st.metric(
        label="📦 Total Orders",
        value=f"{get_total_orders():,}"
    )

with col3:
    st.metric(
        label="📈 Total Profit",
        value=f"${get_total_profit():,}"
    )

with col4:
    st.metric(
        label="🧾 Avg Order Value",
        value=f"${get_average_order_value():,}"
    )

st.divider()

# ── Revenue Over Time ──────────────────────────────────────────
st.subheader("📈 Revenue & Profit Over Time")
revenue_month_df = get_revenue_by_month()
fig_line = px.line(
    revenue_month_df,
    x="month",
    y=["revenue", "profit"],
    markers=True,
    labels={"month": "Month", "value": "Amount ($)", "variable": "Metric"},
)
fig_line.update_layout(hovermode="x unified")
st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ── Region + Segment ──────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🌍 Revenue by Region")
    region_df = get_revenue_by_region()
    fig_region = px.bar(
        region_df,
        x="region",
        y="revenue",
        color="region",
        labels={"region": "Region", "revenue": "Revenue ($)"},
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col_right:
    st.subheader("👥 Revenue by Segment")
    segment_df = get_revenue_by_segment()
    fig_segment = px.pie(
        segment_df,
        names="segment",
        values="revenue",
        hole=0.4,
    )
    st.plotly_chart(fig_segment, use_container_width=True)

st.divider()

# ── Category + Subcategory ────────────────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("🛍️ Revenue by Category")
    category_df = get_revenue_by_category()
    fig_category = px.pie(
        category_df,
        names="category",
        values="revenue",
        hole=0.4,
    )
    st.plotly_chart(fig_category, use_container_width=True)

with col_right2:
    st.subheader("📦 Revenue by Sub-Category")
    subcategory_df = get_revenue_by_subcategory()
    fig_subcategory = px.bar(
        subcategory_df,
        x="revenue",
        y="sub_category",
        orientation="h",
        color="category",
        labels={"revenue": "Revenue ($)", "sub_category": "Sub-Category"},
    )
    fig_subcategory.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_subcategory, use_container_width=True)

st.divider()

# ── Top Products ───────────────────────────────────────────────
st.subheader("🏆 Top 10 Products by Revenue")
products_df = get_top_products(limit=10)
fig_products = px.bar(
    products_df,
    x="revenue",
    y="product_name",
    orientation="h",
    color="category",
    labels={"revenue": "Revenue ($)", "product_name": "Product"},
)
fig_products.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_products, use_container_width=True)

st.divider()

# ── Ship Mode + Top Customers ─────────────────────────────────
col_left3, col_right3 = st.columns(2)

with col_left3:
    st.subheader("🚚 Orders by Ship Mode")
    shipmode_df = get_shipmode_breakdown()
    fig_ship = px.pie(
        shipmode_df,
        names="ship_mode",
        values="total_orders",
        hole=0.4,
    )
    st.plotly_chart(fig_ship, use_container_width=True)

with col_right3:
    st.subheader("👑 Top 10 Customers")
    customers_df = get_top_customers(limit=10)
    st.dataframe(
        customers_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ── Raw Data Table ─────────────────────────────────────────────
st.subheader("🗃️ Raw Orders Data")
with get_engine().connect() as conn:
    raw_df = pd.read_sql(
        text("SELECT * FROM vw_order_summary ORDER BY order_date DESC"),
        conn
    )

st.dataframe(raw_df, use_container_width=True, hide_index=True)

csv = raw_df.to_csv(index=False)
st.download_button(
    label="⬇️ Download CSV",
    data=csv,
    file_name="sales_data.csv",
    mime="text/csv"
)