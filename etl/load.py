import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from db.connection import get_engine
from etl.generate_data import load_superstore_data

def load_all():
    df = load_superstore_data()
    engine = get_engine()

    with engine.begin() as conn:

        # ── Regions ──────────────────────────────────────────
        print("Loading regions...")
        regions = df['region'].dropna().unique()
        for region in regions:
            conn.execute(text(
                "INSERT INTO regions (name) VALUES (:name) ON CONFLICT DO NOTHING"
            ), {"name": region})

        # ── Categories ───────────────────────────────────────
        print("Loading categories...")
        categories = df[['category', 'sub-category']].drop_duplicates()
        for _, row in categories.iterrows():
            conn.execute(text("""
                INSERT INTO categories (name, sub_category)
                VALUES (:name, :sub_category)
                ON CONFLICT (name) DO NOTHING
            """), {
                "name": row['category'],
                "sub_category": row['sub-category']
            })

        # ── Customers ────────────────────────────────────────
        print("Loading customers...")
        customers = df[['customer_id', 'customer_name', 
                        'segment', 'region']].drop_duplicates('customer_id')
        for _, row in customers.iterrows():
            conn.execute(text("""
                INSERT INTO customers (customer_id, full_name, segment, region_id)
                VALUES (
                    :customer_id,
                    :full_name,
                    :segment,
                    (SELECT id FROM regions WHERE name = :region)
                ) ON CONFLICT (customer_id) DO NOTHING
            """), {
                "customer_id": row['customer_id'],
                "full_name": row['customer_name'],
                "segment": row['segment'],
                "region": row['region']
            })

        # ── Products ─────────────────────────────────────────
        print("Loading products...")
        products = df[['product_id', 'product_name', 
                       'category', 'sales', 'quantity']].copy()
        products['unit_price'] = (products['sales'] / 
                                   products['quantity']).round(2)
        products = products[['product_id', 'product_name', 
                             'category', 'unit_price']].drop_duplicates('product_id')
        
        for _, row in products.iterrows():
            conn.execute(text("""
                INSERT INTO products (product_id, name, category_id, unit_price)
                VALUES (
                    :product_id,
                    :name,
                    (SELECT id FROM categories WHERE name = :category),
                    :unit_price
                ) ON CONFLICT (product_id) DO NOTHING
            """), {
                "product_id": row['product_id'],
                "name": row['product_name'],
                "category": row['category'],
                "unit_price": float(row['unit_price'])
            })

        # ── Orders ───────────────────────────────────────────
        print("Loading orders...")
        orders = df[['order_id', 'customer_id', 'order_date', 
                     'ship_date', 'ship_mode']].drop_duplicates('order_id')
        
        order_id_map = {}
        for _, row in orders.iterrows():
            result = conn.execute(text("""
                INSERT INTO orders (order_id, customer_id, order_date, 
                                   ship_date, ship_mode)
                VALUES (
                    :order_id,
                    (SELECT id FROM customers WHERE customer_id = :customer_id),
                    :order_date,
                    :ship_date,
                    :ship_mode
                ) RETURNING id
            """), {
                "order_id": row['order_id'],
                "customer_id": row['customer_id'],
                "order_date": row['order_date'],
                "ship_date": row['ship_date'],
                "ship_mode": row['ship_mode']
            })
            order_id_map[row['order_id']] = result.fetchone()[0]

        # ── Order Items ──────────────────────────────────────
        print("Loading order items...")
        for _, row in df.iterrows():
            unit_price = round(row['sales'] / row['quantity'], 2)
            conn.execute(text("""
                INSERT INTO order_items (order_id, product_id, quantity,
                                        unit_price, discount, profit)
                VALUES (
                    :order_id,
                    (SELECT id FROM products WHERE product_id = :product_id),
                    :quantity,
                    :unit_price,
                    :discount,
                    :profit
                )
            """), {
                "order_id": order_id_map[row['order_id']],
                "product_id": row['product_id'],
                "quantity": int(row['quantity']),
                "unit_price": float(unit_price),
                "discount": float(row['discount']),
                "profit": float(row['profit'])
            })

    print("✅ All Superstore data loaded successfully!")

if __name__ == "__main__":
    load_all()