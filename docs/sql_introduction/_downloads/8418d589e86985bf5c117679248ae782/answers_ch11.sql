-- 11 章 テーブルの設計と定義 演習問題の解答
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/answers_ch11.sql

CREATE TABLE favorites (
    customer_id INTEGER NOT NULL REFERENCES customers (customer_id),
    product_id  INTEGER NOT NULL REFERENCES products (product_id),
    added_on    TEXT    NOT NULL,
    PRIMARY KEY (customer_id, product_id)
);

INSERT INTO favorites (customer_id, product_id, added_on)
VALUES (1, 6, '2025-06-01');

-- 次の文はエラーになります。
INSERT INTO favorites (customer_id, product_id, added_on)
VALUES (1, 6, '2025-06-01');

ALTER TABLE products ADD COLUMN description TEXT;

SELECT name, type FROM pragma_table_info('products');

CREATE VIEW customer_summary AS
SELECT c.customer_id,
       c.name,
       COUNT(DISTINCT o.order_id) AS order_count,
       COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id AND o.status <> 'キャンセル'
LEFT JOIN order_items AS oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.name;

SELECT * FROM customer_summary ORDER BY customer_id;
