.. _appendix-examples:

付録 B サンプルコード一覧
=========================

本書で使用したサンプルコードの一覧です。ファイル名のリンクからダウンロードできます。各ファイルの先頭には、目的と使い方をコメントで記載しています。

シェルスクリプト
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 45 25

   * - ファイル
     - 内容
     - 掲載箇所
   * - :download:`initial_setup.sh <../examples/shell/initial_setup.sh>`
     - システムの更新、ホスト名、ロケール、タイムゾーン、時刻同期の初期設定
     - :ref:`ch-initial-setup`
   * - :download:`create_users.sh <../examples/shell/create_users.sh>`
     - CSV ファイルからのユーザーの一括作成
     - :ref:`ch-user`
   * - :download:`backup.sh <../examples/shell/backup.sh>`
     - ``/etc`` と ``/srv/www`` の日次バックアップ
     - :ref:`ch-storage`
   * - :download:`setup_nginx.sh <../examples/shell/setup_nginx.sh>`
     - nginx による Web サーバーの構築
     - :ref:`ch-nginx`

Python スクリプト
-----------------

いずれも標準ライブラリだけで書かれており、Rocky Linux 10 の ``python3`` で実行できます。flake8 と mypy（``--strict``）で問題がないことを確認しています。

.. list-table::
   :header-rows: 1
   :widths: 30 45 25

   * - ファイル
     - 内容
     - 掲載箇所
   * - :download:`system_info.py <../examples/python/system_info.py>`
     - サーバーの基本情報の収集と表示
     - :ref:`ch-python`
   * - :download:`journal_summary.py <../examples/python/journal_summary.py>`
     - journald のログの発生元と優先度ごとの集計
     - :ref:`ch-python`
   * - :download:`service_monitor.py <../examples/python/service_monitor.py>`
     - systemd のサービスの稼働状態の確認
     - :ref:`ch-python`
   * - :download:`gpu_status.py <../examples/python/gpu_status.py>`
     - NVIDIA の GPU の温度、使用率、メモリの使用量の表示と警告
     - :ref:`ch-gpu`

設定ファイル
------------

.. list-table::
   :header-rows: 1
   :widths: 30 45 25

   * - ファイル
     - 内容
     - 掲載箇所
   * - :download:`minimal.ks <../examples/kickstart/minimal.ks>`
     - 最小構成でインストールする Kickstart ファイル
     - :ref:`ch-installation`
   * - :download:`hello.service <../examples/systemd/hello.service>`
     - 自作サービスの最小の例
     - :ref:`ch-process-service`
   * - :download:`backup.service <../examples/systemd/backup.service>`
     - ``backup.sh`` を実行するサービス
     - :ref:`ch-process-service`
   * - :download:`backup.timer <../examples/systemd/backup.timer>`
     - ``backup.service`` を毎日 2 時に起動するタイマー
     - :ref:`ch-process-service`
   * - :download:`static-ip.nmconnection <../examples/network/static-ip.nmconnection>`
     - 固定 IP アドレスを設定する keyfile
     - :ref:`ch-network`
   * - :download:`web.container <../examples/podman/web.container>`
     - Quadlet で nginx のコンテナを動かす設定
     - :ref:`ch-container`
   * - :download:`example.conf <../examples/nginx/example.conf>`
     - 静的コンテンツを配信する nginx の設定
     - :ref:`ch-nginx`
   * - :download:`reverse_proxy.conf <../examples/nginx/reverse_proxy.conf>`
     - nginx をリバースプロキシとして使う設定
     - :ref:`ch-nginx`
