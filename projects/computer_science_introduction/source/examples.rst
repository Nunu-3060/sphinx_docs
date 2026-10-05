サンプルコード一覧
==================

本書で使用するサンプルコードの一覧を示す。ファイル名のリンクからダウンロードできる。各ファイルの内容と実行結果は、「掲載章」の列に示した章で解説している。

実行方法
--------

サンプルコードは Python 3.12 以降で動作し、標準ライブラリだけを使う。ダウンロードしたファイルがあるフォルダで、次のように実行する。

.. code-block:: console
   :linenos:

   $ python ch01_number_bases.py

.. note::

   ``ch01_utf8_encode.py`` などは、絵文字やアクセント記号付きの文字を出力する。Windows のコンソールの文字コードが UTF-8 以外に設定されている場合は ``UnicodeEncodeError`` が発生することがある。その場合は ``python -X utf8 ch01_utf8_encode.py`` のように ``-X utf8`` オプションを付けて実行する。

サンプルコードの検査には flake8 と mypy を使った。検査に使った設定ファイルは :download:`setup.cfg <../examples/setup.cfg>` である。setup.cfg とサンプルコードを同じフォルダに置き、次のように実行すると同じ検査ができる。

.. code-block:: console
   :linenos:

   $ python -m flake8 .
   $ python -m mypy .

