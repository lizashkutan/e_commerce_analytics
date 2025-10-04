-- Популярность категорий по месяцам
WITH monthly_category_sales AS (
    SELECT
        to_char(date_trunc('month', o.created_at), 'TMMonth YYYY') AS month_year,
        COALESCE(p.category, 'Unknown') AS category,
        SUM(oi.quantity) AS total_quantity
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY 1, 2
),
ranked_categories AS (
    SELECT
        month_year,
        category,
        total_quantity,
        RANK() OVER (PARTITION BY month_year ORDER BY total_quantity DESC) AS rank
    FROM monthly_category_sales
)
SELECT
    month_year,
    category,
    total_quantity
FROM ranked_categories
WHERE rank = 1
ORDER BY to_date(month_year, 'TMMonth YYYY');

-- Популярность методов оплаты и доставки
SELECT 
    payment_method,
    delivery_method,
    COUNT(*) AS orders_count,
    SUM(total_price) AS total_revenue
FROM orders
WHERE order_status = 'доставлен'
GROUP BY payment_method, delivery_method
ORDER BY total_revenue DESC;


-- Повторные покупки
WITH first_orders AS (
    SELECT customer_id, MIN(created_at) AS first_order_date
    FROM orders
    WHERE order_status = 'доставлен'
    GROUP BY customer_id
),
orders_after_first AS (
    SELECT 
        f.customer_id,
        COUNT(o.order_id) AS repeat_orders
    FROM first_orders f
    LEFT JOIN orders o 
        ON o.customer_id = f.customer_id 
        AND o.created_at > f.first_order_date
        AND o.order_status = 'доставлен'
    GROUP BY f.customer_id
)
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN repeat_orders > 0 THEN 1 ELSE 0 END) AS customers_with_repeat_orders
FROM orders_after_first;


-- Среднее время доставки
SELECT
    ROUND(AVG(EXTRACT(EPOCH FROM (delivered_at - created_at)) / 86400), 2) AS avg_delivery_days
FROM orders
WHERE order_status = 'доставлен';


-- Популярность брендов внутри категорий
WITH brand_sales AS (
    SELECT
        p.category,
        p.brand,
        SUM(oi.quantity) AS total_sold
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'доставлен'
    GROUP BY p.category, p.brand
)
SELECT *
FROM (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_sold DESC) AS rn
    FROM brand_sales
) t
WHERE rn <= 3
ORDER BY category, total_sold DESC;

-- Среднее количество товаров в заказе
SELECT
    ROUND(AVG(items_count)) AS avg_items_per_order
FROM (
    SELECT order_id, SUM(quantity) AS items_count
    FROM order_items
    GROUP BY order_id
) t;


-- Выручка и количество заказов по городам
SELECT
    c.city,
    COUNT(*) AS orders_count,
    SUM(o.total_price) AS total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'доставлен'
GROUP BY c.city
ORDER BY total_revenue DESC;


-- Сводка по статусам заказов
SELECT
    order_status,
    COUNT(*) AS orders_count,
    SUM(total_price) AS total_revenue
FROM orders
GROUP BY order_status
ORDER BY orders_count DESC;

