import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy import text
from db.connection import get_engine

def get_total_revenue():
    """total revenue from all completed orders."""
    query = text("""
        SELECT ROUND(SUM(order_total)::numeric, 2) AS total_revenue
        FROM vw_order_summary
        WHERE status = 'completed'
        """)
    with get_engine().connect() as conn:
        result = conn.execute(query)
        return result.fetchone()[0]
    
def get_total_orders():
    """Total number of orders."""
    query = text("""
        SELECT COUNT(*) AS total_orders
        FROM orders
    """)
    with get_engine().connect() as conn:
        result = conn.execute(query)
        return result.fetchone()[0]

def get_average_order_value():
    """Average value of completed orders."""
    query = text("""
        SELECT ROUND(AVG(order_total)::numeric, 2) AS avg_order_value
        FROM vw_order_summary
        WHERE status = 'completed'
    """)
    with get_engine().connect() as conn:
        result = conn.execute(query)
        return result.fetchone()[0]
    
def get_revenue_by_month():
    """Monthly revenue trend for completed orders."""
    query = text("""
        SELECT
            TO_CHAR(order_date, 'YYYY-MM') AS month,
            ROUND(SUM(order_total)::numeric, 2) AS revenue
        FROM vw_order_summary
        WHERE status = 'completed'
        GROUP BY TO_CHAR(order_date, 'YYYY-MM')
        ORDER BY month ASC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)
    
def get_revenue_by_region():
    """Total revenue broken down by region."""
    query = text("""
        SELECT
            region,
            ROUND(SUM(order_total)::numeric, 2) AS revenue,
            COUNT(*) AS total_order
        FROM vw_order_summary
        WHERE status = 'completed'
        GROUP BY region
        ORDER BY revenue DESC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

def get_top_products(limit=10):
    """Top products by total revenue."""
    query = text("""
                 SELECT
                     p.name AS product_name,
                     c.name AS category,
                     SUM(oi.quantity) AS units_sold,
                     ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount))::numeric, 2) AS revenue
                FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.status = 'completed'
        GROUP BY p.name, c.name
        ORDER BY revenue DESC
        LIMIT :limit
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn, params={"limit": limit})

def get_revenue_by_category():
    """Revenue broken down by product category."""
    query = text("""
        SELECT
            c.name AS category,
            ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount))::numeric, 2) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.status = 'completed'
        GROUP BY c.name
        ORDER BY revenue DESC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

def get_order_status_breakdown():
    """Count of orders by status."""
    query = text("""
        SELECT
            status,
            COUNT(*) AS total,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()::numeric, 1) AS percentage
        FROM orders
        GROUP BY status
        ORDER BY total DESC
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn)

def get_top_customers(limit=10):
    """Top customers by total spending."""
    query = text("""
        SELECT
            customer_name,
            region,
            COUNT(*) AS total_orders,
            ROUND(SUM(order_total)::numeric, 2) AS total_spent
        FROM vw_order_summary
        WHERE status = 'completed'
        GROUP BY customer_name, region
        ORDER BY total_spent DESC
        LIMIT :limit
    """)
    with get_engine().connect() as conn:
        return pd.read_sql(query, conn, params={"limit": limit})

if __name__ == "__main__":
    print("Total Revenue:      $", get_total_revenue())
    print("Total Orders:       ", get_total_orders())
    print("Avg Order Value:    $", get_average_order_value())
    print("\nRevenue by Month:")
    print(get_revenue_by_month())
    print("\nRevenue by Region:")
    print(get_revenue_by_region())
    print("\nTop 10 Products:")
    print(get_top_products())
    print("\nRevenue by Category:")
    print(get_revenue_by_category())
    print("\nOrder Status Breakdown:")
    print(get_order_status_breakdown())
    print("\nTop 10 Customers:")
    print(get_top_customers())