一覧
----

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - ファイル
     - 掲載章
     - 内容
   * - :download:`ch01_number_bases.py <../examples/ch01_number_bases.py>`
     - :doc:`ch01_data_representation`
     - 基数変換（剰余の繰り返しとホーナー法）と、8 ビットの 2 の補数・オーバーフローを再現する。
   * - :download:`ch01_float_error.py <../examples/ch01_float_error.py>`
     - :doc:`ch01_data_representation`
     - float を binary64 の符号・指数・仮数に分解し、0.1 + 0.2 の誤差と、isclose、fsum、Decimal、Fraction による対処を比較する。
   * - :download:`ch01_utf8_encode.py <../examples/ch01_utf8_encode.py>`
     - :doc:`ch01_data_representation`
     - UTF-8 の符号化を自前で実装して str.encode の結果と比較し、文字化けの例を表示する。
   * - :download:`ch01_endian.py <../examples/ch01_endian.py>`
     - :doc:`ch01_data_representation`
     - struct と int.to_bytes / int.from_bytes で、ビッグエンディアン・リトルエンディアン・ネットワークバイトオーダーのバイト列を比較する。
   * - :download:`ch01_unicode_normalize.py <../examples/ch01_unicode_normalize.py>`
     - :doc:`ch01_data_representation`
     - NFC・NFD・NFKC の正規化結果をコードポイントの列で表示し、len() と書記素クラスタの数の違いを示す。
   * - :download:`ch01_error_detection.py <../examples/ch01_error_detection.py>`
     - :doc:`ch01_data_representation`
     - パリティ、インターネットチェックサム、CRC-32、ハミング符号 (7,4) を実装し、1 ビットの誤りを訂正する。
   * - :download:`ch01_huffman.py <../examples/ch01_huffman.py>`
     - :doc:`ch01_data_representation`
     - ハフマン符号を構築し、固定長符号、エントロピーの下限、zlib とビット数を比較する。
   * - :download:`ch02_adder.py <../examples/ch02_adder.py>`
     - :doc:`ch02_logic_circuits`
     - NAND ゲートだけから各ゲート、半加算器、全加算器、8 ビットのリプルキャリー加算器を組み立て、真理値表と加算結果を表示する。
   * - :download:`ch03_toy_cpu.py <../examples/ch03_toy_cpu.py>`
     - :doc:`ch03_computer_architecture`
     - 7 命令の簡易 CPU エミュレータで 1 から 10 までの和を計算し、命令ごとの実行の様子を表示する。
   * - :download:`ch03_cache_locality.py <../examples/ch03_cache_locality.py>`
     - :doc:`ch03_computer_architecture`
     - 直接写像キャッシュのシミュレータで、行優先と列優先のアクセス順によるヒット率の違いを比較する。
   * - :download:`ch03_amdahl.py <../examples/ch03_amdahl.py>`
     - :doc:`ch03_computer_architecture`
     - アムダールの法則で、並列化率とコア数から速度向上率と効率の表を作る。
   * - :download:`ch04_linked_list.py <../examples/ch04_linked_list.py>`
     - :doc:`ch04_data_structures`
     - 単方向連結リストの挿入・探索・削除と、たどったノードの数を表示する。
   * - :download:`ch04_hash_table.py <../examples/ch04_hash_table.py>`
     - :doc:`ch04_data_structures`
     - チェイン法によるハッシュ表を実装し、負荷率に応じた再ハッシュを示す。
   * - :download:`ch04_bst.py <../examples/ch04_bst.py>`
     - :doc:`ch04_data_structures`
     - 二分探索木の挿入・探索・走査と、挿入順による木の高さの違いを示す。
   * - :download:`ch04_heap.py <../examples/ch04_heap.py>`
     - :doc:`ch04_data_structures`
     - 二分ヒープを自作して heapq と比較し、heapq を優先度付きキューとして使う。
   * - :download:`ch04_lru_cache.py <../examples/ch04_lru_cache.py>`
     - :doc:`ch04_data_structures`
     - OrderedDict による LRU キャッシュで追い出しの様子を表示し、functools.lru_cache の統計情報を示す。
   * - :download:`ch04_trie_unionfind.py <../examples/ch04_trie_unionfind.py>`
     - :doc:`ch04_data_structures`
     - トライによる接頭辞検索と、Union-Find による連結判定を示す。
   * - :download:`ch04_bloom_filter.py <../examples/ch04_bloom_filter.py>`
     - :doc:`ch04_data_structures`
     - ブルームフィルタを実装し、偽陽性率の実測値と理論値を比較する。
   * - :download:`ch05_search.py <../examples/ch05_search.py>`
     - :doc:`ch05_algorithms`
     - 線形探索と二分探索の比較回数を数え、bisect の使用例を示す。
   * - :download:`ch05_sort.py <../examples/ch05_sort.py>`
     - :doc:`ch05_algorithms`
     - 挿入ソート・マージソート・クイックソートの比較回数と、比較ソートの下限、sorted() の安定性を示す。
   * - :download:`ch05_dp.py <../examples/ch05_dp.py>`
     - :doc:`ch05_algorithms`
     - フィボナッチ数のメモ化、最長共通部分列、硬貨問題で貪欲法が最適解を出さない例を示す。
   * - :download:`ch05_graph.py <../examples/ch05_graph.py>`
     - :doc:`ch05_algorithms`
     - 幅優先探索、深さ優先探索、ダイクストラ法による最短経路の計算と経路の復元を示す。
   * - :download:`ch06_dfa.py <../examples/ch06_dfa.py>`
     - :doc:`ch06_theory_of_computation`
     - 2 進数が 3 の倍数かを判定する決定性有限オートマトンを実装し、状態の移り方を表示する。
   * - :download:`ch06_turing_machine.py <../examples/ch06_turing_machine.py>`
     - :doc:`ch06_theory_of_computation`
     - 2 進数に 1 を加えるチューリングマシンをシミュレートし、テープとヘッドの様子を表示する。
   * - :download:`ch07_calc_interpreter.py <../examples/ch07_calc_interpreter.py>`
     - :doc:`ch07_programming_languages`
     - 四則演算の式を字句解析し、再帰下降構文解析で抽象構文木を作って評価する。
   * - :download:`ch07_generics.py <../examples/ch07_generics.py>`
     - :doc:`ch07_programming_languages`
     - Python 3.12 の型パラメータ構文によるジェネリックな関数とクラスを定義し、mypy の検査が通ることを示す。
   * - :download:`ch08_scheduler.py <../examples/ch08_scheduler.py>`
     - :doc:`ch08_operating_systems`
     - FCFS・SJF・ラウンドロビンの各スケジューリングで、実行順序と平均待ち時間を比較する。
   * - :download:`ch09_race_condition.py <../examples/ch09_race_condition.py>`
     - :doc:`ch09_concurrency_and_io`
     - 複数のスレッドで共有カウンタを更新し、ロックが無いと更新が失われることと、ロックで防げることを示す。
   * - :download:`ch08_page_replacement.py <../examples/ch08_page_replacement.py>`
     - :doc:`ch08_operating_systems`
     - FIFO・LRU・最適置換のページフォールト回数を比較し、Belady の異常を示す。
   * - :download:`ch09_producer_consumer.py <../examples/ch09_producer_consumer.py>`
     - :doc:`ch09_concurrency_and_io`
     - queue.Queue と threading.Condition で生産者・消費者問題を解く。
   * - :download:`ch09_asyncio_echo.py <../examples/ch09_asyncio_echo.py>`
     - :doc:`ch09_concurrency_and_io`
     - asyncio で localhost のエコーサーバと複数のクライアントを動かし、逐次実行と並行実行の所要時間を比較する。
   * - :download:`ch10_tcp_echo.py <../examples/ch10_tcp_echo.py>`
     - :doc:`ch10_networks`
     - localhost 上の TCP エコーサーバとクライアントを同じプロセス内で動かす。
   * - :download:`ch10_http_get.py <../examples/ch10_http_get.py>`
     - :doc:`ch10_networks`
     - ローカルの HTTP サーバに socket で HTTP/1.1 の GET リクエストを送り、レスポンスを表示する。
   * - :download:`ch10_subnet.py <../examples/ch10_subnet.py>`
     - :doc:`ch10_networks`
     - ipaddress モジュールで、CIDR 表記のネットワークアドレス、ブロードキャストアドレス、分割、所属判定を計算する。
   * - :download:`ch11_sqlite_basics.py <../examples/ch11_sqlite_basics.py>`
     - :doc:`ch11_databases`
     - SQLite で表の作成、挿入、結合、集計、NULL の扱い、外部キー制約、プレースホルダによる SQL インジェクション対策を示す。
   * - :download:`ch11_index.py <../examples/ch11_index.py>`
     - :doc:`ch11_databases`
     - インデックスの有無による実行計画（EXPLAIN QUERY PLAN）と実行時間の違い、インデックスが効かない例を示す。
   * - :download:`ch11_transaction.py <../examples/ch11_transaction.py>`
     - :doc:`ch11_databases`
     - 送金処理をトランザクションで実行し、制約違反のときにロールバックされることを示す。
   * - :download:`ch11_join_algorithms.py <../examples/ch11_join_algorithms.py>`
     - :doc:`ch11_databases`
     - 入れ子ループ結合、インデックスを使う入れ子ループ結合、ハッシュ結合、ソートマージ結合の操作回数を比較する。
   * - :download:`ch11_optimistic_lock.py <../examples/ch11_optimistic_lock.py>`
     - :doc:`ch11_databases`
     - SQLite の 2 つの接続で、更新の喪失、悲観的ロック、楽観的ロックによる競合の検出と再試行を再現する。
   * - :download:`ch12_lamport_clock.py <../examples/ch12_lamport_clock.py>`
     - :doc:`ch12_distributed_systems`
     - 3 つのプロセスのメッセージの送受信をシミュレートし、ランポート時計の値と全順序を表示する。
   * - :download:`ch12_idempotent_retry.py <../examples/ch12_idempotent_retry.py>`
     - :doc:`ch12_distributed_systems`
     - 応答が失われる通信を模擬し、指数バックオフで再試行したときの二重処理を、冪等キーの有無で比較する。
   * - :download:`ch13_hash.py <../examples/ch13_hash.py>`
     - :doc:`ch13_security`
     - SHA-256 のハッシュ値と雪崩効果、HMAC の計算と hmac.compare_digest による検証を示す。
   * - :download:`ch14_password.py <../examples/ch14_password.py>`
     - :doc:`ch14_application_security`
     - ソルト付きの PBKDF2 と scrypt で、パスワードの保存と照合を行う。
   * - :download:`ch13_toy_rsa.py <../examples/ch13_toy_rsa.py>`
     - :doc:`ch13_security`
     - 小さな素数を使った教科書的な RSA で、鍵生成、暗号化、復号、署名、検証を示す（学習用）。
   * - :download:`ch14_jwt.py <../examples/ch14_jwt.py>`
     - :doc:`ch14_application_security`
     - 標準ライブラリだけで HS256 の JWT を作成・検証し、改ざんや期限切れを検出する（学習用）。
   * - :download:`ch13_random.py <../examples/ch13_random.py>`
     - :doc:`ch13_security`
     - random の再現性と予測可能性を示し、secrets によるトークンの生成と比較する。
