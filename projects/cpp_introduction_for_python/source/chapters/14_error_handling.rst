エラー処理
============================================================

本章では、C++ でのエラー処理の方法と、C++ に特有の未定義動作を説明します。

例外
------------------------------------------------------------

C++ の例外は、Python の例外とほぼ同じ考え方で使えます。``throw`` で例外を送出し、``try`` と ``catch`` で捕捉します。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Python
     - C++
   * - ``raise ValueError("msg")``
     - ``throw std::invalid_argument("msg");``
   * - ``try:``
     - ``try { }``
   * - ``except ValueError as e:``
     - ``catch (const std::invalid_argument& e) { }``
   * - ``except Exception as e:``
     - ``catch (const std::exception& e) { }``
   * - ``str(e)``
     - ``e.what()``
   * - ``finally:``
     - 対応する構文はなく、RAII で代替する

.. literalinclude:: ../../examples/ch14/exceptions.cpp
   :language: cpp
   :caption: examples/ch14/exceptions.cpp

.. code-block:: text
   :caption: 実行結果

   2.5
   error: division by zero
   cannot convert

標準ライブラリの例外クラスは ``<stdexcept>`` ヘッダーで提供され、すべて ``std::exception`` を基底クラスとしています。代表的な例外クラスを以下に示します。

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - C++
     - 近い Python の例外
     - 用途
   * - ``std::invalid_argument``
     - ``ValueError``
     - 引数の値が不正
   * - ``std::out_of_range``
     - ``IndexError``、``KeyError``
     - 範囲外のアクセス
   * - ``std::runtime_error``
     - ``RuntimeError``
     - 実行時に検出されたその他のエラー

例外は const 参照で捕捉します。値で捕捉すると、例外オブジェクトのコピーが作られるうえ、派生クラスの情報が失われる場合があります。

Python の ``finally`` に相当する構文はありません。C++ では、例外が送出されてブロックを抜ける場合にもデストラクターが呼ばれるため、後処理は RAII で行います。RAII については「:doc:`11_resource_management`」で説明しました。

.. note::

   C++ の標準ライブラリは、Python ほど多くの場面で例外を送出しません。例えば、``std::vector`` の ``[]`` による範囲外アクセスや、整数の 0 による除算では、例外は送出されず未定義動作になります。

std::optional
------------------------------------------------------------

Python では、値が見つからない場合などに ``None`` を返すことがよくあります。C++ では、``int`` などの型の変数に「値がない」状態を持たせることはできません。そこで、C++17 の ``std::optional``\ （``<optional>`` ヘッダー）を使います。``std::optional<T>`` は、``T`` 型の値を持つか、値を持たないかのどちらかの状態を表します。

.. literalinclude:: ../../examples/ch14/optional.cpp
   :language: cpp
   :caption: examples/ch14/optional.cpp

.. code-block:: text
   :caption: 実行結果

   found at 1
   false
   999

主な操作を以下に示します。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 操作
     - 意味
   * - ``return std::nullopt;``
     - 値がない状態を返す（Python の ``return None`` に相当）
   * - ``if (opt)``、``opt.has_value()``
     - 値を持っているかどうかを判定する
   * - ``*opt``、``opt.value()``
     - 値を取り出す
   * - ``opt.value_or(x)``
     - 値を持っていればその値を、持っていなければ ``x`` を返す

値を持たない ``std::optional`` に ``*opt`` を使うと未定義動作になります。値を持っていることを確認してから取り出してください。

``optional.cpp`` の ``if (auto index = find_index(names, "Bob"))`` は、変数を宣言して初期化し、その値を条件として判定する書き方です。``index`` は ``if`` 文の中でだけ使えます。

エラーの原因を呼び出し元に伝えたい場合は、C++23 の ``std::expected`` も使えます。

未定義動作
------------------------------------------------------------

C++ の規格では、一部の操作について「どのような結果になるかを定めない」としています。これを未定義動作と呼びます。未定義動作を含むプログラムは、正しく動作しているように見えることもあれば、誤った結果を返したり、異常終了したり、コンパイラーやビルドの設定によって異なる結果になったりします。

これまでの章で説明した未定義動作の例を以下に示します。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 操作
     - Python の場合
   * - 配列や ``std::vector`` の範囲外アクセス
     - ``IndexError`` が発生する
   * - 初期化していない変数の読み出し
     - ``NameError`` が発生する
   * - 符号付き整数のオーバーフロー
     - 大きな整数に自動的に拡張される
   * - 整数の 0 による除算
     - ``ZeroDivisionError`` が発生する
   * - ``nullptr`` の間接参照
     - ``None`` の属性にアクセスすると ``AttributeError`` が発生する
   * - 寿命が終わったオブジェクトへのアクセス
     - 参照されているオブジェクトは破棄されないため、起こらない

Python ではエラーとして報告される操作の多くが、C++ ではエラーにならずに実行されてしまいます。未定義動作を避けるために、次の対策を行ってください。

* コンパイラーの警告を有効にし、警告をすべて解消する。
* 範囲の検査が必要な場面では ``at`` を使う。
* 開発中はサニタイザーを使って実行する。

サニタイザーは、範囲外アクセスなどの誤りを実行時に検出し、発生した箇所を報告する機能です。GCC と Clang では ``-fsanitize=address,undefined``、MSVC では ``/fsanitize=address`` を付けてコンパイルすると有効になります。
