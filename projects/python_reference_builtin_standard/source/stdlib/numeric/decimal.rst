decimal
=======

10進数を正確に扱うための、精度を指定できる浮動小数点演算を提供するモジュール。``float`` は内部的に2進数で数値を表現するため、``0.1`` のような単純な10進小数でも誤差を持つことがある。金額計算など、誤差が許されない場面では ``float`` の代わりに ``Decimal`` を使うべきである。

Decimal の基本
---------------

``Decimal`` は数値を文字列として渡すことで、10進数としての正確さを
保ったまま計算できる。

.. code-block:: python

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

   >>> price = Decimal("1980")
   >>> tax_rate = Decimal("0.10")
   >>> price * (1 + tax_rate)
   Decimal('2178.00')

四則演算と丸め
--------------

``Decimal`` 同士は通常の演算子でそのまま四則演算ができる。丸めには ``quantize`` を使い、小数点以下の桁数を明示的に指定する。

.. code-block:: python

   >>> from decimal import Decimal, ROUND_HALF_UP
   >>> value = Decimal("19.995")
   >>> value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
   Decimal('20.00')

getcontext().prec
------------------

``getcontext()`` で現在のスレッドにおける演算コンテキストを取得できる。``prec`` 属性で有効桁数（精度）を設定すると、以降の ``Decimal`` 演算すべてに適用される。

.. code-block:: python

   >>> from decimal import getcontext
   >>> getcontext().prec = 4
   >>> Decimal("1") / Decimal("3")
   Decimal('0.3333')
   >>> getcontext().prec = 28
   >>> Decimal("1") / Decimal("3")
   Decimal('0.3333333333333333333333333333')
