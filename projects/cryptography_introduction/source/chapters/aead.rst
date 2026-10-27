認証付き暗号
============

:doc:`symmetric`\ で扱った暗号利用モードは機密性を、:doc:`hash`\ で扱った MAC は完全性を提供する。実際の通信では両方が必要であり、それらを安全に組み合わせる必要がある。本章では、暗号化と改ざん検知を一体として提供する認証付き暗号を扱う。

暗号化だけでは改ざんを防げない
------------------------------

暗号化されていれば、攻撃者は内容を読めないので改ざんもできないと考えるのは誤りである。CTR モードでは :math:`C = P \oplus S`\ （:math:`S` は鍵ストリーム）なので、攻撃者が暗号文のあるビットを反転させると、復号結果の同じ位置のビットが反転する。

.. math::

   (C \oplus \Delta) \oplus S = P \oplus \Delta

例えば平文が ``amount=1000`` であることが分かっていれば、攻撃者は 8 バイト目に対応する暗号文のバイトに ``'1' ⊕ '9'`` を排他的論理和で加えるだけで、鍵を知らずに平文を ``amount=9000`` に書き換えられる。このように、暗号文の操作によって平文を意図どおりに変えられる性質を可鍛性（malleability）と呼ぶ。CBC モードでも、:math:`C_{i-1}` のビットを反転させると、:math:`P_i` の同じ位置のビットが反転する（その代わり :math:`P_{i-1}` は壊れる）。

さらに、改ざんされた暗号文を受け取ったサーバーの反応（エラーの種類など）から平文の情報が漏れることがある。:doc:`pitfalls`\ で扱うパディングオラクル攻撃は、その代表例である。暗号文の完全性を確認せずに復号することは、それ自体が危険なのである。

暗号化と MAC の組み合わせ方
---------------------------

暗号化と MAC を組み合わせる方法には、次の 3 通りが考えられる。

.. list-table:: 暗号化と MAC の組み合わせ方
   :header-rows: 1
   :widths: 25 35 40

   * - 方式
     - 送信するもの
     - 評価
   * - Encrypt-and-MAC
     - :math:`\mathrm{Enc}_{K_1}(m), \; \mathrm{MAC}_{K_2}(m)`
     - タグから平文の情報が漏れることがある（同じ平文は同じタグになる）。SSH が採用していた。
   * - MAC-then-Encrypt
     - :math:`\mathrm{Enc}_{K_1}(m \,\|\, \mathrm{MAC}_{K_2}(m))`
     - タグを検証する前に復号が必要であり、パディングオラクル攻撃などを招きやすい。TLS 1.2 までの CBC 暗号スイートが採用していた。
   * - Encrypt-then-MAC
     - :math:`c = \mathrm{Enc}_{K_1}(m), \; \mathrm{MAC}_{K_2}(c)`
     - タグを検証してから復号するので、改ざんされた暗号文は復号されない。一般的に安全な組み合わせとして推奨される。

Encrypt-then-MAC（:numref:`fig-etm`）では、受信者はまずタグを検証し、正しい場合にだけ復号する。暗号化用の鍵 :math:`K_1` と MAC 用の鍵 :math:`K_2` は別々に用意する。IV やナンスもタグの計算対象に含める必要がある。

.. _fig-etm:

.. graphviz::
   :caption: Encrypt-then-MAC の構成
   :align: center

   digraph etm {
       rankdir=LR;
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb"];
       m [label="平文 m"];
       enc [label="暗号化\n（鍵 K_1）", fillcolor="#fdf1e3"];
       mac [label="MAC\n（鍵 K_2）", fillcolor="#fdf1e3"];
       out [label="IV ‖ 暗号文 c ‖ タグ t", fillcolor="#e8f4ea"];
       m -> enc;
       enc -> mac [label="IV ‖ c"];
       enc -> out;
       mac -> out [label="t"];
   }

ただし、暗号化と MAC を自分で組み合わせると、鍵の使い回し、IV のタグへの含め忘れ、タグの比較方法の誤りなど、細かな実装の誤りが入り込みやすい。そのため現在では、次に述べる認証付き暗号を使うのが標準的である。

AEAD
----

インタフェース
^^^^^^^^^^^^^^

