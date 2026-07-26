import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.queries import (
    get_total_revenue,
    get_total_orders,
    get_average_order_value,
    get_revenue_by_month,
    get_revenue_by_region,
    get_top_products,
    get_revenue_by_category,
    get_order_status_breakdown,
    get_top_customers
)

app = FastAPI(
    title="Sales Analytics API",
    description="REST API for sales dashboard analytics",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/summary")
def summary():
    return{
        "total_revenue": float(get_total_revenue()),
        "total_orders": int(get_total_orders()),
        "avg_order_value": float(get_average_order_value())
    }

@app.get("/revenue-by-region")
def revenue_by_region():
    df = get_revenue_by_month()
    return df.to_dict(orient="records")

@app.get("revenue-by-region")
def revenue_by_region():
    df = get_revenue_by_region()
    return df.to_dict(orient="records")

@app.get("/top-products")
def top_products(limit: int = 10):
    df = get_top_products(limit=limit)
    return df.to_dict(orient="records")

@app.get("/revenue-by-category")
def revenue_by_category():
    df = get_revenue_by_category()
    return df.to_dict(orient="records")

@app.get("/order-status")
def order_status():
    df = get_order_status_breakdown()
    return df.to_dict(orient="records")

@app.get("/top-customers")
def top_customers(limit: int = 10):
    df = get_top_customers(limit=limit)
    return df.to_dict(orient="records")