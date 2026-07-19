import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
Faker.seed(42)

REGIONS =['North', 'South', 'East', 'West', 'Central']
CATEGORIES = ['Electronics', 'Clothing', 'Food', 'Sports', 'Home']

PRODUCTS = [
    ('Laptop Pro', 'Electronics', 999.99),
    ('Wireless Mouse', 'Electronics', 29.99),
    ('Running Shoes', 'Sports', 89.99),
    ('Coffee Maker', 'Home', 49.99),
    ('Python Book', 'Electronics', 39.99),
    ('Yoga Mat', 'Sports', 24.99),
    ('Winter Jacket', 'Clothing', 129.99),
    ('Bluetooth Speaker', 'Electronics', 79.99),
    ('Organic Coffee', 'Food', 14.99),
    ('Smart Watch', 'Electronics', 299.99),
    ('Tennis Racket', 'Sports', 59.99),
    ('Desk Lamp', 'Home', 34.99),
    ('T-Shirt Pack', 'Clothing', 19.99),
    ('Protein Powder', 'Food', 44.99),
    ('Headphones', 'Electronics', 149.99),
]

def generate_customers(n=200):
    customers = []
    for _ in range(n):
        customers.append({
            'full_name': fake.name(),
            'email': fake.unique.email(),
            'region': random.choice(REGIONS),
            'signup_date': fake.date_between(
                start_date=datetime(2022, 1, 1),
                end_date=datetime(2024, 1, 1)
            )
        })
    return pd.DataFrame(customers)
    
def generate_orders(n=500):
    orders = []
    for _ in range(n):
        orders.append({
            'customer_index': random.randint(0, 199),
            'order_date': fake.date_between(
                start_date=datetime(2023, 1, 1),
                end_date=datetime(2024, 12, 31)
            ),
            'status': random.choices(
                ['completed', 'refunded', 'pending'],
                weights=[80, 10, 10]
            )[0]
        })
    return pd.DataFrame(orders)

def generate_order_items(n_orders=500):
    items = []
    for order_index in range(n_orders):
        n_items = random.randint(1, 5)
        chosen = random.sample(PRODUCTS, n_items)
        for product in chosen:
            items.append({
                'order_index': order_index,
                'product_name': product[0],
                'quantity': random.randint(1, 10),
                'discount': round(random.choice([0, 0.05, 0.10, 0.15, 0.20]), 2)
            })
    return pd.DataFrame(items)

if __name__ == "__main__":
    print("Customers:", generate_customers().shape)
    print("Orders:", generate_orders().shape)
    print("Items:", generate_order_items().shape)