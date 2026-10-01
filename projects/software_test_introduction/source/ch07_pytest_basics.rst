7. pytest 入門
==============

pytest は、Python で最も広く使われているテストフレームワークである。unittest より少ない記述でテストを書けるうえ、失敗したときの情報が詳しく、機能を拡張するプラグインも豊富である。この章では、pytest の基本的な使い方を学ぶ。

7.1 pytest の特徴
-----------------

unittest と比べた pytest の主な特徴は次のとおりである。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 特徴
     - 内容
   * - テストを関数で書ける
     - クラスを作らず、名前が ``test_`` で始まる関数としてテストを書ける。
   * - ``assert`` 文で確かめる
     - ``assertEqual`` などのメソッドを覚える必要がなく、Python の ``assert`` 文をそのまま使う。失敗すると、式の各部分の値を表示する。
   * - fixture
     - テストの準備と後始末を、再利用しやすい部品として書ける（8 章）。
   * - パラメーター化
     - 同じテストを、異なる入力と期待値の組で繰り返し実行できる（8 章）。
   * - プラグイン
     - カバレッジの計測（14 章）や並列実行など、多くのプラグインで機能を拡張できる。
   * - unittest との互換性
     - unittest で書かれたテストもそのまま実行できる。

7.2 最初のテスト
----------------

6 章で unittest で書いたカートのテストを、pytest で書き直すと次のようになる。

.. literalinclude:: ../examples/ch07_pytest_basics/test_cart_pytest.py
   :language: python
   :caption: ch07_pytest_basics/test_cart_pytest.py
   :linenos:

unittest 版と比べると、次の点が異なる。

* ``TestCase`` を継承したクラスがなく、テストは関数である。
* ``self.assertEqual(a, b)`` の代わりに ``assert a == b`` と書く。
* ``setUp`` がなく、各テストの中でカートを作っている。準備の処理を共通化する方法は、8 章の fixture で説明する。

商品の ``APPLE`` と ``MELON`` は、モジュールの定数として定義している（7～8 行目）。``Item`` は変更できない（\ ``frozen=True``\ ）ため、テスト間で共有しても互いに影響しない。一方、カートは中身が変わるため、テストごとに新しく作っている。

7.3 テストの実行
----------------

``examples`` フォルダーで、次のようにフォルダーやファイルを指定して実行する。

.. code-block:: console
   :linenos:

   $ python -m pytest ch07_pytest_basics

実行結果は次のとおりである。

.. code-block:: text

   ============================= test session starts =============================
   platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
   rootdir: G:\sphinx\projects\test_introduction\examples
   configfile: pyproject.toml
   plugins: anyio-4.15.1, hypothesis-6.168.3
   collected 8 items

   ch07_pytest_basics\test_approx.py ...                                    [ 37%]
   ch07_pytest_basics\test_cart_pytest.py .....                             [100%]

   ============================== 8 passed in 1.27s ==============================

``collected 8 items`` は、8 つのテストが見つかったことを表す。ファイル名の後の ``.`` は、成功したテスト 1 つを表す。失敗したテストは ``F``\ 、テストの準備などでエラーになったテストは ``E`` で表される。``test_approx.py`` のテストは 7.6 節で説明する。

pytest の主なオプションを次に示す。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - オプション
     - 内容
   * - ``-v``
     - テストごとに名前と結果を表示する。
   * - ``-q``
     - 表示を簡潔にする。
   * - ``-x``
     - 最初に失敗したテストで実行を止める。
   * - ``-k 式``
     - 名前が式に一致するテストだけを実行する。例：``-k "empty or remove"``
   * - ``--lf``
     - 前回失敗したテストだけを実行する。
   * - ``-s``
     - ``print`` の出力をそのまま表示する（既定では、成功したテストの出力は表示しない）。
   * - ``--durations=N``
     - 実行に時間がかかったテストを、上位 N 個表示する。

テストは、ファイル名の後に ``::`` とテストの名前を付けて、1 つだけ指定して実行することもできる。

.. code-block:: console
   :linenos:

   $ python -m pytest -v ch07_pytest_basics/test_cart_pytest.py
   $ python -m pytest "ch07_pytest_basics/test_cart_pytest.py::test_new_cart_is_empty"

1 行目の ``-v`` を付けた実行結果は次のとおりである。

.. code-block:: text

   ch07_pytest_basics/test_cart_pytest.py::test_new_cart_is_empty PASSED    [ 20%]
   ch07_pytest_basics/test_cart_pytest.py::test_add_same_item_accumulates_quantity PASSED [ 40%]
   ch07_pytest_basics/test_cart_pytest.py::test_subtotal_is_sum_of_price_times_quantity PASSED [ 60%]
   ch07_pytest_basics/test_cart_pytest.py::test_add_zero_quantity_raises_value_error PASSED [ 80%]
   ch07_pytest_basics/test_cart_pytest.py::test_remove_item_not_in_cart_raises_key_error PASSED [100%]

   ============================== 5 passed in 1.33s ==============================

pytest は、unittest と異なり、テストをファイルに書いた順に実行する。

7.4 テストの発見の規則と設定ファイル
------------------------------------

フォルダーを指定して実行すると、pytest はその中から次の規則でテストを探す。

