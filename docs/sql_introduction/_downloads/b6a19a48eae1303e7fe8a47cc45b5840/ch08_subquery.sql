-- 8 章 サブクエリと共通テーブル式
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/ch08_subquery.sql

SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC;

SELECT name,
       price,
       price - (SELECT AVG(price) FROM products) AS diff_from_avg
FROM products
WHERE category_id = 8;

SELECT customer_id, name
FROM customers
WHERE customer_id IN (
    SELECT o.customer_id
    FROM orders AS o
    INNER JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE oi.product_id = 6
);

SELECT c.customer_id, c.name
FROM customers AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id
);

SELECT product_id, name
FROM products
WHERE product_id NOT IN (SELECT product_id FROM order_items);

SELECT category_id, name
FROM categories
WHERE category_id NOT IN (SELECT category_id FROM products);

SELECT c.category_id, c.name
FROM categories AS c
WHERE NOT EXISTS (
    SELECT 1 FROM products AS p WHERE p.category_id = c.category_id
);

SELECT p.name, p.category_id, p.price
FROM products AS p
WHERE p.price > (
    SELECT AVG(p2.price)
    FROM products AS p2
    WHERE p2.category_id = p.category_id
)
ORDER BY p.category_id;

SELECT COUNT(*) AS customer_count,
       AVG(total_amount) AS avg_amount
FROM (
    SELECT o.customer_id,
           SUM(oi.quantity * oi.unit_price) AS total_amount
    FROM orders AS o
    INNER JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'キャンセル'
    GROUP BY o.customer_id
) AS customer_totals;

WITH customer_totals AS (
    SELECT o.customer_id,
           SUM(oi.quantity * oi.unit_price) AS total_amount
    FROM orders AS o
    INNER JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'キャンセル'
    GROUP BY o.customer_id
)
SELECT COUNT(*) AS customer_count,
       AVG(total_amount) AS avg_amount
FROM customer_totals;

WITH customer_totals AS (
    SELECT o.customer_id,
           SUM(oi.quantity * oi.unit_price) AS total_amount
    FROM orders AS o
    INNER JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'キャンセル'
    GROUP BY o.customer_id
),
average AS (
    SELECT AVG(total_amount) AS avg_amount FROM customer_totals
)
SELECT c.name, t.total_amount
FROM customer_totals AS t
INNER JOIN customers AS c ON t.customer_id = c.customer_id
CROSS JOIN average AS a
WHERE t.total_amount >= a.avg_amount
ORDER BY t.total_amount DESC;

WITH RECURSIVE numbers (n) AS (
    SELECT 1                              -- 初期部分
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 5 -- 再帰部分
)
SELECT n FROM numbers;

WITH RECURSIVE category_path (category_id, name, path, depth) AS (
    -- 初期部分：最上位のカテゴリ
    SELECT category_id, name, name, 1
    FROM categories
    WHERE parent_id IS NULL
    UNION ALL
    -- 再帰部分：1 つ上の段階で得られたカテゴリの子カテゴリ
    SELECT c.category_id, c.name, cp.path || ' > ' || c.name, cp.depth + 1
    FROM categories AS c
    INNER JOIN category_path AS cp ON c.parent_id = cp.category_id
)
SELECT category_id, path, depth
FROM category_path
ORDER BY path;
