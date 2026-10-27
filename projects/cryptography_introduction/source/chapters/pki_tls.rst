公開鍵基盤と TLS
================

公開鍵暗号もデジタル署名も、使う公開鍵が本当に通信相手のものであることを前提としている。本章では、公開鍵とその持ち主を結び付ける仕組みである公開鍵基盤（public key infrastructure、PKI）と、本書で学んだ要素技術を組み合わせた実際のプロトコルである TLS 1.3 を扱う。

公開鍵の真正性の問題
--------------------

:doc:`key_exchange`\ で見たように、Mallory は Alice と Bob の間で公開値をすり替えることで中間者攻撃を行える。公開鍵暗号でも同じで、Alice が受け取った「Bob の公開鍵」が実は Mallory の公開鍵であれば、Alice が暗号化したメッセージは Mallory に読まれてしまう。公開鍵は秘密にする必要はないが、改ざんされてはならないのである。

公開鍵証明書
------------

この問題を解決するのが\ :term:`公開鍵証明書`\ （以下、証明書）である。証明書は、「この公開鍵の持ち主は www.example.com である」という情報に、信頼できる第三者がデジタル署名したものである。この第三者を\ :term:`認証局`\ （certification authority、CA）と呼ぶ。CA の公開鍵さえ正しく入手できていれば、CA の署名を検証することで、証明書に書かれた公開鍵が本物であると確認できる。

インターネットで使われる証明書の形式は X.509 であり、RFC 5280 [RFC5280]_ で規定されている。X.509 証明書（バージョン 3）の主な項目を\ :numref:`tbl-x509` に示す。

.. _tbl-x509:

.. list-table:: X.509 証明書の主な項目
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 内容
   * - シリアル番号
     - 発行した CA の中で証明書を一意に識別する番号
   * - 署名アルゴリズム
     - CA が証明書に署名するのに使ったアルゴリズム（ECDSA with SHA-256 など）
   * - 発行者（Issuer）
     - 証明書を発行した CA の名前
   * - 有効期間
     - 証明書が有効な期間の開始日時と終了日時
   * - 主体（Subject）
     - 公開鍵の持ち主の名前
   * - 公開鍵情報
     - 主体の公開鍵と、そのアルゴリズム
   * - 拡張
     - 主体の別名（Subject Alternative Name、SAN。Web サーバーのドメイン名はここに書く）、CA かどうか（Basic Constraints）、鍵の用途（Key Usage）など
   * - 署名
     - 上記の内容に対する CA のデジタル署名

信頼の連鎖
----------

CA の公開鍵の正しさは、どのように確認すればよいだろうか。CA の公開鍵も、さらに上位の CA が発行した証明書で保証する。こうして証明書をたどっていくと、最終的には自分自身で署名した自己署名証明書を持つルート CA に行き着く（:numref:`fig-cert-chain`）。ルート CA の証明書は、OS やブラウザにあらかじめ組み込まれており（トラストストアと呼ぶ）、利用者はそれを信頼の起点（トラストアンカー）とする。

.. _fig-cert-chain:

.. graphviz::
   :caption: 証明書チェーン
   :align: center

   digraph chain {
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb"];
       root [label="ルート CA の証明書\n（自己署名、トラストストアに格納）", fillcolor="#e8f4ea"];
       inter [label="中間 CA の証明書\n（ルート CA が署名）"];
       leaf [label="サーバー証明書\nwww.example.com\n（中間 CA が署名）", fillcolor="#fdf1e3"];
       root -> inter [label="署名"];
       inter -> leaf [label="署名"];
       root -> root [label="自己署名"];
   }

ルート CA の秘密鍵は、オフラインの専用装置で厳重に保管される。日々の証明書の発行には中間 CA を使い、万一中間 CA の秘密鍵が漏洩しても、ルート CA がその中間 CA の証明書を失効させれば対処できるようにしている。

クライアントがサーバー証明書を検証する際は、主に次の点を確認する。

