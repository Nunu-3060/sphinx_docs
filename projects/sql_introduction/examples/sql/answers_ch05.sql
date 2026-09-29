-- 5 章 NULL の扱い 演習問題の解答
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/answers_ch05.sql

SELECT name
FROM categories
WHERE parent_id IS NULL;

SELECT name, COALESCE(category_id, 0) AS category_id
FROM products;

SELECT name FROM customers WHERE email = email;

SELECT name, category_id
FROM products
WHERE category_id <> 3 OR category_id IS NULL;
