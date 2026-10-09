.. _ch-initial-setup:

初期設定
========

この章では、インストール直後に行う初期設定を説明します。この章の内容をまとめて実行するスクリプトを章末に掲載しています。

ログインと sudo の確認
----------------------

インストール時に作成したユーザーでログインします。最初は仮想マシンのコンソールからログインし、SSH の設定が終わったらクライアント PC から接続します。

ログインしたら、管理者権限を使えることを確認します。:term:`sudo` は、許可されたユーザーが他のユーザー（通常は root）の権限でコマンドを実行するための仕組みです。

.. code-block:: console
   :linenos:

   $ id
   uid=1000(admin) gid=1000(admin) groups=1000(admin),10(wheel)
   $ sudo whoami
   [sudo] admin のパスワード:
   root

``id`` の出力に ``wheel`` が含まれ、``sudo whoami`` の結果が ``root`` であれば、管理者権限を使えます。``sudo`` を実行すると、root ではなく自分自身のパスワードを求められます。一度パスワードを入力すると、一定時間（既定では 5 分）は再入力が不要です。

システムの更新
--------------

インストールメディアに含まれるパッケージは、メディアの作成時点のものです。最初にすべてのパッケージを最新の状態に更新します。

.. code-block:: console
   :linenos:

   $ sudo dnf upgrade --refresh
   $ sudo systemctl reboot

``--refresh`` は、リポジトリの情報を強制的に最新の状態に更新するオプションです。カーネルが更新された場合は、再起動して新しいカーネルで起動する必要があります。``dnf`` の詳細は「:ref:`ch-package`」で説明します。

ホスト名の設定
--------------

ホスト名は ``hostnamectl`` コマンドで確認・変更します。変更はすぐに反映され、再起動後も維持されます。

.. code-block:: console
   :linenos:

   $ hostnamectl
   $ sudo hostnamectl set-hostname web01.example.com

ロケールとタイムゾーンの設定
----------------------------

ロケールは、メッセージの言語や日付の書式などを決める設定です。ロケールは ``localectl`` コマンドで、タイムゾーンは ``timedatectl`` コマンドで設定します。

.. code-block:: console
   :linenos:

   $ localectl status
   $ sudo localectl set-locale LANG=ja_JP.UTF-8
   $ timedatectl
   $ sudo timedatectl set-timezone Asia/Tokyo

ロケールの変更は、次にログインしたときから有効になります。

.. note::

   サーバーでは、ロケールを英語（``LANG=C.UTF-8`` や ``LANG=en_US.UTF-8``）にしておく運用もよく行われます。エラーメッセージが英語になるため、インターネットで情報を検索しやすくなるという利点があります。本書の実行例は、日本語ロケールで実行した場合の出力を示しています。

日本語環境の導入
----------------

最小構成でインストールした場合、日本語のメッセージを表示するためのデータが含まれていないことがあります。その場合は ``langpacks-ja`` パッケージを導入します。

.. code-block:: console
   :linenos:

   $ sudo dnf install langpacks-ja
   $ localectl list-locales | grep ja_JP
   ja_JP.UTF-8

``langpacks-ja`` は、日本語のロケールデータ、翻訳データ、フォントなど、日本語を扱うためのパッケージをまとめて導入するためのパッケージです。

仮想マシンのコンソールで使うキーボード配列は、次のように設定します。SSH で接続する場合は、クライアント PC 側のキーボード配列が使われるため、この設定は関係しません。

.. code-block:: console
   :linenos:

   $ sudo localectl set-keymap jp106

時刻同期の設定
--------------

サーバーの時刻がずれていると、ログの解析や、証明書の有効期限の判定などで問題が起きます。Rocky Linux では :term:`chrony` が時刻同期を行います。最小構成でも ``chronyd`` サービスが既定で有効になっています。

.. code-block:: console
   :linenos:

   $ systemctl status chronyd
   $ chronyc sources
   MS Name/IP address         Stratum Poll Reach LastRx Last sample
   ===============================================================================
   ^* ntp1.example.net              2   6   377    35   +120us[ +150us] +/-   12ms

``chronyc sources`` の出力で、行頭が ``^*`` の時刻サーバーが、現在同期している時刻サーバーです。社内の時刻サーバーを使う場合は、``/etc/chrony.conf`` にある既定の ``pool`` の行の先頭に ``#`` を付けて無効にし、次のような ``server`` の行を追加します。変更は ``sudo systemctl restart chronyd`` で反映します。

.. code-block:: text
   :linenos:
   :caption: /etc/chrony.conf に追加する行の例

   server ntp.example.com iburst

SSH による接続
--------------