#. サーバー証明書からルート CA の証明書まで、各証明書の署名が上位の CA の公開鍵で正しく検証できる。
#. ルート CA の証明書がトラストストアに含まれている。
#. 全ての証明書が有効期間内であり、失効していない。
#. 中間 CA の証明書に、CA であること（Basic Constraints）が示されている。
#. サーバー証明書の SAN に、接続しようとしているドメイン名が含まれている。

最後の確認を怠ると、正規の CA から自分のドメインの証明書を取得した攻撃者が、他のドメインになりすませてしまう。

証明書の失効
^^^^^^^^^^^^

秘密鍵が漏洩した場合など、有効期間内でも証明書を無効にしなければならないことがある。これを失効と呼ぶ。失効の確認方法には、CA が失効した証明書の一覧を公開する CRL（certificate revocation list）と、証明書ごとに状態を問い合わせる OCSP（online certificate status protocol）がある。しかし、いずれも確認の遅延やプライバシーなどの課題を抱えており、近年は証明書の有効期間を短くすることで失効の確認への依存を減らす方向に進んでいる。CA とブラウザ事業者の団体である CA/Browser Forum は、2025 年に、サーバー証明書の最大有効期間を段階的に 47 日まで短縮することを決定した。

証明書の透明性
^^^^^^^^^^^^^^

CA が誤って、あるいは攻撃を受けて不正な証明書を発行する事故も起きている。2011 年には、オランダの CA である DigiNotar が侵入を受け、google.com などの不正な証明書が発行された。このような不正を検知するため、CA が発行した全ての証明書を、誰でも監査できる追記専用の公開ログに登録させる仕組みが作られた。これを Certificate Transparency（CT）と呼ぶ。主要なブラウザは、CT ログに登録されていない証明書を受け入れない。

Python での証明書の生成と検証
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:numref:`code-inspect-cert` は、``cryptography`` ライブラリでルート CA とサーバーの証明書を作り、内容を表示して、サーバー証明書がルート CA によって発行されたことを検証する例である。

.. _code-inspect-cert:

.. literalinclude:: ../../examples/inspect_cert.py
   :language: python
   :linenos:
   :caption: inspect_cert.py

:download:`inspect_cert.py をダウンロード <../../examples/inspect_cert.py>`

TLS 1.3
-------

TLS の概要
^^^^^^^^^^

TLS（Transport Layer Security）は、TCP などの信頼性のある通信路の上で、機密性、完全性、サーバー（必要に応じてクライアント）の認証を提供するプロトコルである。HTTPS は HTTP を TLS の上で使うものである。TLS の前身である SSL から数えて何度も改訂されており、現在の最新版は 2018 年に RFC 8446 [RFC8446]_ として発行された TLS 1.3 である。

TLS 1.3 は、それまでのバージョンで問題となった多くの古い仕組みを削除した。

* RSA 鍵輸送と、固定の DH 鍵による鍵共有を廃止し、前方秘匿性のある (EC)DHE だけにした。
* CBC モードや RC4 を廃止し、暗号化を AEAD だけにした。
* ハンドシェイクの大部分を暗号化し、往復回数を 1 回（1-RTT）に減らした。

TLS 1.3 で使える暗号スイートは、``TLS_AES_128_GCM_SHA256``、``TLS_AES_256_GCM_SHA384``、``TLS_CHACHA20_POLY1305_SHA256`` などに限られる。暗号スイート名の後半のハッシュ関数は、HKDF による鍵導出などに使う。

ハンドシェイク
^^^^^^^^^^^^^^

TLS 1.3 のハンドシェイクの概略を\ :numref:`fig-tls13` に示す。``{ }`` で囲んだメッセージは、ハンドシェイクの途中で導出された鍵で暗号化されている。

.. _fig-tls13:

