暗号理論入門
============

本書は、Python などのプログラミングの知識を持つエンジニアや工学系の大学生を対象とした、暗号理論の入門書である。古典暗号から始めて、共通鍵暗号、ハッシュ関数、公開鍵暗号、デジタル署名、TLS までを、数式による原理の説明と Python のサンプルコードの両面から解説する。

.. toctree::
   :maxdepth: 2
   :caption: 序章

   chapters/intro

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: 本編

   chapters/basics
   chapters/classical
   chapters/math
   chapters/symmetric
   chapters/hash
   chapters/aead
   chapters/rsa
   chapters/key_exchange
   chapters/ecc
   chapters/signature
   chapters/pki_tls
   chapters/pitfalls
   chapters/advanced

.. toctree::
   :maxdepth: 1
   :caption: 付録

   chapters/examples_list
   chapters/glossary
   chapters/references
