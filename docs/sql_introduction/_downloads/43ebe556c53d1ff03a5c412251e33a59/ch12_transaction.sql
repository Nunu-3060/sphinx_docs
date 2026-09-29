-- 12 章 トランザクション
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/ch12_transaction.sql

SELECT product_id, name, stock FROM products WHERE product_id = 1;

BEGIN;
INSERT INTO orders (order_id, customer_id, ordered_on, status)
VALUES (13, 2, '2025-07-01', '受付済');
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (13, 1, 5, 200);
UPDATE products SET stock = stock - 5 WHERE product_id = 1;

SELECT product_id, name, stock FROM products WHERE product_id = 1;

ROLLBACK;

SELECT product_id, name, stock FROM products WHERE product_id = 1;

SELECT * FROM orders WHERE order_id = 13;

BEGIN;
INSERT INTO orders (order_id, customer_id, ordered_on, status)
VALUES (13, 2, '2025-07-01', '受付済');
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (13, 1, 5, 200);
UPDATE products SET stock = stock - 5 WHERE product_id = 1;
COMMIT;

SELECT product_id, name, stock FROM products WHERE product_id = 1;

BEGIN;
INSERT INTO orders (order_id, customer_id, ordered_on, status)
VALUES (14, 3, '2025-07-02', '受付済');

-- 次の文はエラーになります。
-- 存在しない商品（product_id が 99）の明細
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (14, 99, 1, 100);

ROLLBACK;

SELECT * FROM orders WHERE order_id = 14;

BEGIN;
UPDATE products SET stock = stock + 100 WHERE product_id = 2;
SAVEPOINT before_update_3;
UPDATE products SET stock = stock + 100 WHERE product_id = 3;
ROLLBACK TO before_update_3;
COMMIT;

SELECT product_id, name, stock FROM products WHERE product_id IN (2, 3);
