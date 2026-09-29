secrets
=======

パスワードやセキュリティトークン、認証に使うシークレットなど、
セキュリティに関わる用途向けに、暗号論的に安全な乱数を生成するための
モジュール。

secrets.token_bytes / token_hex / token_urlsafe
------------------------------------------------

いずれも指定したバイト数のランダムなトークンを生成する。``token_bytes`` は ``bytes`` オブジェクト、``token_hex`` は16進数文字列、``token_urlsafe`` は URL に安全に埋め込める文字列を返す。セッショントークンやパスワードリセット用の URL、API キーの生成などに使う。

.. code-block:: python

   >>> import secrets
   >>> secrets.token_bytes(16)  # doctest: +SKIP
   b'\xf7\x9a\x1b...'
   >>> secrets.token_hex(16)  # doctest: +SKIP
   '2556c9a274ff038f6e3d1a0b9c7d5e21'
   >>> secrets.token_urlsafe(16)  # doctest: +SKIP
   'UTGaWlXLHo7yvvaWGXFuuw'

secrets.choice
--------------

シーケンスから要素を1つランダムに選ぶ。:mod:`random` モジュールにも
同名の ``random.choice`` があるが、こちらは暗号論的に安全ではなく、
セキュリティ用途には適さない。パスワード生成やトークン生成のように
予測されては困る場面では、必ず ``secrets.choice`` を使う。

.. code-block:: python

   >>> import secrets
   >>> secrets.choice(["red", "green", "blue"])  # doctest: +SKIP
   'green'

ランダムなパスワードの生成
---------------------------

``secrets.choice`` を使い、文字集合からランダムに文字を選び続けることで、
一定の強度を持つランダムパスワードを生成できる。

.. code-block:: python

   >>> import secrets
   >>> import string
   >>> alphabet = string.ascii_letters + string.digits
   >>> password = "".join(secrets.choice(alphabet) for _ in range(12))
   >>> password  # doctest: +SKIP
   'wWzYsLg2OOwr'

.. note::

   :mod:`random` モジュールが標準で使う擬似乱数生成器（メルセンヌ・ツイスタ）は、内部状態を十分な数の出力から推測できてしまう可能性があり、暗号論的には安全ではない。そのため、パスワードやセッショントークンのようにセキュリティが重要な値の生成には向かない。``secrets`` モジュールは OS が提供する暗号論的に安全な乱数源（:func:`os.urandom` など）を利用しており、こうした用途に適している。
