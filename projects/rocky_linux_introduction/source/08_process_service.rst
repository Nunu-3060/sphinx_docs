.. _ch-process-service:

プロセスとサービスの管理
========================

この章では、実行中のプログラム（プロセス）を確認・操作する方法と、:term:`systemd` を使ってサービスを管理する方法を説明します。

プロセスの確認
--------------

実行中のプログラムをプロセスと呼びます。各プロセスには、プロセス ID（:term:`PID`）という番号が割り当てられます。

プロセスの一覧は ``ps`` コマンドで表示します。

.. code-block:: console
   :linenos:

   $ ps aux
   USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
   root           1  0.0  0.4 108152 17204 ?        Ss   09:00   0:01 /usr/lib/systemd/systemd ...
   root         812  0.0  0.2  16148  9216 ?        Ss   09:00   0:00 sshd: /usr/sbin/sshd -D ...
   $ ps aux | grep nginx
   $ pgrep -a nginx

``ps aux`` は全ユーザーのすべてのプロセスを表示します。PID が 1 のプロセスは systemd で、起動時に最初に実行され、他のすべてのプロセスを管理します。特定のプロセスを探す場合は ``grep`` と組み合わせるか、``pgrep`` を使います。

CPU やメモリを多く使っているプロセスを調べるには、``top`` コマンドを使います。表示は数秒ごとに更新されます。

.. code-block:: console
   :linenos:

   $ top

``top`` の実行中に :kbd:`P` で CPU 使用率順、:kbd:`M` でメモリ使用量順に並べ替えられます。:kbd:`q` で終了します。

シグナルによるプロセスの操作
----------------------------

プロセスを停止するには、``kill`` コマンドでシグナルを送ります。シグナルは、プロセスに何らかの動作を求める通知です。

.. list-table:: 主なシグナル
   :header-rows: 1
   :widths: 20 15 65

   * - シグナル
     - 番号
     - 意味
   * - SIGTERM
     - 15
     - 終了を求める。``kill`` の既定値。プロセスは後片付けをしてから終了できる
   * - SIGKILL
     - 9
     - 強制的に終了させる。プロセスは後片付けができない
   * - SIGHUP
     - 1
     - 端末の切断を通知する。多くのデーモンは、設定ファイルの再読み込みの合図として扱う
   * - SIGINT
     - 2
     - 割り込みを通知する。:kbd:`Ctrl+C` を押したときに送られる

.. code-block:: console
   :linenos:

   $ kill 12345
   $ kill -9 12345
   $ pkill -f "python3 app.py"

1 行目は PID 12345 のプロセスに SIGTERM を送ります。SIGTERM で終了しない場合に限り、2 行目のように SIGKILL を送ります。3 行目の ``pkill -f`` は、コマンドラインが一致するプロセスにまとめてシグナルを送ります。

なお、systemd で管理しているサービスは ``kill`` ではなく、次の節で説明する ``systemctl`` で停止してください。``kill`` で停止すると、設定によっては systemd がサービスを自動で再起動します。

優先度の変更
------------

CPU を多く使う処理を実行するとき、他の処理への影響を減らすために優先度を下げられます。優先度は nice 値で表し、-20（最も高い）から 19（最も低い）までの値を取ります。既定値は 0 です。

.. code-block:: console
   :linenos:

   $ nice -n 10 tar -czf /tmp/archive.tar.gz /srv/data
   $ sudo renice -n 5 -p 12345

1 行目は nice 値を 10 にしてコマンドを実行し、2 行目は実行中のプロセスの nice 値を 5 に変更します。nice 値を下げる（優先度を上げる）には管理者権限が必要です。

ジョブ制御
----------

シェルから実行したコマンドを、バックグラウンドで実行したり、一時停止したりできます。

.. list-table:: ジョブ制御の操作
   :header-rows: 1
   :widths: 30 70

   * - 操作
     - 動作
   * - ``command &``
     - コマンドをバックグラウンドで実行する
   * - :kbd:`Ctrl+Z`
     - 実行中のコマンドを一時停止する
   * - ``jobs``
     - ジョブ（シェルから実行したコマンド）の一覧を表示する
   * - ``bg %1``
     - ジョブ 1 をバックグラウンドで再開する
   * - ``fg %1``
     - ジョブ 1 をフォアグラウンドに戻す

