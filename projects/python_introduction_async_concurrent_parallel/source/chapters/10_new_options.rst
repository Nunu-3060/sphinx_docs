第 10 章 GIL を超える新しい選択肢
=================================

ここまでの章では、CPU バウンドな処理を並列に実行するにはプロセスが必要であると説明してきた。しかし、プロセスには起動の負荷やデータの受け渡しの負荷がある。この制約を解消するため、近年の Python には新しい仕組みが追加されている。この章では、free-threaded ビルドとサブインタプリタを紹介する。

どちらも比較的新しい機能であり、仕様や対応状況は今後のバージョンで変わる可能性がある。実際に使う場合は、使用する Python のバージョンの公式ドキュメントを確認してほしい。

free-threaded ビルド
--------------------

**free-threaded ビルド** は、GIL を無効にした CPython である。PEP 703 で提案され、Python 3.13 で実験的に提供された後、Python 3.14 で正式にサポートされた（PEP 779）。free-threaded ビルドでは、複数のスレッドが Python のコードを本当に並列に実行できるため、CPU バウンドな処理もスレッドで速くなる。

free-threaded ビルドは、通常のビルドとは別に配布されている。実行ファイルの名前は ``python3.14t`` のように末尾に ``t`` が付く。Windows の Python install manager では ``py install 3.14t`` でインストールできる。

実行中の Python が free-threaded ビルドかどうかは、次のサンプルで確認できる。このサンプルは、CPU バウンドな処理を 4 つのスレッドで実行した場合と逐次処理の場合の経過時間も比べる。

:download:`check_gil.py <../../examples/ch10_new_options/check_gil.py>`

.. literalinclude:: ../../examples/ch10_new_options/check_gil.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 7-

通常のビルドの Python 3.14 で実行すると、次のような結果になる。スレッドは逐次処理より遅い。

.. code-block:: text

   Python 3.14.6, free-threaded ビルド: False, GIL 有効: True
   逐次: 1.14 秒
   スレッド 4 個: 3.06 秒

free-threaded ビルドで実行すると、``GIL 有効`` が ``False`` になり、スレッドの数に応じて経過時間が短くなる。``sysconfig.get_config_var("Py_GIL_DISABLED")`` は Python が free-threaded ビルドかどうかを、``sys._is_gil_enabled()`` は実行中に GIL が有効かどうかを返す。free-threaded ビルドでも、GIL に対応していない C 拡張モジュールを import すると、GIL が自動的に有効になることがある。

free-threaded ビルドを使う場合は、次の点に注意する。

* **シングルスレッドの性能が少し下がる。**\ 参照カウントなどをスレッドセーフにするための処理が増えるためである。
* **C 拡張モジュールの対応が必要である。**\ NumPy などの主要なライブラリは対応が進んでいるが、すべてのライブラリが対応しているわけではない。
* **スレッドセーフでないコードの問題が表面化しやすくなる。**\ GIL があることで偶然動いていたコードが、競合状態によって誤動作することがある。:doc:`05_threads` で説明したロックなどによる排他制御が、これまで以上に重要になる。

サブインタプリタ
----------------

**サブインタプリタ** は、1 つのプロセスの中に作られる、互いに独立した Python のインタプリタである。各サブインタプリタは独自のモジュールやグローバル変数を持ち、Python 3.12 以降ではそれぞれ独立した GIL を持つ（PEP 684）。そのため、通常のビルドの Python でも、サブインタプリタを使えば 1 つのプロセスの中で CPU バウンドな処理を並列に実行できる。

Python 3.14 では、サブインタプリタを Python のコードから使うための ``concurrent.interpreters`` モジュール（PEP 734）と、``concurrent.futures.InterpreterPoolExecutor`` が追加された。``InterpreterPoolExecutor`` は、``ThreadPoolExecutor`` や ``ProcessPoolExecutor`` と同じ使い方で、タスクをサブインタプリタで実行する。

:download:`interpreter_pool.py <../../examples/ch10_new_options/interpreter_pool.py>`

.. literalinclude:: ../../examples/ch10_new_options/interpreter_pool.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 7-

執筆環境では次の結果になった。:doc:`06_processes` の ``prime_pool.py`` と同じ計算を、プロセスを使わずに並列に実行できている。

.. code-block:: text

   逐次: 148933 個, 5.93 秒
   サブインタプリタ: 148933 個, 1.27 秒

このサンプルの ``run_in_subinterpreters()`` では、``sys.version_info`` による分岐の中で ``InterpreterPoolExecutor`` を import している。Python 3.13 以前ではこのクラスが存在しないため、このように書くことで、古いバージョンでも import の時点でエラーにならず、mypy による型チェックも通る。

サブインタプリタを使う場合は、次の点に注意する。

* **データはサブインタプリタ間で共有されない。**\ 引数と戻り値は、プロセスと同じように pickle などでコピーして受け渡される。
* **サブインタプリタに対応していない C 拡張モジュールがある。**\ 対応していないモジュールをサブインタプリタの中で import すると、``ImportError`` になる。
* **関数の書き方によっては正しく動かない。**\ 執筆環境の Python 3.14.6 では、``count_primes()`` を ``sum(1 for n in range(start, stop) if is_prime(n))`` のようにジェネレーター式で書くと、サブインタプリタの中で ``NameError: name 'is_prime' is not defined`` が発生した。ジェネレーター式の中からだけグローバルな関数を参照していると、関数がグローバル変数を使わないものとして扱われ、関数が定義されたモジュールの名前空間を持たずにサブインタプリタへ渡されるためと考えられる。このサンプルでは ``for`` 文で書いて回避している。

新しい選択肢の位置付け
----------------------

free-threaded ビルドとサブインタプリタの特徴を、スレッドとプロセスと比べると次のようになる。

.. list-table:: 並列処理の手段の比較
   :header-rows: 1
   :widths: 22 26 26 26

   * - 項目
     - プロセス
     - サブインタプリタ
     - free-threaded ビルドのスレッド
   * - 利用できるバージョン
     - すべて
     - 3.14 以降（``InterpreterPoolExecutor``）
     - 3.13 以降（3.14 で正式サポート）
   * - メモリの共有
     - しない
     - しない
     - する
   * - 起動の負荷
     - 大きい
     - プロセスより小さい
     - 小さい
   * - 排他制御
     - ほぼ不要
     - ほぼ不要
     - 必要
   * - C 拡張の対応
     - 不要
     - 必要
     - 必要

本書の執筆時点では、CPU バウンドな処理を並列に実行する手段としては、プロセスが最も安定しており、ライブラリの対応も問題にならない。free-threaded ビルドとサブインタプリタは、使用するライブラリが対応していることを確認したうえで、プロセスの負荷が問題になる場面で検討するとよい。
