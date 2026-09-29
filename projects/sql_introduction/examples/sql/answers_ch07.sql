-- 7 章 テーブルの結合 演習問題の解答
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/answers_ch07.sql

SELECT p.name AS product_name, c.name AS category_name
FROM products AS p
LEFT JOIN categories AS c ON p.category_id = c.category_id
ORDER BY p.product_id;

SELECT p.name,
       oi.quantity,
       oi.unit_price,
       oi.quantity * oi.unit_price AS subtotal
FROM order_items AS oi
INNER JOIN products AS p ON oi.product_id = p.product_id
WHERE oi.order_id = 6
ORDER BY p.product_id;

SELECT c.category_id, c.name, COUNT(p.product_id) AS product_count
FROM categories AS c
LEFT JOIN products AS p ON c.category_id = p.category_id
GROUP BY c.category_id, c.name
ORDER BY c.category_id;

SELECT c.name
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

SELECT DISTINCT p.name
FROM customers AS c
INNER JOIN orders AS o ON c.customer_id = o.customer_id
INNER JOIN order_items AS oi ON o.order_id = oi.order_id
INNER JOIN products AS p ON oi.product_id = p.product_id
WHERE c.prefecture = '東京都' AND o.status <> 'キャンセル'
ORDER BY p.name;
