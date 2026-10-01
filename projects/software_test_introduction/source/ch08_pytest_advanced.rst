8. pytest の活用
================

この章では、テストの準備を部品化する fixture、同じテストを複数の入力で実行するパラメーター化、テストの扱いを変えるマーカーを学ぶ。あわせて、4 章で設計した送料計算と注文の状態遷移のテストケースを、テストコードとして実装する。

8.1 fixture
-----------

7 章のテストでは、各テストの中でカートを作っていた。テストが増えると、同じ準備の処理があちこちに現れる。:term:`fixture` は、テストの準備（と後始末）を関数として定義し、複数のテストで再利用する仕組みである。

fixture は、``@pytest.fixture`` を付けた関数として定義する。テスト関数の引数に fixture の関数名を書くと、pytest がその fixture を呼び出し、戻り値を引数として渡す。

.. literalinclude:: ../examples/ch08_pytest_advanced/conftest.py
   :language: python
   :caption: ch08_pytest_advanced/conftest.py
   :linenos:

.. literalinclude:: ../examples/ch08_pytest_advanced/test_cart_fixture.py
   :language: python
   :caption: ch08_pytest_advanced/test_cart_fixture.py
   :linenos:

fixture の主な性質は次のとおりである。

* **引数の名前で指定する**：``test_subtotal(cart_with_apples: Cart)`` と書くと、``cart_with_apples`` fixture の戻り値が渡される。
* **fixture は別の fixture を使える**：``cart_with_apples``\ （conftest.py の 21 行目）は、引数で ``cart`` と ``apple`` を受け取っている。pytest は依存関係をたどり、必要な fixture を順に呼び出す。
* **テストごとに作り直される**：既定では、fixture はテスト関数ごとに呼び出される。``test_remove`` でカートからりんごを取り除いても、次の ``test_fixture_is_created_for_each_test`` には、りんごが 3 個入った新しいカートが渡される。

fixture は、テストの準備を「名前の付いた部品」にする。テスト関数の引数を見れば、そのテストが何を前提にしているかが分かる。

8.2 conftest.py
---------------

fixture を ``conftest.py`` という名前のファイルに書くと、同じフォルダーとその下のフォルダーにあるすべてのテストファイルから、import せずに使える。前節の fixture も ``conftest.py`` に書いているため、``test_cart_fixture.py`` は fixture を import していない。

使える fixture の一覧は、``--fixtures`` オプションで確かめられる。

.. code-block:: console
   :linenos:

   $ python -m pytest --fixtures ch08_pytest_advanced/test_cart_fixture.py

出力の最後に、``conftest.py`` で定義した fixture が、docstring とともに表示される。

.. code-block:: text

   ----------------------- fixtures defined from conftest ------------------------
   cart -- ch08_pytest_advanced\conftest.py:15
       空のカート.

   cart_with_apples -- ch08_pytest_advanced\conftest.py:21
       りんごを 3 個入れたカート（fixture は別の fixture を利用できる）.

   apple -- ch08_pytest_advanced\conftest.py:9
       単価 150 円の商品.

8.3 後始末とスコープ
--------------------

fixture の中で ``return`` の代わりに ``yield`` を使うと、テストの後に後始末の処理を実行できる。``yield`` より前が準備、後が後始末である。テストが失敗しても、後始末は実行される。

.. code-block:: python
   :linenos:

   @pytest.fixture
   def connection() -> Iterator[sqlite3.Connection]:
       conn = sqlite3.connect(":memory:")  # 準備
       yield conn                          # ここでテストが実行される
       conn.close()                        # 後始末

``yield`` を使う fixture の戻り値の型は、``collections.abc`` の ``Iterator`` で表す。実際の例は 11 章で扱う。

データベースの接続など、準備に時間がかかるものを、テストごとに作り直すと実行が遅くなる。``scope`` 引数を指定すると、fixture を作り直す範囲を広げられる。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - scope
     - fixture を作り直す単位
   * - ``"function"``
     - テスト関数ごと（既定）
   * - ``"class"``
     - テストクラスごと
   * - ``"module"``
     - テストファイルごと
   * - ``"package"``
     - パッケージ（フォルダー）ごと
   * - ``"session"``
     - テストの実行全体で 1 回

.. code-block:: python
   :linenos:

   @pytest.fixture(scope="module")
   def catalog() -> list[Item]:
       return load_catalog()  # 時間のかかる読み込みを、ファイルごとに 1 回だけ行う

スコープを広げた fixture は、複数のテストで同じオブジェクトを共有する。あるテストがそのオブジェクトの中身を変えると、後のテストの結果が変わってしまう。スコープを広げるのは、テストが中身を変更しないもの（読み取り専用のデータなど）に限るのが安全である。

