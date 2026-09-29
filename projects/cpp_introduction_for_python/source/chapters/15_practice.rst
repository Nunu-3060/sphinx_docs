実践的な開発
============================================================

本章では、実際のプログラム開発で使う CMake とデバッガー、および C++ と Python を連携させる方法を説明します。

CMake
------------------------------------------------------------

ソースファイルが増えると、コンパイラーのコマンドを直接入力するのは手間がかかります。また、コンパイラーごとにオプションの書き方が異なります。CMake は、ビルドの手順を ``CMakeLists.txt`` というファイルに記述し、各環境に合ったビルドファイル（Visual Studio のプロジェクトや Makefile など）を生成するツールです。C++ のプロジェクトでは、事実上の標準として広く使われています。CMake は Visual Studio の「C++ によるデスクトップ開発」ワークロードにも含まれています。

「:doc:`07_functions`」で作成した ``geometry`` のプログラムを、CMake でビルドする例を示します。``main.cpp`` と ``geometry.cpp`` と同じフォルダーに、以下の ``CMakeLists.txt`` を作成します。

.. literalinclude:: ../../examples/ch07/multi/CMakeLists.txt
   :language: cmake
   :caption: examples/ch07/multi/CMakeLists.txt

各行の意味は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 記述
     - 意味
   * - ``cmake_minimum_required``
     - 必要な CMake のバージョンを指定する
   * - ``project``
     - プロジェクトの名前と、使用する言語を指定する
   * - ``set(CMAKE_CXX_STANDARD 17)``
     - C++17 でコンパイルする
   * - ``add_executable``
     - 生成する実行ファイルの名前と、そのソースファイルを指定する
   * - ``target_compile_options``
     - コンパイラーのオプションを指定する（ここではコンパイラーに応じて警告オプションを切り替えている）

``CMakeLists.txt`` があるフォルダーで、以下のコマンドを実行します。1 行目でビルド用のフォルダー ``build`` にビルドファイルを生成し、2 行目でビルドを実行します。

.. code-block:: console

   $ cmake -S . -B build
   $ cmake --build build

Visual Studio のビルドファイルが生成された場合、実行ファイルは ``build\Debug\geometry_demo.exe`` に出力されます。Makefile が生成された場合は ``build/geometry_demo`` に出力されます。

Visual Studio では、「フォルダーを開く」で ``CMakeLists.txt`` があるフォルダーを開くと、コマンドを使わずに IDE 上でビルドや実行ができます。

デバッグ
------------------------------------------------------------

Python では ``print`` 関数や ``pdb`` でデバッグすることが多いでしょう。C++ でもデバッガーを使うと、プログラムを 1 行ずつ実行したり、変数の値を確認したりできます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - デバッガー
     - 主な使用環境
   * - Visual Studio のデバッガー
     - Windows（MSVC）
   * - GDB
     - Linux（GCC）
   * - LLDB
     - macOS（Clang）

デバッガーでソースコードの行や変数名を表示するには、デバッグ情報を付けてコンパイルする必要があります。GCC と Clang では ``-g``、MSVC では ``/Zi`` を指定します。CMake で Visual Studio のビルドファイルを生成した場合は、既定の Debug 構成でデバッグ情報が付きます。Makefile を生成する場合は、``cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug`` のように Debug 構成を指定します。

デバッガーの主な機能を以下に示します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 機能
     - 説明
   * - ブレークポイント
     - 指定した行でプログラムの実行を一時停止する
   * - ステップ実行
     - 一時停止した位置から 1 行ずつ実行する
   * - 変数の監視
     - 一時停止した時点の変数の値を確認する
   * - 呼び出し履歴
     - 現在の関数がどの関数から呼び出されたかを確認する（Python のトレースバックに相当）

Visual Studio では、行番号の左側をクリックしてブレークポイントを設定し、F5 キーでデバッグ実行を開始します。

また、デバッグ中は最適化を無効にしてビルドしてください。最適化を有効にすると、変数が削除されたり実行順序が入れ替わったりして、デバッガーの表示がソースコードと一致しなくなる場合があります。

Python との連携
------------------------------------------------------------

C++ を学んだ Python 利用者にとって実用的な活用方法の 1 つが、処理の重い部分だけを C++ で実装し、Python から呼び出す構成です。pybind11 を使うと、C++ の関数やクラスを Python のモジュールとして公開できます。

.. literalinclude:: ../../examples/ch15/pybind/example.cpp
   :language: cpp
   :caption: examples/ch15/pybind/example.cpp

``PYBIND11_MODULE`` は、Python のモジュール ``example`` を定義し、C++ の関数 ``add`` を Python の関数 ``add`` として登録します。

ビルドには setuptools を使います。``example.cpp`` と同じフォルダーに、以下の 2 つのファイルを作成します。

.. literalinclude:: ../../examples/ch15/pybind/pyproject.toml
   :language: toml
   :caption: examples/ch15/pybind/pyproject.toml

.. literalinclude:: ../../examples/ch15/pybind/setup.py
   :language: python
   :caption: examples/ch15/pybind/setup.py

このフォルダーで ``pip install .`` を実行すると、C++ のコードがコンパイルされ、``example`` モジュールがインストールされます。インストール後は、通常の Python のモジュールと同じように使えます。

.. literalinclude:: ../../examples/ch15/pybind/use_example.py
   :language: python
   :caption: examples/ch15/pybind/use_example.py

.. code-block:: text
   :caption: 実行結果

   5

.. note::

   ビルドには C++ のコンパイラーが必要です。Windows で「Unable to find a compatible Visual Studio installation」というエラーが発生する場合は、Developer Command Prompt で環境変数 ``DISTUTILS_USE_SDK`` を ``1`` に設定してから ``pip install .`` を実行してください。
