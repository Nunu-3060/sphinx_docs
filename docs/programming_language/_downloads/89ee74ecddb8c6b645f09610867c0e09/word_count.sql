-- 文章中の単語の出現回数を数え、上位の単語を表示するサンプル
-- 文章を単語に分割する処理は済んでいるものとし、1 行に 1 単語を格納する。

CREATE TABLE words (
    position INTEGER     PRIMARY KEY,
    word     VARCHAR(32) NOT NULL
);

INSERT INTO words (position, word)
VALUES (1, 'The'), (2, 'quick'), (3, 'brown'), (4, 'fox'),
       (5, 'jumps'), (6, 'over'), (7, 'the'), (8, 'lazy'),
       (9, 'dog'), (10, 'The'), (11, 'dog'), (12, 'sleeps');

-- 小文字にそろえて集計し、出現回数の降順、同数なら単語の昇順で上位 3 件を取り出す
SELECT LOWER(word) AS word,
       COUNT(*) AS occurrences
  FROM words
 GROUP BY LOWER(word)
 ORDER BY occurrences DESC, word ASC
 LIMIT 3;
