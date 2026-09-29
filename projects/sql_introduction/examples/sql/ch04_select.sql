-- 4 章 データの取得
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/ch04_select.sql

SELECT name, price FROM products;

SELECT * FROM categories;

SELECT name, price, price * 1.1 AS price_with_tax
FROM products;

SELECT 7 / 2, -7 / 2, 7 / 2.0, 7 % 2;

SELECT name, price
FROM products
WHERE price >= 500;

SELECT customer_id, name, prefecture
FROM customers
WHERE prefecture = '東京都';

SELECT order_id, ordered_on
FROM orders
WHERE ordered_on < '2025-02-01';

SELECT name, price, stock
FROM products
WHERE price >= 200 AND stock < 30;

-- category_id = 3 の商品と、「category_id = 8 かつ price >= 250」の商品
SELECT name, category_id, price
FROM products
WHERE category_id = 3 OR category_id = 8 AND price >= 250;

-- 「category_id が 3 または 8」かつ「price >= 250」の商品
SELECT name, category_id, price
FROM products
WHERE (category_id = 3 OR category_id = 8) AND price >= 250;

SELECT name, price
FROM products
WHERE price BETWEEN 150 AND 250;

SELECT customer_id, name, prefecture
FROM customers
WHERE prefecture IN ('大阪府', '福岡県');

-- 名前に「コーヒー」を含む商品
SELECT name
FROM products
WHERE name LIKE '%コーヒー%';

-- 名前が「チョコレート」で終わる商品
SELECT name
FROM products
WHERE name LIKE '%チョコレート';

SELECT name, price
FROM products
ORDER BY price DESC;

SELECT name, prefecture, registered_on
FROM customers
ORDER BY prefecture, registered_on DESC;

SELECT name, price
FROM products
ORDER BY price DESC
LIMIT 3;

SELECT name, price
FROM products
ORDER BY price DESC
LIMIT 3 OFFSET 3;

SELECT DISTINCT prefecture
FROM customers
ORDER BY prefecture;

SELECT name || '（' || price || '円）' AS label,
       length(name) AS name_length
FROM products
WHERE category_id = 8;

SELECT order_id,
       ordered_on,
       date(ordered_on, '+7 days') AS due_on,
       strftime('%m', ordered_on) AS month
FROM orders
WHERE order_id <= 3;

SELECT name, price, round(price * 1.1) AS price_with_tax
FROM products
WHERE category_id = 8;

SELECT name,
       price,
       CASE
           WHEN price >= 1000 THEN '高'
           WHEN price >= 300 THEN '中'
           ELSE '低'
       END AS price_rank
FROM products
ORDER BY price DESC;
