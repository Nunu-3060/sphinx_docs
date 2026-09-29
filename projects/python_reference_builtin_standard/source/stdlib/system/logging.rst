logging
=======

アプリケーションの実行状況やエラーを記録するための標準的な仕組みを
提供するモジュール。出力先やフォーマット、重要度に応じた出力可否を
柔軟に設定できるため、本番運用を前提としたコードでは ``print`` の
代わりに ``logging`` を使うことが強く推奨される。

logging.basicConfig
---------------------

ルートロガーに対する基本的な設定（出力レベル、フォーマット、出力先
など）を一度だけ行う。通常はプログラムの起動時に一度だけ呼び出す。

.. code-block:: python

   >>> import logging
   >>> logging.basicConfig(
   ...     level=logging.INFO,
   ...     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
   ... )

.. note::

   ``basicConfig`` はプロセス内で **最初に呼ばれたときだけ** 効果を持つ。ルートロガーに既にハンドラが設定されている状態で ``basicConfig`` を再度呼び出しても、2 回目以降の呼び出しは黙って無視され、``level`` や ``format`` の変更は反映されない。設定を強制的にやり直したい場合は ``force=True`` を渡す必要がある。

   .. code-block:: python

      >>> logging.basicConfig(level=logging.DEBUG)  # 既に設定済みなので無視される
      >>> logging.basicConfig(level=logging.DEBUG, force=True)  # 強制的に再設定

logging.getLogger
-------------------

モジュールごとに独立したロガーを取得する。``__name__`` を渡すのが
慣例で、ログの出力元がどのモジュールかを識別しやすくなる。

.. code-block:: python

   >>> import logging
   >>> logger = logging.getLogger(__name__)
   >>> logger.info("処理を開始します")  # doctest: +SKIP
   2024-01-01 12:00:00 [INFO] __main__: 処理を開始します

ログレベル（DEBUG / INFO / WARNING / ERROR / CRITICAL）
-----------------------------------------------------------

ログには重要度に応じた 5 段階のレベルがあり、``basicConfig`` で設定した ``level`` 未満のメッセージは出力されない。デフォルトのレベルは ``WARNING`` であるため、``INFO`` 以下を表示するには明示的な設定が必要。

以下は、``basicConfig`` を一度も呼んでいない別プロセスでの例
（このページの他の例とは独立している）。``basicConfig`` を呼ばなくても、
ロガーの実効レベルは既定で ``WARNING`` であり、標準エラー出力への
出力自体は Python の logging モジュールが用意する「最終手段のハンドラ
（handler of last resort）」によって行われる。このときルートロガーには
何のハンドラも設定されていないが、``WARNING`` 以上のメッセージは
自動的に標準エラー出力に表示される（``DEBUG`` と ``INFO`` は既定の
レベル ``WARNING`` 未満のため、そもそも出力されない）。このハンドラ
にはフォーマッタが設定されて
いないため、メッセージ本文のみがそのまま出力される。

.. code-block:: python

   >>> import logging
   >>> logger = logging.getLogger(__name__)
   >>> logger.debug("変数の値: x=%s", 10)      # 詳細なデバッグ情報（出力されない）
   >>> logger.info("処理が完了しました")        # 正常な動作の記録（出力されない）
   >>> logger.warning("設定ファイルが見つかりません。デフォルト値を使用します")
   設定ファイルが見つかりません。デフォルト値を使用します
   >>> logger.error("ファイルの読み込みに失敗しました")
   ファイルの読み込みに失敗しました
   >>> logger.critical("データベースに接続できません。処理を中断します")
   データベースに接続できません。処理を中断します

なぜ本番コードで print ではなく logging を使うのか
-------------------------------------------------------

``print`` は常に標準出力へ出力され、後から出力の有無やレベルを
制御できない。一方 ``logging`` は次のような利点を持つ。

- レベルごとに出力の可否を切り替えられる（本番では ``INFO`` 以上のみ
  出力し、調査時だけ ``DEBUG`` を有効にする、といった運用が可能）。
- タイムスタンプや呼び出し元モジュール名などを自動的に付与できる。
- ファイルやシステムログ、外部の監視サービスなど、出力先を後から
  変更・追加しやすい。

.. code-block:: python

   >>> import logging
   >>> logging.basicConfig(
   ...     filename="app.log",
   ...     level=logging.WARNING,
   ...     format="%(asctime)s [%(levelname)s] %(message)s",
   ...     force=True,  # 既に basicConfig 済みでも設定を上書きする
   ... )
   >>> logger = logging.getLogger(__name__)
   >>> logger.info("この行はファイルに出力されない")     # WARNING 未満のため無視
   >>> logger.error("この行はファイルに出力される")

.. note::

   ここでは ``force=True`` を付けている点に注意。このページでは既に「logging.basicConfig」の節で一度 ``basicConfig`` を呼んでいるため、``force=True`` を省略すると、この 2 回目の呼び出しは無視され、``filename="app.log"`` への出力先変更が反映されない。

logger.exception による例外の記録
-------------------------------------

``except`` ブロックの中で ``logger.exception(...)`` を呼ぶと、指定した
メッセージを ``ERROR`` レベルで記録しつつ、現在処理中の例外のトレース
バックを自動的に付加してくれる。``logger.error(msg, exc_info=True)`` と
書くのと同じ効果だが、``exception`` の方が短く書ける。

前節までで ``basicConfig`` にファイル出力（``filename="app.log"``）を設定したが、ここではコンソールでの出力を確認するため、``force=True`` で既定のストリームハンドラ・既定のフォーマット（``"%(levelname)s:%(name)s:%(message)s"``）に一旦リセットしている。

.. code-block:: python

   >>> import logging
   >>> logging.basicConfig(force=True)
   >>> logger = logging.getLogger(__name__)
   >>> try:
   ...     1 / 0
   ... except ZeroDivisionError:
   ...     logger.exception("計算中にエラーが発生しました")
   ...
   ERROR:__main__:計算中にエラーが発生しました
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
   ZeroDivisionError: division by zero

``exception`` は ``except`` ブロックの外で呼んだり、記録したいレベルが ``ERROR`` 以外だったりする場合には使えない。その場合は任意のレベルのメソッドに ``exc_info=True`` を渡せば同様にトレースバックを付加できる。

.. code-block:: python

   >>> try:
   ...     1 / 0
   ... except ZeroDivisionError:
   ...     logger.warning("計算に失敗しましたが処理を継続します", exc_info=True)
   ...  # doctest: +SKIP

.. note::

   ライブラリを実装する場合、ライブラリ自身が ``basicConfig`` を呼ぶべきではない。出力設定はアプリケーション側に委ね、ライブラリ側は ``getLogger(__name__)`` でロガーを取得するだけにとどめるのが慣例。
