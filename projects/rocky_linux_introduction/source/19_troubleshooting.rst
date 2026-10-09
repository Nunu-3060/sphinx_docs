.. _ch-troubleshooting:

トラブルシューティング
======================

この章では、Rocky Linux の運用でよく起きる問題と、その調べ方・直し方を説明します。

問題の切り分けの基本
--------------------

問題が起きたときは、思いつきで設定を変更するのではなく、次の手順で原因を絞り込みます。

1. **事象を正確に把握する**: 何をしたときに、どのような結果になったのかを確認します。エラーメッセージは省略せずに記録します。
2. **変更点を確認する**: 最後に正常に動いていたのはいつか、その後に何を変更したかを確認します。``dnf history`` やシェルの履歴（``history``）が役に立ちます。
3. **ログを確認する**: ``journalctl`` や、アプリケーションのログを確認します（「:ref:`ch-log-monitoring`」を参照）。
4. **範囲を絞り込む**: ネットワーク、ファイアウォール、SELinux、アプリケーションなど、どの層で問題が起きているかを 1 つずつ確認します。
5. **1 つずつ変更する**: 設定を変更するときは、一度に 1 か所だけ変更し、結果を確認します。

起動しない場合
--------------

古いカーネルで起動する
~~~~~~~~~~~~~~~~~~~~~~

カーネルの更新後に起動しなくなった場合は、起動メニューで 1 つ前のカーネルを選んで起動します（「:ref:`ch-boot-kernel`」を参照）。古いカーネルで起動できれば、新しいカーネルとハードウェアやドライバーの組み合わせに問題があると判断できます。問題が解決するまでは、``grubby --set-default`` で古いカーネルを既定にしておきます。

.. _sec-gpu-trouble:

GPU のドライバーの導入後に画面が表示されない
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NVIDIA の GPU のドライバーを導入した後や、カーネルを更新した後に、GUI のログイン画面が表示されなくなることがあります（「:ref:`ch-gpu`」を参照）。多くの場合、OS 自体は起動しているため、:kbd:`Ctrl+Alt+F3` で CUI の仮想コンソールに切り替えてログインできます。切り替えられない場合は、カーネルパラメーターに ``systemd.unit=multi-user.target`` を追加して、CUI で起動します（「:ref:`sec-kernel-param`」を参照）。

ログインしたら、次のコマンドで状態を確認します。

.. code-block:: console
   :linenos:

   $ lsmod | grep -E "nvidia|nouveau"
   $ dkms status
   $ uname -r
   $ sudo journalctl -b -k | grep -i -E "nvidia|nouveau"

主な原因と対処方法は次のとおりです。

.. list-table:: GPU のドライバーに関するよくある問題
   :header-rows: 1
   :widths: 35 65

   * - 症状
     - 対処方法
   * - ``dkms status`` に、使用中のカーネル（``uname -r``）の行がない
     - カーネルモジュールのビルドに失敗しています。``sudo dnf install kernel-devel-matched`` で使用中のカーネルに対応する ``kernel-devel`` を導入し、``sudo dkms autoinstall`` でビルドしてから再起動します
   * - ログに ``Key was rejected by service`` と表示される
     - Secure Boot の鍵が登録されていません。「:ref:`sec-gpu-secureboot`」の手順で鍵を登録します
   * - ``nvidia`` のモジュールは読み込まれているが、``nvidia-smi`` で GPU が見つからない
     - ドライバーのブランチが GPU に対応していない可能性があります。「:ref:`sec-gpu-old`」を確認します
   * - ``nouveau`` が読み込まれている
     - ``cat /proc/cmdline`` で、``nouveau.modeset=0 rd.driver.blacklist=nouveau`` が設定されているかを確認します

すぐに復旧させる必要がある場合は、起動メニューで 1 つ前のカーネルを選んで起動し（前節を参照）、原因を調べてから対処します。

/etc/fstab の誤り
~~~~~~~~~~~~~~~~~

``/etc/fstab`` に誤りがあると、マウントに失敗して緊急モードで停止することがあります（「:ref:`ch-storage`」を参照）。画面に ``You are in emergency mode`` と表示された場合、root のパスワードを入力して緊急モードのシェルに入り、次のように修正します。

.. code-block:: console
   :linenos:

   # journalctl -xb | grep -i mount
   # mount -o remount,rw /
   # vi /etc/fstab
   # systemctl daemon-reload
   # mount -a
   # systemctl reboot

緊急モードでは root としてコマンドを実行するため、プロンプトは ``#`` になります。2 行目で、読み取り専用でマウントされているルートファイルシステムを書き込みできるようにしてから、``/etc/fstab`` を修正しています。

root アカウントが無効になっている場合（Rocky Linux 10 の既定値）は、root のパスワードを入力できず、緊急モードのシェルに入れません。その場合は、次の節の ``rd.break`` を使う方法か、インストールメディアのレスキューモードを使います。

インストールメディアのレスキューモード
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

