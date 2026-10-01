付録 B 早見表
=============

pytest と unittest.mock でよく使う機能をまとめる。

B.1 pytest の実行
-----------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - コマンド
     - 内容
   * - ``python -m pytest``
     - 設定ファイルの ``testpaths``\ （なければ現在のフォルダー）のテストをすべて実行する。
   * - ``python -m pytest フォルダー``
     - 指定したフォルダーのテストを実行する。
   * - ``python -m pytest ファイル::テスト名``
     - 指定したテストだけを実行する。
   * - ``python -m pytest -v``
     - テストごとに名前と結果を表示する。
   * - ``python -m pytest -q``
     - 表示を簡潔にする。
   * - ``python -m pytest -x``
     - 最初の失敗で実行を止める。
   * - ``python -m pytest -k "式"``
     - 名前が式に一致するテストだけを実行する。
   * - ``python -m pytest -m "マーカーの式"``
     - マーカーでテストを選んで実行する。例：``-m "not slow"``
   * - ``python -m pytest --lf``
     - 前回失敗したテストだけを実行する。
   * - ``python -m pytest -s``
     - ``print`` の出力をそのまま表示する。
   * - ``python -m pytest -rsx``
     - スキップと xfail の理由を表示する。
   * - ``python -m pytest --durations=10``
     - 時間のかかったテストの上位 10 個を表示する。
   * - ``python -m pytest --fixtures``
     - 使える fixture の一覧を表示する。
   * - ``python -m pytest --doctest-modules``
     - モジュールの doctest も実行する。

B.2 pytest の検証
-----------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 書き方
     - 内容
   * - ``assert a == b``
     - 等しいことを確かめる。
   * - ``assert x is None``
     - ``None`` であることを確かめる。
   * - ``assert a in b``
     - 含まれることを確かめる。
   * - ``with pytest.raises(ValueError):``
     - ブロックの中で例外が送出されることを確かめる。
   * - ``with pytest.raises(ValueError, match="正規表現"):``
     - 例外のメッセージも確かめる。
   * - ``assert x == pytest.approx(y)``
     - 浮動小数点数が誤差の範囲で等しいことを確かめる。
   * - ``assert x == pytest.approx(y, abs=0.01)``
     - 絶対誤差を指定して比べる。

B.3 fixture とパラメーター化
----------------------------

.. code-block:: python
   :linenos:

   import pytest


   @pytest.fixture
   def cart() -> Cart:                    # テストごとに作り直す
       return Cart()


   @pytest.fixture(scope="module")
   def catalog() -> list[Item]:           # ファイルごとに 1 回だけ作る
       return load_catalog()


   @pytest.fixture
   def conn() -> Iterator[Connection]:    # yield の後が後始末
       c = connect()
       yield c
       c.close()


   @pytest.mark.parametrize(
       ("subtotal", "expected"),
       [
           (4999, 500),
           pytest.param(5000, 0, id="boundary"),  # id でテスト名を付ける
       ],
   )
   def test_fee(subtotal: int, expected: int) -> None:
       assert calc_shipping_fee(subtotal, False, False) == expected

B.4 マーカー
------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 書き方
     - 内容
   * - ``@pytest.mark.skip(reason="理由")``
     - 常にスキップする。
   * - ``@pytest.mark.skipif(条件, reason="理由")``
     - 条件が真のときにスキップする。
   * - ``@pytest.mark.xfail(reason="理由", strict=True)``
     - 失敗が予想されるテスト。成功したら失敗として扱う。
   * - ``@pytest.mark.独自の名前``
     - 独自のマーカー。設定ファイルの ``markers`` に登録する。

B.5 組み込みの fixture
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - fixture
     - 主な使い方
   * - ``tmp_path``
     - ``path = tmp_path / "a.txt"`` で一時フォルダーのファイルを扱う。
   * - ``capsys``
     - ``capsys.readouterr().out`` で標準出力の内容を取り出す。
   * - ``monkeypatch``
     - ``monkeypatch.setenv("KEY", "値")``\ 、``monkeypatch.setattr(モジュール, "名前", 値)`` で一時的に書き換える。
   * - ``caplog``
     - ``caplog.text`` でログの内容を取り出す。

B.6 unittest.mock
-----------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 書き方
     - 内容
   * - ``m = Mock(spec=クラス)``
     - クラスにない属性の使用を禁止したモックを作る。
   * - ``m.method.return_value = 値``
     - メソッドの戻り値を設定する。
   * - ``m.method.side_effect = 例外``
     - 呼び出したときに例外を送出させる。
   * - ``m.method.side_effect = [値1, 値2]``
     - 呼び出すたびに順に値を返させる。
   * - ``m.method.assert_called_once_with(引数)``
     - 指定した引数で 1 回だけ呼ばれたことを確かめる。
   * - ``m.method.assert_not_called()``
     - 呼ばれていないことを確かめる。
   * - ``m.method.call_count``
     - 呼ばれた回数。
   * - ``m.method.call_args_list``
     - 呼ばれたときの引数のリスト。
   * - ``with patch("モジュール.名前", return_value=値):``
     - ブロックの中だけ、名前を差し替える。名前が使われる場所を指定する。

B.7 coverage.py
---------------

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - コマンド
     - 内容
   * - ``python -m coverage run -m pytest``
     - 計測しながら pytest を実行する。
   * - ``python -m coverage report -m``
     - 結果を表示する。実行されなかった行の番号も表示する。
   * - ``python -m coverage report --fail-under=90``
     - カバレッジが 90 % 未満なら失敗させる。
   * - ``python -m coverage html``
     - HTML のレポートを ``htmlcov`` フォルダーに作る。
