.. _ch-nginx:

総合演習: nginx による Web サーバーの構築
==================================================

この章では、これまでの章で学んだ内容を組み合わせて、nginx による Web サーバーを構築します。パッケージの導入、サービスの管理、firewalld、SELinux、ログの確認を、実際の作業の流れの中で使います。

構築する環境
------------

この章では、次の 3 つの機能を持つ Web サーバーを構築します。

.. list-table:: 構築する Web サーバーの機能
   :header-rows: 1
   :widths: 30 70

   * - 機能
     - 内容
   * - 静的コンテンツの配信
     - ``/srv/www/example`` に置いた HTML ファイルを ``http://www.example.com/`` で配信する
   * - HTTPS 化
     - Let's Encrypt の証明書を使い、``https://www.example.com/`` で配信する
   * - リバースプロキシ
     - ``http://app.example.com/`` へのアクセスを、同じサーバーで動くアプリケーション（127.0.0.1:8000）に転送する

ホスト名 ``www.example.com`` と ``app.example.com`` は、実際に使うホスト名に置き換えてください。社内のネットワークで試す場合は、クライアント PC の ``hosts`` ファイル（Windows では ``C:\Windows\System32\drivers\etc\hosts``）に、サーバーの IP アドレスとホスト名を登録すると、DNS を設定しなくても名前でアクセスできます。

nginx の導入と起動
------------------

nginx を導入し、起動と自動起動の設定を行います（「:ref:`ch-package`」、「:ref:`ch-process-service`」を参照）。

.. code-block:: console
   :linenos:

   $ sudo dnf install nginx
   $ sudo systemctl enable --now nginx
   $ systemctl status nginx
   $ curl -I http://localhost/

``curl`` の結果に ``HTTP/1.1 200 OK`` と表示されれば、nginx は動作しています。この時点では、nginx に付属するテストページが表示されます。

ファイアウォールの設定
----------------------

クライアント PC からアクセスできるよう、firewalld で HTTP と HTTPS を許可します（「:ref:`ch-security`」を参照）。

.. code-block:: console
   :linenos:

   $ sudo firewall-cmd --permanent --add-service=http --add-service=https
   $ sudo firewall-cmd --reload
   $ sudo firewall-cmd --list-services

クライアント PC の Web ブラウザーで ``http://<サーバーの IP アドレス>/`` にアクセスし、テストページが表示されることを確認します。

コンテンツの配置と SELinux の設定
---------------------------------

Web コンテンツを ``/srv/www/example`` に配置します。nginx の既定の公開ディレクトリは ``/usr/share/nginx/html`` ですが、パッケージが管理するディレクトリと分けておくと、管理しやすくなります。

.. code-block:: console
   :linenos:

   $ sudo mkdir -p /srv/www/example
   $ echo '<h1>nginx on Rocky Linux 10</h1>' | sudo tee /srv/www/example/index.html
   $ ls -Z /srv/www/example/index.html
   unconfined_u:object_r:var_t:s0 /srv/www/example/index.html

3 行目の結果のとおり、``/srv`` の配下に作成したファイルには ``var_t`` タイプのラベルが付いています。nginx（``httpd_t`` タイプのプロセス）はこのラベルのファイルを読めないため、このままでは nginx が 403 Forbidden のエラーを返します。Web コンテンツ用の ``httpd_sys_content_t`` タイプを設定します（「:ref:`sec-selinux`」を参照）。

.. code-block:: console
   :linenos:

   $ sudo dnf install policycoreutils-python-utils
   $ sudo semanage fcontext -a -t httpd_sys_content_t "/srv/www(/.*)?"
   $ sudo restorecon -Rv /srv/www
   $ ls -Z /srv/www/example/index.html
   unconfined_u:object_r:httpd_sys_content_t:s0 /srv/www/example/index.html

nginx の設定
------------

