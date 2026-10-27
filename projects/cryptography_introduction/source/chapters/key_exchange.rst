鍵共有
======

:doc:`rsa` では、公開鍵暗号でセッション鍵を送る方法を見た。本章では、もう 1 つの方法である鍵共有を扱う。鍵共有では、2 者が公開の通信路でやり取りをするだけで、盗聴者には分からない共通の秘密を作り出す。

Diffie-Hellman 鍵共有
---------------------

手順
^^^^

Diffie-Hellman 鍵共有（DH 鍵共有）は、1976 年に Diffie と Hellman が発表した、公開鍵暗号の考え方に基づく世界初の鍵共有方式である。あらかじめ、大きな素数 :math:`p` と、:math:`\mathbb{Z}_p^*` の元 :math:`g` を公開パラメータとして決めておく。Alice と Bob は次の手順で鍵を共有する（:numref:`fig-dh`）。

#. Alice は秘密の値 :math:`a` をランダムに選び、:math:`A = g^a \bmod p` を Bob に送る。
#. Bob は秘密の値 :math:`b` をランダムに選び、:math:`B = g^b \bmod p` を Alice に送る。
#. Alice は :math:`B^a \bmod p` を、Bob は :math:`A^b \bmod p` を計算する。

.. math::

   B^a = (g^b)^a = g^{ab} = (g^a)^b = A^b \pmod{p}

なので、2 人は同じ値 :math:`g^{ab} \bmod p` を得る。これを共有秘密と呼ぶ。

.. _fig-dh:

.. graphviz::
   :caption: Diffie-Hellman 鍵共有の手順
   :align: center

   digraph dh {
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb"];
       a1 [label="Alice\na をランダムに選ぶ\nA = g^a mod p"];
       b1 [label="Bob\nb をランダムに選ぶ\nB = g^b mod p"];
       a2 [label="B^a mod p\n= g^ab mod p", fillcolor="#e8f4ea"];
       b2 [label="A^b mod p\n= g^ab mod p", fillcolor="#e8f4ea"];
       eve [label="Eve が知りうる値\np, g, A, B", fillcolor="#fbe6e6"];
       {rank=same; a1; b1;}
       {rank=same; a2; eve; b2;}
       a1 -> b2 [label="A を送る"];
       b1 -> a2 [label="B を送る"];
       a1 -> a2 [style=dashed];
       b1 -> b2 [style=dashed];
   }

小さな数で計算してみよう。:math:`p = 23`、:math:`g = 5` とする。Alice が :math:`a = 6` を選ぶと :math:`A = 5^6 \bmod 23 = 8`、Bob が :math:`b = 15` を選ぶと :math:`B = 5^{15} \bmod 23 = 19` である。Alice は :math:`19^6 \bmod 23 = 2`、Bob は :math:`8^{15} \bmod 23 = 2` を計算し、共有秘密 2 を得る。

離散対数問題
^^^^^^^^^^^^

盗聴者 Eve は :math:`p, g, A, B` を知ることができる。Eve が共有秘密を求めるには、例えば :math:`A = g^a \bmod p` から :math:`a` を求めればよい。この問題を\ :term:`離散対数問題`\ （discrete logarithm problem、DLP）と呼ぶ。実数の対数とは異なり、:math:`g^x \bmod p` の値は :math:`x` に対して不規則に変化するため、:math:`p` が十分に大きければ :math:`a` を求めることは非常に難しい。

厳密には、DH 鍵共有の安全性は「:math:`g^a` と :math:`g^b` から :math:`g^{ab}` を求めることが難しい」という計算 Diffie-Hellman 問題（CDH 問題）に基づく。離散対数問題が解ければ CDH 問題も解けるが、逆が成り立つかどうかは一般には分かっていない。

パラメータの選び方
^^^^^^^^^^^^^^^^^^

DH 鍵共有を安全に使うには、パラメータを慎重に選ぶ必要がある。:math:`p - 1` が小さな素因数しか持たないと、離散対数問題が簡単に解けてしまう（ポーリッヒ・ヘルマン法）。そこで、:math:`q` も素数となる :math:`p = 2q + 1` の形の素数（安全素数）を使い、位数が大きな素数 :math:`q` の部分群で計算するのが一般的である。

:math:`p` の長さは RSA の法と同程度（2048 ビット以上）が必要である。2015 年に発表された Logjam 攻撃では、512 ビットの DH パラメータを使うようにサーバーを誘導し、事前計算を利用して通信を解読できることが示された。自分でパラメータを生成するよりも、RFC 3526 や RFC 7919 で定められた標準のパラメータを使うのが安全である。