インストールメディア（ISO イメージ）から起動し、起動メニューの「Troubleshooting」→「Rescue a Rocky Linux system」を選ぶと、レスキューモードで起動します。レスキューモードでは、ディスク上のシステムを ``/mnt/sysroot`` にマウントし、修正作業を行えます。

.. code-block:: console
   :linenos:

   # chroot /mnt/sysroot
   # vi /etc/fstab
   # exit
   # reboot

1 行目の ``chroot`` は、``/mnt/sysroot`` をルートディレクトリとみなしてシェルを起動するコマンドです。以降は、ディスク上のシステムに対して通常どおりにコマンドを実行できます。

.. _sec-reset-password:

パスワードを忘れた場合
----------------------

管理者のパスワードを忘れた場合は、起動時に initramfs の段階で処理を中断し、パスワードを再設定します。この操作にはサーバーのコンソール（仮想マシンの場合は仮想マシンの画面）が必要です。

1. サーバーを再起動し、起動メニューで :kbd:`e` を押して、カーネルパラメーターの編集画面を開きます（「:ref:`sec-kernel-param`」を参照）。
2. ``linux`` から始まる行の末尾に ``rd.break`` を追加し、:kbd:`Ctrl+X` で起動します。
3. initramfs のシェルが起動したら、次のコマンドを実行します。

   .. code-block:: console
      :linenos:

      # mount -o remount,rw /sysroot
      # chroot /sysroot
      # passwd admin
      # touch /.autorelabel
      # exit
      # exit

   1 行目でディスク上のルートファイルシステムを書き込みできるようにし、2 行目でその中に入ります。3 行目で管理者ユーザー（この例では ``admin``）のパスワードを再設定します。4 行目は、次回の起動時に SELinux のラベルを付け直すための指定です。``passwd`` で ``/etc/shadow`` を書き換えるとラベルが正しくなくなり、このファイルを付けないとログインできなくなります。

4. ``exit`` を 2 回実行すると起動が再開されます。SELinux のラベルの付け直しが行われ、自動でもう一度再起動した後、新しいパスワードでログインできます。ラベルの付け直しには、ファイルの数に応じて数分かかります。

.. warning::

   この手順は、コンソールに触れられる人なら誰でもパスワードを変更できることを意味します。物理サーバーの設置場所や、仮想化基盤の管理画面へのアクセスは、適切に制限してください。

ディスクの容量不足
------------------

ディスクの空き容量がなくなると、ログが書き込めなくなったり、サービスが異常終了したりします。まず、どのファイルシステムが満杯になっているかを確認し、容量を使っているディレクトリを探します。

.. code-block:: console
   :linenos:

   $ df -h
   $ sudo du -xh --max-depth=1 / 2>/dev/null | sort -h | tail
   $ sudo du -xh --max-depth=1 /var 2>/dev/null | sort -h | tail

``du`` の ``-x`` は、別のファイルシステムに入らないようにするオプションです。容量を多く使っているディレクトリを順にたどって、原因を特定します。よくある原因と対処方法は次のとおりです。

.. list-table:: 容量不足のよくある原因
   :header-rows: 1
   :widths: 35 65

   * - 原因
     - 対処方法
   * - journald のログ
     - ``sudo journalctl --vacuum-size=500M`` で削減する
   * - アプリケーションのログ
     - logrotate を設定する（「:ref:`ch-log-monitoring`」を参照）
   * - dnf のキャッシュ
     - ``sudo dnf clean all`` で削除する
   * - 古いカーネル
     - ``sudo dnf remove --oldinstallonly`` で削除する
   * - コンテナのイメージ
     - ``podman system prune`` で使われていないイメージなどを削除する
   * - 古いバックアップ
     - 保存期間を見直す（「:ref:`sec-backup`」を参照）

ファイルを削除しても空き容量が増えない場合は、削除したファイルをプロセスがまだ開いている可能性があります。ファイルを開いているプロセスが終了するまで、ディスクの領域は解放されません。

.. code-block:: console
   :linenos:

   $ sudo dnf install lsof
   $ sudo lsof +L1

``lsof +L1`` は、削除されたが開かれたままのファイルを表示します。表示されたプロセス（サービス）を再起動すると、領域が解放されます。ログファイルを削除するときは、``rm`` ではなく、``truncate -s 0 <ファイル>`` で中身を空にする方が安全です。

容量そのものを増やす方法は「:ref:`ch-storage`」を参照してください。

ネットワークにつながらない場合
------------------------------

ネットワークの問題は、下の層から順に確認します。

.. list-table:: ネットワークの問題の確認手順
   :header-rows: 1
   :widths: 10 30 60

   * - 順序
     - 確認すること
     - コマンド
   * - 1
     - インターフェイスが有効か
     - ``ip -br link``、``nmcli device status``
   * - 2
     - IP アドレスが設定されているか
     - ``ip -br address``
   * - 3
     - デフォルトゲートウェイに届くか
     - ``ip route``、``ping -c 4 <ゲートウェイ>``
   * - 4
     - 外部の IP アドレスに届くか
     - ``ping -c 4 8.8.8.8``
   * - 5
     - 名前解決ができるか
     - ``getent hosts www.example.com``、``cat /etc/resolv.conf``
   * - 6
     - サーバーのプログラムが待ち受けているか
     - ``sudo ss -tlnp``
   * - 7
     - ファイアウォールで許可されているか
     - ``sudo firewall-cmd --list-all``

