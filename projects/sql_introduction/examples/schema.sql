-- サンプルデータベース「ネットショップ」のテーブル定義
-- create_shop_db.py から実行されます。

-- 商品カテゴリ（parent_id で親カテゴリを指す階層構造）
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL UNIQUE,
    parent_id   INTEGER REFERENCES categories (category_id)
);

-- 商品
CREATE TABLE products (
    product_id  INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    category_id INTEGER REFERENCES categories (category_id),
    price       INTEGER NOT NULL CHECK (price >= 0),
    stock       INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

-- 顧客
CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    name          TEXT    NOT NULL,
    prefecture    TEXT    NOT NULL,
    email         TEXT    UNIQUE,
    registered_on TEXT    NOT NULL  -- 登録日（YYYY-MM-DD 形式）
);

-- 注文
CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers (customer_id),
    ordered_on  TEXT    NOT NULL,  -- 注文日（YYYY-MM-DD 形式）
    status      TEXT    NOT NULL
                CHECK (status IN ('受付済', '発送済', 'キャンセル'))
);

-- 注文明細（1 件の注文に含まれる商品ごとの行）
CREATE TABLE order_items (
    order_id   INTEGER NOT NULL REFERENCES orders (order_id),
    product_id INTEGER NOT NULL REFERENCES products (product_id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    unit_price INTEGER NOT NULL CHECK (unit_price >= 0),  -- 注文時の単価
    PRIMARY KEY (order_id, product_id)
);
