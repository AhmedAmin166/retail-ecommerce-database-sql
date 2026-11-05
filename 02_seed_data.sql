-- ==============================================================================
-- Portfolio Project: Retail & E-Commerce Mock Seed Data
-- Author: Ahmed Fikry
-- Description: Realistic seed data populating customers, categories, products,
--              inventory, orders, order items, and return records.
-- ==============================================================================

-- 1. SEED CATEGORIES
INSERT INTO categories (category_id, category_name, description) VALUES
(1, 'Consumer Electronics', 'Smartphones, laptops, audio accessories, and tech gadgets'),
(2, 'Apparel & Fashion', 'Men, women, and kids clothing, footwear, and accessories'),
(3, 'Home & Kitchen', 'Home appliances, cookware, decorative lighting, and furniture'),
(4, 'Sports & Fitness', 'Fitness gear, gym equipment, sportswear, and nutrition supplements');

-- 2. SEED CUSTOMERS
INSERT INTO customers (customer_id, first_name, last_name, email, phone, city, state, country, created_at) VALUES
(1, 'Ahmed', 'Hassan', 'ahmed.hassan@example.com', '+201012345671', 'Cairo', 'Cairo', 'Egypt', '2026-01-10 09:30:00'),
(2, 'Sara', 'Ibrahim', 'sara.ibrahim@example.com', '+201012345672', 'Alexandria', 'Alexandria', 'Egypt', '2026-01-15 11:20:00'),
(3, 'Mohamed', 'Ali', 'mohamed.ali@example.com', '+201012345673', 'Giza', 'Giza', 'Egypt', '2026-01-20 14:15:00'),
(4, 'Nour', 'El-Din', 'nour.eldin@example.com', '+201012345674', 'Cairo', 'Cairo', 'Egypt', '2026-02-01 16:45:00'),
(5, 'Mariam', 'Fathy', 'mariam.fathy@example.com', '+201012345675', 'Mansoura', 'Dakahlia', 'Egypt', '2026-02-08 10:10:00'),
(6, 'Omar', 'Khaled', 'omar.khaled@example.com', '+201012345676', 'Alexandria', 'Alexandria', 'Egypt', '2026-02-14 13:50:00'),
(7, 'Youssef', 'Tariq', 'youssef.tariq@example.com', '+201012345677', 'Tanta', 'Gharbia', 'Egypt', '2026-03-01 08:25:00'),
(8, 'Layla', 'Mahmoud', 'layla.mahmoud@example.com', '+201012345678', 'Cairo', 'Cairo', 'Egypt', '2026-03-10 17:00:00'),
(9, 'Karim', 'Saeed', 'karim.saeed@example.com', '+201012345679', 'Giza', 'Giza', 'Egypt', '2026-03-18 12:40:00'),
(10, 'Hoda', 'Mostafa', 'hoda.mostafa@example.com', '+201012345680', 'Ismailia', 'Ismailia', 'Egypt', '2026-03-25 15:30:00');

-- 3. SEED PRODUCTS
INSERT INTO products (product_id, category_id, product_name, sku, cost_price, unit_price, status, created_at) VALUES
(1, 1, 'Pro Wireless Noise-Cancelling Headphones', 'TECH-HEAD-001', 1200.00, 1850.00, 'active', '2026-01-01 00:00:00'),
(2, 1, 'Ultra HD 4K Smart Monitor 27-inch', 'TECH-MON-002', 4500.00, 6400.00, 'active', '2026-01-01 00:00:00'),
(3, 1, 'Ergonomic Mechanical Keyboard', 'TECH-KEY-003', 850.00, 1350.00, 'active', '2026-01-01 00:00:00'),
(4, 2, 'Classic Cotton Oxford Shirt', 'APP-SHIRT-101', 320.00, 599.00, 'active', '2026-01-05 00:00:00'),
(5, 2, 'Slim-Fit Stretch Denim Jeans', 'APP-JEAN-102', 450.00, 850.00, 'active', '2026-01-05 00:00:00'),
(6, 2, 'Breathable Running Athletic Shoes', 'APP-SHOE-103', 750.00, 1450.00, 'active', '2026-01-05 00:00:00'),
(7, 3, 'Espresso & Cappuccino Coffee Maker', 'HOME-COFF-201', 2200.00, 3600.00, 'active', '2026-01-10 00:00:00'),
(8, 3, 'Cast Iron Dutch Oven 5-Quart', 'HOME-COOK-202', 900.00, 1550.00, 'active', '2026-01-10 00:00:00'),
(9, 4, 'Adjustable Dumbbell Set (20kg)', 'SPORT-DUMB-301', 1100.00, 1890.00, 'active', '2026-01-12 00:00:00'),
(10, 4, 'Smart Fitness Tracker & Heart Monitor', 'SPORT-BAND-302', 650.00, 1150.00, 'active', '2026-01-12 00:00:00');

