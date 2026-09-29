traceback
=========

例外発生時のトレースバック（スタックトレース）を、標準エラー出力へ表示したり、
文字列として取得したりするためのモジュール。``except`` ブロック内でエラー
内容を詳しく記録・報告したい場合によく使われる。

traceback.print_exc
--------------------

現在処理中の例外のトレースバックを、標準エラー出力にそのまま表示する。``except`` ブロックの中で、デバッグ用にエラー内容を画面に出力したいだけの場合に最も手軽な方法。

.. code-block:: python

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
     File "<stdin>", line 2, in <module>
     File "<stdin>", line 2, in divide
   ZeroDivisionError: division by zero

traceback.format_exc
----------------------

トレースバックを標準エラー出力に表示するのではなく、文字列として取得する。
取得した文字列は、ログメッセージへの埋め込みやエラーレポートの生成、
独自のエラーページの作成など、出力先を自分でコントロールしたい場面で使う。

.. code-block:: python

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
     File "<stdin>", line 2, in <module>
     File "<stdin>", line 2, in divide
   ZeroDivisionError: division by zero

.. note::

   :doc:`../system/logging` の「logger.exception による例外の記録」で解説した ``logger.exception(...)`` や ``exc_info=True`` は、内部的にこの ``traceback`` モジュールの機能を使ってトレースバックを整形し、ログメッセージに自動的に付加している。ログに残すだけであれば、多くの場合 ``logger.exception`` を使う方が簡潔で済む。``traceback.format_exc()`` を直接呼ぶのは、API のエラーレスポンスに含める、独自のクラッシュレポートファイルに書き出すなど、ログ出力以外の用途でトレースバック文字列そのものが必要な場合になる。

traceback.format_exception
----------------------------

``print_exc`` や ``format_exc`` は「現在処理中の例外」を暗黙に対象とするが、``format_exception`` はより汎用的で、例外オブジェクトを明示的に受け取り、整形済みの行から成るリストを返す。例外を変数として保持し、発生した場所から離れた場所（呼び出し元に伝播させた後など）で処理したい場合に向いている。

.. code-block:: python

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
   ['Traceback (most recent call last):\n', '  File "<stdin>", line 2, in <module>\n', '  File "<stdin>", line 2, in divide\n', 'ZeroDivisionError: division by zero\n']
   >>> print("".join(lines))
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
     File "<stdin>", line 2, in divide
   ZeroDivisionError: division by zero

.. note::

   ``format_exception(exc)`` のように例外オブジェクト 1 つだけを渡す書き方が使える。``sys.exc_info()`` の戻り値をそのまま扱いたい場合や、古いコードとの互換を保ちたい場合は、``traceback.format_exception(type(exc), exc, exc.__traceback__)`` のように 3 引数で呼び出す形も広く使われている。
