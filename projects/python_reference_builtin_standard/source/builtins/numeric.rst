数値演算
========

数値に対する基本的な演算を行う関数群。

abs
---

数値の絶対値を返す。

.. code-block:: python
   :linenos:

   >>> abs(-5)
   5
   >>> abs(3.2)
   3.2

round
-----

数値を指定した桁数に丸める。四捨五入ではなく、ちょうど中間の値は偶数側に丸める（偶数丸め、銀行家の丸め）。また ``float`` は 2 進数で近似されているため、``round(2.675, 2)`` が ``2.67`` になるように直感と異なる結果になることがある。

.. code-block:: python
   :linenos:

   >>> round(3.14159, 2)
   3.14
   >>> round(2.5)
   2

divmod
------

商と余りのタプルを返す。

.. code-block:: python
   :linenos:

   >>> divmod(7, 3)
   (2, 1)

pow
---

累乗を計算する。3 引数版 ``pow(base, exp, mod)`` は ``(base ** exp) % mod`` を効率よく計算する。

.. code-block:: python
   :linenos:

   >>> pow(2, 10)
   1024
   >>> pow(2, 10, 1000)
   24

hex / oct / bin
---------------

整数を、それぞれ 16 進数・8 進数・2 進数を表す文字列に変換する。

.. code-block:: python
   :linenos:

   >>> hex(255)
   '0xff'
   >>> oct(8)
   '0o10'
   >>> bin(5)
   '0b101'

.. note::

   同様の結果は ``format(255, "x")`` のように :doc:`string_repr` の ``format`` を使っても得られる。``hex`` / ``oct`` / ``bin`` は接頭辞付きの文字列を直接返す簡易な手段であり、桁数や記法をより細かく制御したい場合は ``format`` を使う。
