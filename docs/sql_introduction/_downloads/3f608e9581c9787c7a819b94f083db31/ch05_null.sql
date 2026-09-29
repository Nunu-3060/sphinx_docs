-- 5 章 NULL の扱い
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/ch05_null.sql

SELECT customer_id, name, email
FROM customers;

SELECT customer_id, name
FROM customers
WHERE email = NULL;

SELECT NULL = NULL, NULL <> 1, NULL + 1, NULL || 'abc';

SELECT customer_id, name
FROM customers
WHERE email IS NULL;

SELECT customer_id, name, email
FROM customers
WHERE email IS NOT NULL;

SELECT name, category_id
FROM products
WHERE category_id <> 8;

SELECT name, category_id
FROM products
WHERE category_id <> 8 OR category_id IS NULL;

SELECT name, category_id
FROM products
WHERE category_id NOT IN (8, NULL);

SELECT name, COALESCE(email, '（未登録）') AS email
FROM customers;

SELECT name, stock, 1000 / NULLIF(stock, 0) AS ratio
FROM products
WHERE category_id = 5;

SELECT name, category_id
FROM products
ORDER BY category_id NULLS LAST;
