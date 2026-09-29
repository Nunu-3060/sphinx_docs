アルゴリズムとラムダ式
============================================================

本章では、標準ライブラリのアルゴリズムと、その引数として使うラムダ式を説明します。

ラムダ式
------------------------------------------------------------

ラムダ式は、その場で定義する名前のない関数です。Python の ``lambda`` 式に相当します。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Python
     - C++
   * - ``square = lambda x: x * x``
     - ``auto square = [](int x) { return x * x; };``

C++ のラムダ式は、``[キャプチャー](引数) { 本体 }`` の形式で書きます。Python の ``lambda`` 式には 1 つの式しか書けませんが、C++ のラムダ式の本体には複数の文を書けます。

ラムダ式の外側にある変数をラムダ式の中で使うには、角括弧の中にその変数を指定します。これをキャプチャーと呼びます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 書き方
     - 意味
   * - ``[x]``
     - ``x`` をコピーして取り込む（値キャプチャー）
   * - ``[&x]``
     - ``x`` を参照で取り込む（参照キャプチャー）。ラムダ式の中で ``x`` を変更すると、外側の ``x`` も変更される
   * - ``[=]``、``[&]``
     - 使用するすべての変数を、それぞれ値または参照で取り込む

.. literalinclude:: ../../examples/ch13/lambda.cpp
   :language: cpp
   :caption: examples/ch13/lambda.cpp

.. code-block:: text
   :caption: 実行結果

   25
   11
   2

.. warning::

   参照キャプチャーしたラムダ式を、取り込んだ変数の寿命が終わった後に呼び出すと、ダングリング参照になります。ラムダ式を関数の外に返したり、後で呼び出すために保存したりする場合は、値キャプチャーを使ってください。

標準アルゴリズム
------------------------------------------------------------

``<algorithm>`` ヘッダーには、並べ替え、検索、変換など、コンテナに対する汎用的な処理が用意されています。多くのアルゴリズムは、処理の範囲を ``v.begin()`` と ``v.end()`` のイテレーターの組で受け取ります。処理の内容を変えたい場合は、引数にラムダ式を渡します。

.. literalinclude:: ../../examples/ch13/algorithms.cpp
   :language: cpp
   :caption: examples/ch13/algorithms.cpp

.. code-block:: text
   :caption: 実行結果

   1 2 3 5 8 9
   9 8 5 3 2 1
   28
   3
   true
   81 64 25 9 4 1

Python の組み込み関数との対応を以下に示します。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Python
     - C++
   * - ``v.sort()``
     - ``std::sort(v.begin(), v.end())``
   * - ``v.sort(reverse=True)``
     - ``std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; })``
   * - ``min(v)``、``max(v)``
     - ``*std::min_element(v.begin(), v.end())``、``*std::max_element(v.begin(), v.end())``
   * - ``sum(v)``
     - ``std::accumulate(v.begin(), v.end(), 0)``\ （``<numeric>`` ヘッダー）
   * - ``next(x for x in v if x < 4)``
     - ``std::find_if(v.begin(), v.end(), [](int x) { return x < 4; })``
   * - ``any(x % 2 == 0 for x in v)``
     - ``std::any_of(v.begin(), v.end(), [](int x) { return x % 2 == 0; })``
   * - ``[x * x for x in v]``
     - ``std::transform`` で別のコンテナに書き込む

``std::sort`` の第 3 引数には、2 つの要素を受け取り、1 つ目を前に置くべき場合に ``true`` を返す関数を渡します。Python の ``key`` 引数とは考え方が異なる点に注意してください。

``std::find_if`` は、条件を満たす最初の要素を指すイテレーターを返します。見つからない場合は ``v.end()`` を返すため、結果を使う前に ``v.end()`` と比較します。

自分でループを書く代わりに標準アルゴリズムを使うと、処理の意図が名前で明確になり、誤りも減ります。

Ranges
------------------------------------------------------------

C++20 の Ranges ライブラリを使うと、イテレーターの組ではなくコンテナを直接渡して ``std::ranges::sort(v)`` のように書けます。また、ビューと呼ばれる部品を ``|`` でつなぐことで、Python のジェネレーター式に近い処理を記述できます。

.. literalinclude:: ../../examples/ch13/ranges.cpp
   :language: cpp
   :caption: examples/ch13/ranges.cpp

.. code-block:: text
   :caption: 実行結果

   1 9 25 81

``std::views::filter`` は条件を満たす要素だけを取り出し、``std::views::transform`` は各要素を変換します。ビューは、Python のジェネレーター式と同様に、要素が必要になった時点で計算を行います。
