-- 4 章 データの取得 演習問題の解答
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/answers_ch04.sql

SELECT name, registered_on
FROM customers
WHERE registered_on >= '2024-01-01' AND registered_on < '2025-01-01'
ORDER BY registered_on;

SELECT name, stock
FROM products
WHERE stock <= 20;

SELECT name, price
FROM products
WHERE name LIKE '%チョコ%' OR price <= 100;

SELECT name, price * stock AS stock_value
FROM products
ORDER BY stock_value DESC, product_id
LIMIT 3;

SELECT name,
       CASE
           WHEN stock = 0 THEN '在庫なし'
           WHEN stock < 50 THEN '残りわずか'
           ELSE '在庫あり'
       END AS stock_status
FROM products;