nginx の設定ファイルは ``/etc/nginx/nginx.conf`` です。このファイルは ``/etc/nginx/conf.d/*.conf`` を読み込むようになっているため、サイトごとの設定は ``/etc/nginx/conf.d/`` にファイルを作成して記述します。

次に、``/srv/www/example`` のコンテンツを配信する設定の例を示します。

.. literalinclude:: ../examples/nginx/example.conf
   :language: nginx
   :linenos:
   :caption: /etc/nginx/conf.d/example.conf

:download:`example.conf をダウンロード <../examples/nginx/example.conf>`

.. list-table:: 設定の主な項目
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 意味
   * - ``server``
     - 1 つのサイト（仮想ホスト）の設定のまとまり
   * - ``listen``
     - 待ち受けるポート。``[::]:80`` は IPv6 での待ち受け
   * - ``server_name``
     - このサイトとして応答するホスト名。リクエストの ``Host`` ヘッダーと照合される
   * - ``root``
     - コンテンツを置くディレクトリ
   * - ``location``
     - URL のパスごとの処理。``try_files`` は、指定した順にファイルを探し、見つからなければ 404 を返す

設定ファイルを配置したら、文法を検査してから再読み込みします。

.. code-block:: console
   :linenos:

   $ sudo nginx -t
   nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
   nginx: configuration file /etc/nginx/nginx.conf test is successful
   $ sudo systemctl reload nginx
   $ curl -H "Host: www.example.com" http://localhost/
   <h1>nginx on Rocky Linux 10</h1>

5 行目では、DNS を設定していなくても動作を確認できるよう、``-H`` で ``Host`` ヘッダーを指定しています。

ここまでの手順をまとめて実行するスクリプトを次に示します。

.. literalinclude:: ../examples/shell/setup_nginx.sh
   :language: bash
   :linenos:
   :caption: setup_nginx.sh

:download:`setup_nginx.sh をダウンロード <../examples/shell/setup_nginx.sh>`

HTTPS 化
--------

Web サイトを HTTPS で配信するには、サーバー証明書が必要です。ここでは、無償で証明書を発行する認証局である :term:`Let's Encrypt` の証明書を、``certbot`` というツールで取得します。

前提条件
~~~~~~~~

Let's Encrypt の証明書を取得するには、次の条件を満たす必要があります。

* ``www.example.com`` が、インターネットの DNS でこのサーバーのグローバル IP アドレスに名前解決できること
* インターネットからこのサーバーの 80 番ポートにアクセスできること（Let's Encrypt がドメインの所有を確認するために使う）

社内のネットワークだけで使うサーバーなど、この条件を満たせない場合は、社内の認証局で発行した証明書や、自己署名の証明書を使ってください。その場合の nginx の設定は、次の「証明書の取得」で ``certbot`` が自動で追加する設定と同じ形式で、証明書のファイルの場所を指定します。

証明書の取得
~~~~~~~~~~~~

``certbot`` と nginx 用のプラグインは EPEL で提供されています（「:ref:`sec-epel`」を参照）。

.. code-block:: console
   :linenos:

   $ sudo dnf install certbot python3-certbot-nginx
   $ sudo certbot --nginx -d www.example.com

``certbot`` を実行すると、メールアドレスの入力と利用規約への同意を求められます。証明書の取得に成功すると、``certbot`` は ``/etc/nginx/conf.d/example.conf`` に HTTPS の設定と、HTTP から HTTPS へ転送する設定を自動で追加し、nginx を再読み込みします。取得した証明書は ``/etc/letsencrypt/live/www.example.com/`` に保存されます。

証明書の自動更新
~~~~~~~~~~~~~~~~

Let's Encrypt の証明書の有効期間は短いため、定期的に更新する必要があります。EPEL の ``certbot`` パッケージには、更新を行う systemd タイマーが含まれています。

.. code-block:: console
   :linenos:

   $ sudo systemctl enable --now certbot-renew.timer
   $ systemctl list-timers certbot-renew.timer
   $ sudo certbot renew --dry-run

3 行目の ``--dry-run`` は、実際には更新せずに、更新の手順が正しく動作するかを確認します。

リバースプロキシの設定
----------------------

リバースプロキシは、クライアントからのリクエストを受け取り、背後にある別のサーバーやアプリケーションに転送する仕組みです。アプリケーションの前に nginx を置くと、HTTPS の処理、静的ファイルの配信、アクセスログの記録などを nginx に任せられます。

転送先のアプリケーションの準備
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ここでは動作確認のため、Python に標準で付属する簡易 Web サーバーを、転送先のアプリケーションとして使います。別の端末で次のコマンドを実行し、127.0.0.1 の 8000 番ポートで待ち受けます。

.. code-block:: console
   :linenos:

   $ mkdir -p ~/app && echo 'Hello from backend' > ~/app/index.html
   $ python3 -m http.server 8000 --bind 127.0.0.1 --directory ~/app

127.0.0.1 で待ち受けているため、このアプリケーションには外部から直接アクセスできず、nginx を経由した場合だけアクセスできます。

nginx の設定
~~~~~~~~~~~~

次に、``app.example.com`` へのアクセスを 127.0.0.1:8000 に転送する設定の例を示します。

.. literalinclude:: ../examples/nginx/reverse_proxy.conf
   :language: nginx
   :linenos:
   :caption: /etc/nginx/conf.d/reverse_proxy.conf

:download:`reverse_proxy.conf をダウンロード <../examples/nginx/reverse_proxy.conf>`

``proxy_pass`` で転送先を指定し、``proxy_set_header`` で元のリクエストの情報（クライアントの IP アドレスや、HTTP と HTTPS のどちらでアクセスされたか）を転送先に伝えています。

SELinux は、既定では Web サーバーが他のポートへ接続することを禁止しています。リバースプロキシとして使うには、ブール値 ``httpd_can_network_connect`` を有効にします（「:ref:`sec-selinux`」を参照）。

.. code-block:: console
   :linenos:

   $ sudo setsebool -P httpd_can_network_connect on
   $ sudo nginx -t
   $ sudo systemctl reload nginx
   $ curl -H "Host: app.example.com" http://localhost/
   Hello from backend

動作確認とトラブルシューティング
--------------------------------

構築した Web サーバーにアクセスできない場合は、次の表を参考に原因を調べてください。

.. list-table:: よくある問題と確認方法
   :header-rows: 1
   :widths: 30 35 35

   * - 症状
     - 主な原因
     - 確認方法
   * - クライアント PC から接続できない（タイムアウトする）
     - firewalld で HTTP または HTTPS が許可されていない
     - ``sudo firewall-cmd --list-services``
   * - 接続を拒否される
     - nginx が起動していない、または待ち受けていない
     - ``systemctl status nginx``、``sudo ss -tlnp``
   * - 403 Forbidden が返る
     - ファイルの SELinux のラベルまたはパーミッションが正しくない
     - ``ls -Z``、``sudo ausearch -m AVC -ts recent``
   * - 502 Bad Gateway が返る
     - 転送先のアプリケーションが動いていない、または SELinux のブール値が無効
     - ``curl http://127.0.0.1:8000/``、``getsebool httpd_can_network_connect``
   * - 意図しないサイトが表示される
     - ``server_name`` がリクエストのホスト名と一致していない
     - ``sudo nginx -T`` で読み込まれている設定を確認する

nginx のログは ``/var/log/nginx/`` に出力されます。この章の設定では、サイトごとに別のファイルにアクセスログとエラーログを出力しています。

.. code-block:: console
   :linenos:

   $ sudo tail -f /var/log/nginx/example.error.log
   $ journalctl -u nginx -e
