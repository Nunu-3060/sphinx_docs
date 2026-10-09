.. _ch-log-monitoring:

ログと監視
==========

この章では、ログの確認方法、リソースの監視、Web ブラウザーからサーバーを管理できる :term:`Cockpit`、性能の調整（:term:`tuned` と sysctl）、障害時の情報収集（:term:`sos report`）を説明します。

ログの仕組み
------------

Rocky Linux では、次の 2 つの仕組みでログを記録しています。

.. list-table:: ログを記録する仕組み
   :header-rows: 1
   :widths: 20 80

   * - 仕組み
     - 内容
   * - :term:`journald`
     - systemd に含まれるログの仕組み。カーネル、サービス、アプリケーションのログをまとめてバイナリ形式で保存し、``journalctl`` コマンドで検索する
   * - rsyslog
     - journald が受け取ったログを、従来どおりテキストファイル（``/var/log/messages`` など）に書き出す

journald と rsyslog には同じログが記録されるため、用途に応じて使い分けます。条件を指定した検索には ``journalctl``、``grep`` などのテキスト処理のコマンドとの組み合わせや、従来のツールとの連携にはテキストファイルが便利です。

journalctl によるログの確認
---------------------------

``journalctl`` の主な使い方を次に示します。一般ユーザーが他のユーザーやシステムのログを読むには、``sudo`` を付けるか、``wheel`` グループまたは ``systemd-journal`` グループに所属している必要があります。

.. list-table:: journalctl の主なオプション
   :header-rows: 1
   :widths: 40 60

   * - コマンド
     - 動作
   * - ``journalctl -e``
     - 最新のログを表示する（末尾にジャンプする）
   * - ``journalctl -f``
     - 新しいログを表示し続ける
   * - ``journalctl -u <サービス>``
     - 指定したサービスのログを表示する
   * - ``journalctl -b``
     - 今回の起動以降のログを表示する。``-b -1`` で前回の起動時のログを表示する
   * - ``journalctl -p err``
     - 優先度が err（エラー）以上のログだけを表示する
   * - ``journalctl --since "1 hour ago"``
     - 指定した日時以降のログを表示する。``--until`` で終了の日時も指定できる
   * - ``journalctl -k``
     - カーネルのログを表示する
   * - ``journalctl -o json``
     - JSON 形式で表示する。プログラムで処理する場合に使う

これらのオプションは組み合わせて使えます。次の例では、今回の起動以降の nginx のエラーを表示しています。

.. code-block:: console
   :linenos:

   $ journalctl -u nginx -b -p err

前回の起動時のログ（``-b -1``）を参照するには、ログがディスクに永続的に保存されている必要があります。``/var/log/journal`` ディレクトリが存在すれば永続的に保存されます。存在しない場合は、次のように作成します。

.. code-block:: console
   :linenos:

   $ sudo mkdir -p /var/log/journal
   $ sudo systemctl restart systemd-journald
   $ journalctl --list-boots

journald のログが使用しているディスク容量の確認と削減は、次のように行います。

.. code-block:: console
   :linenos:

   $ journalctl --disk-usage
   $ sudo journalctl --vacuum-size=500M

テキスト形式のログファイル
--------------------------

rsyslog が書き出す主なログファイルは次のとおりです。

.. list-table:: 主なログファイル
   :header-rows: 1
   :widths: 30 70

   * - ファイル
     - 内容
   * - ``/var/log/messages``
     - システム全体の一般的なログ
   * - ``/var/log/secure``
     - 認証に関するログ（ログイン、``sudo`` の実行など）
   * - ``/var/log/cron``
     - cron の実行のログ
   * - ``/var/log/dnf.log``
     - ``dnf`` によるパッケージの操作のログ
   * - ``/var/log/audit/audit.log``
     - 監査ログ（SELinux の拒否の記録など）。auditd が書き出す

.. code-block:: console
   :linenos:

   $ sudo tail -f /var/log/secure
   $ sudo grep "Failed password" /var/log/secure | tail

最小構成で ``/var/log/messages`` が存在しない場合は、``sudo dnf install rsyslog`` で rsyslog を導入し、``sudo systemctl enable --now rsyslog`` で起動してください。

ログローテーション
------------------

テキスト形式のログファイルは、放っておくと際限なく大きくなります。logrotate は、ログファイルを定期的に別の名前に変えて（ローテーションして）新しいファイルに切り替え、古いファイルを削除するツールです。設定は ``/etc/logrotate.conf`` と ``/etc/logrotate.d/`` 内のファイルに記述します。

自作のアプリケーションのログをローテーションする設定の例を次に示します。

