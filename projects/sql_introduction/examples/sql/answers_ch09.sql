-- 9 章 ウィンドウ関数 演習問題の解答
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/answers_ch09.sql

SELECT name,
       price,
       round(price * 100.0 / SUM(price) OVER (), 1) AS ratio
FROM products
ORDER BY price DESC;

SELECT ROW_NUMBER() OVER (ORDER BY registered_on, customer_id) AS row_num,
       name,
       registered_on
FROM customers
ORDER BY row_num;

SELECT prefecture,
       ROW_NUMBER() OVER (
           PARTITION BY prefecture ORDER BY registered_on, customer_id
       ) AS row_num,
       name,
       registered_on
FROM customers
ORDER BY prefecture, row_num;

WITH ranked AS (
    SELECT order_id,
           product_id,
           quantity * unit_price AS subtotal,
           ROW_NUMBER() OVER (
               PARTITION BY order_id ORDER BY quantity * unit_price DESC
           ) AS row_num
    FROM order_items
)
SELECT order_id, product_id, subtotal
FROM ranked
WHERE row_num = 1
ORDER BY order_id;

WITH with_prev AS (
    SELECT customer_id,
           order_id,
           ordered_on,
           LAG(ordered_on) OVER (
               PARTITION BY customer_id ORDER BY ordered_on
           ) AS prev_ordered_on
    FROM orders
)
SELECT customer_id,
       order_id,
       ordered_on,
       prev_ordered_on,
       julianday(ordered_on) - julianday(prev_ordered_on) AS days
FROM with_prev
ORDER BY customer_id, ordered_on;
