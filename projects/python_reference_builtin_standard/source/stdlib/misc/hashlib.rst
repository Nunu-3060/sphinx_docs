hashlib
=======

MD5 や SHA-256 など、さまざまなハッシュアルゴリズムを扱うためのモジュール。ファイルの一意性確認や、通信・保存の途中で生じた偶発的な破損の検出など、ハッシュ値が必要な場面で使う。ただし MD5 や SHA-1 は意図的な改ざん（衝突攻撃）に対する耐性がないため、悪意ある攻撃者を想定する必要がある改ざん検出には使うべきではない（詳しくは後述）。

sha256 によるハッシュ計算
----------------------------

``sha256`` は暗号論的にも安全性が高く、ファイルの完全性検証などによく使われる。特に理由がなければ、まずこちらを検討するとよい。

.. code-block:: python
   :linenos:

   >>> import hashlib
   >>> h = hashlib.sha256(b"hello")
   >>> h.hexdigest()
   '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'

md5 によるハッシュ計算
-------------------------

``hashlib.md5()`` にバイト列を渡してハッシュオブジェクトを作成する。文字列を渡す場合は ``encode()`` でバイト列に変換しておく必要がある。

.. code-block:: python
   :linenos:

   >>> h = hashlib.md5(b"hello")
   >>> h.hexdigest()
   '5d41402abc4b2a76b9719d911017c592'

.. note::

   MD5 は計算が高速で古いコードやツールとの互換性のために今も見かけるが、衝突攻撃に対して脆弱であり、暗号論的な安全性が必要な用途には使うべきではない。ここでは API の使い方を示す例として掲載しているだけであり、新しいコードでは前述の ``sha256`` や後述の BLAKE2 を使うのが望ましい。既存の仕様との互換のためにセキュリティ目的以外で MD5 を使う場合は、``hashlib.md5(data, usedforsecurity=False)`` のように明示しておくと、FIPS モードが有効な環境などでも利用できる場合がある。

update() による逐次的な入力
------------------------------

大きなファイルなどを一度にメモリへ読み込みたくない場合、``update()`` を繰り返し呼び出して少しずつデータを与えられる（ファイル全体のハッシュを計算するだけなら、後述の ``file_digest()`` を使う方が簡単である）。

.. code-block:: python
   :linenos:

   >>> h = hashlib.sha256()
   >>> with open("large_file.bin", "rb") as f:
   ...     for chunk in iter(lambda: f.read(8192), b""):
   ...         h.update(chunk)
   ...
   >>> h.hexdigest()  # doctest: +SKIP

hexdigest() と digest()
--------------------------

``hexdigest()`` は 16 進数文字列としてハッシュ値を返し、``digest()`` は生のバイト列として返す。ログ出力やファイル名などには ``hexdigest()`` が扱いやすい。

.. code-block:: python
   :linenos:

   >>> h = hashlib.sha256(b"hello")
   >>> h.digest()
   b',\xf2M\xba_\xb0\xa3\x0e&\xe8;*\xc5\xb9\xe2\x9e\x1b\x16\x1e\\\x1f\xa7B^s\x043b\x93\x8b\x98$'
   >>> len(h.hexdigest())
   64

hashlib.new()、BLAKE2、file_digest()
----------------------------------------

アルゴリズム名を文字列として渡して汎用的にハッシュオブジェクトを作りたい場合は、個別の関数の代わりに ``hashlib.new(名前, データ)`` が使える。

.. code-block:: python
   :linenos:

   >>> h = hashlib.new("sha256", b"hello")
   >>> h.hexdigest()
   '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'

``blake2b``/``blake2s`` は MD5 や SHA-1 よりも高速かつ安全な、比較的新しいハッシュアルゴリズムで、鍵付きハッシュ（HMAC 相当の機能）を標準でサポートしている。暗号論的な安全性までは不要な用途（キャッシュのキー生成など）でも、MD5/SHA-1 の代わりにまず検討する価値がある。

.. code-block:: python
   :linenos:

   >>> h = hashlib.blake2b(b"hello", digest_size=16, key=b"secret-key")
   >>> h.hexdigest()  # doctest: +SKIP

ファイル全体のハッシュを計算する際は、``update()`` をチャンクごとに呼び出すループを自分で書く代わりに、Python 3.11 で追加された ``hashlib.file_digest()`` にバイナリモードで開いたファイルオブジェクトとアルゴリズム名を渡すだけで済む。

.. code-block:: python
   :linenos:

   >>> with open("large_file.bin", "rb") as f:
   ...     digest = hashlib.file_digest(f, "sha256")
   ...
   >>> digest.hexdigest()  # doctest: +SKIP

.. note::

   MD5 や SHA-1 に限らず、SHA-256 のような汎用のハッシュ関数をそのままパスワードのハッシュ化に使うべきではない。これらは高速に計算できるよう設計されているため、総当たり攻撃にも弱いからである。パスワードを保存する場合は、ソルトやストレッチングを考慮した専用の関数やライブラリ（標準ライブラリの ``hashlib.pbkdf2_hmac``/``hashlib.scrypt`` や、より高レベルなサードパーティ製の ``bcrypt``、``argon2-cffi`` など）を使用すべきである。
