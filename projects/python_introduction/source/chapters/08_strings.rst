第 8 章 文字列操作
==================

文字列の基本操作
----------------

Python の文字列には、あらかじめ多くのメソッドが用意されています。代表的なメソッドを次に示します。

.. list-table::
   :header-rows: 1

   * - メソッド
     - 説明
     - 例
   * - ``strip``
     - 前後の空白を取り除く
     - ``" ab ".strip()``
   * - ``lower``
     - すべて小文字に変換する
     - ``"AB".lower()``
   * - ``upper``
     - すべて大文字に変換する
     - ``"ab".upper()``
   * - ``replace``
     - 文字列を置換する
     - ``"ab".replace("a", "x")``
   * - ``split``
     - 文字列を分割してリストにする
     - ``"a-b".split("-")``
   * - ``join``
     - リストを結合して文字列にする
     - ``"-".join(["a", "b"])``

これらのメソッドは、元の文字列を変更するのではなく、処理結果を新しい文字列として返す点に注意してください。なお、後述のサンプルコードでは、文字列の前後にある空白の有無を確認しやすくするために、``repr`` 関数を使って文字列を引用符付きで表示しています。

.. code-block:: python
   :linenos:

   print(repr("  Python  "))  # '  Python  '

f 文字列（f-string）による文字列の組み立て
-------------------------------------------

文字列と変数を組み合わせて 1 つの文字列を作りたい場合は、f 文字列（f-string）を使うと簡潔に書けます。文字列の前に ``f`` を付け、波括弧 ``{}`` の中に変数や式を書きます。

.. code-block:: python
   :linenos:

   name = "高橋"
   greeting = f"こんにちは、{name} さん。"
   print(greeting)

スライスによる部分文字列の取得
-------------------------------

文字列の一部を取り出す操作をスライスと呼びます。``文字列[開始位置:終了位置]`` のように書くことで、開始位置から終了位置の直前までの文字列を取得できます。

.. code-block:: python
   :linenos:

   sentence = "Python は 1991 年に誕生しました。"
   print(sentence[:6])  # Python

サンプルコード
--------------

文字列メソッドと f 文字列、スライスの使い方をまとめたサンプルコードです。

:download:`strings.py <../../examples/ch08_strings/strings.py>`

.. literalinclude:: ../../examples/ch08_strings/strings.py
   :language: python3
   :linenos:
