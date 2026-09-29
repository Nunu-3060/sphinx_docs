-- 6 章 集計とグループ化
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/ch06_aggregate.sql

SELECT COUNT(*) AS product_count,
       SUM(stock) AS total_stock,
       AVG(price) AS avg_price,
       MIN(price) AS min_price,
       MAX(price) AS max_price
FROM products;

SELECT COUNT(*) AS order_count
FROM orders
WHERE status = '発送済';

SELECT COUNT(*) AS customer_count,
       COUNT(email) AS email_count
FROM customers;

SELECT COUNT(*) AS cnt, SUM(price) AS total
FROM products
WHERE price > 10000;

SELECT COUNT(*) AS order_count,
       COUNT(DISTINCT customer_id) AS customer_count
FROM orders;

SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status;

SELECT order_id,
       COUNT(*) AS item_count,
       SUM(quantity * unit_price) AS amount
FROM order_items
GROUP BY order_id;

SELECT strftime('%Y-%m', ordered_on) AS month,
       status,
       COUNT(*) AS order_count
FROM orders
GROUP BY month, status
ORDER BY month, status;

SELECT category_id, COUNT(*) AS product_count
FROM products
GROUP BY category_id;

SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 2;

SELECT customer_id, COUNT(*) AS order_count
FROM orders
WHERE status = '発送済'
GROUP BY customer_id
HAVING COUNT(*) >= 2;
