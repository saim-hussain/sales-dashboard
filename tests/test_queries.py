import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.queries import (
    get_total_revenue,
    get_total_orders,
    get_average_order_value,
    get_revenue_by_month,
    get_revenue_by_region,
    get_top_products
)

def test_total_revenue_is_positve():
    revenue = get_total_revenue()
    assert revenue > 0, "Total revenue should be posituve"

def test_total_orders_is_positive():
    orders = get_total_orders()
    assert orders > 0, "Total orders should be positive"

def test_average_order_value_is_positive():
    avg = get_average_order_value()
    assert avg > 0, "Average order value should be positive"

def test_revenue_by_month_has_data():
    df = get_revenue_by_month()
    assert len(df) > 0, "Should have monthly revenue data"
    assert "month" in df.columns
    assert "revenue" in df.columns

def test_revenue_by_region_has_all_regions():
    df = get_revenue_by_region()
    assert len(df) == 5, "Should have 5 regions"

def test_top_products_returns_correct_limit():
    df = get_top_products(limit=5)
    assert len(df) == 5, "Should return exactly 5 products"

def test_top_products_has_required_columns():
    df = get_top_products()
    assert "product_name" in df.columns
    assert "revenue" in df.columns
    assert "units_sold" in df.columns