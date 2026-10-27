公開鍵暗号と RSA
================

共通鍵暗号は高速で安全だが、通信を始める前に相手と鍵を共有しておかなければならない。本章では、この問題を解決する公開鍵暗号の考え方と、その代表である RSA 暗号を扱う。

鍵配送問題
----------

共通鍵暗号を使うには、通信する 2 者が同じ鍵を持っている必要がある。しかし、インターネット上で初めて通信する相手と、盗聴されずに鍵を共有するにはどうすればよいだろうか。鍵を暗号化して送るには別の鍵が必要になり、問題は解決しない。これを鍵配送問題と呼ぶ。

さらに、:math:`n` 人の利用者が互いに秘密の通信をするには、全ての 2 人の組ごとに異なる鍵が必要になり、鍵の総数は :math:`n(n-1)/2` になる。1000 人なら 499500 個であり、その管理は現実的でない。

公開鍵暗号の考え方
------------------

1976 年、Whitfield Diffie と Martin Hellman は、暗号化の鍵と復号の鍵を分けるという考え方を発表した。受信者 Bob は、:term:`公開鍵`\ と\ :term:`秘密鍵`\ の組（鍵ペア）を作り、公開鍵を誰にでも公開する。送信者は Bob の公開鍵で暗号化し、その暗号文は Bob の秘密鍵でしか復号できない（:numref:`fig-public-key`）。公開鍵は盗聴されても構わないので、鍵配送問題が解決する。また、各利用者が 1 つの鍵ペアを持てばよいので、鍵の総数は :math:`n` 組で済む。

.. _fig-public-key:

.. graphviz::
   :caption: 公開鍵暗号による暗号化と復号
   :align: center

   digraph public_key {
       rankdir=LR;
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb"];
       gen [label="Bob が鍵ペアを生成", fillcolor="#f3f3f3"];
       pk [label="公開鍵 pk\n（誰でも入手できる）", fillcolor="#e8f4ea"];
       sk [label="秘密鍵 sk\n（Bob だけが持つ）", fillcolor="#fbe6e6"];
       m1 [label="平文 m"];
       enc [label="暗号化", fillcolor="#fdf1e3"];
       dec [label="復号", fillcolor="#fdf1e3"];
       m2 [label="平文 m"];
       gen -> pk; gen -> sk;
       m1 -> enc; pk -> enc;
       enc -> dec [label="暗号文 c"];
       sk -> dec;
       dec -> m2;
   }

公開鍵暗号を実現するには、次の性質を持つ\ :term:`トラップドア一方向性関数`\ が必要である。

* 順方向の計算は誰でも簡単にできる（公開鍵で暗号化できる）。
* 逆方向の計算は、特別な情報（トラップドア）を知らなければ非常に難しい。
* トラップドアを知っていれば、逆方向の計算も簡単にできる（秘密鍵で復号できる）。

Diffie と Hellman の論文は公開鍵暗号の概念と鍵共有の方法（:doc:`key_exchange`）を示したが、公開鍵暗号を実現する具体的な関数は示していなかった。翌 1977 年、Ron Rivest、Adi Shamir、Leonard Adleman が、素因数分解の難しさを利用した RSA 暗号を発表した。

RSA 暗号
--------

鍵生成・暗号化・復号
^^^^^^^^^^^^^^^^^^^^

RSA 暗号の鍵生成は次の手順で行う。

#. 大きな素数 :math:`p, q`\ （それぞれ 1024 ビット以上）をランダムに生成する。
#. :math:`n = pq` を計算する。
#. :math:`\lambda(n) = \mathrm{lcm}(p - 1, q - 1)` を計算する。:math:`\lambda` はカーマイケル関数と呼ばれる。
#. :math:`\gcd(e, \lambda(n)) = 1` を満たす :math:`e` を選ぶ。通常は :math:`e = 65537 = 2^{16} + 1` を使う。
#. :math:`d = e^{-1} \bmod \lambda(n)` を拡張ユークリッド法で計算する。

公開鍵は :math:`(n, e)`、秘密鍵は :math:`d` である（:math:`p, q, \lambda(n)` も秘密にする）。:math:`\lambda(n)` の代わりにオイラーの :math:`\varphi` 関数 :math:`\varphi(n) = (p-1)(q-1)` を使って :math:`d` を求めても、同様に正しく復号できる。

平文は :math:`0 \le m < n` の整数として表す。暗号化と復号は、次のべき乗剰余で行う。

.. math::

   c = m^e \bmod n, \qquad m = c^d \bmod n

小さな数で計算してみよう。:math:`p = 61`、:math:`q = 53` とすると、:math:`n = 3233`、:math:`\lambda(n) = \mathrm{lcm}(60, 52) = 780` である。:math:`e = 17` とすると、:math:`17 \times 413 = 7021 = 9 \times 780 + 1` なので :math:`d = 413` となる。平文 :math:`m = 65` を暗号化すると :math:`c = 65^{17} \bmod 3233 = 2790` となり、:math:`2790^{413} \bmod 3233 = 65` で元に戻る。

正しさの証明
^^^^^^^^^^^^

