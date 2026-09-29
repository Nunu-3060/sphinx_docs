Python と C++ の対応表
============================================================

本文で扱った Python と C++ の対応を一覧にまとめます。C++ の列は代表的な書き方であり、詳細は各章を参照してください。

基本文法
------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 項目
     - Python
     - C++
   * - 出力
     - ``print(x)``
     - ``std::cout << x << '\n';``
   * - 1 行の入力
     - ``s = input()``
     - ``std::getline(std::cin, s);``
   * - コメント
     - ``# コメント``
     - ``// コメント``
   * - ライブラリの取り込み
     - ``import math``
     - ``#include <cmath>``
   * - 変数の宣言
     - ``x = 1``
     - ``int x = 1;`` または ``auto x = 1;``
   * - 定数
     - ``MAX = 100``\ （慣習）
     - ``constexpr int max = 100;``
   * - 型変換
     - ``float(n)``
     - ``static_cast<double>(n)``
   * - 整数の除算
     - ``a // b``
     - ``a / b``\ （丸め方向が異なる）
   * - 論理演算
     - ``and``、``or``、``not``
     - ``&&``、``||``、``!``
   * - 条件式
     - ``a if cond else b``
     - ``cond ? a : b``

制御構文と関数
------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 項目
     - Python
     - C++
   * - 条件分岐
     - ``if x > 0:``、``elif``、``else:``
     - ``if (x > 0) { }``、``else if``、``else { }``
   * - 回数を指定した繰り返し
     - ``for i in range(n):``
     - ``for (int i = 0; i < n; ++i) { }``
   * - 要素の繰り返し
     - ``for x in v:``
     - ``for (const auto& x : v) { }``
   * - 関数の定義
     - ``def f(x):``
     - ``int f(int x) { }``
   * - 値を返さない関数
     - ``return`` を書かない（``None`` を返す）
     - 戻り値の型を ``void`` にする
   * - 無名関数
     - ``lambda x: x * 2``
     - ``[](int x) { return x * 2; }``

データ構造
------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 項目
     - Python
     - C++
   * - 文字列
     - ``str``
     - ``std::string``
   * - リスト
     - ``list``
     - ``std::vector``
   * - 辞書
     - ``dict``
     - ``std::unordered_map``、``std::map``
   * - 集合
     - ``set``
     - ``std::unordered_set``、``std::set``
   * - 要素数
     - ``len(v)``
     - ``v.size()``
   * - 末尾への追加
     - ``v.append(x)``
     - ``v.push_back(x)``
   * - アンパック代入
     - ``a, b = pair``
     - ``auto [a, b] = pair;``
   * - 並べ替え
     - ``v.sort()``
     - ``std::sort(v.begin(), v.end());``
   * - 値がないこと
     - ``None``
     - ``std::nullopt``\ （``std::optional``）、``nullptr``\ （ポインター）

クラスとエラー処理
------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 項目
     - Python
     - C++
   * - 初期化
     - ``__init__``
     - コンストラクター
   * - 自分自身
     - ``self``
     - ``this``\ （通常は省略する）
   * - 継承
     - ``class B(A):``
     - ``class B : public A { };``
   * - 抽象メソッド
     - ``@abstractmethod``
     - ``virtual void f() = 0;``
   * - 後処理
     - ``with`` 文
     - RAII（デストラクター）
   * - 例外の送出
     - ``raise``
     - ``throw``
   * - 例外の捕捉
     - ``try:``、``except E as e:``
     - ``try { }``、``catch (const E& e) { }``
