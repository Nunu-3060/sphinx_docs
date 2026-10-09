.. _ch-container:

コンテナ
========

この章では、Rocky Linux の標準のコンテナエンジンである :term:`Podman` の使い方を説明します。また、:term:`Quadlet` を使って、コンテナを systemd のサービスとして動かす方法も説明します。

コンテナとは
------------

コンテナは、アプリケーションとその実行に必要なライブラリや設定をまとめて、OS の他の部分から隔離された環境で動かす技術です。仮想マシンとは異なり、ホストの OS のカーネルを共有するため、軽量で素早く起動できます。

コンテナの元になる、アプリケーションと実行環境をまとめたものを\ :term:`コンテナイメージ`\ と呼びます。コンテナイメージは、Docker Hub などの「レジストリ」で配布されています。

Podman の特徴
-------------

Podman は、Docker と互換性のあるコマンド体系を持つコンテナエンジンです。Docker と比べて、次のような特徴があります。

.. list-table:: Podman の特徴
   :header-rows: 1
   :widths: 25 75

   * - 特徴
     - 内容
   * - デーモンが不要
     - Docker のように常駐するデーモンを必要とせず、``podman`` コマンドが直接コンテナを起動する
   * - :term:`rootless コンテナ`
     - 一般ユーザーの権限でコンテナを実行できる。コンテナが乗っ取られても、ホストへの影響を一般ユーザーの権限の範囲に抑えられる
   * - systemd との連携
     - Quadlet を使って、コンテナを systemd のサービスとして管理できる
   * - Docker との互換性
     - ``docker`` コマンドとほぼ同じ使い方ができる。``podman-docker`` パッケージを導入すると、``docker`` コマンドとして ``podman`` を呼び出せる

Podman の導入
-------------

.. code-block:: console
   :linenos:

   $ sudo dnf install podman
   $ podman --version
   $ podman info

コンテナの基本操作
------------------

以降の操作は、一般ユーザーで実行します（rootless コンテナ）。

イメージの取得
~~~~~~~~~~~~~~

.. code-block:: console
   :linenos:

   $ podman pull docker.io/library/nginx:stable
   $ podman images

イメージの名前は、「レジストリ/名前空間/イメージ名:タグ」の形式で、レジストリから省略せずに指定します。``nginx`` のようにレジストリを省略した短い名前を指定すると、``/etc/containers/registries.conf.d/`` に登録された別名の設定に従って取得元が決まるか、どのレジストリから取得するかを対話的に尋ねられます。取得元を明確にし、意図しないレジストリから取得するのを防ぐため、完全な名前で指定することをお勧めします。

コンテナの起動と操作
~~~~~~~~~~~~~~~~~~~~

.. code-block:: console
   :linenos:

   $ podman run -d --name web -p 8080:80 docker.io/library/nginx:stable
   $ podman ps
   $ curl -I http://localhost:8080/
   $ podman logs web
   $ podman exec -it web /bin/bash
   $ podman stop web
   $ podman rm web

.. list-table:: podman の主なサブコマンドとオプション
   :header-rows: 1
   :widths: 35 65

   * - コマンド
     - 動作
   * - ``podman run``
     - コンテナを作成して起動する。``-d`` はバックグラウンドで実行、``--name`` はコンテナの名前、``-p ホスト側:コンテナ側`` はポートの対応付け
   * - ``podman ps``
     - 実行中のコンテナを一覧表示する。``-a`` で停止中のコンテナも表示する
   * - ``podman logs``
     - コンテナの出力（ログ）を表示する
   * - ``podman exec -it <コンテナ> <コマンド>``
     - 実行中のコンテナの中でコマンドを実行する
   * - ``podman stop`` / ``podman start``
     - コンテナを停止・起動する
   * - ``podman rm``
     - コンテナを削除する
   * - ``podman rmi``
     - イメージを削除する

ホストの 8080 番ポートをファイアウォールで許可すれば（「:ref:`ch-security`」を参照）、他のコンピューターからもコンテナの nginx にアクセスできます。

ボリュームのマウント
~~~~~~~~~~~~~~~~~~~~

コンテナを削除すると、コンテナの中で作成したファイルも失われます。残しておきたいデータは、ホストのディレクトリをコンテナにマウントして保存します。

