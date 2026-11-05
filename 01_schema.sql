-- ==============================================================================
-- Portfolio Project: Retail & E-Commerce Relational Database Management System
-- Author: Ahmed Fikry
-- Dialect: ANSI SQL / PostgreSQL & SQLite compatible
-- Description: 3NF Relational Database Schema with Constraints, Foreign Keys & Indexes
-- ==============================================================================

-- Drop tables if they exist to allow clean re-runs (ordered by foreign key dependencies)
DROP TABLE IF EXISTS returns;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS customers;

-- 1. CUSTOMERS TABLE
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(25),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50),
    country VARCHAR(50) NOT NULL DEFAULT 'Egypt',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. CATEGORIES TABLE
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- 3. PRODUCTS TABLE
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    product_name VARCHAR(120) NOT NULL,
    sku VARCHAR(30) NOT NULL UNIQUE,
    cost_price DECIMAL(10, 2) NOT NULL CHECK (cost_price >= 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= cost_price),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'discontinued', 'out_of_stock')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (category_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 4. INVENTORY TABLE
CREATE TABLE inventory (
    inventory_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL UNIQUE,
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),
    reorder_level INTEGER NOT NULL DEFAULT 10 CHECK (reorder_level >= 0),
    last_restock_date DATE,
    FOREIGN KEY (product_id) REFERENCES products (product_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- 5. ORDERS TABLE
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    order_status VARCHAR(25) NOT NULL DEFAULT 'Pending' 
        CHECK (order_status IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled')),
    shipping_cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (shipping_cost >= 0),
    payment_method VARCHAR(30) NOT NULL 
        CHECK (payment_method IN ('Credit Card', 'Cash on Delivery', 'Digital Wallet', 'Bank Transfer')),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 6. ORDER ITEMS TABLE (Intersection between Orders and Products)
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    discount_pct DECIMAL(5, 2) NOT NULL DEFAULT 0.00 CHECK (discount_pct >= 0 AND discount_pct <= 100),
    FOREIGN KEY (order_id) REFERENCES orders (order_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (product_id) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 7. RETURNS TABLE
CREATE TABLE returns (
    return_id INTEGER PRIMARY KEY,
    order_item_id INTEGER NOT NULL UNIQUE,
    return_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    return_reason VARCHAR(100) NOT NULL 
        CHECK (return_reason IN ('Defective', 'Wrong Item', 'Size Mismatch', 'Late Delivery', 'Changed Mind', 'Damaged in Transit')),
    refund_amount DECIMAL(10, 2) NOT NULL CHECK (refund_amount >= 0),
    return_status VARCHAR(20) NOT NULL DEFAULT 'Pending' 
        CHECK (return_status IN ('Pending', 'Approved', 'Refunded', 'Rejected')),
    FOREIGN KEY (order_item_id) REFERENCES order_items (order_item_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- ==============================================================================
-- INDEXES FOR QUERY OPTIMIZATION & SEARCH SPEED
-- ==============================================================================
CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_returns_item ON returns(order_item_id);

-- ==============================================================================
-- BUSINESS VIEW: DETAILED ORDER SUMMARY
-- Pre-aggregated view calculating gross sales, discounts, net sales, and returns
-- ==============================================================================
DROP VIEW IF EXISTS view_order_financial_summary;

CREATE VIEW view_order_financial_summary AS
SELECT 
    o.order_id,
    o.order_date,
    o.order_status,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.city,
    COUNT(oi.order_item_id) AS total_items,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_sales_amount,
    ROUND(SUM(oi.quantity * oi.unit_price * (oi.discount_pct / 100.0)), 2) AS total_discount_amount,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - (oi.discount_pct / 100.0))), 2) AS net_sales_amount,
    COALESCE(ROUND(SUM(r.refund_amount), 2), 0.00) AS total_refunded_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN returns r ON oi.order_item_id = r.order_item_id AND r.return_status = 'Refunded'
GROUP BY o.order_id, o.order_date, o.order_status, c.customer_id, c.first_name, c.last_name, c.city;