.. graphviz::
   :caption: TLS 1.3 のハンドシェイク（概略）
   :align: center

   digraph tls13 {
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb", width=3.6];
       c1 [label="【クライアント → サーバー】\nClientHello\n（対応する暗号スイート、key_share：ECDHE の公開鍵）"];
       s1 [label="【サーバー → クライアント】\nServerHello\n（選んだ暗号スイート、key_share：ECDHE の公開鍵）\n{EncryptedExtensions}\n{Certificate}：サーバー証明書\n{CertificateVerify}：これまでのやり取りへの署名\n{Finished}：これまでのやり取りへの MAC", fillcolor="#fdf1e3"];
       c2 [label="【クライアント → サーバー】\n{Finished}：これまでのやり取りへの MAC"];
       app [label="【双方向】\n[アプリケーションデータ]（AEAD で暗号化）", fillcolor="#e8f4ea"];
       c1 -> s1 -> c2 -> app;
   }

各ステップで行われていることは次のとおりである。

#. クライアントは ClientHello で、対応する暗号スイートと、ECDHE（X25519 など）の公開鍵を送る。
#. サーバーは ServerHello で、選んだ暗号スイートと自分の ECDHE の公開鍵を返す。この時点で双方が共有秘密を計算でき、HKDF でハンドシェイク用の鍵を導出する。以降のメッセージは暗号化される。
#. サーバーは Certificate で証明書チェーンを送り、CertificateVerify で、ここまでのハンドシェイクの内容（ECDHE の公開鍵を含む）に秘密鍵で署名する。クライアントは証明書チェーンを検証し、証明書の公開鍵で署名を検証する。これにより、ECDHE の公開鍵が中間者にすり替えられていないことが確認できる。
#. 双方が Finished で、ハンドシェイクの全内容に対する MAC（HMAC）を送り、やり取りが改ざんされていないことを確認する。
#. 以降のアプリケーションデータは、HKDF で導出したトラフィック鍵を使い、AEAD で暗号化する。

本書で学んだ要素技術との対応
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TLS 1.3 は、本書で学んだ要素技術を組み合わせて作られている。

.. list-table:: TLS 1.3 で使われる要素技術
   :header-rows: 1
   :widths: 35 35 30

   * - TLS 1.3 での役割
     - 要素技術
     - 本書の章
   * - 鍵共有
     - ECDHE（X25519、P-256）、DHE
     - 第 8 章、第 9 章
   * - サーバーの認証
     - デジタル署名（ECDSA、Ed25519、RSA-PSS）、X.509 証明書
     - 第 10 章、第 11 章
   * - 鍵の導出
     - HKDF（HMAC、SHA-256 / SHA-384）
     - 第 5 章、第 8 章
   * - ハンドシェイクの完全性
     - HMAC（Finished メッセージ）
     - 第 5 章
   * - データの暗号化
     - AEAD（AES-GCM、ChaCha20-Poly1305）
     - 第 6 章
   * - 乱数
     - 暗号論的擬似乱数生成器
     - 第 12 章

Python での TLS 接続
^^^^^^^^^^^^^^^^^^^^

Python の標準ライブラリ ``ssl`` を使うと、TLS で接続できる。``ssl.create_default_context()`` は、システムの既定のトラストストアを使った証明書チェーンの検証と、ホスト名の確認を有効にした設定を返す。次のコードは、Web サーバーに接続して、使われた TLS のバージョンと暗号スイートを表示する（実行にはインターネット接続が必要である）。

.. code-block:: python
   :linenos:

   import socket
   import ssl

   hostname = "www.python.org"
   context = ssl.create_default_context()  # 証明書の検証とホスト名の確認が有効
   with socket.create_connection((hostname, 443)) as sock:
       with context.wrap_socket(sock, server_hostname=hostname) as tls:
           print(tls.version())  # 例: TLSv1.3
           print(tls.cipher())  # 例: ('TLS_AES_256_GCM_SHA384', 'TLSv1.3', 256)
           print(tls.getpeercert()["subject"])

``context.check_hostname = False`` や ``context.verify_mode = ssl.CERT_NONE`` のように検証を無効にすると、中間者攻撃を防げなくなる。開発中のエラーを回避する目的でも、検証を無効にしたまま運用してはならない。
