sys
===

Python インタプリタ自体や実行環境に関する情報・機能を提供するモジュール。``os`` がオペレーティングシステム側の機能を扱うのに対し、``sys`` はインタプリタの内部状態（コマンドライン引数、モジュール検索パス、標準入出力、終了処理など）を扱う。

sys.argv
--------

スクリプト実行時に渡されたコマンドライン引数のリスト。先頭の要素 ``sys.argv[0]`` はスクリプト名自身になる。

.. code-block:: python

   >>> import sys
   >>> sys.argv  # doctest: +SKIP
   ['script.py', '--verbose', 'input.txt']
   >>> script_name, *args = sys.argv
   >>> args  # doctest: +SKIP
   ['--verbose', 'input.txt']

.. note::

   本格的なコマンドライン引数の解析には :doc:`argparse` を使うのが一般的。

sys.exit
--------

プログラムを終了させる。引数に整数を渡すと終了コードとして扱われ、
文字列を渡すと標準エラー出力に表示した上で終了コード 1 で終了する。

.. code-block:: python

   >>> import sys
   >>> def main(value):
   ...     if value < 0:
   ...         sys.exit("エラー: value は 0 以上である必要があります")
   ...     return value * 2
   >>> main(-1)  # doctest: +SKIP
   エラー: value は 0 以上である必要があります

sys.path
--------

``import`` 文がモジュールを探索するディレクトリのリスト。実行時に
リストへ追加すれば、任意のディレクトリからモジュールを読み込めるように
なる。

.. code-block:: python

   >>> import sys
   >>> sys.path  # doctest: +SKIP
   ['', '/usr/lib/python3.12', '/usr/lib/python3.12/lib-dynload', ...]
   >>> sys.path.append("/opt/mylibs")

sys.stdout / sys.stderr
------------------------

標準出力・標準エラー出力に対応するファイルオブジェクト。``print`` は
内部的に ``sys.stdout`` へ書き込んでいるため、これを差し替えることで
出力先を変更できる。

.. code-block:: python

   >>> import sys
   >>> print("通常の出力")
   通常の出力
   >>> print("エラーメッセージ", file=sys.stderr)
   >>> sys.stderr.write("直接書き込むことも可能\n")  # doctest: +SKIP

sys.version_info / sys.maxsize
--------------------------------

実行中の Python のバージョン情報、およびプラットフォームが扱える
最大の整数サイズ（``Py_ssize_t`` の最大値）を取得する。バージョンに
応じて処理を分岐したい場合などに利用する。

.. code-block:: python

   >>> import sys
   >>> sys.version_info  # doctest: +SKIP
   sys.version_info(major=3, minor=12, micro=1, releaselevel='final', serial=0)
   >>> if sys.version_info >= (3, 10):
   ...     print("match 文が使用可能")
   match 文が使用可能
   >>> sys.maxsize  # doctest: +SKIP
   9223372036854775807
