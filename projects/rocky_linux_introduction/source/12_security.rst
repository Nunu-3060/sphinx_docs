.. _ch-security:

セキュリティ
============

この章では、Rocky Linux のサーバーを守るための基本的な仕組みとして、:term:`firewalld`、:term:`SELinux`、SSH の堅牢化、:term:`crypto-policies`、セキュリティアップデートの自動適用、fail2ban を説明します。特に firewalld と SELinux は、RHEL 系のディストリビューションを初めて使う人がつまずきやすい点です。仕組みを理解したうえで、無効にせずに使ってください。

firewalld
---------

firewalld は、サーバーに届く通信のうち、どれを受け入れるかを制御するファイアウォールです。Rocky Linux では既定で有効になっており、SSH などの一部のサービスを除き、外部からの接続は拒否されます。

ゾーン
~~~~~~

firewalld は、:term:`ゾーン`\ という単位で規則を管理します。ゾーンは「信頼の度合い」ごとに用意された規則の集まりで、ネットワークインターフェイスや送信元の IP アドレスをゾーンに割り当てて使います。既定のゾーンは ``public`` で、すべてのインターフェイスは特に指定しなければ ``public`` に属します。

.. code-block:: console
   :linenos:

   $ sudo firewall-cmd --get-default-zone
   public
   $ sudo firewall-cmd --list-all
   public (default, active)
     target: default
     interfaces: enp1s0
     services: cockpit dhcpv6-client ssh
     ports:
     ...

``services`` の行が、現在受け入れているサービスです。``ssh`` が含まれているため、SSH で接続できます。

規則の追加と削除
~~~~~~~~~~~~~~~~

サービスやポートを許可するには、次のようにします。

.. code-block:: console
   :linenos:

   $ sudo firewall-cmd --permanent --add-service=http
   $ sudo firewall-cmd --permanent --add-port=8080/tcp
   $ sudo firewall-cmd --reload
   $ sudo firewall-cmd --list-all

firewalld の設定には「ランタイム（現在の設定）」と「パーマネント（保存された設定）」の 2 種類があります。``--permanent`` を付けるとパーマネントの設定だけが変更されるため、3 行目の ``--reload`` でランタイムに反映します。``--permanent`` を付けずに実行すると、ランタイムの設定だけが変更され、再起動や ``--reload`` で元に戻ります。

許可を取り消すには、``--add-`` を ``--remove-`` に置き換えて実行します。サービス名として指定できる名前の一覧は、``firewall-cmd --get-services`` で確認できます。

特定のネットワークからの接続だけを許可したい場合は、送信元の IP アドレスを別のゾーンに割り当てます。次の例では、``192.168.10.0/24`` からの接続を ``internal`` ゾーンで扱い、そのゾーンでだけ Cockpit（「:ref:`ch-log-monitoring`」を参照）を許可しています。

.. code-block:: console
   :linenos:

   $ sudo firewall-cmd --permanent --zone=internal --add-source=192.168.10.0/24
   $ sudo firewall-cmd --permanent --zone=internal --add-service=cockpit
   $ sudo firewall-cmd --permanent --zone=public --remove-service=cockpit
   $ sudo firewall-cmd --reload

.. _sec-selinux:

SELinux
-------

SELinux（Security-Enhanced Linux）は、プロセスがアクセスできるファイルやポートを、あらかじめ定められたポリシーに従って制限する仕組みです。通常のパーミッションでは「どのユーザーが」アクセスできるかを制御しますが、SELinux では「どのプログラムが」何にアクセスできるかを制御します。例えば、nginx に脆弱性があって攻撃者に乗っ取られても、nginx のプロセスは Web コンテンツ以外のファイルにアクセスできないため、被害を限定できます。

動作モード
~~~~~~~~~~

SELinux には次の 3 つの動作モードがあります。Rocky Linux の既定値は ``enforcing`` です。

.. list-table:: SELinux の動作モード
   :header-rows: 1
   :widths: 20 80

   * - モード
     - 動作
   * - ``enforcing``
     - ポリシーに違反するアクセスを拒否し、ログに記録する
   * - ``permissive``
     - ポリシーに違反するアクセスを拒否せず、ログに記録だけする。問題の調査に使う
   * - ``disabled``
     - SELinux を使わない

.. code-block:: console
   :linenos:

   $ getenforce
   Enforcing
   $ sudo setenforce 0
   $ getenforce
   Permissive
   $ sudo setenforce 1

``setenforce`` による変更は一時的なもので、再起動すると ``/etc/selinux/config`` の設定に戻ります。問題が起きたときに ``setenforce 0`` で解決するかを試すのは、原因が SELinux かどうかを切り分けるのに有効ですが、調査が終わったら必ず ``setenforce 1`` で元に戻してください。

