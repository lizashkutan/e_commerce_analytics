-- Самые популярные товары в каждой категории
WITH sales_per_product AS (
    SELECT 
        p.category,
        p.name,
        p.brand,
        SUM(oi.quantity) AS total_sold
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status IN ('оплачен', 'доставлен')
    GROUP BY p.category, p.name, p.brand
)
SELECT *
FROM (
    SELECT 
        category,
        name,
        brand,
        total_sold,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_sold DESC) AS rn
    FROM sales_per_product
) t
WHERE rn <= 3
ORDER BY category, total_sold DESC;


-- Самые дорогие товары в каждой категории
WITH product_prices AS (
    SELECT
        category,
        name,
        brand,
        price
    FROM products
)
SELECT *
FROM (
    SELECT
        category,
        name,
        brand,
        price,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC) AS rn
    FROM product_prices
) t
WHERE rn <= 3
ORDER BY category, price DESC;