* ファイル名が ``test_*.py`` または ``*_test.py`` のファイル
* その中の、名前が ``test`` で始まる関数
* 名前が ``Test`` で始まるクラス（\ ``__init__`` メソッドを持たないもの）の中の、名前が ``test`` で始まるメソッド
* unittest の ``TestCase`` を継承したクラスのテストメソッド

引数を指定せずに ``python -m pytest`` と実行した場合の探索の範囲や、毎回指定するオプションは、設定ファイルに書いておける。本書のサンプルコードでは、``pyproject.toml`` に次の設定を書いている。

.. literalinclude:: ../examples/pyproject.toml
   :language: toml
   :caption: pyproject.toml（pytest の設定の部分）
   :lines: 8-26
   :lineno-start: 8
   :linenos:

``pythonpath``\ （10 行目）は、import の起点に加えるフォルダーである。``examples`` フォルダーを加えることで、どの章のテストからも ``from shop.cart import Cart`` のように ``shop`` パッケージを読み込める。``testpaths``\ （12～23 行目）は、引数を指定しないときにテストを探すフォルダーである。``addopts`` と ``markers`` は 8 章で説明する。

7.5 失敗したときの出力を読む
----------------------------

pytest の大きな利点の 1 つは、テストが失敗したときの情報の詳しさである。わざと誤った期待値を書いたテストで確かめてみる。

.. literalinclude:: ../examples/ch07_pytest_basics/failing_example.py
   :language: python
   :caption: ch07_pytest_basics/failing_example.py
   :linenos:

このファイルは、名前が ``test_`` で始まらないため、引数なしで pytest を実行したときには収集されない。ファイルを直接指定すると実行される。

.. code-block:: console
   :linenos:

   $ python -m pytest ch07_pytest_basics/failing_example.py

実行結果は次のとおりである。

.. code-block:: text

   collected 1 item

   ch07_pytest_basics\failing_example.py F                                  [100%]

   ================================== FAILURES ===================================
   ____________________ test_subtotal_with_wrong_expectation _____________________

       def test_subtotal_with_wrong_expectation() -> None:
           cart = Cart()
           cart.add(Item("りんご", 150), 3)
   >       assert cart.subtotal() == 400  # 正しくは 450
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   E       assert 450 == 400
   E        +  where 450 = subtotal()
   E        +    where subtotal = <shop.cart.Cart object at 0x000001DDC30A2510>.subtotal

   ch07_pytest_basics\failing_example.py:15: AssertionError
   =========================== short test summary info ===========================
   FAILED ch07_pytest_basics/failing_example.py::test_subtotal_with_wrong_expectation
   ============================== 1 failed in 1.55s ==============================

出力は次のように読む。

* ``>`` の行が、失敗した ``assert`` 文である。
* ``E`` で始まる行が、失敗の内容である。``assert 450 == 400`` は、左辺の ``cart.subtotal()`` が 450 を返したことを示す。``where`` の行は、式の各部分がどのような値だったかを示している。
* ``failing_example.py:15`` は、失敗した箇所のファイル名と行番号である。
* 最後の ``short test summary info`` に、失敗したテストの一覧がまとめて表示される。

pytest は、``assert`` 文を実行前に書き換えて、式の途中の値を記録している。そのため、``assert`` 文を書くだけで、unittest のアサーションメソッドと同等以上の情報が得られる。

テストが失敗したら、まずテスト対象と期待値のどちらが誤っているかを考える。この例では期待値が誤っているが、実際の開発では、テスト対象の欠陥を見つけたことを意味する場合も、テストの期待値が仕様の変更に追従していないことを意味する場合もある。

7.6 例外と浮動小数点数の検証
----------------------------

例外が送出されることは、``pytest.raises`` を ``with`` 文と組み合わせて確かめる（7.2 節のコードの 33 行目）。``match`` 引数を指定すると、例外のメッセージが正規表現に一致することも確かめられる。

.. code-block:: python
   :linenos:

   with pytest.raises(ValueError, match="1 以上"):
       cart.add(APPLE, 0)

``match`` を指定しない場合、同じ種類の例外であれば、想定と異なる理由で送出されたものでもテストが成功してしまう。例外の種類が広く使われるもの（\ ``ValueError`` など）であるときは、``match`` でメッセージも確かめるとよい。

浮動小数点数は、2 進数で正確に表せない値があるため、計算結果を ``==`` で比べると期待どおりにならないことがある。``pytest.approx`` を使うと、許容する誤差の範囲で比べられる。

.. literalinclude:: ../examples/ch07_pytest_basics/test_approx.py
   :language: python
   :caption: ch07_pytest_basics/test_approx.py
   :linenos:

``pytest.approx`` の既定の許容誤差は、期待値に対する相対誤差 :math:`10^{-6}` である。``abs`` 引数で絶対誤差を、``rel`` 引数で相対誤差を指定できる（17 行目）。リストや辞書の要素をまとめて比べることもできる。

7.7 まとめ
----------

* pytest では、名前が ``test_`` で始まる関数としてテストを書き、``assert`` 文で結果を確かめる。
* テストの探索の範囲や既定のオプションは、``pyproject.toml`` などの設定ファイルに書ける。
* 失敗したときは、``>`` の行と ``E`` の行から、どの式がどの値で失敗したかを読み取れる。
* 例外は ``pytest.raises`` で、浮動小数点数は ``pytest.approx`` で確かめる。