.. warning::

   インターネット上には「まず SELinux を無効にする」という手順が多く見られますが、本書では推奨しません。SELinux を無効にすると、上で述べた被害を限定する効果が失われます。次に説明する方法で、SELinux を有効にしたまま問題を解決してください。

コンテキスト（ラベル）
~~~~~~~~~~~~~~~~~~~~~~

SELinux は、すべてのファイルとプロセスに「コンテキスト」（ラベル）を付け、その組み合わせでアクセスを許可するかを判断します。コンテキストは ``-Z`` オプションで確認できます。

.. code-block:: console
   :linenos:

   $ ls -Z /usr/share/nginx/html/index.html
   system_u:object_r:httpd_sys_content_t:s0 /usr/share/nginx/html/index.html
   $ ps -eZ | grep nginx
   system_u:system_r:httpd_t:s0        1520 ?        00:00:00 nginx

コンテキストは ``:`` で区切られた 4 つの項目からなり、このうち 3 番目の「タイプ」（``httpd_sys_content_t`` や ``httpd_t``）が最も重要です。この例では、``httpd_t`` タイプで動作する nginx のプロセスが、``httpd_sys_content_t`` タイプのファイルを読むことがポリシーで許可されています。

よくある問題は、Web コンテンツを既定とは別の場所（例えば ``/srv/www``）に置いたときに、ファイルに適切なタイプが付いていないため nginx が読めない、というものです。この場合は、``semanage fcontext`` でディレクトリに付けるタイプを登録し、``restorecon`` で実際のファイルに適用します。

.. code-block:: console
   :linenos:

   $ sudo dnf install policycoreutils-python-utils
   $ sudo semanage fcontext -a -t httpd_sys_content_t "/srv/www(/.*)?"
   $ sudo restorecon -Rv /srv/www

2 行目の ``"/srv/www(/.*)?"`` は、``/srv/www`` とその配下のすべてのファイルを表す正規表現です。``chcon`` コマンドでもラベルを変更できますが、``chcon`` による変更は ``restorecon`` の実行時などに元に戻るため、``semanage fcontext`` を使ってください。

ブール値
~~~~~~~~

SELinux のポリシーには、よく使われる設定を切り替えるためのブール値（オン・オフのスイッチ）が用意されています。

.. code-block:: console
   :linenos:

   $ getsebool -a | grep httpd
   $ sudo setsebool -P httpd_can_network_connect on

2 行目は、Web サーバーが他のサーバーやポートへ接続することを許可します。nginx をリバースプロキシとして使う場合に必要です（「:ref:`ch-nginx`」を参照）。``-P`` を付けないと、再起動後に元に戻ります。

ポート
~~~~~~

SELinux は、プログラムが待ち受けられるポートも制限しています。例えば、SSH を既定の 22 番以外のポートで待ち受けるには、ポートに ``ssh_port_t`` タイプを割り当てる必要があります。

.. code-block:: console
   :linenos:

   $ sudo semanage port -l | grep ssh
   ssh_port_t                     tcp      22
   $ sudo semanage port -a -t ssh_port_t -p tcp 2222

.. _sec-selinux-log:

拒否されたアクセスの調査
~~~~~~~~~~~~~~~~~~~~~~~~

SELinux がアクセスを拒否すると、監査ログ ``/var/log/audit/audit.log`` に AVC と呼ばれる記録が残ります。

.. code-block:: console
   :linenos:

   $ sudo ausearch -m AVC -ts recent
   $ sudo dnf install setroubleshoot-server
   $ sudo sealert -a /var/log/audit/audit.log

1 行目は、最近（10 分以内）の拒否の記録を表示します。``setroubleshoot-server`` パッケージを導入すると、3 行目の ``sealert`` で、拒否の原因と解決方法の候補を分かりやすい文章で表示できます。具体的な調査の手順は「:ref:`ch-troubleshooting`」で説明します。

.. _sec-ssh-hardening:

SSH の堅牢化
------------

SSH はサーバーを操作する入口であり、インターネットに公開しているサーバーでは常に攻撃を受けます。公開鍵認証で接続できることを確認したうえで（「:ref:`sec-ssh-key`」を参照）、パスワード認証を禁止します。

SSH サーバーの設定は ``/etc/ssh/sshd_config`` に記述されていますが、このファイルを直接編集するのではなく、``/etc/ssh/sshd_config.d/`` に設定ファイルを追加します。``sshd`` は同じ項目が複数あると最初に読み込んだ値を使い、このディレクトリのファイルは名前の順に読み込まれます。既存のファイルより優先させるため、名前の先頭に小さい番号を付けます。

.. code-block:: text
   :linenos:
   :caption: /etc/ssh/sshd_config.d/01-hardening.conf

   # パスワード認証を禁止し、公開鍵認証だけを許可する
   PasswordAuthentication no
   KbdInteractiveAuthentication no
   # root でのログインを禁止する
   PermitRootLogin no
   # ログインを許可するユーザーを限定する
   AllowUsers admin alice