8.4 パラメーター化
------------------

4 章の境界値分析では、同じ関数を異なる入力と期待値で何度も試すテストケースを設計した。これをテスト関数ごとに書くと、ほぼ同じコードが並ぶ。``@pytest.mark.parametrize`` を使うと、1 つのテスト関数を、入力と期待値の組ごとに繰り返し実行できる。

.. literalinclude:: ../examples/ch08_pytest_advanced/test_shipping_table.py
   :language: python
   :caption: ch08_pytest_advanced/test_shipping_table.py
   :linenos:

``parametrize`` の第 1 引数には引数の名前を、第 2 引数には値の組のリストを指定する（8～15 行目）。値の組は、4 章の境界値分析の表をそのまま写したものである。このように、テストケースの表とテストコードが 1 対 1 に対応していると、設計したテストケースが漏れなく実装されているかを確かめやすい。

39～55 行目は、4.4 節のデシジョンテーブルの 8 つの規則の実装である。``pytest.param`` の ``id`` 引数で、各テストに規則の番号を名前として付けている。``-v`` オプションを付けて実行すると、値の組ごとに 1 つのテストとして表示される。

.. code-block:: console
   :linenos:

   $ python -m pytest -v ch08_pytest_advanced/test_shipping_table.py

.. code-block:: text

   collecting ... collected 14 items

   ch08_pytest_advanced/test_shipping_table.py::test_boundary_for_regular_member[0-500] PASSED [  7%]
   ch08_pytest_advanced/test_shipping_table.py::test_boundary_for_regular_member[4999-500] PASSED [ 14%]
   ch08_pytest_advanced/test_shipping_table.py::test_boundary_for_regular_member[5000-0] PASSED [ 21%]
   ch08_pytest_advanced/test_shipping_table.py::test_boundary_for_premium_member[2999-500] PASSED [ 28%]
   ch08_pytest_advanced/test_shipping_table.py::test_boundary_for_premium_member[3000-0] PASSED [ 35%]
   ch08_pytest_advanced/test_shipping_table.py::test_negative_subtotal_raises_value_error PASSED [ 42%]
   ch08_pytest_advanced/test_shipping_table.py::test_decision_table[rule1] PASSED [ 50%]
   ch08_pytest_advanced/test_shipping_table.py::test_decision_table[rule2] PASSED [ 57%]
   ch08_pytest_advanced/test_shipping_table.py::test_decision_table[rule3] PASSED [ 64%]
   ch08_pytest_advanced/test_shipping_table.py::test_decision_table[rule4] PASSED [ 71%]
   ch08_pytest_advanced/test_shipping_table.py::test_decision_table[rule5] PASSED [ 78%]
   ch08_pytest_advanced/test_shipping_table.py::test_decision_table[rule6] PASSED [ 85%]
   ch08_pytest_advanced/test_shipping_table.py::test_decision_table[rule7] PASSED [ 92%]
   ch08_pytest_advanced/test_shipping_table.py::test_decision_table[rule8] PASSED [100%]

   ============================= 14 passed in 1.43s ==============================

``id`` を指定しない場合は、``[0-500]`` のように値からテストの名前が作られる。どの値の組で失敗したかが名前から分かるため、1 つの関数の中でループを回して確かめるよりも、失敗の原因を特定しやすい。

8.5 状態遷移テストの実装
------------------------

4.5 節の状態遷移テストも、パラメーター化で実装できる。状態遷移表の有効な遷移を辞書で表し、そこに含まれない状態と操作の組み合わせを、無効な遷移として自動で作っている。

.. literalinclude:: ../examples/ch08_pytest_advanced/test_order_state.py
   :language: python
   :caption: ch08_pytest_advanced/test_order_state.py
   :linenos:

``VALID_TRANSITIONS``\ （10～16 行目）は状態遷移表の 5 つの有効な遷移を、``INVALID_TRANSITIONS``\ （19～24 行目）は残りの 15 の無効な遷移を表す。無効な遷移のテストでは、例外が送出されることに加えて、状態が変わっていないこと（65 行目）も確かめている。

``make_order``\ （36～42 行目）は、指定した状態の注文を作る補助関数である。``Order`` の ``status`` 属性に直接値を代入しても同じ状態を作れるが、正しい操作の順序で作ることで、実際の使われ方に近い状態でテストできる。

このテストファイルは、有効な遷移 5 つ、無効な遷移 15 個、作成直後の状態の確認 1 つの、合わせて 21 のテストになる。表の 20 のマスをすべてテストしていることになり、4.5 節の 0 スイッチカバレッジも満たしている。

