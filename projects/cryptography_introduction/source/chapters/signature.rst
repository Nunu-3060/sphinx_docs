デジタル署名
============

公開鍵暗号では、公開鍵で暗号化し、秘密鍵で復号した。デジタル署名では役割が逆になり、秘密鍵で署名を作り、公開鍵で署名を検証する。秘密鍵を持つ本人しか作れず、誰でも検証できる署名は、紙の書類における手書きの署名や印鑑の役割を果たす。

デジタル署名の役割
------------------

:term:`デジタル署名`\ は、次の 3 つの性質を提供する。

* 完全性：署名されたメッセージが改ざんされていないことを確認できる。
* 認証：メッセージが秘密鍵の持ち主によって作成されたことを確認できる。
* 否認防止：秘密鍵の持ち主は、後になって署名したことを否定できない。

MAC も完全性と認証を提供するが、否認防止は提供できない。両者の違いを\ :numref:`tbl-mac-vs-signature` にまとめる。

.. _tbl-mac-vs-signature:

.. list-table:: MAC とデジタル署名の比較
   :header-rows: 1
   :widths: 30 35 35

   * - 項目
     - MAC
     - デジタル署名
   * - 使う鍵
     - 送信者と受信者が共有する共通鍵
     - 作成には秘密鍵、検証には公開鍵
   * - 検証できる者
     - 共通鍵を持つ者だけ
     - 公開鍵を入手できる誰でも
   * - 否認防止
     - できない（受信者もタグを作れる）
     - できる
   * - 処理速度
     - 高速
     - 低速

デジタル署名は、ソフトウェアの配布（コード署名）、OS の更新、公開鍵証明書（:doc:`pki_tls`）、TLS のハンドシェイク、電子契約、暗号資産の取引など、幅広い場面で使われている。

署名方式のモデル
----------------

署名方式は、次の 3 つのアルゴリズムからなる（:numref:`fig-signature`）。

* 鍵生成 :math:`\mathsf{Gen}`：秘密鍵 :math:`sk` と公開鍵 :math:`pk` の組を生成する。
* 署名 :math:`\mathsf{Sign}`：秘密鍵 :math:`sk` とメッセージ :math:`m` から署名 :math:`\sigma` を計算する。
* 検証 :math:`\mathsf{Verify}`：公開鍵 :math:`pk`、メッセージ :math:`m`、署名 :math:`\sigma` から、署名が正しいかどうか（受理か拒否か）を判定する。

.. _fig-signature:

.. graphviz::
   :caption: デジタル署名の生成と検証
   :align: center

   digraph signature {
       rankdir=LR;
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb"];
       m [label="メッセージ m"];
       sk [label="秘密鍵 sk\n（署名者だけが持つ）", fillcolor="#fbe6e6"];
       sign [label="署名", fillcolor="#fdf1e3"];
       verify [label="検証", fillcolor="#fdf1e3"];
       pk [label="公開鍵 pk\n（誰でも入手できる）", fillcolor="#e8f4ea"];
       result [label="受理 / 拒否", fillcolor="#f3f3f3"];
       m -> sign; sk -> sign;
       sign -> verify [label="m, 署名 σ"];
       pk -> verify;
       verify -> result;
   }

署名方式の安全性は、攻撃者が好きなメッセージの署名を入手できる状況（選択メッセージ攻撃）でも、まだ署名されていないメッセージについて正しい署名を作れないこととして定義される。これを EUF-CMA（existential unforgeability under chosen message attack）安全性と呼ぶ。

実際の署名方式では、長いメッセージに直接署名するのではなく、メッセージのハッシュ値に署名する。これを hash-then-sign と呼ぶ。このため、署名に使うハッシュ関数には衝突困難性が必要である。衝突する 2 つのメッセージ :math:`m, m'` を作れれば、:math:`m` の署名はそのまま :math:`m'` の署名としても通用してしまうからである。

