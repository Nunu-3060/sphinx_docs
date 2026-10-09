.. _ch-package:

パッケージ管理
==============

この章では、ソフトウェアの導入・更新・削除を行うパッケージ管理の仕組みと、運用で必要になるセキュリティアップデートの管理方法を説明します。

RPM と DNF
----------

Rocky Linux のソフトウェアは、:term:`RPM` 形式のパッケージとして提供されます。1 つのパッケージには、プログラムのファイルに加えて、バージョン、依存する他のパッケージ、導入時に実行する処理などの情報が含まれています。

パッケージを扱うコマンドには ``rpm`` と ``dnf`` の 2 つがあります。

.. list-table:: rpm と dnf の違い
   :header-rows: 1
   :widths: 20 80

   * - コマンド
     - 役割
   * - ``rpm``
     - 個々のパッケージファイルを導入したり、導入済みのパッケージの情報を調べたりする低レベルのコマンド。依存関係の解決は行わない
   * - ``dnf``
     - リポジトリからパッケージを取得し、依存関係を自動で解決して導入・更新・削除するコマンド。通常はこちらを使う

:term:`DNF` は、以前の RHEL 系で使われていた ``yum`` の後継です。Rocky Linux 10 でも ``yum`` コマンドは ``dnf`` の別名として残っているため、古い資料に書かれた ``yum`` のコマンドもそのまま動作します。

リポジトリの構成
----------------

リポジトリは、パッケージを配布するサーバー上の保管場所です。Rocky Linux では、次のリポジトリが標準で用意されています。

.. list-table:: Rocky Linux の主なリポジトリ
   :header-rows: 1
   :widths: 20 15 65

   * - リポジトリ
     - 既定の状態
     - 内容
   * - :term:`BaseOS`
     - 有効
     - OS の中核となるパッケージ（カーネル、systemd、基本コマンドなど）
   * - :term:`AppStream`
     - 有効
     - アプリケーション、言語処理系、データベースなどのパッケージ
   * - extras
     - 有効
     - Rocky Linux が独自に提供する追加パッケージ（``epel-release`` など）
   * - :term:`CRB`
     - 無効
     - 開発用のライブラリやツール。EPEL のパッケージの依存先として必要になることが多い

リポジトリの一覧は次のコマンドで確認できます。リポジトリの設定ファイルは ``/etc/yum.repos.d/`` にあります。

.. code-block:: console
   :linenos:

   $ dnf repolist
   $ dnf repolist --all

``--all`` を付けると、無効になっているリポジトリも表示されます。

パッケージの基本操作
--------------------

``dnf`` の主なサブコマンドを次に示します。導入・更新・削除には管理者権限が必要です。

.. list-table:: dnf の主なサブコマンド
   :header-rows: 1
   :widths: 40 60

   * - コマンド
     - 動作
   * - ``dnf search <キーワード>``
     - パッケージを名前と説明文から検索する
   * - ``dnf info <パッケージ>``
     - パッケージの詳細を表示する
   * - ``sudo dnf install <パッケージ>``
     - パッケージを導入する
   * - ``sudo dnf remove <パッケージ>``
     - パッケージを削除する
   * - ``sudo dnf upgrade``
     - 導入済みのパッケージをすべて更新する
   * - ``dnf check-update``
     - 更新できるパッケージの一覧を表示する
   * - ``dnf list --installed``
     - 導入済みのパッケージを一覧表示する
   * - ``dnf provides <ファイル>``
     - 指定したファイルを含むパッケージを探す
   * - ``dnf group list``
     - パッケージグループ（関連するパッケージの集まり）を一覧表示する
   * - ``sudo dnf group install <グループ>``
     - パッケージグループを導入する
   * - ``dnf history``
     - 過去に行った操作の履歴を表示する
   * - ``sudo dnf history undo <番号>``
     - 履歴の番号を指定して、その操作を取り消す

次の例では、``semanage`` コマンドがどのパッケージに含まれているかを調べてから導入しています。

.. code-block:: console
   :linenos:

   $ dnf provides '*/semanage'
   policycoreutils-python-utils-3.8-1.el10.noarch : SELinux policy core python utilities
   $ sudo dnf install policycoreutils-python-utils

導入済みのパッケージの情報は ``rpm`` コマンドでも調べられます。

.. code-block:: console
   :linenos:

   $ rpm -q nginx
   $ rpm -qi nginx
   $ rpm -ql nginx
   $ rpm -qf /etc/nginx/nginx.conf

上から順に、バージョンの確認、詳細情報の表示、含まれるファイルの一覧表示、指定したファイルを含むパッケージの表示です。

.. _sec-epel:

EPEL の導入
-----------

:term:`EPEL` （Extra Packages for Enterprise Linux）は、Fedora プロジェクトが提供する追加パッケージのリポジトリです。標準のリポジトリに含まれない多くのソフトウェア（``htop``、``fail2ban``、``certbot`` など）を導入できます。

EPEL のパッケージの多くは CRB リポジトリのパッケージに依存しているため、CRB を有効にしてから EPEL を導入します。

.. code-block:: console
   :linenos:

   $ sudo dnf config-manager --set-enabled crb
   $ sudo dnf install epel-release
   $ dnf repolist

