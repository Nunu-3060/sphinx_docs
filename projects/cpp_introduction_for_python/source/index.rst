C++ 入門 ― Python 経験者のための C++
====================================================

本資料は、Python の使用経験はあるものの C++ を使ったことがない方を対象とした C++ の入門資料です。Python と比較しながら、C++ の考え方と基本的な書き方を段階的に説明します。

対象読者
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 前提
   * - C++ の使用経験
     - なし
   * - Python の使用経験
     - あり（変数、関数、クラス、リスト、辞書を使ったプログラムを書ける程度）

本資料の構成
--------------------

.. list-table::
   :header-rows: 1
   :widths: 10 25 65

   * - 章
     - 題目
     - 主な内容
   * - 1
     - はじめに
     - 本資料の目的、読み方、前提とする環境
   * - 2
     - C++ の概要
     - C++ の特徴、Python との違い、C++ の規格
   * - 3
     - 開発環境とビルドの流れ
     - コンパイラーの導入、Hello World、ビルドの流れ、コンパイラーの警告
   * - 4
     - 基本文法
     - main 関数、文とブロック、コメント、標準入出力、名前空間
   * - 5
     - 変数と型
     - 基本型、静的型付け、初期化、auto、const と constexpr、型変換
   * - 6
     - 演算子と制御構文
     - 演算子、条件分岐、繰り返し
   * - 7
     - 関数
     - 宣言と定義、引数の渡し方、オーバーロード、ヘッダーファイル
   * - 8
     - ポインターと参照
     - メモリの考え方、ポインター、参照、Python の変数との違い
   * - 9
     - 標準ライブラリのコンテナ
     - std::string、std::vector、std::map などとイテレーター
   * - 10
     - クラス
     - クラスの定義、コンストラクター、継承、仮想関数
   * - 11
     - リソース管理
     - RAII、スマートポインター、コピーとムーブ
   * - 12
     - テンプレート
     - 関数テンプレート、クラステンプレート、コンセプト
   * - 13
     - アルゴリズムとラムダ式
     - 標準アルゴリズム、ラムダ式、Ranges
   * - 14
     - エラー処理
     - 例外、std::optional、未定義動作
   * - 15
     - 実践的な開発
     - CMake、デバッグ、Python との連携
   * - 16
     - コーディング規約
     - 代表的なガイドライン、命名規則、clang-format、静的解析
   * - 付録
     - 付録
     - Python と C++ の対応表、用語集、参考資料

目次
--------------------

.. toctree::
   :maxdepth: 2
   :numbered:

   chapters/01_introduction
   chapters/02_overview
   chapters/03_environment
   chapters/04_basic_syntax
   chapters/05_variables_and_types
   chapters/06_operators_and_control
   chapters/07_functions
   chapters/08_pointers_and_references
   chapters/09_containers
   chapters/10_classes
   chapters/11_resource_management
   chapters/12_templates
   chapters/13_algorithms_and_lambdas
   chapters/14_error_handling
   chapters/15_practice
   chapters/16_coding_standards

.. toctree::
   :maxdepth: 2
   :caption: 付録

   chapters/appendix_a_correspondence
   chapters/appendix_b_glossary
   chapters/appendix_c_references
