サンプルコード一覧
==================

本書のサンプルコードの一覧です。ファイル名のリンクからダウンロードできます。どのファイルも Python 3.10 以降の標準ライブラリだけで動作し、Linux、macOS、Windows のいずれでも ``python transfer_time.py`` のように実行できます。

第 1 部 ネットワーク
--------------------

.. list-table:: 第 1 部のサンプルコード
   :header-rows: 1
   :widths: 28 24 36 12

   * - ファイル
     - 関連する章
     - 内容
     - インターネット接続
   * - :download:`transfer_time.py <../examples/transfer_time.py>`
     - :doc:`n01_network_overview`
     - 帯域幅と遅延からの転送時間の計算と、帯域幅遅延積
     - 不要
   * - :download:`subnet_calc.py <../examples/subnet_calc.py>`
     - :doc:`n04_internet_layer`
     - ``ipaddress`` モジュールによるサブネットと CIDR の計算
     - 不要
   * - :download:`routing_table.py <../examples/routing_table.py>`
     - :doc:`n04_internet_layer`
     - 最長一致によるルーティングテーブルの検索
     - 不要
   * - :download:`udp_echo.py <../examples/udp_echo.py>`
     - :doc:`n05_transport_layer`
     - パケットの損失を模擬した UDP のエコーサーバーと、タイムアウトで再送するクライアント
     - 不要
   * - :download:`congestion_sim.py <../examples/congestion_sim.py>`
     - :doc:`n05_transport_layer`
     - TCP の輻輳制御（スロースタートと AIMD）のシミュレーター
     - 不要
   * - :download:`dns_query.py <../examples/dns_query.py>`
     - :doc:`n06_dns`
     - DNS の問い合わせメッセージの組み立てと、応答の解析
     - 必要
   * - :download:`http_raw_client.py <../examples/http_raw_client.py>`
     - :doc:`n07_http`
     - ソケットによる生の HTTP/1.1 リクエストの送信
     - 不要
   * - :download:`tls_inspect.py <../examples/tls_inspect.py>`
     - :doc:`n08_network_security`
     - TLS のバージョン、暗号スイート、証明書の内容の表示
     - 必要
   * - :download:`tcp_echo_server.py <../examples/tcp_echo_server.py>`
     - :doc:`n09_socket_programming`
     - 基本の TCP エコーサーバー（Ctrl+C で終了）
     - 不要
   * - :download:`tcp_echo_client.py <../examples/tcp_echo_client.py>`
     - :doc:`n09_socket_programming`
     - TCP エコーサーバーに接続するクライアント
     - 不要
   * - :download:`framing.py <../examples/framing.py>`
     - :doc:`n09_socket_programming`
     - 長さの前置によるメッセージのフレーミング
     - 不要
   * - :download:`asyncio_chat_server.py <../examples/asyncio_chat_server.py>`
     - :doc:`n09_socket_programming`
     - ``asyncio`` による複数クライアント対応のチャットサーバー
     - 不要
   * - :download:`port_check.py <../examples/port_check.py>`
     - :doc:`n10_network_troubleshooting`
     - タイムアウト付きの接続によるポートの疎通確認
     - 不要（外部のホストを調べる場合は必要）

第 2 部 分散システム
--------------------

.. list-table:: 第 2 部のサンプルコード
   :header-rows: 1
   :widths: 28 24 36 12

   * - ファイル
     - 関連する章
     - 内容
     - インターネット接続
   * - :download:`lamport_clock.py <../examples/lamport_clock.py>`
     - :doc:`d03_time_and_order`
     - ランポート時計と、それによるイベントの全順序
     - 不要
   * - :download:`vector_clock.py <../examples/vector_clock.py>`
     - :doc:`d03_time_and_order`
     - ベクトル時計による因果関係と並行性の判定
     - 不要
   * - :download:`retry_backoff.py <../examples/retry_backoff.py>`
     - :doc:`d04_communication`
     - 指数バックオフとジッターによるリトライと、冪等キーによる重複の排除
     - 不要
   * - :download:`quorum_sim.py <../examples/quorum_sim.py>`
     - :doc:`d05_replication`
     - リーダーレスレプリケーションとクォーラムによる読み書き
     - 不要
   * - :download:`consistent_hash.py <../examples/consistent_hash.py>`
     - :doc:`d07_partitioning`
     - 剰余による割り当てとコンシステントハッシュの比較
     - 不要
   * - :download:`two_phase_commit.py <../examples/two_phase_commit.py>`
     - :doc:`d08_consensus`
     - 2 相コミットと、コーディネーターの故障による阻塞
     - 不要
   * - :download:`raft_election.py <../examples/raft_election.py>`
     - :doc:`d08_consensus`
     - Raft のリーダー選出のシミュレーター
     - 不要
   * - :download:`circuit_breaker.py <../examples/circuit_breaker.py>`
     - :doc:`d09_reliability`
     - サーキットブレーカーの状態遷移
     - 不要

各ファイルの内容は、関連する章の本文で行番号付きで閲覧できます。

コードの品質について
--------------------

すべてのサンプルコードには型ヒントを記述しています。また、次のコマンドで、PEP 8 に従っていること、および型の誤りがないことを確認しています。

.. code-block:: console
   :linenos:

   $ flake8 examples
   $ mypy --strict examples
