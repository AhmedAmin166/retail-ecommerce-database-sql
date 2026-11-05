-- ==============================================================================
-- Portfolio Project: Retail & E-Commerce Business Analytical Queries
-- Author: Ahmed Fikry
-- Techniques Used: CTEs, Window Functions (DENSE_RANK, LAG, SUM OVER), 
--                  Aggregate Metrics, CASE Expressions, Cohort/RFM Concepts
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: EXECUTIVE FINANCIAL KPI DASHBOARD
-- High-level overview: Gross Revenue, Total Discounts, Net Revenue, Refunds,
-- Cost of Goods Sold (COGS), Gross Profit, and Net Profit Margin %.
-- ------------------------------------------------------------------------------
WITH SalesMetrics AS (
    SELECT 
        SUM(oi.quantity * oi.unit_price) AS gross_revenue,
        SUM(oi.quantity * oi.unit_price * (oi.discount_pct / 100.0)) AS total_discounts,
        SUM(oi.quantity * oi.unit_price * (1.0 - (oi.discount_pct / 100.0))) AS net_revenue,
        SUM(oi.quantity * p.cost_price) AS total_cogs
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status NOT IN ('Cancelled')
),
RefundMetrics AS (
    SELECT 
        COALESCE(SUM(refund_amount), 0.00) AS total_refunds
    FROM returns
    WHERE return_status IN ('Refunded', 'Approved')
)
SELECT 
    ROUND(sm.gross_revenue, 2) AS gross_revenue_egp,
    ROUND(sm.total_discounts, 2) AS total_discounts_egp,
    ROUND(sm.net_revenue, 2) AS net_revenue_egp,
    ROUND(rm.total_refunds, 2) AS total_refunds_egp,
    ROUND(sm.net_revenue - rm.total_refunds, 2) AS final_realized_revenue_egp,
    ROUND(sm.total_cogs, 2) AS cogs_egp,
    ROUND((sm.net_revenue - rm.total_refunds) - sm.total_cogs, 2) AS gross_profit_egp,
    ROUND((((sm.net_revenue - rm.total_refunds) - sm.total_cogs) / (sm.net_revenue - rm.total_refunds)) * 100.0, 2) AS profit_margin_pct
FROM SalesMetrics sm
CROSS JOIN RefundMetrics rm;


-- ------------------------------------------------------------------------------
-- QUERY 2: PRODUCT PERFORMANCE, PROFITABILITY & RETURN RATE ANALYSIS
-- Identifies top profit drivers vs products with high return rates needing QA.
-- Techniques: CTE, LEFT JOIN, DENSE_RANK() Window Function, CASE expressions
-- ------------------------------------------------------------------------------
WITH ProductSales AS (
    SELECT 
        p.product_id,
        p.product_name,
        c.category_name,
        p.unit_price,
        p.cost_price,
        SUM(oi.quantity) AS units_sold,
        SUM(oi.quantity * oi.unit_price * (1.0 - (oi.discount_pct / 100.0))) AS net_sales,
        SUM(oi.quantity * p.cost_price) AS total_cost
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status <> 'Cancelled'
    GROUP BY p.product_id, p.product_name, c.category_name, p.unit_price, p.cost_price
),
ProductReturns AS (
    SELECT 
        oi.product_id,
        COUNT(r.return_id) AS total_returns_count,
        COALESCE(SUM(r.refund_amount), 0.00) AS total_refunded
    FROM order_items oi
    JOIN returns r ON oi.order_item_id = r.order_item_id
    WHERE r.return_status IN ('Refunded', 'Approved')
    GROUP BY oi.product_id
)
SELECT 
    ps.product_name,
    ps.category_name,
    ps.units_sold,
    ROUND(ps.net_sales, 2) AS net_sales_egp,
    COALESCE(pr.total_returns_count, 0) AS units_returned,
    ROUND(COALESCE((pr.total_returns_count * 100.0) / ps.units_sold, 0.0), 1) AS return_rate_pct,
    ROUND(ps.net_sales - COALESCE(pr.total_refunded, 0) - ps.total_cost, 2) AS net_profit_egp,
    DENSE_RANK() OVER (ORDER BY (ps.net_sales - COALESCE(pr.total_refunded, 0) - ps.total_cost) DESC) AS profitability_rank
