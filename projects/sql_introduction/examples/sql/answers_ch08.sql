-- 8 章 サブクエリと共通テーブル式 演習問題の解答
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/answers_ch08.sql

SELECT name, price
FROM products
WHERE price = (SELECT MAX(price) FROM products);

SELECT c.name
FROM customers AS c
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id AND o.status = 'キャンセル'
);

SELECT p.name,
       p.price,
       (SELECT MAX(p2.price)
        FROM products AS p2
        WHERE p2.category_id = p.category_id) AS max_price_in_category
FROM products AS p
WHERE p.category_id IS NOT NULL
ORDER BY p.category_id, p.price DESC;

WITH order_amounts AS (
    SELECT o.order_id,
           SUM(oi.quantity * oi.unit_price) AS amount
    FROM orders AS o
    INNER JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'キャンセル'
    GROUP BY o.order_id
)
SELECT COUNT(*) AS order_count
FROM order_amounts
WHERE amount >= 1000;

WITH RECURSIVE sub_categories (category_id, name) AS (
    SELECT category_id, name
    FROM categories
    WHERE category_id = 1
    UNION ALL
    SELECT c.category_id, c.name
    FROM categories AS c
    INNER JOIN sub_categories AS s ON c.parent_id = s.category_id
)
SELECT category_id, name
FROM sub_categories
ORDER BY category_id;
