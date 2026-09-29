-- 7 章 テーブルの結合
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/ch07_join.sql

SELECT orders.order_id,
       orders.ordered_on,
       customers.name
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;

SELECT o.order_id, o.ordered_on, c.name
FROM orders AS o
INNER JOIN customers AS c ON o.customer_id = c.customer_id
WHERE c.prefecture = '東京都'
ORDER BY o.ordered_on;

SELECT o.order_id,
       o.ordered_on,
       p.name AS product_name,
       oi.quantity,
       oi.unit_price
FROM order_items AS oi
INNER JOIN orders AS o ON oi.order_id = o.order_id
INNER JOIN products AS p ON oi.product_id = p.product_id
WHERE o.order_id <= 3
ORDER BY o.order_id, p.product_id;

SELECT c.name,
       SUM(oi.quantity * oi.unit_price) AS total_amount
FROM customers AS c
INNER JOIN orders AS o ON c.customer_id = o.customer_id
INNER JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'キャンセル'
GROUP BY c.customer_id, c.name
ORDER BY total_amount DESC;

SELECT c.customer_id, c.name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;

SELECT c.name, COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;

SELECT p.product_id, p.name
FROM products AS p
LEFT JOIN order_items AS oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL;

-- 条件を WHERE 句に書いた場合
SELECT c.name, COUNT(o.order_id) AS shipped_count
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.status = '発送済'
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;

-- 条件を ON 句に書いた場合
SELECT c.name, COUNT(o.order_id) AS shipped_count
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id AND o.status = '発送済'
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;

SELECT child.name AS category, parent.name AS parent_category
FROM categories AS child
LEFT JOIN categories AS parent ON child.parent_id = parent.category_id
ORDER BY child.category_id;

SELECT c.name AS category, s.status
FROM categories AS c
CROSS JOIN (SELECT DISTINCT status FROM orders) AS s
WHERE c.parent_id IS NULL
ORDER BY c.category_id, s.status;

-- どちらかの期間に注文した顧客
SELECT customer_id FROM orders
WHERE ordered_on BETWEEN '2025-01-01' AND '2025-02-28'
UNION
SELECT customer_id FROM orders
WHERE ordered_on BETWEEN '2025-05-01' AND '2025-06-30';

-- 両方の期間に注文した顧客
SELECT customer_id FROM orders
WHERE ordered_on BETWEEN '2025-01-01' AND '2025-02-28'
INTERSECT
SELECT customer_id FROM orders
WHERE ordered_on BETWEEN '2025-05-01' AND '2025-06-30';

-- 1 月から 2 月に注文し、5 月から 6 月には注文していない顧客
SELECT customer_id FROM orders
WHERE ordered_on BETWEEN '2025-01-01' AND '2025-02-28'
EXCEPT
SELECT customer_id FROM orders
WHERE ordered_on BETWEEN '2025-05-01' AND '2025-06-30';