設定ファイルを作成したら、文法を検査してから反映します。

.. code-block:: console
   :linenos:

   $ sudo sshd -t
   $ sudo systemctl reload sshd

.. warning::

   設定を反映した後は、現在の SSH の接続を切断せずに、別のウィンドウから新しく SSH で接続できることを確認してください。設定を誤った場合でも、切断していない接続から元に戻せます。

SSH のポート番号を変更する場合は、SELinux のポートの設定（前節を参照）と、firewalld の設定も変更する必要があります。

.. _sec-crypto-policies:

システム全体の暗号化ポリシー
----------------------------

Rocky Linux では、OpenSSL、OpenSSH、GnuTLS など、暗号化を扱うライブラリやプログラムが使用できる暗号方式を、:term:`crypto-policies` という仕組みでまとめて管理しています。個々のプログラムの設定ではなく、システム全体で 1 つのポリシーを選びます。

.. list-table:: 主な暗号化ポリシー
   :header-rows: 1
   :widths: 20 80

   * - ポリシー
     - 内容
   * - ``DEFAULT``
     - 既定値。現時点で安全とされる暗号方式だけを許可する
   * - ``LEGACY``
     - 古いシステムとの互換性のため、安全性の低い古い暗号方式も許可する
   * - ``FUTURE``
     - 将来の攻撃に備え、より強い暗号方式だけを許可する
   * - ``FIPS``
     - 米国の暗号モジュールの規格である FIPS 140 に適合する暗号方式だけを許可する

.. code-block:: console
   :linenos:

   $ update-crypto-policies --show
   DEFAULT
   $ sudo update-crypto-policies --set LEGACY

古いクライアントや古い機器から SSH や HTTPS で接続できない場合、原因が crypto-policies であることがよくあります。``LEGACY`` に変更すると接続できるようになることがありますが、サーバー全体の安全性が下がります。まずはクライアント側を更新することを検討し、``LEGACY`` は一時的な回避策にとどめてください。ポリシーを変更した後は、すべてのプログラムに反映させるため、再起動することをお勧めします。

なお、``FIPS`` ポリシーを正しく使うには、インストール時から FIPS モードを有効にする必要があります。後から ``update-crypto-policies`` で ``FIPS`` に変更するだけでは、FIPS に適合したシステムにはなりません。

.. _sec-dnf-automatic:

セキュリティアップデートの自動適用
----------------------------------

「:ref:`sec-security-update`」で説明したセキュリティアップデートを、自動で適用するには ``dnf-automatic`` を使います。

.. code-block:: console
   :linenos:

   $ sudo dnf install dnf-automatic

設定ファイル ``/etc/dnf/automatic.conf`` で、適用する更新の種類と、実際に適用するかどうかを設定します。

.. code-block:: ini
   :linenos:
   :caption: /etc/dnf/automatic.conf の設定例

   [commands]
   # セキュリティの修正だけを対象にする
   upgrade_type = security
   # 更新をダウンロードするだけでなく、適用する
   apply_updates = yes

設定したら、定期実行のタイマーを有効にします。

.. code-block:: console
   :linenos:

   $ sudo systemctl enable --now dnf-automatic.timer
   $ systemctl list-timers dnf-automatic.timer

自動適用では、カーネルなど再起動が必要な更新を適用しても、自動では再起動しません。定期的に ``dnf needs-restarting -r`` で確認し、計画的に再起動してください。また、自動適用によってアプリケーションの動作が変わる可能性もあるため、重要なシステムでは、検証環境で確認してから手動で適用する運用も検討してください。

fail2ban
--------

fail2ban は、ログを監視し、認証に何度も失敗した IP アドレスからの接続を一定時間拒否するツールです。パスワード認証を禁止していても、攻撃によるログの増加や負荷を抑えられます。fail2ban は EPEL で提供されています（「:ref:`sec-epel`」を参照）。

.. code-block:: console
   :linenos:

   $ sudo dnf install fail2ban fail2ban-firewalld

設定は ``/etc/fail2ban/jail.local`` に記述します。次の例では、SSH への攻撃を対象にしています。

.. code-block:: ini
   :linenos:
   :caption: /etc/fail2ban/jail.local の設定例

   [DEFAULT]
   # 1 時間拒否する
   bantime = 1h
   # 10 分間に
   findtime = 10m
   # 5 回失敗したら拒否する
   maxretry = 5

   [sshd]
   enabled = true

.. code-block:: console
   :linenos:

   $ sudo systemctl enable --now fail2ban
   $ sudo fail2ban-client status sshd

``fail2ban-firewalld`` パッケージを導入すると、拒否の処理に firewalld が使われます。
