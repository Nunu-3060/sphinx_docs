-- 6 章 集計とグループ化 演習問題の解答
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/answers_ch06.sql

SELECT SUM(price * stock) AS total_stock_value
FROM products;

SELECT prefecture, COUNT(*) AS customer_count
FROM customers
GROUP BY prefecture
ORDER BY customer_count DESC, prefecture;

SELECT product_id, SUM(quantity) AS total_quantity
FROM order_items
GROUP BY product_id
HAVING SUM(quantity) >= 5
ORDER BY product_id;

SELECT strftime('%Y-%m', ordered_on) AS month,
       COUNT(*) AS order_count
FROM orders
WHERE status <> 'キャンセル'
GROUP BY month
ORDER BY month;