-- 4. SEED INVENTORY
INSERT INTO inventory (inventory_id, product_id, stock_quantity, reorder_level, last_restock_date) VALUES
(1, 1, 45, 15, '2026-04-01'),
(2, 2, 18, 10, '2026-03-20'),
(3, 3, 60, 20, '2026-04-10'),
(4, 4, 120, 30, '2026-04-15'),
(5, 5, 85, 25, '2026-04-12'),
(6, 6, 32, 15, '2026-04-05'),
(7, 7, 8, 10, '2026-03-15'),  -- Below reorder level!
(8, 8, 22, 12, '2026-03-28'),
(9, 9, 14, 10, '2026-04-02'),
(10, 10, 5, 15, '2026-03-10'); -- Below reorder level!

-- 5. SEED ORDERS
INSERT INTO orders (order_id, customer_id, order_date, order_status, shipping_cost, payment_method) VALUES
(101, 1, '2026-01-25 10:15:00', 'Delivered', 50.00, 'Credit Card'),
(102, 2, '2026-02-03 14:30:00', 'Delivered', 0.00, 'Credit Card'),
(103, 3, '2026-02-12 18:20:00', 'Delivered', 60.00, 'Cash on Delivery'),
(104, 1, '2026-02-28 11:05:00', 'Delivered', 50.00, 'Credit Card'),
(105, 4, '2026-03-05 09:45:00', 'Delivered', 0.00, 'Digital Wallet'),
(106, 5, '2026-03-12 16:10:00', 'Delivered', 75.00, 'Cash on Delivery'),
(107, 6, '2026-03-22 13:00:00', 'Delivered', 50.00, 'Digital Wallet'),
(108, 2, '2026-04-02 15:40:00', 'Delivered', 0.00, 'Credit Card'),
(109, 7, '2026-04-08 17:50:00', 'Shipped', 65.00, 'Cash on Delivery'),
(110, 8, '2026-04-14 12:25:00', 'Delivered', 50.00, 'Credit Card'),
(111, 9, '2026-04-18 19:15:00', 'Processing', 50.00, 'Credit Card'),
(112, 3, '2026-04-22 10:30:00', 'Delivered', 60.00, 'Cash on Delivery'),
(113, 10, '2026-04-26 14:00:00', 'Delivered', 70.00, 'Bank Transfer'),
(114, 1, '2026-04-28 16:45:00', 'Delivered', 0.00, 'Credit Card'),
(115, 5, '2026-05-01 11:20:00', 'Pending', 75.00, 'Cash on Delivery');

-- 6. SEED ORDER ITEMS
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price, discount_pct) VALUES
(1, 101, 1, 1, 1850.00, 0.00),
(2, 101, 3, 1, 1350.00, 10.00),
(3, 102, 2, 1, 6400.00, 5.00),
(4, 103, 4, 2, 599.00, 0.00),
(5, 103, 5, 1, 850.00, 0.00),
(6, 104, 7, 1, 3600.00, 10.00),
(7, 105, 6, 1, 1450.00, 0.00),
(8, 105, 10, 1, 1150.00, 15.00),
(9, 106, 8, 1, 1550.00, 0.00),
(10, 107, 9, 2, 1890.00, 5.00),
(11, 108, 1, 2, 1850.00, 10.00),
(12, 108, 3, 1, 1350.00, 0.00),
(13, 109, 5, 2, 850.00, 0.00),
(14, 110, 7, 1, 3600.00, 0.00),
(15, 110, 8, 1, 1550.00, 5.00),
(16, 111, 2, 1, 6400.00, 8.00),
(17, 112, 6, 1, 1450.00, 0.00),
(18, 113, 10, 2, 1150.00, 10.00),
(19, 114, 4, 3, 599.00, 15.00),
(20, 114, 9, 1, 1890.00, 0.00),
(21, 115, 1, 1, 1850.00, 0.00);

-- 7. SEED RETURNS
INSERT INTO returns (return_id, order_item_id, return_date, return_reason, refund_amount, return_status) VALUES
(1, 4, '2026-02-16 11:30:00', 'Size Mismatch', 599.00, 'Refunded'),
(2, 7, '2026-03-09 14:00:00', 'Defective', 1450.00, 'Refunded'),
(3, 15, '2026-04-20 09:15:00', 'Damaged in Transit', 1472.50, 'Refunded'),
(4, 18, '2026-04-30 16:40:00', 'Changed Mind', 2070.00, 'Approved');