:math:`m^{ed} \equiv m \pmod{n}` が成り立つことを示す。:math:`ed \equiv 1 \pmod{\lambda(n)}` なので、ある整数 :math:`k \ge 0` を使って :math:`ed = 1 + k \lambda(n)` と書ける。

まず法 :math:`p` で考える。:math:`m` が :math:`p` の倍数でないとき、:math:`\lambda(n)` は :math:`p - 1` の倍数なので、フェルマーの小定理より次が成り立つ。

.. math::

   m^{ed} = m \cdot \left( m^{p-1} \right)^{k \lambda(n) / (p-1)} \equiv m \cdot 1 = m \pmod{p}

:math:`m` が :math:`p` の倍数のときは、両辺とも :math:`0` と合同なので、やはり :math:`m^{ed} \equiv m \pmod{p}` である。同様に :math:`m^{ed} \equiv m \pmod{q}` も成り立つ。:math:`p` と :math:`q` は異なる素数なので、中国剰余定理より :math:`m^{ed} \equiv m \pmod{n}` が成り立つ。

RSA の安全性
^^^^^^^^^^^^

:math:`n` を素因数分解して :math:`p, q` が分かれば、:math:`\lambda(n)` が計算でき、公開鍵の :math:`e` から秘密鍵 :math:`d` が求まる。したがって、RSA の安全性は少なくとも素因数分解の難しさに依存している。2020 年には 829 ビットの RSA-250 が素因数分解されている。現在は、法 :math:`n` の長さを最低でも 2048 ビット、128 ビットの安全性を求める場合は 3072 ビットにすることが推奨されている（:numref:`tbl-security-strength` を参照）。

:numref:`code-toy-rsa` は、RSA 暗号のおもちゃ実装である（:ref:`toy-warning`\ を参照）。

.. _code-toy-rsa:

.. literalinclude:: ../../examples/toy_rsa.py
   :language: python
   :linenos:
   :caption: toy_rsa.py

:download:`toy_rsa.py をダウンロード <../../examples/toy_rsa.py>`

教科書的 RSA の問題点
---------------------

前節の、平文をそのまま :math:`m^e \bmod n` で暗号化する方式を教科書的 RSA（textbook RSA）と呼ぶ。教科書的 RSA は、そのままでは安全な暗号として使えない。

* **決定的である。**\ 同じ平文は常に同じ暗号文になるので、IND-CPA 安全ではない。例えば平文が「はい」か「いいえ」のどちらかだと分かっていれば、攻撃者は両方を公開鍵で暗号化して暗号文と比べるだけで平文を特定できる。
* **可鍛性を持つ。**\ :math:`(m_1^e)(m_2^e) = (m_1 m_2)^e` なので、2 つの暗号文の積は、平文の積の暗号文になる。攻撃者は、平文を知らなくても、平文を :math:`s` 倍した暗号文 :math:`c \cdot s^e \bmod n` を作れる。
* **小さな平文が危険である。** :math:`e = 3` で :math:`m^3 < n` となるほど :math:`m` が小さいと、:math:`c = m^3` となり、:math:`c` の通常の立方根を計算するだけで :math:`m` が求まる。

OAEP
^^^^

これらの問題を解決するため、実際の RSA 暗号では、平文に乱数を含むパディングを施してから暗号化する。現在推奨されている方式は OAEP（optimal asymmetric encryption padding）であり、PKCS #1 v2.2（RFC 8017 [RFC8017]_）で規定されている。OAEP はハッシュ関数と乱数を使って平文を :math:`n` と同程度の長さの値に変換するため、同じ平文でも暗号化するたびに異なる暗号文になる。OAEP を使った RSA 暗号は、適切な仮定のもとで IND-CCA 安全であることが証明されている。

古い方式である PKCS #1 v1.5 の暗号化用パディングには、1998 年に Daniel Bleichenbacher が発見した選択暗号文攻撃がある。復号時にパディングが正しいかどうかが攻撃者に分かると、それを手がかりに暗号文を解読できる。新しいシステムでは OAEP を使うべきである。

ハイブリッド暗号
----------------

RSA 暗号は、共通鍵暗号に比べて桁違いに遅く、一度に暗号化できるデータも法 :math:`n` の長さ（OAEP のパディング分を除く）までに限られる。そのため、公開鍵暗号でデータそのものを暗号化することはまずない。

実際には、ランダムに生成した共通鍵（セッション鍵）でデータを暗号化し、そのセッション鍵だけを公開鍵暗号で暗号化して送る。これを\ :term:`ハイブリッド暗号`\ と呼ぶ。公開鍵暗号の「鍵配送が不要」という利点と、共通鍵暗号の「高速」という利点を組み合わせた方式である。:numref:`code-rsa-oaep` は、``cryptography`` ライブラリで RSA-OAEP とハイブリッド暗号を使う例である。

.. _code-rsa-oaep:

.. literalinclude:: ../../examples/rsa_oaep.py
   :language: python
   :linenos:
   :caption: rsa_oaep.py

:download:`rsa_oaep.py をダウンロード <../../examples/rsa_oaep.py>`

なお、RSA 暗号でセッション鍵を送る方法（RSA 鍵輸送）は、TLS 1.2 までは広く使われていたが、TLS 1.3 では廃止された。その理由は\ :doc:`key_exchange`\ の前方秘匿性の節で説明する。
