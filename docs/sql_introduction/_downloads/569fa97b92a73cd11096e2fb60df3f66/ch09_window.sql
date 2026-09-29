-- 9 章 ウィンドウ関数
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/ch09_window.sql

SELECT name,
       price,
       AVG(price) OVER () AS avg_price
FROM products
ORDER BY product_id;

SELECT name,
       category_id,
       price,
       AVG(price) OVER (PARTITION BY category_id) AS category_avg,
       price - AVG(price) OVER (PARTITION BY category_id) AS diff
FROM products
WHERE category_id IS NOT NULL
ORDER BY category_id, price;

WITH order_counts AS (
    SELECT customer_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id,
       order_count,
       ROW_NUMBER() OVER (ORDER BY order_count DESC, customer_id) AS row_num,
       RANK() OVER (ORDER BY order_count DESC) AS rank_no,
       DENSE_RANK() OVER (ORDER BY order_count DESC) AS dense_rank_no
FROM order_counts
ORDER BY order_count DESC, customer_id;

SELECT name,
       category_id,
       price,
       RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS price_rank
FROM products
WHERE category_id IS NOT NULL
ORDER BY category_id, price_rank;

WITH ranked AS (
    SELECT name,
           category_id,
           price,
           ROW_NUMBER() OVER (
               PARTITION BY category_id ORDER BY price DESC
           ) AS row_num
    FROM products
    WHERE category_id IS NOT NULL
)
SELECT name, category_id, price
FROM ranked
WHERE row_num = 1
ORDER BY category_id;

WITH monthly_sales AS (
    SELECT strftime('%Y-%m', o.ordered_on) AS month,
           SUM(oi.quantity * oi.unit_price) AS sales
    FROM orders AS o
    INNER JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'キャンセル'
    GROUP BY month
)
SELECT month,
       sales,
       SUM(sales) OVER (ORDER BY month) AS cumulative_sales
FROM monthly_sales
ORDER BY month;

WITH monthly_sales AS (
    SELECT strftime('%Y-%m', o.ordered_on) AS month,
           SUM(oi.quantity * oi.unit_price) AS sales
    FROM orders AS o
    INNER JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'キャンセル'
    GROUP BY month
)
SELECT month,
       sales,
       round(AVG(sales) OVER (
           ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ), 1) AS moving_avg
FROM monthly_sales
ORDER BY month;

WITH monthly_sales AS (
    SELECT strftime('%Y-%m', o.ordered_on) AS month,
           SUM(oi.quantity * oi.unit_price) AS sales
    FROM orders AS o
    INNER JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'キャンセル'
    GROUP BY month
)
SELECT month,
       sales,
       LAG(sales) OVER (ORDER BY month) AS prev_sales,
       sales - LAG(sales) OVER (ORDER BY month) AS diff
FROM monthly_sales
ORDER BY month;
