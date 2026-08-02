import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy import text
from db.connection import get_engine
import streamlit as st

# ── Cached query functions ────────────────────────────────────

@st.cache_data(ttl=600)
def get_total_revenue():
    """Total revenue from all orders."""
    query = text("""
        SELECT ROUND(SUM(order_total)::numeric, 2) AS total_revenue
        FROM vw_order_summary
    """)
    with get_engine().connect() as conn:
        result = conn.execute(query)
        return result.fetchone()[0]

@st.cache_data(ttl=600)
def get_total_orders():
    """Total number of unique orders."""
    query = text("""
        SELECT COUNT(DISTINCT order_reference) AS total_orders
        FROM vw_order_summary
    """)
    with get_engine().connect() as conn:
        result = conn.execute(query)
        return result.fetchone()[0]

@st.cache_data(ttl=600)
def get_total_profit():
    """Total profit from all orders."""
    query = text("""
        SELECT ROUND(SUM(profit)::numeric, 2) AS total_profit
        FROM vw_order_summary
    """)
    with get_engine().connect() as conn:
        result = conn.execute(query)
        return result.fetchone()[0]

@st.cache_data(ttl=600)
def get_average_order_value():
    """Average order value."""
    query = text("""
        SELECT ROUND(AVG(order_total)::numeric, 2) AS avg_order_value
        FROM vw_order_summary
    """)
    with get_engine().connect() as conn:
        result = conn.execute(query)
        return result.fetchone()[0]

@st.cache_data(ttl=600)
def get_revenue_by_month():
    """Monthly revenue trend."""
    query = text("""
        SELECT
            TO_CHAR(order_date, 'YYYY-MM') AS month,
            ROUND(SUM(order_total)::numeric, 2) AS revenue,
            ROUND(SUM(profit)::numeric, 2) AS profit
        FROM vw_order_summary
        GROUP BY TO_CHAR(order_date, 'YYYY-MM')
        ORDER BY month ASC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_revenue_by_region():
    """Revenue and profit by region."""
    query = text("""
        SELECT
            region,
            ROUND(SUM(order_total)::numeric, 2) AS revenue,
            ROUND(SUM(profit)::numeric, 2) AS profit,
            COUNT(DISTINCT order_reference) AS total_orders
        FROM vw_order_summary
        GROUP BY region
        ORDER BY revenue DESC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_top_products(limit=10):
    """Top products by revenue."""
    query = text("""
        SELECT
            product_name,
            category,
            sub_category,
            SUM(quantity) AS units_sold,
            ROUND(SUM(order_total)::numeric, 2) AS revenue,
            ROUND(SUM(profit)::numeric, 2) AS profit
        FROM vw_order_summary
        GROUP BY product_name, category, sub_category
        ORDER BY revenue DESC
        LIMIT :limit
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn, params={"limit": limit})

@st.cache_data(ttl=600)
def get_revenue_by_category():
    """Revenue by category."""
    query = text("""
        SELECT
            category,
            ROUND(SUM(order_total)::numeric, 2) AS revenue,
            ROUND(SUM(profit)::numeric, 2) AS profit
        FROM vw_order_summary
        GROUP BY category
        ORDER BY revenue DESC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_revenue_by_subcategory():
    """Revenue by sub-category."""
    query = text("""
        SELECT
            sub_category,
            category,
            ROUND(SUM(order_total)::numeric, 2) AS revenue,
            ROUND(SUM(profit)::numeric, 2) AS profit
        FROM vw_order_summary
        GROUP BY sub_category, category
        ORDER BY revenue DESC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_revenue_by_segment():
    """Revenue by customer segment."""
    query = text("""
        SELECT
            segment,
            ROUND(SUM(order_total)::numeric, 2) AS revenue,
            ROUND(SUM(profit)::numeric, 2) AS profit,
            COUNT(DISTINCT order_reference) AS total_orders
        FROM vw_order_summary
        GROUP BY segment
        ORDER BY revenue DESC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_shipmode_breakdown():
    """Orders by shipping mode."""
    query = text("""
        SELECT
            ship_mode,
            COUNT(DISTINCT order_reference) AS total_orders,
            ROUND(SUM(order_total)::numeric, 2) AS revenue
        FROM vw_order_summary
        GROUP BY ship_mode
        ORDER BY total_orders DESC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=600)
def get_top_customers(limit=10):
    """Top customers by revenue."""
    query = text("""
        SELECT
            customer_name,
            segment,
            region,
            COUNT(DISTINCT order_reference) AS total_orders,
            ROUND(SUM(order_total)::numeric, 2) AS total_spent,
            ROUND(SUM(profit)::numeric, 2) AS total_profit
        FROM vw_order_summary
        GROUP BY customer_name, segment, region
        ORDER BY total_spent DESC
        LIMIT :limit
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn, params={"limit": limit})

if __name__ == "__main__":
    print("Total Revenue:   $", get_total_revenue())
    print("Total Orders:    ", get_total_orders())
    print("Total Profit:    $", get_total_profit())
    print("Avg Order Value: $", get_average_order_value())
    print("\nRevenue by Month:")
    print(get_revenue_by_month())
    print("\nRevenue by Region:")
    print(get_revenue_by_region())
    print("\nTop 10 Products:")
    print(get_top_products())
    print("\nRevenue by Category:")
    print(get_revenue_by_category())
    print("\nRevenue by Segment:")
    print(get_revenue_by_segment())
    print("\nShip Mode Breakdown:")
    print(get_shipmode_breakdown())
    print("\nTop 10 Customers:")
    print(get_top_customers())