FROM ProductSales ps
LEFT JOIN ProductReturns pr ON ps.product_id = pr.product_id
ORDER BY profitability_rank;


-- ------------------------------------------------------------------------------
-- QUERY 3: MONTHLY REVENUE RUNNING TOTAL & MOM GROWTH
-- Tracks business velocity month-over-month.
-- Techniques: DATE formatting, Window Functions (SUM() OVER, LAG())
-- ------------------------------------------------------------------------------
WITH MonthlySales AS (
    SELECT 
        SUBSTR(o.order_date, 1, 7) AS sales_month,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.quantity * oi.unit_price * (1.0 - (oi.discount_pct / 100.0))) AS monthly_net_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status <> 'Cancelled'
    GROUP BY SUBSTR(o.order_date, 1, 7)
)
SELECT 
    sales_month,
    total_orders,
    ROUND(monthly_net_revenue, 2) AS current_month_revenue,
    ROUND(LAG(monthly_net_revenue, 1) OVER (ORDER BY sales_month), 2) AS previous_month_revenue,
    ROUND(
        ((monthly_net_revenue - LAG(monthly_net_revenue, 1) OVER (ORDER BY sales_month)) 
        / LAG(monthly_net_revenue, 1) OVER (ORDER BY sales_month)) * 100.0, 
    2) AS mom_growth_rate_pct,
    ROUND(SUM(monthly_net_revenue) OVER (ORDER BY sales_month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS cumulative_running_revenue
FROM MonthlySales
ORDER BY sales_month;


-- ------------------------------------------------------------------------------
-- QUERY 4: RFM CUSTOMER VALUE SEGMENTATION
-- Recency (Days since last order), Frequency (Order count), Monetary (Total spend).
-- Categorizes customers into: VIP, Loyal, High-Potential, at-Risk.
-- ------------------------------------------------------------------------------
WITH CustomerAggregates AS (
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        c.city,
        COUNT(DISTINCT o.order_id) AS order_frequency,
        MAX(o.order_date) AS last_order_date,
        SUM(oi.quantity * oi.unit_price * (1.0 - (oi.discount_pct / 100.0))) AS monetary_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status <> 'Cancelled'
    GROUP BY c.customer_id, c.first_name, c.last_name, c.city
)
SELECT 
    customer_id,
    customer_name,
    city,
    order_frequency,
    ROUND(monetary_value, 2) AS total_spent_egp,
    last_order_date,
    CASE 
        WHEN monetary_value >= 5000 AND order_frequency >= 3 THEN 'VIP Platinum Customer'
        WHEN monetary_value >= 3000 OR order_frequency >= 2 THEN 'Loyal Repeat Customer'
        WHEN monetary_value >= 1500 THEN 'Mid-Tier Value'
        ELSE 'One-Time / Low Value'
    END AS customer_segment
FROM CustomerAggregates
ORDER BY monetary_value DESC;


-- ------------------------------------------------------------------------------
-- QUERY 5: INVENTORY HEALTH & REORDER RESTOCK ALERT
-- Identifies products near depletion and calculates replenishment cost.
-- ------------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    i.stock_quantity,
    i.reorder_level,
    (i.reorder_level - i.stock_quantity) AS stock_deficit,
    ROUND((i.reorder_level - i.stock_quantity) * p.cost_price, 2) AS estimated_restock_cost_egp,
    CASE 
        WHEN i.stock_quantity = 0 THEN 'CRITICAL: OUT OF STOCK'
        WHEN i.stock_quantity <= (i.reorder_level / 2) THEN 'URGENT: HIGH STOCKOUT RISK'
        WHEN i.stock_quantity <= i.reorder_level THEN 'WARNING: REORDER NEEDED'
        ELSE 'HEALTHY STOCK'
    END AS inventory_status
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
WHERE i.stock_quantity <= i.reorder_level
ORDER BY i.stock_quantity ASC;
