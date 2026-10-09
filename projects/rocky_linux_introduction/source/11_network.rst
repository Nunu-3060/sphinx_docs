.. _ch-network:

ネットワーク
============

この章では、:term:`NetworkManager` によるネットワークの設定、名前解決、疎通確認、サーバー間のファイル転送を説明します。ファイアウォールの設定は「:ref:`ch-security`」で説明します。

NetworkManager の基本
---------------------

Rocky Linux では、NetworkManager がネットワークの設定を管理します。NetworkManager は、次の 2 つの概念でネットワークを扱います。

.. list-table:: デバイスと接続
   :header-rows: 1
   :widths: 20 80

   * - 用語
     - 意味
   * - デバイス
     - ネットワークインターフェイス（``enp1s0`` など）そのもの
   * - 接続（コネクション）
     - デバイスに適用する設定（IP アドレス、ゲートウェイ、DNS サーバーなど）の組

1 つのデバイスに対して複数の接続を作成しておき、切り替えて使うこともできます。設定は ``nmcli`` コマンドで行います。

.. code-block:: console
   :linenos:

   $ nmcli device status
   DEVICE  TYPE      STATE                   CONNECTION
   enp1s0  ethernet  connected               enp1s0
   lo      loopback  connected (externally)  lo
   $ nmcli connection show
   $ nmcli connection show enp1s0

3 行目の ``CONNECTION`` 列が、デバイスに適用されている接続の名前です。インストール時に作成された接続は、デバイスと同じ名前になっています。

現在の IP アドレスと経路は ``ip`` コマンドで確認します。

.. code-block:: console
   :linenos:

   $ ip address show
   $ ip route show
   default via 192.168.10.1 dev enp1s0 proto static metric 100
   192.168.10.0/24 dev enp1s0 proto kernel scope link src 192.168.10.20 metric 100

``default via`` の行がデフォルトゲートウェイです。

.. note::

   ``ifconfig`` や ``netstat`` などの古いコマンドは、最小構成には含まれていません。本書では、後継の ``ip`` と ``ss`` を使います。

IP アドレスの固定
-----------------

インストール時は DHCP で IP アドレスを取得する設定になっています。サーバーとして使う場合は、IP アドレスを固定するのが一般的です。

.. code-block:: console
   :linenos:

   $ sudo nmcli connection modify enp1s0 \
       ipv4.method manual \
       ipv4.addresses 192.168.10.20/24 \
       ipv4.gateway 192.168.10.1 \
       ipv4.dns "192.168.10.1 8.8.8.8"
   $ sudo nmcli connection up enp1s0

``modify`` で接続の設定を変更し、``up`` で変更を反映します。SSH で接続している場合、IP アドレスを変更すると接続が切れるため、新しい IP アドレスで接続し直してください。設定を誤ると接続できなくなるため、仮想マシンのコンソールから操作するのが安全です。

DHCP に戻すには、``ipv4.method auto`` を指定し、``ipv4.addresses``、``ipv4.gateway``、``ipv4.dns`` を空にします。

対話的に設定したい場合は、メニュー形式で操作できる ``nmtui`` コマンドも使えます。

keyfile 形式の設定ファイル
--------------------------

NetworkManager の接続の設定は、``/etc/NetworkManager/system-connections/`` に :term:`keyfile` 形式のファイル（拡張子 ``.nmconnection``）として保存されます。``nmcli`` で変更すると、このファイルが更新されます。

Rocky Linux 9 以前で使われていた ``/etc/sysconfig/network-scripts/ifcfg-*`` 形式のファイルは、Rocky Linux 10 では使えません（「:ref:`sec-rocky10-changes`」を参照）。古い資料の手順を参考にする場合は注意してください。

次に、固定 IP アドレスを設定する keyfile の例を示します。多数のサーバーに同じ形式の設定を配布する場合などに、ファイルを直接作成する方法が便利です。

.. literalinclude:: ../examples/network/static-ip.nmconnection
   :language: ini
   :linenos:
   :caption: static-ip.nmconnection

:download:`static-ip.nmconnection をダウンロード <../examples/network/static-ip.nmconnection>`

ファイルを配置したら、NetworkManager に読み込ませて接続を有効にします。

.. code-block:: console
   :linenos:

   $ sudo install -m 600 static-ip.nmconnection /etc/NetworkManager/system-connections/
   $ sudo nmcli connection reload
   $ sudo nmcli connection up static-ip

