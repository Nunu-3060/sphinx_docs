6. unittest 入門
================

第 II 部では、第 I 部で学んだ考え方を Python のテストコードとして実装する。この章では、Python の標準ライブラリに含まれるテストフレームワーク unittest を使って、自動テストの基本的な仕組みを学ぶ。

6.1 テストフレームワークとは
----------------------------

テストを自動化するには、「テスト対象を呼び出し、結果を期待値と比べ、合否を記録する」処理を何度も書くことになる。:term:`テストフレームワーク`\ は、この処理の共通部分を提供する仕組みである。主に次の機能を持つ。

* テストの書き方の枠組み（テストを関数やクラスとして書く規則）
* 結果を期待値と比べる機能（:term:`アサーション`\ ）
* テストの発見と実行、結果の報告
* テストの前後の準備と後始末

Python では、標準ライブラリの unittest と、外部パッケージの pytest が広く使われている。unittest は追加のインストールなしで使え、Java の JUnit と同じ系統の書き方をする。本書では 7 章以降で pytest を主に使うが、pytest は unittest で書かれたテストもそのまま実行できる。既存のプロジェクトで unittest のテストを読む機会も多いため、この章で基本を押さえておく。

6.2 テスト対象
--------------

この章と 7 章では、題材のショッピングカート ``Cart`` をテストする。

.. literalinclude:: ../examples/shop/cart.py
   :language: python
   :caption: shop/cart.py
   :linenos:

``Item`` は商品名と単価を持つ商品である（6～16 行目）。``frozen=True`` を指定しているため、値を変更できず、辞書のキーとして使える。``Cart`` は、商品ごとの数量を辞書で保持する（23 行目）。

6.3 最初のテスト
----------------

unittest でテストを書く手順は次のとおりである。

1. ``unittest.TestCase`` を継承したクラスを作る。
2. 名前が ``test`` で始まるメソッドとしてテストを書く。
3. ``assertEqual`` などのメソッドで、結果を確かめる。

.. literalinclude:: ../examples/ch06_unittest/test_cart_unittest.py
   :language: python
   :caption: ch06_unittest/test_cart_unittest.py
   :linenos:

``setUp`` メソッド（11～15 行目）は、各テストメソッドの実行前に毎回呼び出される。ここで作ったカートは、テストメソッドごとに新しく作り直されるため、あるテストでカートに追加した商品が、ほかのテストに影響することはない。テストの後に毎回呼び出される ``tearDown`` メソッドもあり、ファイルの削除などの後始末に使う。

例外が送出されることを確かめるには、``assertRaises`` を ``with`` 文と組み合わせて使う（31～33 行目）。``with`` のブロックの中で指定した例外が送出されればテストは成功し、送出されなければ失敗する。

最後の 2 行（40～41 行目）は、このファイルを ``python test_cart_unittest.py`` のように直接実行したときに、テストを実行するためのものである。

6.4 テストの実行
----------------

``examples`` フォルダーで次のコマンドを実行する。``-v`` オプションを付けると、テストごとの結果を表示する。

.. code-block:: console
   :linenos:

   $ python -m unittest -v ch06_unittest/test_cart_unittest.py

実行結果は次のとおりである。

.. code-block:: text

   test_add_same_item_accumulates_quantity (ch06_unittest.test_cart_unittest.TestCart.test_add_same_item_accumulates_quantity) ... ok
   test_add_zero_quantity_raises_value_error (ch06_unittest.test_cart_unittest.TestCart.test_add_zero_quantity_raises_value_error) ... ok
   test_new_cart_is_empty (ch06_unittest.test_cart_unittest.TestCart.test_new_cart_is_empty) ... ok
   test_remove_item_not_in_cart_raises_key_error (ch06_unittest.test_cart_unittest.TestCart.test_remove_item_not_in_cart_raises_key_error) ... ok
   test_subtotal_is_sum_of_price_times_quantity (ch06_unittest.test_cart_unittest.TestCart.test_subtotal_is_sum_of_price_times_quantity) ... ok

   ----------------------------------------------------------------------
   Ran 5 tests in 0.002s

   OK

5 つのテストがすべて成功した（``ok``\ ）。テストメソッドは、ファイルに書いた順ではなく、名前の順に実行される。テストが実行の順序に依存しないように書くことが前提になっているためである。

6.5 主なアサーションメソッド
----------------------------

``TestCase`` には、目的に応じたアサーションメソッドが用意されている。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - メソッド
     - 確かめる内容
   * - ``assertEqual(a, b)``
     - ``a == b``
   * - ``assertNotEqual(a, b)``
     - ``a != b``
   * - ``assertTrue(x)``
     - ``bool(x) is True``
   * - ``assertFalse(x)``
     - ``bool(x) is False``
   * - ``assertIs(a, b)``
     - ``a is b``
   * - ``assertIsNone(x)``
     - ``x is None``
   * - ``assertIn(a, b)``
     - ``a in b``
   * - ``assertIsInstance(a, cls)``
     - ``isinstance(a, cls)``
   * - ``assertAlmostEqual(a, b)``
     - ``round(a - b, 7) == 0``\ （浮動小数点数の比較）
   * - ``assertRaises(exc)``
     - 例外 ``exc`` が送出される

``assertEqual`` を使えば多くの場合は確かめられるが、目的に合ったメソッドを使うと、失敗したときのメッセージが分かりやすくなる。たとえば ``assertIn`` は、失敗すると「どの要素がどのコレクションに含まれなかったか」を表示する。

6.6 テストの発見
----------------

テストが増えたら、ファイルを 1 つずつ指定する代わりに、テストを自動で探して実行できる。``python -m unittest discover`` は、指定したフォルダーから名前が ``test`` で始まるファイルを探し、その中のテストをすべて実行する。ただし、unittest の探索は、フォルダーが import できるパッケージ（``__init__.py`` を持つフォルダー）であることを前提にしている。本書のサンプルコードの章ごとのフォルダーは ``__init__.py`` を持たないため、この章ではファイルを指定して実行する。7 章の pytest は、パッケージでないフォルダーからもテストを探せる。

6.7 まとめ
----------

* テストフレームワークは、テストの書き方、アサーション、テストの発見と実行、準備と後始末の仕組みを提供する。
* unittest では、``TestCase`` を継承したクラスに、名前が ``test`` で始まるメソッドとしてテストを書く。
* ``setUp`` はテストメソッドごとに実行されるため、テスト同士が影響し合わない。
* 目的に合ったアサーションメソッドを使うと、失敗したときのメッセージが分かりやすくなる。
