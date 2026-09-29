コーディング規約
============================================================

本章では、C++ のコーディング規約と、規約を守るためのツールを説明します。

C++ のコーディング規約の状況
------------------------------------------------------------

Python には PEP 8 という公式のスタイルガイドがあり、多くのプロジェクトがこれに従っています。一方、C++ には言語の標準として定められたスタイルガイドがなく、組織やプロジェクトごとに異なる規約が使われています。

代表的なガイドラインを以下に示します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ガイドライン
     - 概要
   * - `C++ Core Guidelines <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>`_
     - C++ の設計者である Bjarne Stroustrup らがまとめた、安全で効率的な C++ の書き方の指針。書式よりも、設計やリソース管理などの内容面を扱う
   * - `Google C++ Style Guide <https://google.github.io/styleguide/cppguide.html>`_
     - Google 社内の規約を公開したもの。命名規則や書式を含めて詳細に定めている
   * - `LLVM Coding Standards <https://llvm.org/docs/CodingStandards.html>`_
     - Clang などを開発する LLVM プロジェクトの規約

既存のプロジェクトに参加する場合は、そのプロジェクトの規約に従ってください。新しくプロジェクトを始める場合は、既存のガイドラインのいずれかを基にして規約を決め、一貫して守ることが重要です。

命名規則
------------------------------------------------------------

C++ の命名規則はガイドラインによって異なります。本資料のサンプルコードで用いた命名規則を、PEP 8 と比較して以下に示します。

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 対象
     - PEP 8
     - 本資料
   * - 変数、関数
     - ``snake_case``
     - ``snake_case``
   * - クラス
     - ``CapWords``
     - ``CapWords``
   * - 定数
     - ``UPPER_CASE``
     - ``snake_case``\ （``constexpr`` や ``const`` を付ける）
   * - 非公開のメンバー
     - ``_leading_underscore``
     - ``trailing_underscore_``\ （``private`` の下に宣言する）

C++ では、``UPPER_CASE`` の名前をマクロ（``#define`` で定義する名前）に使う慣習があります。マクロとの衝突を避けるため、定数には ``UPPER_CASE`` を使わない規約が多くあります。

.. warning::

   アンダースコアで始まり大文字が続く名前（``_Value`` など）や、アンダースコアが 2 つ連続する名前（``my__value`` など）は、コンパイラーと標準ライブラリのために予約されており、使ってはいけません。Python の ``_private`` のような名前を C++ のメンバー変数に使うと、この規則に抵触しやすいため、本資料では末尾にアンダースコアを付けています。

書式と clang-format
------------------------------------------------------------

インデントの幅、波括弧の位置、1 行の最大文字数などの書式は、手作業で揃えるのではなくツールで自動的に整形します。C++ では clang-format が広く使われています。clang-format は Python の Black に相当するツールで、Visual Studio にも組み込まれています。

clang-format の設定は、プロジェクトのフォルダーに置いた ``.clang-format`` ファイルに記述します。

.. literalinclude:: ../../examples/ch16/.clang-format
   :language: yaml
   :caption: examples/ch16/.clang-format

この設定は、Google のスタイルを基にし、インデントを 4 文字、1 行の最大文字数を 100 文字に変更します。以下のコマンドでファイルを整形します。

.. code-block:: console

   $ clang-format -i main.cpp

Visual Studio では、「編集」メニューの「詳細」から「ドキュメントのフォーマット」を実行すると、``.clang-format`` の設定に従って整形されます。

静的解析
------------------------------------------------------------

コンパイラーの警告に加えて、静的解析ツールを使うと、規約に反する書き方や誤りの可能性がある書き方を検出できます。C++ では clang-tidy がよく使われ、C++ Core Guidelines に基づく検査も行えます。Python の Ruff や Pylint に相当するツールです。Visual Studio にも、コード分析の機能として静的解析が組み込まれています。

本資料で推奨した書き方
------------------------------------------------------------

本資料の各章で推奨した書き方を、規約の観点から以下にまとめます。いずれも C++ Core Guidelines の内容と一致しています。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 推奨する書き方
     - 説明した章
   * - 変数は宣言時に初期化する
     - :doc:`05_variables_and_types`
   * - 変更しない変数には ``const`` を付ける
     - :doc:`05_variables_and_types`
   * - 型変換には ``static_cast`` を使う
     - :doc:`05_variables_and_types`
   * - コピーのコストが大きい引数は const 参照で受け取る
     - :doc:`07_functions`
   * - ヘッダーファイルで ``using namespace`` を使わない
     - :doc:`04_basic_syntax`
   * - ポインターより参照を優先する
     - :doc:`08_pointers_and_references`
   * - 仮想関数を上書きする場合は ``override`` を付ける
     - :doc:`10_classes`
   * - ``new`` と ``delete`` を直接使わず、スマートポインターを使う
     - :doc:`11_resource_management`
   * - 自分でループを書く前に、標準アルゴリズムを検討する
     - :doc:`13_algorithms_and_lambdas`
   * - コンパイラーの警告を有効にし、すべて解消する
     - :doc:`03_environment`
