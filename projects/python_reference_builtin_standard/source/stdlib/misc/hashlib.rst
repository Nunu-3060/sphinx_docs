hashlib
=======

MD5 や SHA-256 など、さまざまなハッシュアルゴリズムを扱うためのモジュール。
ファイルの一意性確認や、通信・保存の途中で生じた偶発的な破損の検出など、
ハッシュ値が必要な場面で使う。ただし MD5 や SHA-1 は意図的な改ざん
（衝突攻撃）に対する耐性がないため、悪意ある攻撃者を想定する必要がある
改ざん検出には使うべきではない（詳しくは後述）。

sha256 によるハッシュ計算
----------------------------

``sha256`` は暗号学的にも安全性が高く、ファイルの完全性検証などによく
使われる。特に理由がなければ、まずこちらを検討するとよい。

.. code-block:: python

   >>> import hashlib
   >>> h = hashlib.sha256(b"hello")
   >>> h.hexdigest()
   '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'

md5 によるハッシュ計算
-------------------------

``hashlib.md5()`` にバイト列を渡してハッシュオブジェクトを作成する。
文字列を渡す場合は ``encode()`` でバイト列に変換しておく必要がある。

.. code-block:: python

   >>> h = hashlib.md5(b"hello")
   >>> h.hexdigest()
   '5d41402abc4b2a76b9719d911017c592'

.. note::

   MD5 は計算が高速で古いコードやツールとの互換性のために今も見かけるが、
   衝突攻撃に対して脆弱であり、暗号学的な安全性が必要な用途には使うべき
   ではない。ここでは API の使い方を示す例として掲載しているだけであり、
   新しいコードでは前述の ``sha256`` や後述の BLAKE2 を使うのが望ましい。

update() による逐次的な入力
------------------------------

大きなファイルなどを一度にメモリへ読み込みたくない場合、``update()`` を
繰り返し呼び出して少しずつデータを与えられる。

.. code-block:: python

   >>> h = hashlib.sha256()
   >>> with open("large_file.bin", "rb") as f:
   ...     for chunk in iter(lambda: f.read(8192), b""):
   ...         h.update(chunk)
   >>> h.hexdigest()  # doctest: +SKIP

hexdigest() と digest()
--------------------------

``hexdigest()`` は 16 進数文字列としてハッシュ値を返し、``digest()`` は
生のバイト列として返す。ログ出力やファイル名などには ``hexdigest()`` が
扱いやすい。

.. code-block:: python

   >>> h = hashlib.sha256(b"hello")
   >>> h.digest()
   b',\xf2M\xba_\xb0\xa3\x0e&\xe8;*\xc5\xb9\xe2\x9e\x1b\x16\x1e\\\x1f\xa7B^s\x043b\x93\x8b\x98$'
   >>> len(h.hexdigest())
   64

hashlib.new()、BLAKE2、file_digest()
----------------------------------------

アルゴリズム名を文字列として渡して汎用的にハッシュオブジェクトを作りたい
場合は、個別の関数の代わりに ``hashlib.new(名前, データ)`` が使える。

.. code-block:: python

   >>> h = hashlib.new("sha256", b"hello")
   >>> h.hexdigest()
   '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'

``blake2b``/``blake2s`` は MD5 や SHA-1 よりも高速かつ安全な、比較的
新しいハッシュアルゴリズムで、鍵付きハッシュ（HMAC 相当の機能）を
標準でサポートしている。暗号学的な安全性までは不要な用途
（キャッシュのキー生成など）でも、MD5/SHA-1 の代わりにまず検討する
価値がある。

.. code-block:: python

   >>> h = hashlib.blake2b(b"hello", digest_size=16, key=b"secret-key")
   >>> h.hexdigest()  # doctest: +SKIP

ファイル全体のハッシュを計算する際、Python 3.11 以降では ``update()`` をチャンクごとに呼び出すループを自分で書く代わりに、``hashlib.file_digest()`` にバイナリモードで開いたファイルオブジェクトを渡すだけで済む。

.. code-block:: python

   >>> with open("large_file.bin", "rb") as f:
   ...     digest = hashlib.file_digest(f, "sha256")
   ...
   >>> digest.hexdigest()  # doctest: +SKIP

.. note::

   前述のとおり MD5 や SHA-1 には安全性の問題があるため、パスワードのハッシュ化にも適さない。パスワードを保存する場合は、ソルトやストレッチングを考慮した専用のライブラリ（``hashlib.pbkdf2_hmac`` や、より高レベルな ``bcrypt``、``argon2-cffi`` など）を使用すべきである。
