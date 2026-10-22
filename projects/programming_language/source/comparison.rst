言語の比較
==========

本章では、:doc:`languages/index`\ で述べた各言語の特徴を、:doc:`concepts`\ で示した観点ごとに表にまとめて比較する。表の内容は各言語の代表的な処理系と一般的な使い方に基づく要約であり、例外や処理系による違いについては各言語の章を参照してほしい。

基本的な性質
------------

.. list-table:: 各言語の基本的な性質
   :header-rows: 1
   :widths: 12 8 24 18 20 18

   * - 言語
     - 登場年
     - 主なパラダイム
     - 型付け
     - 実行方式
     - メモリ管理
   * - C
     - 1972
     - 手続き型
     - 静的・弱い
     - AOT コンパイル
     - 手動
   * - C++
     - 1983
     - 手続き型、オブジェクト指向、ジェネリック
     - 静的・弱い
     - AOT コンパイル
     - 手動、RAII
   * - Rust
     - 2010
     - 手続き型、関数型
     - 静的・強い
     - AOT コンパイル
     - 所有権
   * - Go
     - 2009
     - 手続き型
     - 静的・強い
     - AOT コンパイル
     - GC
   * - Java
     - 1995
     - オブジェクト指向
     - 静的・強い
     - VM（JIT）
     - GC
   * - C#
     - 2000
     - オブジェクト指向、関数型
     - 静的・強い
     - VM（JIT）
     - GC
   * - Kotlin
     - 2011
     - オブジェクト指向、関数型
     - 静的・強い
     - VM（JIT）
     - GC
   * - Swift
     - 2014
     - オブジェクト指向、プロトコル指向、関数型
     - 静的・強い
     - AOT コンパイル
     - 参照カウント（ARC）
   * - Python
     - 1991
     - オブジェクト指向、手続き型、関数型
     - 動的・強い
     - インタプリタ（バイトコード）
     - 参照カウント、GC
   * - JavaScript
     - 1995
     - プロトタイプベース、関数型
     - 動的・弱い
     - インタプリタ、JIT
     - GC
   * - TypeScript
     - 2012
     - JavaScript と同じ
     - 静的（漸進的）
     - JavaScript へトランスパイル
     - GC（JavaScript の処理系による）
   * - Ruby
     - 1995
     - オブジェクト指向
     - 動的・強い
     - インタプリタ（バイトコード）、JIT
     - GC
   * - PHP
     - 1995
     - 手続き型、オブジェクト指向
     - 動的・弱い
     - インタプリタ（オペコード）、JIT
     - 参照カウント、GC
   * - SQL
     - 1974
     - 宣言型
     - 静的（表の定義による）
     - RDBMS が実行計画を作成して実行
     - RDBMS が管理

型付けの「強い」「弱い」は、暗黙の型変換をどの程度許すかに基づく目安である（:doc:`concepts`\ を参照）。Kotlin は JVM 以外に、ネイティブコードや JavaScript を生成することもできる。C# と Java にも、事前に機械語へコンパイルする手段（Native AOT、GraalVM Native Image）がある。

型システム
----------

.. list-table:: 型システムの比較
   :header-rows: 1
   :widths: 13 22 22 23 20

   * - 言語
     - 型推論
     - null 安全
     - ジェネリクス
     - 部分型の判定
   * - C
     - 限定的（C23 の ``auto``）
     - なし
     - なし（マクロ、``_Generic`` で代用）
     - なし
   * - C++
     - ``auto``
     - なし（``std::optional`` で表現）
     - テンプレート（単相化）
     - 名目的
   * - Rust
     - 関数の内部で強力
     - あり（``Option``）
     - 単相化
     - トレイトの実装による
   * - Go
     - ``:=``
     - なし（nil がある）
     - 型パラメータ（Go 1.18 以降）
     - 構造的（インタフェース）
   * - Java
     - ``var`` （局所変数）
     - なし（``Optional`` で表現）
     - 型消去
     - 名目的
   * - C#
     - ``var``
     - あり（null 許容参照型。警告による）
     - 実行時にも型情報を保持
     - 名目的
   * - Kotlin
     - 強力
     - あり
     - 型消去（JVM の場合）
     - 名目的
   * - Swift
     - 強力
     - あり（オプショナル）
     - 実行時の型情報と特殊化
     - 名目的（プロトコル）
   * - Python
     - 型検査ツールが推論
     - 型検査ツールで検査可能
     - 型ヒントで記述
     - 名目的、構造的（``Protocol``）
   * - JavaScript
     - ―
     - なし
     - ―
     - ―
   * - TypeScript
     - 強力
     - あり（``strictNullChecks``）
     - 型消去
     - 構造的
   * - Ruby
     - ―（RBS と型検査ツールで補う）
     - なし
     - ―
     - ―（ダックタイピング）
   * - PHP
     - ―
     - 型宣言で null の可否を指定
     - なし（PHPDoc の注釈で補う）
     - 名目的