.. code-block:: console
   :linenos:

   $ mkdir -p ~/web
   $ echo '<h1>Hello from Podman</h1>' > ~/web/index.html
   $ podman run -d --name web -p 8080:80 -v ~/web:/usr/share/nginx/html:Z docker.io/library/nginx:stable
   $ curl http://localhost:8080/

3 行目の ``-v ホスト側:コンテナ側:Z`` の ``:Z`` は、ホストのディレクトリの SELinux のラベルを、コンテナから読み書きできるラベルに付け替える指定です。``:Z`` を付けないと、SELinux によってコンテナからのアクセスが拒否されます（「:ref:`sec-selinux`」を参照）。``:Z`` は、システムのディレクトリ（``/home`` や ``/etc`` など）には付けないでください。ラベルが付け替えられ、他のプログラムがそのディレクトリを使えなくなります。

rootless コンテナの注意点
-------------------------

rootless コンテナには、次のような制限があります。

* 1024 未満のポート（80 番や 443 番など）を、ホスト側で直接待ち受けられません。8080 番などの大きい番号のポートを使い、必要に応じてリバースプロキシ（「:ref:`ch-nginx`」を参照）やファイアウォールの転送の機能で 80 番からの通信を転送します。
* コンテナの中の root は、ホストでは自分自身のユーザーに対応付けられます。コンテナの中のその他のユーザーは、``/etc/subuid`` と ``/etc/subgid`` に定められた範囲の UID と GID に対応付けられます。この範囲は、``useradd`` でユーザーを作成したときに自動で割り当てられます。
* イメージとコンテナは、ユーザーごとに ``~/.local/share/containers/`` に保存されます。``sudo podman`` で扱うイメージやコンテナとは別のものです。

コンテナイメージの作成
----------------------

独自のコンテナイメージは、作成手順を記述した Containerfile（Docker の Dockerfile と同じ形式）から作成します。

.. code-block:: docker
   :linenos:
   :caption: Containerfile

   FROM docker.io/library/nginx:stable
   COPY index.html /usr/share/nginx/html/index.html

.. code-block:: console
   :linenos:

   $ podman build -t localhost/myweb:1.0 .
   $ podman run -d --name myweb -p 8081:80 localhost/myweb:1.0

Quadlet によるサービス化
------------------------

``podman run`` で起動したコンテナは、OS を再起動すると起動しません。コンテナを自動で起動し、異常終了したときに再起動するには、Quadlet を使って systemd のサービスとして管理します。

Quadlet では、コンテナの設定を ``.container`` という拡張子のファイルに記述します。systemd は、このファイルから自動でサービスのユニットファイルを生成します。次に、前節のボリュームを使った nginx のコンテナを、一般ユーザーのサービスとして動かす例を示します。

.. literalinclude:: ../examples/podman/web.container
   :language: ini
   :linenos:
   :caption: web.container

:download:`web.container をダウンロード <../examples/podman/web.container>`

``[Container]`` セクションの項目は、``podman run`` のオプションに対応しています。``%h`` はホームディレクトリを表します。

一般ユーザーのサービスとして登録する手順は次のとおりです。前節で起動したコンテナ ``web`` が残っている場合は、先に ``podman rm -f web`` で削除してください。

.. code-block:: console
   :linenos:

   $ mkdir -p ~/.config/containers/systemd
   $ cp web.container ~/.config/containers/systemd/
   $ systemctl --user daemon-reload
   $ systemctl --user start web.service
   $ systemctl --user status web.service
   $ sudo loginctl enable-linger $USER

``systemctl --user`` は、一般ユーザーのサービスを操作します。Quadlet から生成されたサービスは、``.container`` ファイルの ``[Install]`` セクションによって自動起動が設定されるため、``systemctl enable`` を実行する必要はありません（実行するとエラーになります）。

一般ユーザーのサービスは、通常はそのユーザーがログインしている間だけ動作します。6 行目の ``loginctl enable-linger`` を実行すると、ログアウトした後も動作し続け、OS の起動時にも自動で起動するようになります。

システム全体のサービスとして root で動かす場合は、``.container`` ファイルを ``/etc/containers/systemd/`` に置き、``--user`` を付けずに ``systemctl`` を実行します。

コンテナから GPU を使う方法は、「:ref:`ch-gpu`」で説明します。