ファイルのパーミッションが ``600`` でない場合、パスワードなどの機密情報を含む可能性があるため、NetworkManager はそのファイルを読み込みません。

同じデバイス（この例では ``enp1s0``）を対象とする接続が他にもあると、どちらが使われるかが分かりにくくなります。新しい接続が有効になったことを確認したら、``sudo nmcli connection delete enp1s0`` のように、不要になった接続を削除してください。

名前解決
--------

ホスト名から IP アドレスを求める処理を名前解決と呼びます。Rocky Linux では、次の順序で名前解決を行います（``/etc/nsswitch.conf`` の ``hosts`` の行で設定されています）。

1. ``/etc/hosts`` に記述されたホスト名と IP アドレスの対応
2. DNS サーバーへの問い合わせ

DNS サーバーの設定は ``/etc/resolv.conf`` に書かれていますが、このファイルは NetworkManager が自動で生成するため、直接編集しても上書きされます。DNS サーバーは、前節のように NetworkManager の接続の設定（``ipv4.dns``）で変更してください。

名前解決の結果は次のコマンドで確認できます。

.. code-block:: console
   :linenos:

   $ getent hosts www.example.com
   $ sudo dnf install bind-utils
   $ dig www.example.com

``getent hosts`` は ``/etc/hosts`` と DNS の両方を使って名前解決します。``dig`` は DNS サーバーに直接問い合わせ、詳細な応答を表示します。``dig`` を使うには ``bind-utils`` パッケージが必要です。

疎通確認
--------

ネットワークの問題を調べるときに使う主なコマンドを次に示します。

.. list-table:: 疎通確認に使うコマンド
   :header-rows: 1
   :widths: 35 65

   * - コマンド
     - 用途
   * - ``ping -c 4 <宛先>``
     - 宛先に ICMP のパケットを送り、応答があるかを確認する
   * - ``tracepath <宛先>``
     - 宛先までの経路（経由するルーター）を表示する
   * - ``ss -tlnp``
     - 待ち受けている TCP のポートと、そのプロセスを表示する
   * - ``ss -tn``
     - 確立している TCP の接続を表示する
   * - ``curl -I http://<宛先>/``
     - HTTP でアクセスし、応答のヘッダーを表示する

``ss -tlnp`` は、サーバーのプログラムが正しくポートを待ち受けているかを確認するときによく使います。

.. code-block:: console
   :linenos:

   $ sudo ss -tlnp
   State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
   LISTEN  0       128           0.0.0.0:22         0.0.0.0:*      users:(("sshd",pid=812,fd=3))
   LISTEN  0       511           0.0.0.0:80         0.0.0.0:*      users:(("nginx",pid=1520,fd=6))

``Local Address`` が ``0.0.0.0`` の場合はすべての IP アドレスで、``127.0.0.1`` の場合はサーバー自身からの接続だけを待ち受けています。ネットワークが通じない場合の切り分けの手順は「:ref:`ch-troubleshooting`」で説明します。

.. _sec-file-transfer:

ファイル転送
------------

SSH を使って、クライアント PC とサーバーの間や、サーバー同士でファイルを転送できます。いずれのコマンドも、SSH の公開鍵認証（「:ref:`sec-ssh-key`」を参照）の設定をそのまま利用します。

.. list-table:: ファイル転送のコマンド
   :header-rows: 1
   :widths: 20 80

   * - コマンド
     - 特徴
   * - ``scp``
     - 1 回のコマンドでファイルをコピーする。手軽に使える
   * - ``sftp``
     - 対話的にファイルを転送する。転送先のディレクトリを確認しながら操作できる
   * - ``rsync``
     - 差分だけを転送する。大量のファイルや、繰り返しの同期に向く

.. code-block:: console
   :linenos:

   $ scp ./app.conf admin@web01:/tmp/
   $ scp admin@web01:/var/log/nginx/access.log ./
   $ rsync -avz ./site/ admin@web01:/srv/www/example/

1 行目は手元のファイルをサーバーへ、2 行目はサーバーのファイルを手元へコピーします。3 行目は、手元のディレクトリの内容をサーバーへ同期します（``-z`` は転送時に圧縮する指定です）。

Windows 11 の PowerShell でも ``scp`` と ``sftp`` を使えます。``rsync`` は Windows には含まれていないため、Windows から転送する場合は ``scp`` を使うか、WinSCP などの GUI のツールを使ってください。
