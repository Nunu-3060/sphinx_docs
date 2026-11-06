traceback
=========

例外発生時のトレースバック（スタックトレース）を、標準エラー出力へ表示したり、文字列として取得したりするためのモジュール。``except`` ブロック内でエラー内容を詳しく記録・報告したい場合によく使われる。

traceback.print_exc
--------------------

現在処理中の例外のトレースバックを、標準エラー出力にそのまま表示する。``except`` ブロックの中で、デバッグ用にエラー内容を画面に出力したいだけの場合に最も手軽な方法である。

.. code-block:: python
   :linenos:

   >>> import traceback
   >>> def divide(a, b):
   ...     return a / b
   ...
   >>> try:
   ...     divide(10, 0)
   ... except ZeroDivisionError:
   ...     traceback.print_exc()
   ...
   Traceback (most recent call last):
     File "<python-input-2>", line 2, in <module>
       divide(10, 0)
       ~~~~~~^^^^^^^
     File "<python-input-1>", line 2, in divide
       return a / b
              ~~^~~
   ZeroDivisionError: division by zero

.. note::

   ``~~^~~`` のような記号は、例外の原因となった式の位置を示すもので、Python 3.11 以降のトレースバックに表示される。また ``<python-input-N>`` は Python 3.13 以降の対話モード（REPL）で入力した各コードに付けられる名前で、スクリプトを実行した場合はここにファイルのパスが表示される。Python 3.13 以降では、端末に表示されるトレースバックはデフォルトで色付けされる（環境変数 ``PYTHON_COLORS=0`` や ``NO_COLOR`` で無効化できる）。

traceback.format_exc
----------------------

トレースバックを標準エラー出力に表示するのではなく、文字列として取得する。取得した文字列は、ログメッセージへの埋め込みやエラーレポートの生成、独自のエラーページの作成など、出力先を自分でコントロールしたい場面で使う。

.. code-block:: python
   :linenos:

   >>> import traceback
   >>> def divide(a, b):
   ...     return a / b
   ...
   >>> try:
   ...     divide(10, 0)
   ... except ZeroDivisionError:
   ...     error_text = traceback.format_exc()
   ...     print(error_text)
   ...
   Traceback (most recent call last):
     File "<python-input-2>", line 2, in <module>
       divide(10, 0)
       ~~~~~~^^^^^^^
     File "<python-input-1>", line 2, in divide
       return a / b
              ~~^~~
   ZeroDivisionError: division by zero

.. note::

   :doc:`../system/logging` の「logger.exception による例外の記録」で解説した ``logger.exception(...)`` や ``exc_info=True`` は、内部的にこの ``traceback`` モジュールの機能を使ってトレースバックを整形し、ログメッセージに自動的に付加している。ログに残すだけであれば、多くの場合 ``logger.exception`` を使う方が簡潔で済む。``traceback.format_exc()`` を直接呼ぶのは、API のエラーレスポンスに含める、独自のクラッシュレポートファイルに書き出すなど、ログ出力以外の用途でトレースバック文字列そのものが必要な場合になる。

traceback.format_exception
----------------------------

``print_exc`` や ``format_exc`` は「現在処理中の例外」を暗黙に対象とするが、``format_exception`` はより汎用的で、例外オブジェクトを明示的に受け取り、整形済みの行から成るリストを返す。例外を変数として保持し、発生した場所から離れた場所（呼び出し元に伝播させた後など）で処理したい場合に向いている。

.. code-block:: python
   :linenos:

   >>> import traceback
   >>> def divide(a, b):
   ...     return a / b
   ...
   >>> try:
   ...     divide(10, 0)
   ... except ZeroDivisionError as exc:
   ...     lines = traceback.format_exception(exc)
   ...     lines
   ...
   ['Traceback (most recent call last):\n', '  File "<python-input-2>", line 2, in <module>\n    divide(10, 0)\n    ~~~~~~^^^^^^^\n', '  File "<python-input-1>", line 2, in divide\n    return a / b\n           ~~^~~\n', 'ZeroDivisionError: division by zero\n']
   >>> print("".join(lines))
   Traceback (most recent call last):
     File "<python-input-2>", line 2, in <module>
       divide(10, 0)
       ~~~~~~^^^^^^^
     File "<python-input-1>", line 2, in divide
       return a / b
              ~~^~~
   ZeroDivisionError: division by zero

.. note::

   ``format_exception(exc)`` のように例外オブジェクト 1 つだけを渡す書き方は Python 3.10 で追加されたもので、本書が対象とする Python 3.11 以降ではいつでも使える。``sys.exc_info()`` の戻り値をそのまま扱いたい場合や、古いコードとの互換を保ちたい場合は、``traceback.format_exception(type(exc), exc, exc.__traceback__)`` のように 3 引数で呼び出す形も広く使われている。