SQL は表の列ごとに型を定義するが、ほかの言語とは型システムの性質が大きく異なるため、この表では省略する。「―」は、動的型付けのため該当する仕組みがないことを表す。

静的型付けの言語では、2010 年代以降に設計された Rust、Kotlin、Swift、TypeScript が、強力な型推論と null 安全を最初から備えている点が目立つ。古い言語も、Java の ``var`` や C# の null 許容参照型のように、後から同様の機能を取り入れている。動的型付けの言語では、型ヒントや型シグネチャによって静的な検査を追加する動きが共通して見られる。

メモリ管理と安全性
------------------

.. list-table:: メモリ管理と安全性の比較
   :header-rows: 1
   :widths: 14 22 20 44

   * - 言語
     - メモリ管理
     - メモリ安全性
     - 補足
   * - C
     - 手動
     - なし
     - 範囲外アクセスなどは未定義動作となる。
   * - C++
     - RAII、スマートポインタ
     - なし
     - RAII で多くの誤りを防げるが、言語として保証はしない。
   * - Rust
     - 所有権
     - あり
     - ``unsafe`` ブロックの中では保証されない。データ競合もコンパイル時に防ぐ。
   * - Go
     - GC
     - おおむねあり
     - データ競合が起きた場合は保証されない。実行時の検出ツール（race detector）がある。
   * - Java、Kotlin
     - GC
     - あり
     - データ競合は言語として防がない。
   * - C#
     - GC
     - あり
     - ``unsafe`` コンテキストではポインタを使える。
   * - Swift
     - 参照カウント（ARC）
     - あり
     - ``Unsafe`` で始まる API を除く。Swift 6 の言語モードではデータ競合をコンパイル時に検出する。
   * - Python、Ruby
     - 参照カウントと GC（Python）、GC（Ruby）
     - あり
     - GIL・GVL によって処理系の内部状態は保護されるが、複数の操作にまたがる競合は防げない。
   * - JavaScript、TypeScript
     - GC
     - あり
     - 共有メモリを使う処理は限られ、データ競合は起きにくい。
   * - PHP
     - 参照カウントと GC
     - あり
     - リクエストごとに状態が破棄される。

ここでいうメモリ安全性は、プログラムが確保していないメモリへのアクセスや解放済みメモリの使用が、言語の仕組みによって起こらないことを指す。メモリ安全性を持つ言語でも、処理系自体（多くは C や C++ で書かれている）や、C で書かれたライブラリを呼び出す部分にはこの保証が及ばない。

並行処理
--------

.. list-table:: 並行処理の比較
   :header-rows: 1
   :widths: 15 55 30

   * - 言語
     - 主な並行処理の手段
     - CPU コアを使った並列実行
   * - C
     - OS スレッド（POSIX スレッド、C11 のスレッド）
     - 可能
   * - C++
     - ``std::thread``、``std::async``、コルーチン（C++20）
     - 可能
   * - Rust
     - OS スレッド、async/await（Tokio などのランタイム）
     - 可能
   * - Go
     - goroutine、チャネル
     - 可能
   * - Java
     - スレッド、仮想スレッド、``CompletableFuture``
     - 可能
   * - C#
     - ``Task``、async/await
     - 可能
   * - Kotlin
     - コルーチン、JVM のスレッド
     - 可能
   * - Swift
     - async/await、actor
     - 可能
   * - Python
     - ``asyncio``、スレッド、マルチプロセス
     - GIL により制限（マルチプロセスかフリースレッド版で可能）
   * - JavaScript、TypeScript
     - Promise、async/await
     - Web Worker などの別の実行環境を使えば可能
   * - Ruby
     - スレッド、Fiber
     - GVL により制限（Ractor で可能）
   * - PHP
     - 基本はリクエストごとに独立したプロセスやスレッドで処理する。Fiber（PHP 8.1）
     - リクエスト単位では可能

