-- 13 章 インデックスと性能
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/ch13_index.sql

EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 1;

CREATE INDEX idx_orders_customer_id ON orders (customer_id);

EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE customer_id = 1;

SELECT name, tbl_name
FROM sqlite_schema
WHERE type = 'index'
ORDER BY tbl_name, name;

EXPLAIN QUERY PLAN
SELECT * FROM products WHERE product_id = 3;

EXPLAIN QUERY PLAN
SELECT c.name, o.order_id, o.ordered_on
FROM customers AS c
INNER JOIN orders AS o ON c.customer_id = o.customer_id
WHERE c.customer_id = 1;

CREATE INDEX idx_orders_customer_date ON orders (customer_id, ordered_on);

EXPLAIN QUERY PLAN
SELECT * FROM orders
WHERE customer_id = 1 AND ordered_on >= '2025-02-01';

EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE ordered_on = '2025-03-05';

CREATE INDEX idx_orders_ordered_on ON orders (ordered_on);

-- 列に関数を適用した条件
EXPLAIN QUERY PLAN
SELECT * FROM orders WHERE substr(ordered_on, 1, 7) = '2025-03';

-- 列をそのまま比較する条件
EXPLAIN QUERY PLAN
SELECT * FROM orders
WHERE ordered_on >= '2025-03-01' AND ordered_on < '2025-04-01';

EXPLAIN QUERY PLAN
SELECT customer_id, ordered_on FROM orders WHERE customer_id = 1;