:term:`認証付き暗号`\ は、暗号化と改ざん検知を 1 つの暗号方式として提供する。特に、暗号化しないが改ざんは検知したいデータ（:term:`関連データ`）も扱えるものを AEAD（authenticated encryption with associated data）と呼ぶ。AEAD のインタフェースは次のとおりである。

.. math::

   \begin{aligned}
   \mathsf{Enc}(K, N, A, P) &\to (C, T) \\
   \mathsf{Dec}(K, N, A, C, T) &\to P \;\text{または}\; \bot
   \end{aligned}

ここで :math:`K` は鍵、:math:`N` はナンス、:math:`A` は関連データ、:math:`P` は平文、:math:`C` は暗号文、:math:`T` はタグである。復号時には、:math:`C`、:math:`A`、:math:`N` のいずれかが改ざんされていればタグの検証に失敗し、平文の代わりにエラー :math:`\bot` を返す。関連データには、通信のヘッダー（宛先、シーケンス番号、プロトコルのバージョンなど）のように、中継に必要なため暗号化できないが改ざんされては困る情報を入れる。

AES-GCM
^^^^^^^

AES-GCM（Galois/Counter Mode）は、NIST SP 800-38D [SP800-38D]_ で規定された AEAD であり、最も広く使われている。暗号化には AES の CTR モードを使い、タグの計算には GHASH と呼ばれる :math:`\mathrm{GF}(2^{128})` 上の多項式の計算を使う。多くの CPU が備える専用命令（AES-NI と、多項式の掛け算を行う PCLMULQDQ など）により、非常に高速である。ナンスは 96 ビット、タグは 128 ビットとするのが一般的である。

AES-GCM で特に注意すべきなのはナンスの扱いである。同じ鍵で同じナンスを 2 回使うと、CTR モードと同様に平文の排他的論理和が漏れるだけでなく、GHASH の鍵が計算できてしまい、攻撃者が任意のメッセージのタグを偽造できるようになる。ナンスをランダムに生成する場合、96 ビットのナンスでは誕生日のパラドックスによって衝突の確率が無視できなくなるため、SP 800-38D は 1 つの鍵で暗号化するメッセージを :math:`2^{32}` 個までに制限している。ナンスをカウンタとして管理する方法もある。

ChaCha20-Poly1305
^^^^^^^^^^^^^^^^^

ChaCha20-Poly1305 は、ストリーム暗号 ChaCha20 と、MAC の一種である Poly1305 を組み合わせた AEAD であり、RFC 8439 [RFC8439]_ で規定されている。AES 専用命令を持たない環境（一部のスマートフォンや組み込み機器）でも高速かつ安全に実装できるため、TLS 1.3 や WireGuard などで使われている。AES-GCM と同様に、同じ鍵でナンスを再利用してはならない。

ナンスの再利用に強い方式
^^^^^^^^^^^^^^^^^^^^^^^^

ナンスの管理を誤る危険を減らすため、AES-GCM-SIV（RFC 8452）のように、ナンスを再利用しても被害が限定される方式も提案されている。AES-GCM-SIV では、同じナンスで同じ平文を暗号化したことが分かる以上の情報は漏れない。

Python での利用例
-----------------

:numref:`code-aead-demo` は、``cryptography`` ライブラリで AES-GCM と ChaCha20-Poly1305 を使う例である。暗号文や関連データを 1 ビットでも書き換えると、復号時に ``InvalidTag`` 例外が送出される。

.. _code-aead-demo:

.. literalinclude:: ../../examples/aead_demo.py
   :language: python
   :linenos:
   :caption: aead_demo.py

:download:`aead_demo.py をダウンロード <../../examples/aead_demo.py>`

.. code-block:: text
   :linenos:

   AES-256-GCM: 14 バイトの平文 -> 42 バイト（ナンス 12 + 暗号文 14 + タグ 16）
     復号: b'secret message'
     暗号文の改ざんを検知した
     関連データの改ざんを検知した
   ChaCha20-Poly1305: 14 バイトの平文 -> 42 バイト（ナンス 12 + 暗号文 14 + タグ 16）
     復号: b'secret message'
     暗号文の改ざんを検知した
     関連データの改ざんを検知した

共通鍵でデータを暗号化する場合は、本章の AEAD を使うのが原則である。:doc:`symmetric`\ の CBC モードや CTR モードを単独で使うのは、互換性の維持などやむを得ない場合に限るべきである。
