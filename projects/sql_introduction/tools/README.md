# tools：本文の生成と検査のためのスクリプト

このフォルダーには、「SQL 入門」の本文（`source/*.rst`）を生成するスクリプトと、表記を検査するスクリプトがあります。読者向けのサンプルではなく、資料を保守するためのものです。

## ファイル構成

| ファイル | 内容 |
| --- | --- |
| `generate_docs.py` | テンプレートから `source/*.rst` と `examples/sql/*.sql` を生成します |
| `check_style.py` | 生成された `source/*.rst` の表記を検査します |
| `templates/*.rst` | 本文のテンプレート。**本文を修正するときは、このファイルを編集します** |
| `setup.cfg` | flake8 と mypy の設定 |

## 本文を修正する手順

1. `tools/templates/` のテンプレートを編集します。`source/*.rst` は生成されるファイルなので、直接編集しないでください。直接編集しても、次に生成したときに上書きされます。
2. プロジェクトのルートで生成スクリプトを実行します。

   ```console
   python tools/generate_docs.py
   ```

3. 表記を検査します。問題がなければ「問題のある行: 0 行」と表示されます。

   ```console
   python tools/check_style.py
   ```

4. `build_html.bat` で HTML をビルドし、表示を確認します。

## テンプレートの書き方

テンプレートは通常の rst ファイルです。ただし、次の独自のディレクティブを使えます。これらのディレクティブは、生成時に通常の rst に展開されます。

### sqlfile

```rst
.. sqlfile:: ch04_select 4 章 データの取得
```

以降の `sqlrun` の SQL を `examples/sql/ch04_select.sql` に書き出すことを指定します。2 つ目以降の単語は、SQL ファイルの先頭のコメントと、付録 E の一覧に表示されるタイトルです。

SQL を実行するデータベースは、`sqlfile` ごとにサンプルデータベースの初期状態から用意されます。同じ `sqlfile` の `sqlrun` は、書かれた順に、前の `sqlrun` を実行した後のデータに対して実行されます。

### sqlrun

```rst
.. sqlrun::

   SELECT name, price
   FROM products
   WHERE price >= 500;
```

中に書いた SQL を実行し、次の 2 つに展開します。

* 行番号付きの SQL のコードブロック
* 実行結果の list-table。実行計画（`EXPLAIN QUERY PLAN`）の場合は sqlite3 コマンドと同様の形式、結果が 0 行の場合は「結果は 0 行です。」という文

複数の文を書いた場合は、最後に結果を返した文の結果を表示します。

次のオプションを指定できます。

| オプション | 内容 |
| --- | --- |
| `:error:` | SQL がエラーになることを期待します。エラーメッセージを表示します。エラーにならなかった場合は生成を中止します |
| `:hide-code:` | SQL のコードブロックを出力しません |
| `:hide-result:` | 実行結果を出力しません |
| `:no-export:` | `examples/sql/` の SQL ファイルに書き出しません |

`:error:` を指定していない SQL がエラーになった場合も、生成を中止します。これにより、本文に誤った SQL が載ることを防ぎます。

### pyoutput

```rst
.. pyoutput:: run_query.py -e "SELECT * FROM categories;"
```

`examples/` の Python スクリプトを実行し、その出力のコードブロックに展開します。スクリプトの後に引数を指定できます。

実行の前後に `create_shop_db.py` を実行して `examples/shop.db` を初期状態に戻すため、`shop.db` に加えた変更は失われます。生成の前に `shop.db` がなかった場合は、生成の後に削除します。

### 付録 E の自動生成部分

`templates/appendix_e_samples.rst` の `SQLFILE_ROWS` と `SQLFILE_INCLUDES` は、SQL ファイルの一覧表と内容の埋め込みに置き換えられます。

## 生成時に自動で行う処理

* インライン記法の前後に、必要に応じてエスケープした空白（`\ `）を補います。rst では、インライン記法の直後に全角括弧などが続くと、記法として解釈されないためです。テンプレートでは、この点を気にせずに書いてかまいません。
* 連続する空行を 1 行にまとめます。

## 注意事項

* `examples/sql/*.sql` も生成されるファイルです。直接編集しないでください。
* 13 章のベンチマーク（`ch13_index_benchmark.py`）の測定時間は実行するたびに変わるため、生成するたびに `source/ch13_index.rst` の該当部分が変わります。
* 生成には Python 3.12 以上が必要です。
* flake8 と mypy は、このフォルダーで実行します。

  ```console
  python -m flake8 .
  python -m mypy .
  ```
