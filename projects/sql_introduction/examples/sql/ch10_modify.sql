-- 10 章 データの追加・更新・削除
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/ch10_modify.sql

INSERT INTO customers (customer_id, name, prefecture, email, registered_on)
VALUES (9, '小林真由', '神奈川県', 'mayu@example.com', '2025-03-01');

SELECT * FROM customers WHERE customer_id = 9;

INSERT INTO products (name, category_id, price)
VALUES ('ほうじ茶', 7, 450);

SELECT * FROM products WHERE name = 'ほうじ茶';

INSERT INTO categories (category_id, name, parent_id)
VALUES (9, 'ジュース', 2),
       (10, '紅茶', 2);

INSERT INTO orders (order_id, customer_id, ordered_on, status)
VALUES (13, 5, '2025-07-01', '受付済');

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
SELECT 13, oi.product_id, oi.quantity, p.price
FROM order_items AS oi
INNER JOIN products AS p ON oi.product_id = p.product_id
WHERE oi.order_id = 12;

SELECT * FROM order_items WHERE order_id IN (12, 13);

INSERT INTO products (name, category_id, price, stock)
VALUES ('玄米茶', 7, 400, 30)
RETURNING product_id, name;

UPDATE orders
SET status = '発送済'
WHERE order_id = 10;

SELECT * FROM orders WHERE order_id = 10;

UPDATE products
SET price = price + 30,
    stock = stock + 10
WHERE category_id = 8;

SELECT product_id, name, price, stock FROM products WHERE category_id = 8;

UPDATE products
SET price = price * 90 / 100
WHERE product_id NOT IN (SELECT product_id FROM order_items);

SELECT product_id, name, price FROM products WHERE product_id >= 12;

DELETE FROM order_items
WHERE order_id = 13 AND product_id = 4;

SELECT * FROM order_items WHERE order_id = 13;

-- 次の文はエラーになります。
DELETE FROM customers WHERE customer_id = 1;

DELETE FROM customers WHERE customer_id = 8;

INSERT INTO products (product_id, name, category_id, price, stock)
VALUES (12, '抹茶ラテ', 7, 315, 10)
ON CONFLICT (product_id) DO UPDATE SET stock = stock + excluded.stock;

SELECT product_id, name, price, stock FROM products WHERE product_id = 12;