並行処理を言語の中心的な機能として設計した Go は、goroutine とチャネルによって最も簡潔に並行処理を記述できる。async/await は C# で実用化されたのち、多くの言語に広まった。一方で、async/await は非同期の関数とそうでない関数を区別する必要があり、呼び出し関係を通じてコード全体に影響が広がる（いわゆる「関数の色」の問題）。Go の goroutine や Java の仮想スレッドは、この区別を必要としない方式である。

性能の傾向
----------

実行性能は、処理系、ライブラリ、アルゴリズム、プログラマの技量に大きく左右されるため、言語だけで一概に順位を付けることはできない。ここでは、一般的な傾向を定性的に示す。

.. list-table:: 実行性能の一般的な傾向
   :header-rows: 1
   :widths: 25 25 50

   * - 傾向
     - 言語
     - 理由
   * - 最も高速
     - C、C++、Rust
     - 機械語に直接コンパイルされ、GC がなく、メモリの配置まで細かく制御できる。
   * - 高速
     - Go、Swift、Java、C#、Kotlin
     - Go と Swift は AOT コンパイルされるが、GC や参照カウントのコストがある。Java、C#、Kotlin は JIT コンパイルにより、長時間動作するプログラムでは C++ に迫る性能を出すこともある。
   * - 中程度
     - JavaScript、TypeScript
     - 動的型付けだが、V8 などの高度な JIT コンパイラにより高い性能を持つ。
   * - 比較的低速
     - Python、Ruby、PHP
     - 動的型付けで、主にバイトコードを解釈して実行する。JIT コンパイラの導入などで改善が進んでいる。

ただし、比較的低速な言語でも、重い処理を C などで書かれたライブラリに任せることで、実用上十分な性能を得られることが多い（Python の NumPy など）。また、Web アプリケーションのように処理時間の多くをデータベースやネットワークの待ち時間が占める場合、言語の実行性能の差は全体の性能にあまり表れない。

エコシステム
------------

.. list-table:: エコシステムの比較
   :header-rows: 1
   :widths: 13 27 20 40

   * - 言語
     - ビルド・パッケージ管理
     - パッケージリポジトリ
     - 代表的なフレームワーク・ライブラリ
   * - C
     - Make、CMake（標準のパッケージマネージャはない）
     - ―
     - ―
   * - C++
     - CMake、vcpkg、Conan
     - ―
     - Boost、Qt、Unreal Engine
   * - Rust
     - Cargo
     - crates.io
     - Tokio、Serde、Axum
   * - Go
     - ``go`` コマンド（Go モジュール）
     - （Git リポジトリなどから直接取得）
     - Gin、gRPC、Cobra
   * - Java
     - Maven、Gradle
     - Maven Central
     - Spring Boot、Jakarta EE、Quarkus
   * - C#
     - ``dotnet`` コマンド、MSBuild
     - NuGet
     - ASP.NET Core、Entity Framework Core、Unity
   * - Kotlin
     - Gradle、Maven
     - Maven Central
     - Ktor、Jetpack Compose、Spring Boot
   * - Swift
     - Swift Package Manager、Xcode
     - （Git リポジトリなどから直接取得）
     - SwiftUI、UIKit、Vapor
   * - Python
     - pip、uv、Poetry、conda
     - PyPI
     - Django、FastAPI、NumPy、pandas、PyTorch
   * - JavaScript、TypeScript
     - npm、pnpm、Yarn
     - npm レジストリ
     - React、Vue.js、Angular、Next.js、Express
   * - Ruby
     - RubyGems、Bundler
     - RubyGems.org
     - Ruby on Rails、Sinatra
   * - PHP
     - Composer
     - Packagist
     - Laravel、Symfony、WordPress
   * - SQL
     - （RDBMS ごとに異なる）
     - ―
     - ORM、マイグレーションツール

2010 年代以降に登場した言語（Rust、Go など）は、ビルド、依存関係の管理、テスト、フォーマットといったツールを公式に一体で提供する傾向がある。一方、C と C++ はツールが統一されておらず、プロジェクトごとにビルドの方法が異なることが多い。

サンプルプログラムの比較
------------------------

各言語の章で示した\ :ref:`sample-program`\ の実装を比べると、言語の性格の違いがよく分かる。