RSA 署名
--------

RSA は署名にも使える。秘密鍵 :math:`d` でハッシュ値 :math:`H(m)` を「復号」したものを署名とし、公開鍵 :math:`e` で「暗号化」して元に戻るかを確かめる。

.. math::

   \sigma = H(m)^d \bmod n, \qquad \text{検証：} \sigma^e \bmod n \stackrel{?}{=} H(m)

:doc:`rsa` の\ :numref:`code-toy-rsa` の ``sign()`` と ``verify()`` は、この計算を行っている。ただし、教科書的 RSA 暗号と同じく、ハッシュ値をそのままべき乗する方式は安全とはいえない。ハッシュ関数を使わずにメッセージ :math:`m` そのものに署名する場合はさらに危険であり、攻撃者は適当な :math:`\sigma` を選んで :math:`m = \sigma^e \bmod n` を計算するだけで、（意味のない）メッセージと正しい署名の組を作れる。また、:math:`\sigma_1 \sigma_2` は :math:`m_1 m_2` の正しい署名になる。

実際の RSA 署名では、ハッシュ値に乱数を含むパディングを施す RSA-PSS（RFC 8017 [RFC8017]_）を使うのが推奨される。古い PKCS #1 v1.5 方式の署名も広く使われており、正しく検証すれば現在のところ安全とされている。

ECDSA
-----

署名の生成と検証
^^^^^^^^^^^^^^^^

ECDSA（Elliptic Curve Digital Signature Algorithm）は、楕円曲線を使った署名方式であり、FIPS 186-5 [FIPS186-5]_ で規定されている。:math:`\mathbb{Z}_p^*` 上の DSA を楕円曲線に置き換えたものである。曲線のベースポイントを :math:`G`\ （位数 :math:`n`）、秘密鍵を :math:`d`、公開鍵を :math:`Q = dG` とする。また、メッセージのハッシュ値を整数とみなしたものを :math:`z` とする。

署名は次の手順で作る。

#. 乱数 :math:`k \in [1, n-1]` を選ぶ。:math:`k` をナンスと呼ぶ。用語集の一般的なナンスの定義とは異なり、ECDSA のナンスは秘密かつ一様ランダムでなければならない。
#. :math:`kG = (x_1, y_1)` を計算し、:math:`r = x_1 \bmod n` とする。
#. :math:`s = k^{-1} (z + r d) \bmod n` とする。
#. :math:`(r, s)` を署名とする。

検証は次の手順で行う。

#. :math:`w = s^{-1} \bmod n`、:math:`u_1 = z w \bmod n`、:math:`u_2 = r w \bmod n` を計算する。
#. :math:`u_1 G + u_2 Q = (x, y)` を計算する。
#. :math:`x \bmod n = r` ならば受理する。

検証が正しく働くことは次のように確かめられる。:math:`Q = dG` なので、

.. math::

   u_1 G + u_2 Q = (z w + r w d) G = (z + r d) \, w \, G = (z + r d) (z + r d)^{-1} k \, G = kG

となる。ここで :math:`s = k^{-1}(z + rd)` より :math:`w = s^{-1} = k (z + rd)^{-1}` であることを使った。

ナンスの再利用による秘密鍵の漏洩
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ECDSA では、ナンス :math:`k` を署名ごとに秘密の一様乱数として選ばなければならない。異なる 2 つのメッセージ（ハッシュ値 :math:`z_1, z_2`）の署名に同じ :math:`k` を使うと、:math:`r` が同じになり、

.. math::

   s_1 - s_2 = k^{-1} (z_1 - z_2) \pmod{n}

から :math:`k = (z_1 - z_2)(s_1 - s_2)^{-1} \bmod n` が求まる。:math:`k` が分かれば、:math:`s_1 = k^{-1}(z_1 + r d)` を :math:`d` について解いて、秘密鍵 :math:`d = (s_1 k - z_1) r^{-1} \bmod n` が計算できてしまう。:math:`k` が完全に同じでなくても、乱数生成器の偏りによって :math:`k` の数ビットが予測できるだけで、多数の署名から秘密鍵を求める攻撃が知られている。