シェルから実行したコマンドは、ログアウトすると終了します。ログアウト後も動かし続けたい処理は、systemd のサービスとして登録するか、``tmux`` などの端末多重化ツールの中で実行してください。

systemd とユニット
------------------

systemd は、起動時に最初に実行されるプロセスで、サービスの起動・停止・監視、ログの管理、マウントなど、システム全体を管理します。systemd が管理する対象を\ :term:`ユニット`\ と呼び、種類ごとに拡張子で区別します。

.. list-table:: 主なユニットの種類
   :header-rows: 1
   :widths: 20 80

   * - 種類
     - 管理する対象
   * - ``.service``
     - サービス（常駐するプログラムや、1 回だけ実行する処理）
   * - ``.socket``
     - ソケット。接続があったときに対応するサービスを起動する
   * - ``.timer``
     - タイマー。指定した日時や間隔でサービスを起動する
   * - ``.target``
     - 複数のユニットをまとめたグループ。起動時の状態を表す（「:ref:`ch-boot-kernel`」を参照）
   * - ``.mount``
     - ファイルシステムのマウント

サービスの操作
--------------

サービスの操作には ``systemctl`` コマンドを使います。

.. list-table:: systemctl の主なサブコマンド
   :header-rows: 1
   :widths: 40 60

   * - コマンド
     - 動作
   * - ``systemctl status <サービス>``
     - 状態と直近のログを表示する
   * - ``sudo systemctl start <サービス>``
     - サービスを起動する
   * - ``sudo systemctl stop <サービス>``
     - サービスを停止する
   * - ``sudo systemctl restart <サービス>``
     - サービスを再起動する
   * - ``sudo systemctl reload <サービス>``
     - サービスを停止せずに設定を再読み込みする（対応しているサービスのみ）
   * - ``sudo systemctl enable <サービス>``
     - OS の起動時に自動で起動するようにする
   * - ``sudo systemctl disable <サービス>``
     - OS の起動時に自動で起動しないようにする
   * - ``sudo systemctl enable --now <サービス>``
     - 自動起動を有効にし、同時に起動する
   * - ``systemctl is-active <サービス>``
     - 稼働中かどうかを表示する
   * - ``systemctl list-units --type=service``
     - 読み込まれているサービスを一覧表示する
   * - ``systemctl --failed``
     - 起動に失敗したユニットを一覧表示する

``start`` と ``enable`` は独立した操作であることに注意してください。``start`` は今すぐ起動しますが、再起動後には起動しません。``enable`` は次回の起動時から自動で起動しますが、今すぐには起動しません。

.. code-block:: console
   :linenos:

   $ systemctl status sshd
   ● sshd.service - OpenSSH server daemon
        Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; preset: enabled)
        Active: active (running) since Mon 2026-10-05 09:00:12 JST; 1h 2min ago
      Main PID: 812 (sshd)

``Loaded`` の行の ``enabled`` は自動起動が有効であることを、``Active`` の行の ``active (running)`` は稼働中であることを表します。

ユニットファイル
----------------

ユニットの設定は、ユニットファイルと呼ばれるテキストファイルに記述します。ユニットファイルは次の場所に置かれます。

.. list-table:: ユニットファイルの置き場所
   :header-rows: 1
   :widths: 35 65

   * - ディレクトリ
     - 用途
   * - ``/usr/lib/systemd/system/``
     - パッケージが導入するユニットファイル。直接編集しない
   * - ``/etc/systemd/system/``
     - 管理者が作成・変更するユニットファイル。同じ名前のファイルがあると、こちらが優先される

パッケージが導入したユニットファイルの設定を変更する場合は、ファイルを直接編集するのではなく、``systemctl edit`` で差分（ドロップインファイル）を作成します。パッケージを更新しても変更が失われません。

.. code-block:: console
   :linenos:

   $ systemctl cat nginx
   $ sudo systemctl edit nginx

``systemctl edit`` を実行するとエディターが開くので、変更したい項目だけを記述して保存します。例えば、サービスにプロキシサーバーの環境変数を渡す場合は次のように記述します（「:ref:`sec-proxy`」を参照）。

.. code-block:: ini
   :linenos:

   [Service]
   Environment=https_proxy=http://proxy.example.com:8080

自作サービスの登録
------------------

