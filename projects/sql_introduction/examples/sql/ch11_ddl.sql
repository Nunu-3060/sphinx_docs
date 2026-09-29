-- 11 章 テーブルの設計と定義
--
-- 使い方（examples フォルダーで実行します）:
--   python run_query.py sql/ch11_ddl.sql

CREATE TABLE reviews (
    review_id   INTEGER PRIMARY KEY,
    product_id  INTEGER NOT NULL REFERENCES products (product_id),
    customer_id INTEGER NOT NULL REFERENCES customers (customer_id),
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment     TEXT,
    status      TEXT    NOT NULL DEFAULT '公開',
    UNIQUE (product_id, customer_id)
);

SELECT name, type, "notnull", dflt_value, pk
FROM pragma_table_info('reviews');

CREATE TABLE type_demo (i INTEGER, t TEXT);

INSERT INTO type_demo (i, t) VALUES ('123', 456), ('abc', 7.5);

SELECT i, typeof(i), t, typeof(t) FROM type_demo;

CREATE TABLE strict_demo (i INTEGER, t TEXT) STRICT;

-- 次の文はエラーになります。
INSERT INTO strict_demo (i, t) VALUES ('abc', 'text');

INSERT INTO reviews (product_id, customer_id, rating, comment)
VALUES (1, 1, 5, 'おいしかったです。');

SELECT * FROM reviews;

-- 次の文はエラーになります。
INSERT INTO reviews (product_id, customer_id, rating)
VALUES (2, 1, 6);

-- 次の文はエラーになります。
INSERT INTO reviews (product_id, customer_id)
VALUES (2, 1);

-- 次の文はエラーになります。
INSERT INTO reviews (product_id, customer_id, rating)
VALUES (1, 1, 4);

-- 次の文はエラーになります。
INSERT INTO reviews (product_id, customer_id, rating)
VALUES (99, 1, 4);

ALTER TABLE reviews ADD COLUMN posted_on TEXT;

SELECT * FROM reviews;

DROP TABLE type_demo;

CREATE VIEW order_totals AS
SELECT o.order_id,
       o.customer_id,
       o.ordered_on,
       o.status,
       SUM(oi.quantity * oi.unit_price) AS amount
FROM orders AS o
INNER JOIN order_items AS oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.customer_id, o.ordered_on, o.status;

SELECT order_id, ordered_on, amount
FROM order_totals
WHERE amount >= 1000
ORDER BY amount DESC;