サーバーの操作は、通常はクライアント PC から SSH で接続して行います。Rocky Linux では SSH サーバー（``sshd``）が既定で起動しており、ファイアウォールでも SSH が許可されています。

まず、サーバーの IP アドレスを確認します。

.. code-block:: console
   :linenos:

   $ ip -br address
   lo               UNKNOWN        127.0.0.1/8 ::1/128
   enp1s0           UP             192.168.10.20/24 fe80::5054:ff:fe12:3456/64

Windows 11 には SSH クライアントが標準で含まれています。PowerShell から次のように接続します。初回の接続時にはサーバーの鍵の指紋（フィンガープリント）が表示されるので、確認したうえで ``yes`` と入力します。

.. code-block:: powershell
   :linenos:

   PS> ssh admin@192.168.10.20

.. _sec-ssh-key:

公開鍵認証の設定
~~~~~~~~~~~~~~~~

パスワード認証よりも安全な公開鍵認証で接続できるようにします。公開鍵認証では、クライアント PC で作成した鍵のペアのうち、公開鍵をサーバーに登録し、秘密鍵はクライアント PC で厳重に保管します。

1. クライアント PC で鍵のペアを作成します。パスフレーズ（秘密鍵を保護するパスワード）を設定することをお勧めします。

   .. code-block:: powershell
      :linenos:

      PS> ssh-keygen -t ed25519

   ``C:\Users\<ユーザー名>\.ssh\`` に、秘密鍵 ``id_ed25519`` と公開鍵 ``id_ed25519.pub`` が作成されます。

2. 公開鍵をサーバーの ``~/.ssh/authorized_keys`` に追加します。Windows には、Linux の ``ssh-copy-id`` に相当するコマンドがないため、次のように実行します。

   .. code-block:: powershell
      :linenos:

      PS> Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | ssh admin@192.168.10.20 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

   クライアントが Linux や macOS の場合は、``ssh-copy-id admin@192.168.10.20`` で同じことができます。

3. もう一度 ``ssh admin@192.168.10.20`` で接続し、サーバーのパスワードではなく、鍵のパスフレーズを求められることを確認します。

接続先が多い場合は、クライアント PC の ``~/.ssh/config`` （Windows では ``C:\Users\<ユーザー名>\.ssh\config``）に接続情報を書いておくと、``ssh web01`` のように短い名前で接続できます。

.. code-block:: text
   :linenos:
   :caption: ~/.ssh/config の例

   Host web01
       HostName 192.168.10.20
       User admin
       IdentityFile ~/.ssh/id_ed25519

パスワード認証を禁止するなど、SSH サーバー側の設定を強化する方法は「:ref:`ch-security`」で説明します。

.. _sec-proxy:

プロキシ環境での設定
--------------------

社内ネットワークなど、インターネットへの接続にプロキシサーバーを経由する必要がある環境では、各ツールにプロキシサーバーを設定する必要があります。

多くのコマンド（``curl`` など）は、環境変数 ``http_proxy`` と ``https_proxy`` を参照します。全ユーザーに設定するには、``/etc/profile.d/`` に次のようなファイルを作成します。

.. code-block:: bash
   :linenos:
   :caption: /etc/profile.d/proxy.sh

   export http_proxy="http://proxy.example.com:8080"
   export https_proxy="http://proxy.example.com:8080"
   export no_proxy="localhost,127.0.0.1,.example.com"
   export HTTP_PROXY="${http_proxy}"
   export HTTPS_PROXY="${https_proxy}"
   export NO_PROXY="${no_proxy}"

ツールによって小文字と大文字のどちらの環境変数を参照するかが異なるため、両方を設定しています。``no_proxy`` には、プロキシサーバーを経由せずに直接接続する宛先を指定します。

ただし、次のツールは環境変数とは別にプロキシサーバーを設定する必要があります。

* ``dnf``: ``/etc/dnf/dnf.conf`` に設定します（「:ref:`sec-dnf-proxy`」を参照）。
* ``sudo`` で実行するコマンド: ``sudo`` は安全のために多くの環境変数を引き継がないため、上記の環境変数が使われない場合があります。
* systemd のサービス: ログイン時に読み込まれる ``/etc/profile.d/`` の設定は使われません。サービスごとに ``Environment=`` で設定します（「:ref:`ch-process-service`」を参照）。

初期設定のスクリプト
--------------------

この章で説明した設定のうち、システムの更新、ホスト名、ロケール、タイムゾーン、時刻同期の設定をまとめて行うスクリプトを示します。

.. literalinclude:: ../examples/shell/initial_setup.sh
   :language: bash
   :linenos:
   :caption: initial_setup.sh

:download:`initial_setup.sh をダウンロード <../examples/shell/initial_setup.sh>`
