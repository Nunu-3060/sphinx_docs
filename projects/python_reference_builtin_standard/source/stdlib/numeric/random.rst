random
======

擬似乱数を生成するためのモジュール。乱数の取得、リストからのランダムな選択、要素の並べ替えなど、ゲームやシミュレーション、シャッフル処理などでよく使われる機能を提供する。

.. note::

   このモジュールが生成する乱数は暗号論的に安全ではない。パスワードやトークン、セキュリティ関連の用途には、暗号論的に安全な乱数を生成する :doc:`../misc/secrets` モジュールを使用すること。

random.random
-------------

``0.0`` 以上 ``1.0`` 未満の浮動小数点数を返す。

.. code-block:: python
   :linenos:

   >>> import random
   >>> random.random()  # doctest: +SKIP
   0.6394267984578837

random.randint
--------------

指定した範囲（両端を含む）のランダムな整数を返す。

.. code-block:: python
   :linenos:

   >>> random.randint(1, 6)  # doctest: +SKIP
   4
   >>> [random.randint(1, 6) for _ in range(5)]  # doctest: +SKIP
   [3, 1, 6, 2, 5]

random.choice / random.sample
-------------------------------

``choice`` はシーケンスから要素を 1 つ選ぶ。``sample`` は重複なしで指定した個数の要素を選ぶ。

.. code-block:: python
   :linenos:

   >>> members = ["Alice", "Bob", "Carol", "Dave"]
   >>> random.choice(members)  # doctest: +SKIP
   'Carol'
   >>> random.sample(members, 2)  # doctest: +SKIP
   ['Dave', 'Alice']

random.uniform
--------------

指定した範囲の浮動小数点数を返す。``randint`` の浮動小数点数版で、両端の値も含まれる可能性がある。

.. code-block:: python
   :linenos:

   >>> random.uniform(1.0, 10.0)  # doctest: +SKIP
   8.599796663725433

random.choices
--------------

``sample`` とは異なり重複を許した（同じ要素を何度でも選べる）サンプリングを行う。``weights`` 引数で要素ごとの重みを指定すると、重みが大きい要素ほど選ばれやすくなる（重み付きサンプリング）。

.. code-block:: python
   :linenos:

   >>> members = ["Alice", "Bob", "Carol"]
   >>> random.choices(members, k=5)  # doctest: +SKIP
   ['Bob', 'Alice', 'Alice', 'Carol', 'Bob']
   >>> # "Alice" が他の 10 倍選ばれやすくなる
   >>> random.choices(members, weights=[10, 1, 1], k=5)  # doctest: +SKIP
   ['Alice', 'Alice', 'Alice', 'Alice', 'Alice']

random.shuffle
--------------

リストの要素をその場（in-place）でランダムに並べ替える。

.. code-block:: python
   :linenos:

   >>> cards = [1, 2, 3, 4, 5]
   >>> random.shuffle(cards)
   >>> cards  # doctest: +SKIP
   [3, 1, 5, 2, 4]

random.seed
-----------

乱数生成器の種（シード）を設定する。同じシードを与えると、以降の乱数列が再現可能になるため、テストやデバッグに有用である。

.. code-block:: python
   :linenos:

   >>> random.seed(0)
   >>> random.random()
   0.8444218515250481
   >>> random.seed(0)
   >>> random.random()
   0.8444218515250481

.. note::

   モジュールレベルの関数はすべて 1 つの共有された乱数生成器を使う。他のコードの影響を受けずに再現性のある乱数列を得たい場合は、``rng = random.Random(0)`` のように独立したインスタンスを生成し、そのメソッド（``rng.random()`` など）を使うとよい。

コマンドラインからの利用
------------------------

Python 3.13 以降では、``python -m random`` としてコマンドラインから直接乱数を得られる。引数が整数なら 1 以上その値以下の整数、浮動小数点数なら 0 以上その値以下の浮動小数点数を表示し、それ以外の文字列（または複数の引数）なら、その中からランダムに 1 つを選んで表示する。``-c`` / ``-i`` / ``-f`` オプションで動作を明示することもできる。

.. code-block:: text
   :linenos:

   $ python -m random 6
   4
   $ python -m random Alice Bob Carol
   Bob
