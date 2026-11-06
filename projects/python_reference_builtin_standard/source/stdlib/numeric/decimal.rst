decimal
=======

10 進数を正確に扱うための、精度を指定できる浮動小数点演算を提供するモジュール。``float`` は内部的に 2 進数で数値を表現するため、``0.1`` のような単純な 10 進小数でも誤差を持つことがある。金額計算など、誤差が許されない場面では ``float`` の代わりに ``Decimal`` を使うべきである。

Decimal の基本
---------------

``Decimal`` は数値を文字列として渡すことで、10 進数としての正確さを保ったまま計算できる。

.. code-block:: python
   :linenos:

   >>> 0.1 + 0.2
   0.30000000000000004
   >>> from decimal import Decimal
   >>> Decimal("0.1") + Decimal("0.2")
   Decimal('0.3')

.. note::

   ``Decimal(0.1)`` のように ``float`` を直接渡すと、その ``float`` がすでに持っている誤差がそのまま引き継がれてしまう。必ず文字列（または整数）から生成すること。

金額計算での利用
------------------

金額のような、誤差が許されない値の計算には ``Decimal`` が適している。

.. code-block:: python
   :linenos:

   >>> price = Decimal("1980")
   >>> tax_rate = Decimal("0.10")
   >>> price * (1 + tax_rate)
   Decimal('2178.00')

四則演算と丸め
--------------

``Decimal`` 同士は通常の演算子でそのまま四則演算ができる。丸めには ``quantize`` を使い、小数点以下の桁数を明示的に指定する。``rounding`` を省略した場合はコンテキストの丸めモード（既定では偶数への丸めである ``ROUND_HALF_EVEN``）が使われるため、一般的な四捨五入をしたい場合は ``ROUND_HALF_UP`` を明示する。

.. code-block:: python
   :linenos:

   >>> from decimal import Decimal, ROUND_HALF_UP
   >>> value = Decimal("19.995")
   >>> value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
   Decimal('20.00')
   >>> Decimal("0.125").quantize(Decimal("0.01"))  # 既定の ROUND_HALF_EVEN
   Decimal('0.12')

getcontext().prec
------------------

``getcontext()`` で現在のスレッドにおける演算コンテキストを取得できる。``prec`` 属性で有効桁数（精度）を設定すると、以降の ``Decimal`` 演算すべてに適用される。

.. code-block:: python
   :linenos:

   >>> from decimal import getcontext
   >>> getcontext().prec = 4
   >>> Decimal("1") / Decimal("3")
   Decimal('0.3333')
   >>> getcontext().prec = 28
   >>> Decimal("1") / Decimal("3")
   Decimal('0.3333333333333333333333333333')

コンテキストの変更はそのスレッド内の以降のすべての演算に影響する。一部の計算だけ精度を変えたい場合は、``with`` ブロックを抜けると元に戻る ``localcontext()`` を使うとよい。

.. code-block:: python
   :linenos:

   >>> from decimal import localcontext
   >>> with localcontext(prec=4):
   ...     print(Decimal("1") / Decimal("3"))
   ...
   0.3333
   >>> Decimal("1") / Decimal("3")
   Decimal('0.3333333333333333333333333333')
