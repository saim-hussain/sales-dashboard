DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS regions CASCADE;

CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    sub_category VARCHAR(100)
);

CREATE TABLE customers(
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(200) NOT NULL,
    segment VARCHAR(50),
    region_id INT REFERENCES regions(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE products(
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(300) NOT NULL,
    category_id INT REFERENCES categories(id),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders(
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    customer_id INT NOT NULL REFERENCES customers(id),
    order_date DATE NOT NULL,
    ship_date DATE,
    ship_mode VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items(
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id),
    product_id INT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL,
    discount NUMERIC(3,2) NOT NULL DEFAULT 0
    CHECK (discount BETWEEN 0 AND 1),
    profit NUMERIC(10,2)
);
CREATE OR REPLACE VIEW vw_order_summary AS
SELECT
o.id AS order_id,
o.order_id AS order_reference,
o.order_date,
o.ship_mode,
c.full_name AS customer_name,
c.segment,
r.name AS region,
p.name AS product_name,
cat.name AS category,
cat.sub_category,
oi.quantity,
oi.unit_price,
oi.discount,
oi.profit,
ROUND((oi.quantity * oi.unit_price * (1 - oi.discount))::numeric, 2) AS order_total
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN regions r ON c.region_id = r.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
JOIN categories cat ON p.category_id = cat.id;