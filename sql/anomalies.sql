-- Заказы дороже 100k руб.
SELECT order_number, total_price, created_at
FROM orders
WHERE total_price > 100000
ORDER BY total_price DESC;


-- Подозрительные клиенты (слишком много отменённых заказов)
SELECT c.first_name, c.last_name, c.email, COUNT(*) AS cancelled_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'отменен'
GROUP BY c.customer_id
HAVING COUNT(*) > 5
ORDER BY cancelled_orders DESC;


-- Подозрительная активность (слишком много заказов за день)
SELECT 
    customer_id,
    COUNT(*) AS orders_count,
    DATE(created_at) AS order_date
FROM orders
GROUP BY customer_id, DATE(created_at)
HAVING COUNT(*) > 2
ORDER BY orders_count DESC;
