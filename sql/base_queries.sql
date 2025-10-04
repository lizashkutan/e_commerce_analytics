-- Количество клиентов, товаров, заказов
SELECT 
    (SELECT COUNT(*) FROM customers) AS total_customers,
    (SELECT COUNT(*) FROM products) AS total_products,
    (SELECT COUNT(*) FROM orders) AS total_orders;

	
-- ТОП-10 популярных товаров
SELECT p.name, p.brand, p.category, SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.name, p.brand, p.category
ORDER BY total_sold DESC
LIMIT 10;


-- ТОП-10 клиентов по сумме заказов
SELECT c.first_name, c.last_name, c.email, SUM(o.total_price) AS total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 10;


-- Средний чек
SELECT ROUND(AVG(total_price), 2) AS avg_order_value
FROM orders
WHERE order_status IN ('оплачен', 'доставлен');

