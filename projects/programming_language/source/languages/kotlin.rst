.. _lang-kotlin:

Kotlin
======

基本情報
--------

.. list-table::
   :header-rows: 0
   :widths: 25 75

   * - 登場年
     - 2011 年（2016 年に 1.0）
   * - 設計者
     - JetBrains（開発の初期はアンドレイ・ブレスラフが主導）
   * - 標準仕様
     - Kotlin Language Specification（JetBrains が公開）
   * - 主な処理系
     - Kotlin コンパイラ（JVM、JavaScript、ネイティブ、WebAssembly 向けのコードを生成）
   * - 2026 年時点の状況
     - 2024 年の Kotlin 2.0 で新しいコンパイラ（K2）が正式に採用され、コンパイルが高速化された。Android 開発では Kotlin が第一の言語として推奨されている。

誕生の背景と設計思想
--------------------

Kotlin は、IntelliJ IDEA などの開発ツールを手がける JetBrains が、自社の大規模な Java のコードを書くための、より生産的な言語として開発した。Java は後方互換性を重視するために言語の改良が遅く、記述も冗長であった。一方で Scala のような既存の JVM 言語は、コンパイルが遅く言語仕様も複雑であった。

Kotlin は「実用的な言語」を目標とし、Java との完全な相互運用性を最優先に設計された。既存の Java のコードやライブラリをそのまま呼び出せ、Java から Kotlin のコードを呼び出すこともできるため、既存のプロジェクトに少しずつ導入できる。名称はロシアのサンクトペテルブルク近くにあるコトリン島に由来する。

2017 年に Google が Kotlin を Android の公式開発言語として採用し、2019 年には Android 開発で Kotlin を第一の言語とする「Kotlin-first」の方針を発表したことで、利用が急速に拡大した。

主な特徴
--------

* **null 安全**\ ：型 ``String`` は null を許容せず、``String?`` のように ``?`` を付けた型だけが null を取り得る。安全呼び出し演算子 ``?.`` やエルビス演算子 ``?:`` によって、null の扱いを簡潔に記述できる。
* **簡潔な構文**\ ：型推論、データクラス（``data class``）、デフォルト引数と名前付き引数、文字列テンプレートなどにより、Java と比べて記述量を大幅に減らせる。
* **拡張関数**\ ：既存のクラスを変更せずに、そのクラスのメソッドのように呼び出せる関数を追加できる。
* **コルーチン**\ ：``suspend`` 関数とライブラリ kotlinx.coroutines によって、非同期処理を逐次的なコードとして記述できる（:term:`コルーチン`）。
* **マルチプラットフォーム**\ ：Kotlin Multiplatform により、共通のコードを Android、iOS、デスクトップ、Web、サーバで共有できる。

コード例
--------

.. literalinclude:: ../../examples/kotlin/WordCount.kt
   :language: kotlin
   :linenos:
   :caption: WordCount.kt

Kotlin では、クラスに属さない関数をファイルの最上位に直接書ける（4 行目、10 行目、15 行目）。本体が 1 つの式だけの関数は ``=`` で書ける。6〜7 行目の ``groupingBy { it.value }.eachCount()`` は、標準ライブラリのコレクション操作によって出現回数を数えている。``{ it.value }`` はラムダ式であり、引数が 1 つの場合は暗黙の名前 ``it`` で参照できる。17 行目の ``(word, count)`` は ``Pair`` を分解して受け取る分解宣言である。

同じ処理を書いた :ref:`Java のコード例 <lang-java>`\ と比べると、JVM 上で動作する言語でありながら、記述がかなり簡潔になっていることが分かる。

主な用途
--------

* Android アプリ（UI ツールキット Jetpack Compose も Kotlin で記述する）
* サーバサイドアプリケーション（Spring Boot、Ktor）
* Kotlin Multiplatform による、モバイルアプリのロジックの共通化
* Gradle のビルドスクリプト（Kotlin DSL）

エコシステム
------------

* **ビルドツール**\ ：Gradle（Kotlin DSL）、Maven
* **パッケージリポジトリ**\ ：Maven Central（Java と共通）
* **主要なライブラリとフレームワーク**\ ：kotlinx.coroutines、Ktor、Jetpack Compose、Compose Multiplatform
* **開発環境**\ ：IntelliJ IDEA、Android Studio

長所と短所
----------

長所

* Java と完全な相互運用性を持ち、Java の豊富な資産を利用できる。
* null 安全と簡潔な構文により、安全で読みやすいコードを書ける。
* Android 開発の標準言語であり、情報や人材が豊富である。
* JVM 以外のプラットフォームにも展開できる。

短所

* コンパイル速度が Java より遅い傾向がある（K2 コンパイラで改善された）。
* Android 以外の分野では、Java ほど採用事例や技術者が多くない。
* 開発環境が JetBrains の製品に大きく依存している。