例えば、4 は成功するが 5 で失敗する場合は、DNS の設定に問題があると判断できます。外部から接続できない場合は、6 と 7 をサーバー側で確認したうえで、サーバー自身から ``curl http://localhost/`` のようにアクセスできるかを確認します。サーバー自身からはアクセスでき、外部からアクセスできない場合は、firewalld や、途中のネットワーク機器の設定を疑います。

なお、ネットワーク機器やクラウドの設定によっては ICMP が遮断されており、``ping`` に応答がなくても通信できる場合があります。``ping`` の結果だけで判断しないようにしてください。

SELinux によるアクセスの拒否
----------------------------

パーミッションは正しいのに ``Permission denied`` になる、サービスが起動しない、Web サーバーが 403 を返す、といった場合は、SELinux による拒否を疑います。次の手順で確認します。

1. 拒否の記録があるかを確認します。

   .. code-block:: console
      :linenos:

      $ sudo ausearch -m AVC -ts recent
      type=AVC msg=audit(1759712400.123:456): avc:  denied  { read } for  pid=1520 comm="nginx" name="index.html" dev="dm-0" ino=12345 scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:var_t:s0 tclass=file permissive=0

   この例では、``httpd_t`` で動作する nginx（``comm="nginx"``）が、``var_t`` のラベルが付いたファイル ``index.html`` の読み取り（``{ read }``）を拒否されています。

2. 原因と対処方法の候補を確認します。

   .. code-block:: console
      :linenos:

      $ sudo sealert -a /var/log/audit/audit.log

   ``sealert`` は ``setroubleshoot-server`` パッケージに含まれています（「:ref:`sec-selinux-log`」を参照）。

3. 表示された候補の中から、適切な対処を選びます。多くの場合、次のいずれかに当てはまります。

   * ファイルのラベルが正しくない → ``semanage fcontext`` と ``restorecon`` でラベルを設定する
   * 機能がブール値で無効になっている → ``setsebool -P`` で有効にする
   * 既定以外のポートを使っている → ``semanage port`` でポートを登録する

``sealert`` は、``audit2allow`` を使って独自のポリシーを作成する方法も提案することがあります。これはアクセスを無条件に許可するもので、他の方法で解決できない場合の最後の手段です。安易に使わないでください。

原因の調査中に、特定のプログラムだけを一時的に permissive にすることもできます。システム全体を ``setenforce 0`` にするより影響を小さくできます。

.. code-block:: console
   :linenos:

   $ sudo semanage permissive -a httpd_t
   $ sudo semanage permissive -d httpd_t

1 行目で ``httpd_t`` だけを permissive にし、調査が終わったら 2 行目で元に戻します。

パッケージの問題
----------------

``dnf`` の操作で問題が起きた場合の主な対処方法は次のとおりです。

.. list-table:: パッケージの問題と対処方法
   :header-rows: 1
   :widths: 35 65

   * - 症状
     - 対処方法
   * - リポジトリの情報を取得できない
     - ネットワークとプロキシの設定（「:ref:`sec-dnf-proxy`」を参照）を確認する。``sudo dnf clean all`` でキャッシュを削除してから再度実行する
   * - 依存関係のエラーで導入できない
     - エラーメッセージに表示されたパッケージがどのリポジトリにあるかを確認する。EPEL のパッケージの場合は CRB が有効かを確認する（「:ref:`sec-epel`」を参照）
   * - 更新後にアプリケーションが動かなくなった
     - ``dnf history`` で更新の内容を確認し、``sudo dnf history undo <番号>`` で取り消す
   * - パッケージのファイルが壊れていないか確認したい
     - ``rpm -V <パッケージ>`` で、導入時からのファイルの変更を確認する

``rpm -V`` は、パッケージに含まれるファイルのサイズ、パーミッション、内容などが、導入時から変わっていないかを確認します。設定ファイルの変更も表示されるため、意図した変更かどうかを確認してください。

それでも解決しない場合
----------------------

自分で解決できない場合は、次の方法で情報を集め、助けを求めます。

* エラーメッセージで検索します。英語のメッセージで検索すると、より多くの情報が見つかります（「:ref:`ch-initial-setup`」のロケールの注記を参照）。
* Rocky Linux のフォーラムやチャットで質問します。質問の際は、バージョン、実行したコマンド、エラーメッセージ、試したことを具体的に書きます。
* 保守契約を結んでいる場合は、「:ref:`sec-sos-report`」で情報を収集して問い合わせます。

参照先は「:ref:`appendix-references`」にまとめています。
