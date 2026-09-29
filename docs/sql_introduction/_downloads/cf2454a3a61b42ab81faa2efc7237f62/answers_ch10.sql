-- 10 章 データの追加・更新・削除 演習問題の解答
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/answers_ch10.sql

INSERT INTO customers (customer_id, name, prefecture, email, registered_on)
VALUES (9, '木村蓮', '京都府', NULL, '2025-04-10');

SELECT * FROM customers;

UPDATE products
SET price = price * 110 / 100
WHERE category_id = 3;

SELECT product_id, name, price FROM products WHERE category_id = 3;

DELETE FROM order_items
WHERE order_id IN (SELECT order_id FROM orders WHERE status = 'キャンセル');

DELETE FROM orders
WHERE status = 'キャンセル';

SELECT COUNT(*) AS cancelled_count FROM orders WHERE status = 'キャンセル';

INSERT INTO products (product_id, name, category_id, price, stock)
VALUES (5, '味噌', 5, 500, 20)
ON CONFLICT (product_id) DO UPDATE SET stock = stock + excluded.stock;

SELECT product_id, name, stock FROM products WHERE product_id = 5;