.. list-table:: サンプルプログラムの実装の比較
   :header-rows: 1
   :widths: 13 30 30 12 15

   * - 言語
     - 出現回数の集計
     - 並べ替え
     - 行数
     - 参照先
   * - C
     - 構造体の配列を線形探索
     - ``qsort`` と比較関数
     - 53
     - :ref:`lang-c`
   * - C++
     - ``std::map``
     - ``std::ranges::sort`` とラムダ式
     - 36
     - :ref:`lang-cpp`
   * - Rust
     - ``HashMap`` の ``entry``
     - ``sort_by`` とクロージャ
     - 24
     - :ref:`lang-rust`
   * - Go
     - 組込みの ``map``
     - ``slices.SortFunc``
     - 39
     - :ref:`lang-go`
   * - Java
     - ストリームと ``Collectors.groupingBy``
     - ``Comparator`` の組み合わせ
     - 32
     - :ref:`lang-java`
   * - C#
     - LINQ の ``GroupBy``
     - LINQ の ``OrderByDescending``・``ThenBy``
     - 25
     - :ref:`lang-csharp`
   * - Kotlin
     - ``groupingBy`` と ``eachCount``
     - ``sortedWith`` と比較関数の組み合わせ
     - 14
     - :ref:`lang-kotlin`
   * - Swift
     - 辞書の既定値付きの添字
     - ``sorted`` とクロージャ
     - 17
     - :ref:`lang-swift`
   * - Python
     - ``collections.Counter``
     - ``sorted`` とキー関数
     - 12
     - :ref:`lang-python`
   * - JavaScript
     - ``Map``
     - ``sort`` と比較関数
     - 16
     - :ref:`lang-javascript`
   * - TypeScript
     - ``Map``
     - ``sort`` と比較関数
     - 17
     - :ref:`lang-typescript`
   * - Ruby
     - ``tally``
     - ``sort_by`` とブロック
     - 10
     - :ref:`lang-ruby`
   * - PHP
     - ``array_count_values``
     - ``uksort`` と宇宙船演算子
     - 16
     - :ref:`lang-php`
   * - SQL
     - ``GROUP BY`` と ``COUNT(*)``
     - ``ORDER BY``
     - 14
     - :ref:`lang-sql`

行数は、空行とコメントを除いたサンプルコードの行数である。書き方や書式の規約によって変わるため、目安として扱ってほしい。

標準ライブラリに連想配列を持たない C は、データ構造から自分で実装する必要があり、最も長くなっている。Go は「ループと条件分岐で明示的に書く」文化を反映して比較的長い。一方、Ruby、Python、Kotlin は、出現回数の集計そのものを 1 つのメソッドや関数で表現でき、短く記述できる。ただし、コードが短いことは必ずしも優れていることを意味しない。C のコードは何が起きているかがすべて明示されており、Go のコードは誰が書いても似た形になる。それぞれの言語が何を重視しているかが、コードの形に表れている。

人気と採用の動向
----------------

言語の人気や利用状況を示す指標はいくつかあるが、調査の方法によって結果は大きく異なる。主な指標を次に示す。

.. list-table:: 言語の人気を示す主な指標
   :header-rows: 1
   :widths: 25 40 35

   * - 指標
     - 方法
     - 近年の傾向
   * - TIOBE Index [TIOBE]_
     - 検索エンジンでの言語名の検索結果の数を基に、毎月算出する。
     - 2021 年 10 月に Python が初めて首位となり、その後も首位を維持している。C、C++、Java も上位に位置する。
   * - Stack Overflow Developer Survey [SO-Survey]_
     - 開発者へのアンケートを毎年実施する。
     - 使用率では JavaScript が長年にわたって首位である。Rust は「使い続けたい言語」として高い評価を得続けている。
   * - GitHub Octoverse [Octoverse]_
     - GitHub 上のリポジトリや開発者の活動を集計する。
     - 2025 年の報告で、TypeScript が貢献者数で Python と JavaScript を上回り、GitHub で最も使われている言語となった。

これらの指標は、言語の優劣ではなく、話題性や利用者の層を反映したものである。言語を選ぶ際には、人気の指標よりも、目的の分野でのライブラリの充実度や、チームの経験を重視するべきである。言語の選び方については\ :doc:`selection`\ で述べる。