.. code-block:: text
   :linenos:
   :caption: /etc/logrotate.d/myapp

   /var/log/myapp/*.log {
       # 毎日ローテーションする
       daily
       # 14 世代分を残す
       rotate 14
       # 古いログを gzip で圧縮する
       compress
       # 直前の世代は圧縮しない (アプリケーションが書き込み中の場合に備える)
       delaycompress
       # ログファイルがなくてもエラーにしない
       missingok
       # 空のログファイルはローテーションしない
       notifempty
   }

設定の誤りは、次のコマンドで実際にはローテーションせずに確認できます。

.. code-block:: console
   :linenos:

   $ sudo logrotate -d /etc/logrotate.d/myapp

リソースの監視
--------------

サーバーの負荷やリソースの使用状況を確認する主なコマンドを次に示します。

.. list-table:: リソースを確認するコマンド
   :header-rows: 1
   :widths: 30 70

   * - コマンド
     - 確認できる内容
   * - ``uptime``
     - 稼働時間と、ロードアベレージ（1 分、5 分、15 分間の平均の負荷）
   * - ``top``
     - CPU とメモリの使用状況、プロセスごとの使用量（「:ref:`ch-process-service`」を参照）
   * - ``free -h``
     - メモリとスワップの使用量
   * - ``df -h``
     - ファイルシステムの使用量
   * - ``vmstat 5``
     - 5 秒ごとの CPU、メモリ、ディスク I/O の状況
   * - ``iostat -x 5``
     - 5 秒ごとのディスクごとの I/O の状況（``sysstat`` パッケージが必要）
   * - ``sar``
     - 過去のリソースの使用状況（``sysstat`` パッケージが必要）

``free -h`` の出力では、``free`` 列ではなく ``available`` 列を見て、メモリに余裕があるかを判断します。Linux は空いているメモリをファイルのキャッシュとして積極的に使うため、``free`` 列の値は通常小さくなります。

.. code-block:: console
   :linenos:

   $ free -h
                  total        used        free      shared  buff/cache   available
   Mem:           3.6Gi       812Mi       1.2Gi        12Mi       1.9Gi       2.8Gi
   Swap:          4.0Gi          0B       4.0Gi

過去の使用状況を確認できるようにするには、``sysstat`` を導入して記録を有効にします。既定では 10 分ごとに記録されます。

.. code-block:: console
   :linenos:

   $ sudo dnf install sysstat
   $ sudo systemctl enable --now sysstat
   $ sar -u
   $ sar -r

``sar -u`` は CPU の、``sar -r`` はメモリの使用状況の記録を表示します。

Cockpit による Web 管理
-----------------------

Cockpit は、Web ブラウザーからサーバーの状態を確認したり、管理作業を行ったりできるツールです。リソースの使用状況のグラフ、ログの検索、サービスの操作、ストレージやネットワークの設定、端末の操作などを、GUI で行えます。

.. code-block:: console
   :linenos:

   $ sudo dnf install cockpit
   $ sudo systemctl enable --now cockpit.socket

クライアント PC の Web ブラウザーで ``https://<サーバーの IP アドレス>:9090/`` にアクセスし、サーバーのユーザー名とパスワードでログインします。既定の firewalld の ``public`` ゾーンでは Cockpit が許可されているため、ファイアウォールの設定は不要です。証明書は自己署名のものが使われるため、初回のアクセス時に Web ブラウザーが警告を表示します。

Cockpit では管理者権限が必要な操作も行えるため、インターネットから直接アクセスできる状態にしないでください。アクセスできるネットワークを限定する方法は「:ref:`ch-security`」を参照してください。

tuned による性能の調整
----------------------

tuned は、サーバーの用途に合わせて、カーネルやデバイスの設定をまとめて調整するサービスです。用途ごとに「プロファイル」が用意されており、選ぶだけで適切な設定が適用されます。

.. code-block:: console
   :linenos:

   $ tuned-adm active
   Current active profile: virtual-guest
   $ tuned-adm list
   $ tuned-adm recommend
   $ sudo tuned-adm profile throughput-performance

.. list-table:: 主な tuned のプロファイル
   :header-rows: 1
   :widths: 35 65

   * - プロファイル
     - 用途
   * - ``balanced``
     - 性能と消費電力のバランスを取る
   * - ``throughput-performance``
     - 処理能力（スループット）を重視する。物理サーバーの多くの用途に向く
   * - ``virtual-guest``
     - 仮想マシンの中で動かす場合に向く
   * - ``powersave``
     - 消費電力を抑える

インストール時に、環境に合ったプロファイルが自動で選ばれています。通常は変更する必要はありません。

.. _sec-sysctl:

sysctl によるカーネルパラメーターの調整
---------------------------------------

sysctl は、実行中のカーネルの動作を調整するパラメーターです。「:ref:`sec-kernel-param`」で説明した起動時のカーネルパラメーターとは異なり、再起動せずに変更できます。

.. code-block:: console
   :linenos:

   $ sysctl net.ipv4.ip_forward
   net.ipv4.ip_forward = 0
   $ sudo sysctl -w net.ipv4.ip_forward=1

``sysctl -w`` による変更は再起動すると元に戻ります。永続的に変更するには、``/etc/sysctl.d/`` に設定ファイルを作成し、``sysctl --system`` で反映します。

.. code-block:: text
   :linenos:
   :caption: /etc/sysctl.d/90-custom.conf

   # IP パケットの転送を有効にする (ルーターとして使う場合)
   net.ipv4.ip_forward = 1

.. code-block:: console
   :linenos:

   $ sudo sysctl --system

tuned もプロファイルに従って sysctl の値を設定します。tuned と同じパラメーターを ``/etc/sysctl.d/`` で設定すると、どちらの値が使われるかが分かりにくくなるため、変更したパラメーターは記録しておいてください。

.. _sec-sos-report:

sos report による情報収集
-------------------------

sos report は、障害の調査に必要なシステムの情報（設定ファイル、ログ、コマンドの出力など）をまとめて収集し、1 つのファイルに保存するツールです。コミュニティや保守を依頼している業者に問い合わせる際に、このファイルを提出すると調査がスムーズに進みます。

.. code-block:: console
   :linenos:

   $ sudo dnf install sos
   $ sudo sos report

実行すると、収集した情報が ``/var/tmp/`` に圧縮ファイルとして保存されます。収集した情報には、ホスト名、IP アドレス、設定ファイルの内容など、外部に出すべきでない情報が含まれる場合があります。提出する前に内容を確認してください。``sos report --clean`` を指定すると、IP アドレスやホスト名などを別の値に置き換えて匿名化できます。