中間者攻撃
----------

DH 鍵共有は、盗聴するだけの受動的攻撃者に対しては安全である。しかし、通信を改ざんできる能動的攻撃者 Mallory に対しては、そのままでは無力である。Mallory は Alice と Bob の間に入り込み、Alice から送られた :math:`A` を自分の公開値 :math:`M` にすり替えて Bob に送り、Bob から送られた :math:`B` も :math:`M` にすり替えて Alice に送る（:numref:`fig-mitm`）。

.. _fig-mitm:

.. graphviz::
   :caption: DH 鍵共有に対する中間者攻撃
   :align: center

   digraph mitm {
       rankdir=LR;
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb"];
       alice [label="Alice"];
       mallory [label="Mallory\n（中間者）", fillcolor="#fbe6e6"];
       bob [label="Bob"];
       alice -> mallory [label="A"];
       mallory -> bob [label="M（A のつもり）"];
       bob -> mallory [label="B"];
       mallory -> alice [label="M（B のつもり）"];
   }

その結果、Alice は Mallory と鍵 :math:`g^{am}` を、Bob は Mallory と鍵 :math:`g^{bm}` を共有することになる。Alice と Bob は互いに相手と鍵を共有したと信じているが、Mallory は両者の通信を復号し、内容を読んだり書き換えたりしてから転送できる。これを\ :term:`中間者攻撃`\ （man-in-the-middle attack）と呼ぶ。

中間者攻撃を防ぐには、受け取った公開値が本当に相手から送られたものであることを確認する必要がある。そのために使われるのが、デジタル署名（:doc:`signature`）と公開鍵証明書（:doc:`pki_tls`）である。TLS では、サーバーが DH の公開値を含むハンドシェイクの内容に署名し、クライアントはサーバーの証明書を使ってその署名を検証する。:numref:`code-toy-dh` は、DH 鍵共有と中間者攻撃のシミュレーションである。

.. _code-toy-dh:

.. literalinclude:: ../../examples/toy_dh.py
   :language: python
   :linenos:
   :caption: toy_dh.py

:download:`toy_dh.py をダウンロード <../../examples/toy_dh.py>`

.. code-block:: text
   :linenos:

   通常の鍵共有
     Alice の鍵: c3b19d0c7bc97fccb53bdc538fd1aa70...
     Bob の鍵  : c3b19d0c7bc97fccb53bdc538fd1aa70...
     一致するか: True
   中間者攻撃
     Alice と Mallory の鍵が一致: True
     Bob と Mallory の鍵が一致  : True
     Alice と Bob の鍵が一致    : False

前方秘匿性
----------

RSA 鍵輸送（:doc:`rsa`）では、クライアントがセッション鍵をサーバーの公開鍵で暗号化して送る。攻撃者が暗号化された通信を全て記録しておき、何年も後にサーバーの秘密鍵を入手すると、記録しておいた全ての通信を復号できてしまう。

一方、通信のたびに新しい :math:`a, b` を生成し、使い終わったら直ちに消去する DH 鍵共有（ephemeral DH、DHE と呼ぶ。楕円曲線を使うものは ECDHE と呼ぶ）では、後でサーバーの長期的な秘密鍵（署名鍵）が漏洩しても、過去のセッション鍵は求められない。このように、長期的な鍵が漏洩しても過去の通信の安全性が保たれる性質を\ :term:`前方秘匿性`\ （forward secrecy）と呼ぶ。TLS 1.3 では、鍵共有に前方秘匿性のある (EC)DHE だけが使われる。

共有秘密から鍵を導出する
------------------------

DH 鍵共有で得られる共有秘密 :math:`g^{ab} \bmod p` は、一様ランダムなビット列ではない（値は :math:`\mathbb{Z}_p^*` の特定の部分群の元に限られ、ビットの分布も偏っている）。そのため、共有秘密をそのまま AES の鍵として使わず、:term:`鍵導出関数`\ （key derivation function、KDF）を通して、必要な長さの一様ランダムに見える鍵に変換する。

代表的な KDF は、HMAC を使った HKDF（RFC 5869 [RFC5869]_）である。HKDF は、共有秘密から擬似ランダムな鍵を取り出す Extract 段階と、その鍵から用途ごとに必要な長さの鍵を生成する Expand 段階からなる。Expand 段階に用途を表す文字列（info）を与えることで、1 つの共有秘密から、暗号化用の鍵、MAC 用の鍵、送信方向ごとの鍵など、互いに独立な複数の鍵を導出できる。TLS 1.3 の鍵スケジュールも HKDF に基づいている。
