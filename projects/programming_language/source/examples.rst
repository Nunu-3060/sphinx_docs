サンプルコード一覧
==================

:doc:`languages/index`\ で示した\ :ref:`sample-program`\ のソースコードを、言語ごとに示す。各ファイルは、リンクからダウンロードできる。ソースコードの内容と解説は、各言語の章を参照してほしい。

サンプルコードは、各言語で代表的なコーディング規約に従って記述した。執筆環境（Windows 11）で処理系や検査ツールを利用できた言語については、実際にコンパイル・実行し、静的解析ツールで検査した。処理系を利用できなかった言語については、規約に従って記述したものの、実行による確認はしていない。

.. list-table:: サンプルコードの一覧
   :header-rows: 1
   :widths: 12 25 33 30

   * - 言語
     - ファイル
     - 準拠した規約
     - 検査の状況
   * - C
     - :download:`word_count.c <../examples/c/word_count.c>`、:download:`.clang-format <../examples/c/.clang-format>`、:download:`.clang-tidy <../examples/c/.clang-tidy>`
     - 書式は LLVM のスタイルを基に字下げを 4 文字としたもの（``.clang-format``）
     - 検査済み
   * - C++
     - :download:`word_count.cpp <../examples/cpp/word_count.cpp>`、:download:`.clang-format <../examples/cpp/.clang-format>`、:download:`.clang-tidy <../examples/cpp/.clang-tidy>`
     - C++ Core Guidelines、書式は C と同じ
     - 検査済み
   * - Rust
     - :download:`word_count.rs <../examples/rust/word_count.rs>`
     - The Rust Style Guide（rustfmt の既定の書式）
     - 未実行
   * - Go
     - :download:`word_count.go <../examples/go/word_count.go>`
     - Effective Go、gofmt の書式
     - 未実行
   * - Java
     - :download:`WordCount.java <../examples/java/WordCount.java>`
     - Google Java Style Guide
     - 未実行
   * - C#
     - :download:`WordCount.cs <../examples/csharp/WordCount.cs>`
     - .NET の C# コーディング規則
     - 検査済み
   * - Kotlin
     - :download:`WordCount.kt <../examples/kotlin/WordCount.kt>`
     - Kotlin Coding Conventions
     - 未実行
   * - Swift
     - :download:`word_count.swift <../examples/swift/word_count.swift>`
     - Swift API Design Guidelines
     - 未実行
   * - Python
     - :download:`word_count.py <../examples/python/word_count.py>`、:download:`setup.cfg <../examples/python/setup.cfg>`
     - PEP 8、型ヒント（PEP 484）
     - 検査済み
   * - JavaScript
     - :download:`word_count.js <../examples/javascript/word_count.js>`
     - Prettier の既定の書式、JSDoc による型注釈
     - 検査済み
   * - TypeScript
     - :download:`word_count.ts <../examples/typescript/word_count.ts>`、:download:`tsconfig.json <../examples/typescript/tsconfig.json>`
     - Prettier の既定の書式
     - 検査済み
   * - Ruby
     - :download:`word_count.rb <../examples/ruby/word_count.rb>`
     - Ruby Style Guide（RuboCop の既定の規則）
     - 未実行
   * - PHP
     - :download:`word_count.php <../examples/php/word_count.php>`
     - PER Coding Style（PSR-12 の後継）
     - 未実行
   * - SQL
     - :download:`word_count.sql <../examples/sql/word_count.sql>`
     - SQL Style Guide（Simon Holywell）
     - 検査済み（SQLite）

検査の方法
----------

「検査済み」とした言語は、次の方法で確認した。いずれも警告やエラーは検出されず、実行結果が\ :ref:`sample-program`\ の期待される出力と一致した。

.. list-table:: 検査の方法
   :header-rows: 1
   :widths: 15 85

   * - 言語
     - 方法
   * - C
     - MSVC で ``/std:c17 /W4 /WX`` を指定してコンパイルし、実行した。clang-format で書式を、clang-tidy（``.clang-tidy`` の設定）で静的解析を行った。
   * - C++
     - MSVC で ``/std:c++20 /EHsc /W4 /WX`` を指定してコンパイルし、実行した。clang-format と clang-tidy で C と同様に検査した。
   * - C#
     - Roslyn コンパイラ（csc）で、警告をエラーとして扱い（``-warnaserror``）、null 許容参照型を有効にしてコンパイルし、.NET のランタイムで実行した。
   * - Python
     - flake8（行長は 120 文字まで許容）と mypy（``strict = True``）で検査し、実行した。設定は ``setup.cfg`` に記述している。
   * - JavaScript
     - Node.js で実行した。TypeScript のコンパイラで JSDoc の型注釈を検査した（``--checkJs --strict``）。
   * - TypeScript
     - TypeScript のコンパイラで ``tsconfig.json`` の設定（``strict`` など）に従って型検査し、Node.js で実行した。
   * - SQL
     - SQLite（Python の ``sqlite3`` モジュール）で実行した。

Python のサンプルは、次のコマンドで検査と実行ができる。

.. code-block:: console
   :linenos:

   $ cd examples/python
   $ flake8 word_count.py
   $ mypy word_count.py
   Success: no issues found in 1 source file
   $ python word_count.py
   the: 3
   dog: 2
   brown: 1
