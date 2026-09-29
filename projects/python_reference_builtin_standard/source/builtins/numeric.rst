数値演算
========

数値に対する基本的な演算を行う関数群。

abs
---

数値の絶対値を返す。

.. code-block:: python

   >>> abs(-5)
   5
   >>> abs(3.2)
   3.2

round
-----

数値を指定した桁数で四捨五入する（正確には偶数丸め）。

.. code-block:: python

   >>> round(3.14159, 2)
   3.14
   >>> round(2.5)
   2

divmod
------

商と余りのタプルを返す。

.. code-block:: python

   >>> divmod(7, 3)
   (2, 1)

pow
---

累乗を計算する。3引数版では剰余演算を含めて計算できる。

.. code-block:: python

   >>> pow(2, 10)
   1024
   >>> pow(2, 10, 1000)
   24

hex / oct / bin
---------------

整数を、それぞれ16進数・8進数・2進数を表す文字列に変換する。

.. code-block:: python

   >>> hex(255)
   '0xff'
   >>> oct(8)
   '0o10'
   >>> bin(5)
   '0b101'

.. note::

   同様の結果は ``format(255, "x")`` のように :doc:`string_repr` の ``format`` を使っても得られる。``hex`` / ``oct`` / ``bin`` は接頭辞付きの文字列を直接返す簡易な手段であり、桁数や記法をより細かく制御したい場合は ``format`` を使う。
