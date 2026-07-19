import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sqlalchemy import text
from db.connection import get_engine
from etl.generate_data import (
    generate_customers, generate_orders,
    generate_order_items, REGIONS, CATEGORIES, PRODUCTS
)

def load_all():
    engine = get_engine()
    
    with engine.begin() as conn:
        print("loading regions...")
        for region in REGIONS:
            conn.execute(text(
                "INSERT INTO regions (name) VALUES (:name) ON CONFLICT DO NOTHING"
            ), {"name": region})
        
        print("loading categories...")
        for category in CATEGORIES:
            conn.execute(text(
                "INSERT INTO categories (name) VALUES (:name) ON CONFLICT DO NOTHING"
            ), {"name": category})
            
        print("Loading products...")
        for name, category, price in PRODUCTS:
            conn.execute(text(
                """ INSERT INTO products (name, category_id, unit_price)
                VALUES (
                    :name,
                    (SELECT id FROM categories WHERE name = :category),
                    :price
                ) ON CONFLICT DO NOTHING
            """), {"name": name, "category": category, "price": price})
            
        print("Loading customers...")
        customers_df = generate_customers()
        customer_ids = []
        for _, row in customers_df.iterrows():
            result = conn.execute(text("""
                INSERT INTO customers (full_name, email, region_id, signup_date)
                VALUES (
                    :full_name,
                    :email,
                    (SELECT id FROM regions WHERE name = :region),
                    :signup_date
                ) RETURNING id
            """), {
                "full_name": row['full_name'],
                "email": row['email'],
                "region": row['region'],
                "signup_date": row['signup_date']
            })
            customer_ids.append(result.fetchone()[0])
        
        print("Loading orders...")
        orders_df = generate_orders()
        order_ids = []
        for _, row in orders_df.iterrows():
            result = conn.execute(text("""
                INSERT INTO orders (customer_id, order_date, status)
                VALUES (:customer_id, :order_date, :status)
                RETURNING id
            """), {
                "customer_id": customer_ids[row['customer_index']],
                "order_date": row['order_date'],
                "status": row['status']
            })
            order_ids.append(result.fetchone()[0])
            
        print("Loading order items...")
        items_df = generate_order_items()
        for _, row in items_df.iterrows():
            conn.execute(text("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount)
                VALUES (
                    :order_id,
                    (SELECT id FROM products WHERE name = :product_name),
                    :quantity,
                    (SELECT unit_price FROM products WHERE name = :product_name),
                    :discount
                )
            """), {
                "order_id": order_ids[row['order_index']],
                "product_name": row['product_name'],
                "quantity": row['quantity'],
                "discount": row['discount']
            })
        print("✅ All data loaded successfully!")

if __name__ == "__main__":
    load_all()