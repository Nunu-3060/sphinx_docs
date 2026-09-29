uuid
====

重複する可能性が極めて低い一意な識別子（UUID: Universally Unique Identifier）を生成するためのモジュール。データベースのレコード ID やセッション ID など、システム全体で衝突しない識別子が必要な場面で使う。

uuid4() によるランダムな UUID
---------------------------------

最もよく使われるのは、乱数から生成する ``uuid4()``。呼び出すたびに
異なる値が生成される。

.. code-block:: python

   >>> import uuid
   >>> uuid.uuid4()  # doctest: +SKIP
   UUID('c994db5d-afc0-4bfd-a988-69c323db57e9')
   >>> uuid.uuid4()  # doctest: +SKIP
   UUID('504685d9-2774-4c0b-8059-de2e6500ff4f')

uuid1() によるホスト情報を含む UUID
---------------------------------------

``uuid1()`` は現在時刻とネットワークインタフェースの MAC アドレスなどを
元に生成される。生成順序に一定の時系列性があるが、MAC アドレスの情報が
含まれるためプライバシー上の懸念がある場合は ``uuid4()`` を使う方が無難である。

.. code-block:: python

   >>> uuid.uuid1()  # doctest: +SKIP
   UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')

uuid3() / uuid5() による名前ベースの UUID
------------------------------------------------

``uuid3()`` と ``uuid5()`` は、名前空間（``uuid.NAMESPACE_DNS`` など）と
名前の文字列から決定的に UUID を生成する。乱数を使わないため、同じ
名前空間と名前を渡せば、何度呼び出しても常に同じ UUID が得られる。

.. code-block:: python

   >>> uuid.uuid5(uuid.NAMESPACE_DNS, "example.com")
   UUID('cfbff0d1-9375-5685-968c-48ce8b15ae17')
   >>> uuid.uuid5(uuid.NAMESPACE_DNS, "example.com")
   UUID('cfbff0d1-9375-5685-968c-48ce8b15ae17')

内部的には ``uuid3()`` が MD5、``uuid5()`` が SHA-1 でハッシュ計算を行う。:doc:`hashlib` でも触れているように MD5 は衝突攻撃に対して脆弱であるため、特別な理由がない限り ``uuid3()`` より ``uuid5()`` を選ぶのが無難である。

.. note::

   Python 3.14 で追加された ``uuid7()`` は、RFC 9562 で定義された
   時系列順に並ぶ UUID を生成する。``uuid4()`` が完全にランダムなのに
   対し、``uuid7()`` はミリ秒単位のタイムスタンプを値の先頭に埋め込むため、
   生成順に単調増加する値になる。データベースの主キーとして使うと、
   ランダムな ``uuid4()`` に比べてインデックスへの挿入が局所化され
   性能上有利になりつつ、実用上一意性も保たれるという利点がある。

   .. code-block:: python

      >>> uuid.uuid7()  # doctest: +SKIP
      UUID('018f4f3e-2c1a-7c3e-9b2a-5e6f7a8b9c0d')

一意な識別子としての利用例
----------------------------

ファイル名やレコードのキーなど、他と衝突してはいけない識別子を発行する
用途で使われることが多い。

.. code-block:: python

   >>> class User:
   ...     def __init__(self, name):
   ...         self.id = uuid.uuid4()
   ...         self.name = name
   ...
   >>> u = User("Alice")
   >>> u.id  # doctest: +SKIP
   UUID('16fd2706-8baf-433b-82eb-8c7fada847da')

str(uuid_obj) による文字列化
--------------------------------

``uuid4()`` などが返す ``UUID`` オブジェクトは、``str()`` に渡すことで
ハイフン区切りの文字列表現に変換できる。JSON など、UUID 型を直接扱えない
形式で保存する場合によく使う。

.. code-block:: python

   >>> u = uuid.uuid4()
   >>> str(u)  # doctest: +SKIP
   '550e8400-e29b-41d4-a716-446655440000'
   >>> type(str(u))
   <class 'str'>

.. note::

   逆に文字列から ``UUID`` オブジェクトを復元したい場合は、``uuid.UUID("550e8400-e29b-41d4-a716-446655440000")`` のようにコンストラクタへ文字列を渡す。
