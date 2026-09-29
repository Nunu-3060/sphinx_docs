-- 12 章 トランザクション 演習問題の解答
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/answers_ch12.sql

SELECT SUM(stock) AS total_stock FROM products;

BEGIN;
UPDATE products SET stock = 0;

SELECT SUM(stock) AS total_stock FROM products;

ROLLBACK;

SELECT SUM(stock) AS total_stock FROM products;

BEGIN;
INSERT INTO orders (order_id, customer_id, ordered_on, status)
VALUES (13, 8, '2025-07-05', '受付済');
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (13, 10, 3, 180);
UPDATE products SET stock = stock - 3 WHERE product_id = 10;
COMMIT;

SELECT * FROM order_items WHERE order_id = 13;

SELECT product_id, name, stock FROM products WHERE product_id = 10;
