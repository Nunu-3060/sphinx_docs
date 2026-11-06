sys
===

Python インタプリタ自体や実行環境に関する情報・機能を提供するモジュール。``os`` がオペレーティングシステム側の機能を扱うのに対し、``sys`` はインタプリタの内部状態（コマンドライン引数、モジュール検索パス、標準入出力、終了処理など）を扱う。

sys.argv
--------

スクリプト実行時に渡されたコマンドライン引数のリスト。先頭の要素 ``sys.argv[0]`` はスクリプト名自身になり、実際の引数は ``sys.argv[1:]`` に入る。要素はすべて文字列である。

.. code-block:: python
   :linenos:

   >>> import sys
   >>> sys.argv  # doctest: +SKIP
   ['script.py', '--verbose', 'input.txt']
   >>> script_name, *args = sys.argv
   >>> args  # doctest: +SKIP
   ['--verbose', 'input.txt']

.. note::

   本格的なコマンドライン引数の解析には :doc:`argparse` を使うのが一般的である。

sys.exit
--------

プログラムを終了させる。引数に整数を渡すと終了コードとして扱われ、文字列を渡すと標準エラー出力に表示した上で終了コード 1 で終了する。引数を省略した場合（または ``None``）は終了コード 0 となる。実際には ``SystemExit`` 例外を送出するだけなので、``finally`` 節や ``with`` 文の後処理は実行される。

.. code-block:: python
   :linenos:

   >>> import sys
   >>> def main(value):
   ...     if value < 0:
   ...         sys.exit("エラー: value は 0 以上である必要があります")
   ...     return value * 2
   >>> main(-1)  # doctest: +SKIP
   エラー: value は 0 以上である必要があります

sys.path
--------

``import`` 文がモジュールを探索するディレクトリのリスト。実行時にリストへ追加すれば、任意のディレクトリからモジュールを読み込めるようになる。

.. code-block:: python
   :linenos:

   >>> import sys
   >>> sys.path  # doctest: +SKIP
   ['', '/usr/lib/python314.zip', '/usr/lib/python3.14', '/usr/lib/python3.14/lib-dynload', ...]
   >>> sys.path.append("/opt/mylibs")

sys.stdout / sys.stderr
------------------------

標準出力・標準エラー出力に対応するファイルオブジェクト。``print`` は内部的に ``sys.stdout`` へ書き込んでいるため、これを差し替えることで出力先を変更できる。

.. code-block:: python
   :linenos:

   >>> import sys
   >>> print("通常の出力")
   通常の出力
   >>> print("エラーメッセージ", file=sys.stderr)
   >>> sys.stderr.write("直接書き込むことも可能\n")  # doctest: +SKIP

sys.version_info / sys.maxsize
--------------------------------

実行中の Python のバージョン情報、および ``Py_ssize_t`` 型の最大値を取得する。``sys.version_info`` はタプルとして比較できるため、バージョンに応じて処理を分岐したい場合などに利用する。Python の ``int`` には上限がないため、``sys.maxsize`` は整数の最大値ではなく、リストや文字列の長さなどコンテナのサイズの上限を表す（64 ビット環境では ``2**63 - 1``）。

.. code-block:: python
   :linenos:

   >>> import sys
   >>> sys.version_info  # doctest: +SKIP
   sys.version_info(major=3, minor=14, micro=0, releaselevel='final', serial=0)
   >>> if sys.version_info >= (3, 11):
   ...     print("tomllib モジュールが使用可能")
   ...
   tomllib モジュールが使用可能
   >>> sys.maxsize  # doctest: +SKIP
   9223372036854775807

sys._is_gil_enabled
-------------------

Python 3.13 以降で利用できる関数で、実行中のインタプリタで GIL（Global Interpreter Lock）が有効かどうかを返す。通常のビルドでは常に ``True`` を返す。GIL を無効化できるフリースレッドビルド（3.13 で実験的に導入され、3.14 で正式にサポートされた）では、GIL が無効な状態であれば ``False`` を返す。フリースレッドビルドについては :doc:`../concurrency/threading` も参照。

.. code-block:: python
   :linenos:

   >>> import sys
   >>> sys._is_gil_enabled()  # 通常のビルドの場合
   True