これは理論上の話ではない。2010 年には、家庭用ゲーム機 PlayStation 3 のコード署名で ECDSA のナンスが固定値になっていたことが発表され、署名用の秘密鍵が計算された。2013 年には、Android の乱数生成器の不具合によって Bitcoin のウォレットアプリでナンスが重複し、資金が盗まれる事件が起きている。:numref:`code-ecdsa-nonce-reuse` は、secp256k1 上で ECDSA を実装し、ナンスの再利用から秘密鍵を復元するプログラムである。

.. _code-ecdsa-nonce-reuse:

.. literalinclude:: ../../examples/ecdsa_nonce_reuse.py
   :language: python
   :linenos:
   :caption: ecdsa_nonce_reuse.py

:download:`ecdsa_nonce_reuse.py をダウンロード <../../examples/ecdsa_nonce_reuse.py>`

この問題への対策として、RFC 6979 [RFC6979]_ は、秘密鍵とメッセージのハッシュ値から HMAC を使ってナンスを決定的に生成する方法を規定している。同じメッセージには同じナンス、異なるメッセージには（実質的に）異なるナンスが使われるので、乱数生成器の品質に依存しない。

EdDSA と Ed25519
----------------

EdDSA（Edwards-curve Digital Signature Algorithm）は、ねじれエドワーズ曲線と呼ばれる形の楕円曲線を使う署名方式であり、RFC 8032 [RFC8032]_ で規定されている。Curve25519 と同じ有限体の上の曲線を使うものを Ed25519 と呼ぶ。Ed25519 には次の特徴がある。

* 秘密鍵から導出した値とメッセージをハッシュ関数に通してナンスを決定的に生成するため、乱数の品質に起因する ECDSA の事故が起こらない。
* 公開鍵は 32 バイト、署名は 64 バイトと小さく、署名と検証が高速である。
* 例外的な場合分けが少なく、タイミング攻撃に強い実装がしやすい。

Ed25519 は SSH、TLS 1.3、Signal などで使われており、FIPS 186-5 でも承認されている。なお、:math:`\mathbb{Z}_p^*` 上の DSA は、FIPS 186-5 で新たな署名の生成には使えなくなった。

Python での利用例
-----------------

:numref:`code-signatures-demo` は、``cryptography`` ライブラリで RSA-PSS、ECDSA（P-256）、Ed25519 の署名を作り、検証する例である。メッセージを 1 文字でも書き換えると、検証に失敗する。

.. _code-signatures-demo:

.. literalinclude:: ../../examples/signatures_demo.py
   :language: python
   :linenos:
   :caption: signatures_demo.py

:download:`signatures_demo.py をダウンロード <../../examples/signatures_demo.py>`

.. code-block:: text
   :linenos:

   RSA-PSS（署名 384 バイト）
     正しいメッセージ: 検証成功
     改ざんされたメッセージ: 検証失敗
   ECDSA P-256（署名 71 バイト、DER 形式）
     正しいメッセージ: 検証成功
     改ざんされたメッセージ: 検証失敗
   Ed25519（署名 64 バイト）
     同じメッセージの署名は同じか: True（決定的）
     正しいメッセージ: 検証成功
     改ざんされたメッセージ: 検証失敗

ECDSA の署名の長さが実行ごとに 70 〜 72 バイト程度で変わるのは、:math:`(r, s)` を DER 形式で符号化しているためである。

署名は「その公開鍵に対応する秘密鍵の持ち主が署名した」ことを保証するが、「その公開鍵が本当に Bob のものである」ことまでは保証しない。公開鍵と持ち主を結び付ける仕組みが、次章で扱う公開鍵基盤である。