自作のプログラムを systemd のサービスとして登録すると、自動起動、異常終了時の再起動、ログの記録を systemd に任せられます。次に、60 秒ごとにメッセージを出力するだけの最小のサービスの例を示します。

.. literalinclude:: ../examples/systemd/hello.service
   :language: ini
   :linenos:
   :caption: hello.service

:download:`hello.service をダウンロード <../examples/systemd/hello.service>`

ユニットファイルは ``[Unit]``、``[Service]``、``[Install]`` の 3 つのセクションで構成されます。主な項目の意味は次のとおりです。

.. list-table:: サービスのユニットファイルの主な項目
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 意味
   * - ``Description``
     - サービスの説明。``systemctl status`` などで表示される
   * - ``After``
     - 指定したユニットの後に起動する
   * - ``Type``
     - サービスの種類。``simple`` は ``ExecStart`` のプロセスがそのままサービスの本体であることを表す。1 回だけ実行して終了する処理には ``oneshot`` を使う
   * - ``ExecStart``
     - 実行するコマンド。絶対パスで指定する
   * - ``User``、``DynamicUser``
     - サービスを実行するユーザー。``DynamicUser=yes`` は、サービスの実行中だけ一時的なユーザーを割り当てる
   * - ``Restart``
     - 終了時に再起動する条件。``on-failure`` は異常終了したときだけ再起動する
   * - ``WantedBy``
     - ``enable`` したときに、どのターゲットから起動されるか。通常のサービスは ``multi-user.target`` を指定する

ユニットファイルを ``/etc/systemd/system/`` に配置し、systemd に読み込ませてから起動します。

.. code-block:: console
   :linenos:

   $ sudo cp hello.service /etc/systemd/system/
   $ sudo systemctl daemon-reload
   $ sudo systemctl enable --now hello.service
   $ journalctl -u hello.service -f

``daemon-reload`` は、ユニットファイルを追加・変更したときに必要な操作です。サービスの出力は journald に記録され、4 行目のように ``journalctl -u`` で確認できます（「:ref:`ch-log-monitoring`」を参照）。

.. _sec-systemd-timer:

systemd タイマー
----------------

決まった日時や間隔で処理を実行するには、systemd タイマーを使います。タイマーは、実行する処理を記述した ``.service`` ファイルと、実行する日時を記述した ``.timer`` ファイルの組で構成します。次に、毎日 2 時にバックアップを実行する例を示します。バックアップのスクリプト ``backup.sh`` の内容は「:ref:`ch-storage`」で説明します。

.. literalinclude:: ../examples/systemd/backup.service
   :language: ini
   :linenos:
   :caption: backup.service

.. literalinclude:: ../examples/systemd/backup.timer
   :language: ini
   :linenos:
   :caption: backup.timer

:download:`backup.service をダウンロード <../examples/systemd/backup.service>`

:download:`backup.timer をダウンロード <../examples/systemd/backup.timer>`

タイマーを有効にするときは、``.service`` ではなく ``.timer`` を ``enable`` します。

.. code-block:: console
   :linenos:

   $ sudo systemctl daemon-reload
   $ sudo systemctl enable --now backup.timer
   $ systemctl list-timers
   $ systemd-analyze calendar "*-*-* 02:00:00"

3 行目で、登録されているタイマーと次回の実行日時を確認できます。4 行目の ``systemd-analyze calendar`` は、``OnCalendar`` の書式が正しいかを検査し、次回の実行日時を表示します。

定期的な処理には、従来から使われている cron も使えます。両者の違いは次のとおりです。

.. list-table:: systemd タイマーと cron の比較
   :header-rows: 1
   :widths: 30 35 35

   * - 項目
     - systemd タイマー
     - cron
   * - 設定ファイル
     - ``.service`` と ``.timer`` の 2 つ
     - ``crontab`` の 1 行
   * - ログ
     - journald に自動で記録される
     - 出力を自分でファイルに保存する必要がある
   * - 停止中に実行できなかった処理
     - ``Persistent=true`` で起動後に実行できる
     - 実行されない
   * - 手動での実行
     - ``systemctl start`` で同じ条件で実行できる
     - コマンドを直接実行する
   * - 資源の制限
     - ``Nice`` やメモリの上限などを設定できる
     - 設定できない

新しく作成する定期処理には、管理しやすい systemd タイマーをお勧めします。
