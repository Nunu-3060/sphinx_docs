-- 13 章 インデックスと性能 演習問題の解答
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/answers_ch13.sql

EXPLAIN QUERY PLAN
SELECT * FROM order_items WHERE product_id = 1;

CREATE INDEX idx_order_items_product_id ON order_items (product_id);

EXPLAIN QUERY PLAN
SELECT * FROM order_items WHERE product_id = 1;

CREATE INDEX idx_customers_pref_registered
ON customers (prefecture, registered_on);

EXPLAIN QUERY PLAN
SELECT name FROM customers
WHERE prefecture = '東京都' AND registered_on >= '2024-06-01';

CREATE INDEX idx_products_price ON products (price);

EXPLAIN QUERY PLAN
SELECT name, price FROM products WHERE price * 1.1 >= 550;

EXPLAIN QUERY PLAN
SELECT name, price FROM products WHERE price >= 500;