8.6 マーカー
------------

:term:`マーカー`\ は、テストに目印を付けて、扱いを変える仕組みである。主な組み込みのマーカーを次に示す。

.. literalinclude:: ../examples/ch08_pytest_advanced/test_markers.py
   :language: python
   :caption: ch08_pytest_advanced/test_markers.py
   :linenos:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - マーカー
     - 内容
   * - ``skip``
     - テストを実行しない（スキップする）。``reason`` に理由を書く。
   * - ``skipif``
     - 条件が真のときにスキップする。特定の OS やバージョンでしか意味のないテストに使う。
   * - ``xfail``
     - 失敗することが分かっているテストに付ける。失敗しても全体の結果は失敗にならない。``strict=True`` を指定すると、予想に反して成功したときに失敗として扱う。

``xfail`` は、欠陥が見つかったがすぐには修正しない場合に、その欠陥を記録しておくために使う。``strict=True`` を指定しておくと、欠陥が修正されてテストが成功したときに気付けるため、マーカーを外し忘れることがない。

``-rsx`` オプションを付けて実行すると、スキップしたテストと ``xfail`` のテストの理由が表示される。

.. code-block:: console
   :linenos:

   $ python -m pytest -rsx ch08_pytest_advanced/test_markers.py

.. code-block:: text

   collected 4 items

   ch08_pytest_advanced\test_markers.py s.x.                                [100%]

   =========================== short test summary info ===========================
   SKIPPED [1] ch08_pytest_advanced\test_markers.py:9: 仕様が確定するまで実行しない
   XFAIL ch08_pytest_advanced/test_markers.py::test_known_bug - 既知の欠陥: 四捨五入になっていない
   =================== 2 passed, 1 skipped, 1 xfailed in 2.00s ===================

``s`` はスキップ、``x`` は予想どおりの失敗を表す。``test_windows_only`` は Windows で実行したため、スキップされずに成功している。

``slow`` のような独自のマーカーを付けると、``-m`` オプションでテストを選んで実行できる。たとえば、時間のかかるテストを除いて実行するには次のようにする。

.. code-block:: console
   :linenos:

   $ python -m pytest -m "not slow" ch08_pytest_advanced/test_markers.py

独自のマーカーは、設定ファイルの ``markers`` に登録しておく（7.4 節の ``pyproject.toml`` の 26 行目）。本書のサンプルコードでは ``addopts`` に ``--strict-markers`` を指定しているため（同 25 行目）、登録していないマーカーを使うとエラーになる。マーカー名の打ち間違いで、意図したテストが選ばれなくなることを防げる。

8.7 組み込みの fixture
----------------------

pytest には、よく使う準備の処理が fixture として組み込まれている。引数に名前を書くだけで使える。

.. literalinclude:: ../examples/ch08_pytest_advanced/test_builtin_fixtures.py
   :language: python
   :caption: ch08_pytest_advanced/test_builtin_fixtures.py
   :linenos:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - fixture
     - 内容
   * - ``tmp_path``
     - テストごとに作られる一時フォルダーの ``pathlib.Path``\ 。ファイルを読み書きするテストで使う。
   * - ``capsys``
     - 標準出力と標準エラー出力に書かれた内容を取り出す。
   * - ``monkeypatch``
     - 環境変数、属性、辞書の要素などを一時的に書き換える。テストが終わると元に戻る。
   * - ``caplog``
     - ``logging`` で出力されたログを取り出す。
   * - ``tmp_path_factory``
     - ``session`` スコープで一時フォルダーを作る。
   * - ``request``
     - 実行中のテストの情報を取り出す。fixture の中で使う。

``monkeypatch`` は、テストが外部の状態（環境変数など）に依存する場合や、テスト対象の一部を差し替えたい場合に使う。テストの中で環境変数を ``os.environ`` に直接書き込むと、ほかのテストに影響が残るが、``monkeypatch`` はテストの終了時に自動で元に戻す。差し替えについては、9 章のテストダブルで詳しく扱う。

8.8 まとめ
----------

* fixture は、テストの準備と後始末を再利用できる部品にする。テスト関数の引数の名前で指定する。
* ``conftest.py`` に書いた fixture は、同じフォルダー以下のテストから import せずに使える。
* ``yield`` を使う fixture で後始末を書ける。スコープを広げるときは、テスト間の共有に注意する。
* パラメーター化を使うと、テストケースの表をそのままテストコードにできる。
* マーカーで、スキップ、予想される失敗、テストの選択を指定できる。