EPEL は Red Hat や Rocky Linux の公式なサポート対象ではなく、ボランティアによって保守されています。業務システムで使う場合は、使用するパッケージの保守状況を確認してください。

モジュールストリームについて
----------------------------

Rocky Linux 8 と 9 では、「モジュールストリーム」という仕組みで、同じソフトウェアの複数のバージョン（例えば Node.js の 18 と 20）から使うものを選べました。この仕組みは Rocky Linux 10 で廃止され、``dnf module`` コマンドで別のバージョンに切り替える方法は使えなくなりました。

Rocky Linux 10 では、別のバージョンのソフトウェアは、通常の RPM パッケージとして提供されます。例えば Rocky Linux 10.2 では、PHP の 8.3 と 8.4 が別々のパッケージとして提供されています。提供されているバージョンは、次のように確認します。

.. code-block:: console
   :linenos:

   $ dnf repoquery php
   $ dnf search php

同じソフトウェアの複数のバージョンが提供されている場合、関連するパッケージを導入するときに、使用中のバージョンと一致するものを選ぶよう注意してください。

.. _sec-security-update:

セキュリティアップデートの管理
------------------------------

Rocky Linux では、パッケージの更新ごとに「アドバイザリー」と呼ばれる情報が公開されます。アドバイザリーには次の 3 種類があり、それぞれに識別子が付けられています。

.. list-table:: アドバイザリーの種類
   :header-rows: 1
   :widths: 20 80

   * - 識別子
     - 内容
   * - RLSA
     - セキュリティの修正（Rocky Linux Security Advisory）
   * - RLBA
     - 不具合の修正（Rocky Linux Bug Fix Advisory）
   * - RLEA
     - 機能の追加（Rocky Linux Enhancement Advisory）

適用されていないアドバイザリーは ``dnf updateinfo`` で確認できます。

.. code-block:: console
   :linenos:

   $ dnf updateinfo summary
   $ dnf updateinfo list --security
   $ dnf updateinfo info RLSA-2025:1234

1 行目で種類ごとの件数を、2 行目でセキュリティの修正の一覧を、3 行目で特定のアドバイザリーの詳細を表示します（3 行目の識別子は例です）。セキュリティの修正だけを適用するには、次のようにします。

.. code-block:: console
   :linenos:

   $ sudo dnf upgrade --security

更新後に再起動やサービスの再起動が必要かどうかは、``dnf needs-restarting`` で確認できます。

.. code-block:: console
   :linenos:

   $ sudo dnf needs-restarting -r
   $ sudo dnf needs-restarting -s

``-r`` はシステムの再起動が必要かどうかを、``-s`` は再起動が必要なサービスの一覧を表示します。

セキュリティアップデートを自動で適用する方法は「:ref:`ch-security`」で説明します。

.. _sec-upgrade-policy:

更新とアップグレードの方針
--------------------------

Rocky Linux のバージョンを上げる作業は、マイナーバージョンとメジャーバージョンで方法が大きく異なります。

マイナーバージョンの更新
~~~~~~~~~~~~~~~~~~~~~~~~

10.0 から 10.1 のようなマイナーバージョンの更新は、通常の ``sudo dnf upgrade`` で行われます。新しいマイナーバージョンが公開されると、リポジトリの内容が新しいバージョンに切り替わり、次回の ``dnf upgrade`` で自動的に更新されます。同じメジャーバージョン内では互換性が保たれるため、特別な作業は必要ありません。

Rocky Linux では、古いマイナーバージョンには修正が提供されません。必ず最新のマイナーバージョンに更新して使ってください。

メジャーバージョンのアップグレード
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rocky Linux 9 から 10 のようなメジャーバージョンのアップグレードを、稼働中のシステム上で行う方法（インプレースアップグレード）は、Rocky Linux では公式にはサポートされていません。メジャーバージョンを上げる場合は、次の手順を推奨します。

1. 新しいメジャーバージョンで新しいサーバーを構築します。
2. アプリケーションとデータを移行し、動作を確認します。
3. 新しいサーバーに切り替え、古いサーバーを停止します。

この手順を容易にするため、サーバーの構築手順をスクリプトや構成管理ツール（「:ref:`ch-next-steps`」を参照）で自動化しておくことをお勧めします。

.. _sec-dnf-proxy:

dnf のプロキシ設定
------------------

プロキシサーバーを経由してインターネットに接続する環境では、``/etc/dnf/dnf.conf`` の ``[main]`` セクションにプロキシサーバーを設定します。``dnf`` はシェルの環境変数 ``http_proxy`` などを参照しない場合があるため、必ずこのファイルに設定してください（「:ref:`sec-proxy`」を参照）。

.. code-block:: ini
   :linenos:
   :caption: /etc/dnf/dnf.conf への追加例

   [main]
   proxy=http://proxy.example.com:8080
   # 認証が必要な場合
   proxy_username=user01
   proxy_password=password

プロキシサーバーのパスワードを記述する場合は、``/etc/dnf/dnf.conf`` を一般ユーザーが読めないよう、パーミッションに注意してください。
