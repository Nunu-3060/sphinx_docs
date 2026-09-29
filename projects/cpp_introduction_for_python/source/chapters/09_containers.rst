標準ライブラリのコンテナ
============================================================

本章では、複数の値をまとめて扱うための標準ライブラリのコンテナと、文字列を扱う ``std::string`` を説明します。

Python の組み込み型との対応
------------------------------------------------------------

Python の組み込み型と、それに近い C++ の型を以下に示します。C++ のコンテナでは格納する要素の型を ``std::vector<int>`` のように ``< >`` の中に指定する必要があり、異なる型の要素を混在させることはできません。

.. list-table::
   :header-rows: 1
   :widths: 15 30 25 30

   * - Python
     - C++
     - ヘッダーファイル
     - 備考
   * - ``str``
     - ``std::string``
     - ``<string>``
     - C++ の文字列は変更可能
   * - ``list``
     - ``std::vector``
     - ``<vector>``
     - 要素数を変更できる配列
   * - ``tuple``
     - ``std::tuple``
     - ``<tuple>``
     - 要素数と各要素の型が固定の組
   * - ``tuple``
     - ``std::array``
     - ``<array>``
     - 要素数が固定で、すべての要素が同じ型の配列
   * - ``dict``
     - ``std::unordered_map``
     - ``<unordered_map>``
     - 要素の順序は保証されない
   * - ``dict``
     - ``std::map``
     - ``<map>``
     - 要素はキーの順に並ぶ
   * - ``set``
     - ``std::unordered_set``
     - ``<unordered_set>``
     - 要素の順序は保証されない
   * - ``set``
     - ``std::set``
     - ``<set>``
     - 要素は値の順に並ぶ

「ヘッダーファイル」の列は、その型を使うために ``#include`` するヘッダーファイルです。

std::string
------------------------------------------------------------

``std::string`` は文字列を表す型です。Python の ``str`` と異なり、文字列の内容を直接変更できます。

.. literalinclude:: ../../examples/ch09/string.cpp
   :language: cpp
   :caption: examples/ch09/string.cpp

.. code-block:: text
   :caption: 実行結果

   Hello, World
   12
   Hello
   7
   Jello, World
   43

主な操作と Python との対応を以下に示します。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Python
     - C++
   * - ``len(s)``
     - ``s.size()``
   * - ``s + t``、``s += t``
     - ``s + t``、``s += t``
   * - ``s[i:i + n]``
     - ``s.substr(i, n)``
   * - ``s.find(t)``
     - ``s.find(t)``\ （見つからない場合は ``std::string::npos`` を返す）
   * - ``int(s)``
     - ``std::stoi(s)``
   * - ``str(n)``
     - ``std::to_string(n)``

``substr`` の 2 番目の引数は、終了位置ではなく取り出す文字数である点に注意してください。

.. warning::

   ``std::string`` の ``size`` や ``[]`` はバイト単位で扱います。UTF-8 の日本語は 1 文字が 3 バイトであることが多いため、``size`` は文字数と一致しません。

std::vector
------------------------------------------------------------

``std::vector`` は、要素数を変更できる配列で、Python の ``list`` に相当します。C++ で最もよく使うコンテナです。

.. literalinclude:: ../../examples/ch09/vector.cpp
   :language: cpp
   :caption: examples/ch09/vector.cpp

.. code-block:: text
   :caption: 実行結果

   4
   3
   1
   3 1 4
   out of range

主な操作と Python との対応を以下に示します。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Python
     - C++
   * - ``v.append(x)``
     - ``v.push_back(x)``
   * - ``v.pop()``
     - ``v.back()`` で値を取得してから ``v.pop_back()`` で削除する
   * - ``len(v)``
     - ``v.size()``
   * - ``v[i]``
     - ``v[i]`` または ``v.at(i)``
   * - ``v[-1]``
     - ``v.back()``
   * - ``v.clear()``
     - ``v.clear()``

.. warning::

   ``v[i]`` は、``i`` が範囲外かどうかを検査しません。範囲外のアクセスは未定義動作になり、Python のように ``IndexError`` は発生しません。範囲の検査が必要な場合は ``v.at(i)`` を使います。``at`` は範囲外のときに ``std::out_of_range`` 例外を送出します。例外については「:doc:`14_error_handling`」で説明します。また、C++ では負の添字で末尾から数えることはできません。

std::map と std::unordered_map
------------------------------------------------------------

``std::map`` と ``std::unordered_map`` は、キーと値の組を格納するコンテナで、Python の ``dict`` に相当します。``std::map`` は要素をキーの順に並べて保持し、``std::unordered_map`` は順序を保証しない代わりに一般に高速です。

.. literalinclude:: ../../examples/ch09/map.cpp
   :language: cpp
   :caption: examples/ch09/map.cpp

.. code-block:: text
   :caption: 実行結果

   30
   3
   Dave not found
   0
   4
   Alice: 30
   Bob: 25
   Carol: 35
   Dave: 0

キーが存在するかどうかは ``count`` で確認します。C++20 以降では ``contains`` も使えます。

.. warning::

   存在しないキーに ``[]`` でアクセスすると、Python の ``dict`` のように ``KeyError`` が発生するのではなく、そのキーの要素が既定値（数値の場合は ``0``）で自動的に追加されます。要素を追加せずに値を読み出すには、``at`` を使うか、``find`` で要素を探します。

イテレーター
------------------------------------------------------------

イテレーターは、コンテナの要素を指し示すオブジェクトです。``begin()`` は先頭の要素を指すイテレーターを、``end()`` は末尾の要素の「次」を指すイテレーターを返します。イテレーターに ``++`` を適用すると次の要素に進み、``*`` を適用すると指している要素を取得できます。

.. literalinclude:: ../../examples/ch09/iterator.cpp
   :language: cpp
   :caption: examples/ch09/iterator.cpp

.. code-block:: text
   :caption: 実行結果

   10 20 30

範囲 ``for`` 文は、内部でこのようにイテレーターを使って実現されています。通常は範囲 ``for`` 文を使えば十分ですが、「:doc:`13_algorithms_and_lambdas`」で説明する標準アルゴリズムでは、処理の範囲をイテレーターの組で指定します。

範囲 for 文での要素の受け取り方
------------------------------------------------------------

範囲 ``for`` 文で要素を受け取る変数の型は、引数の渡し方と同じ考え方で選びます。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 書き方
     - 意味
   * - ``for (int x : v)``
     - 各要素のコピーを受け取る
   * - ``for (const auto& x : v)``
     - 各要素を読み取り専用の参照で受け取る。コピーのコストが大きい要素に使う
   * - ``for (auto& x : v)``
     - 各要素を参照で受け取る。要素を変更する場合に使う

構造化束縛
------------------------------------------------------------

C++17 の構造化束縛を使うと、Python のアンパック代入 ``name, age = pair`` に近い書き方で、複数の値をまとめて受け取れます。前述の ``map.cpp`` では、``for (const auto& [name, age] : ages)`` と書いて、各要素のキーと値を ``name`` と ``age`` に受け取っています。
