はじめに
========

正規表現とは
------------

:term:`正規表現`\ は、文字列の「形」を記述するための小さな言語である。たとえば「数字が 3 個、ハイフン、数字が 4 個」という形は、正規表現では ``\d{3}-\d{4}`` と書ける。この記述を\ :term:`パターン`\ と呼ぶ。パターンを使うと、文字列の中からその形に一致する部分を探したり、文字列全体がその形になっているかを確かめたりできる。

正規表現の起源は、1950 年代に数学者スティーヴン・クリーネが考案した形式言語の理論にある。1960 年代後半にケン・トンプソンがテキストエディター QED に実装し、その後 ed や grep などの UNIX のツールを通じて広まった。現在では、ほとんどのプログラミング言語、テキストエディター、データベース、コマンドラインツールが正規表現に対応している。

何に使うのか
------------

正規表現の用途は、大きく次の 4 つに分けられる。

.. list-table:: 正規表現の主な用途
   :header-rows: 1
   :widths: 15 45 40

   * - 用途
     - 内容
     - 例
   * - 検索
     - 文字列の中にパターンに一致する部分があるかを調べる
     - ログから ``ERROR`` を含む行を探す
   * - 検証
     - 文字列全体がパターンの形になっているかを調べる
     - 入力された郵便番号が ``123-4567`` の形かを確かめる
   * - 抽出
     - 一致した部分や、その一部を取り出す
     - ログの各行から日時とメッセージを取り出す
   * - 置換
     - 一致した部分を別の文字列に置き換える
     - ``2026/10/19`` を ``2026-10-19`` に書き換える

正規表現を使わなくても、Python の文字列メソッドだけで同じ処理を書くことはできる。たとえば「数字 3 個、ハイフン、数字 4 個」かどうかを調べる処理は次のようになる。

.. code-block:: python
   :linenos:
   :caption: 文字列メソッドだけで郵便番号の形を調べる

   def is_postal_code(s: str) -> bool:
       if len(s) != 8 or s[3] != "-":
           return False
       digits = s[:3] + s[4:]
       return all(c in "0123456789" for c in digits)

正規表現を使うと、同じ処理を 1 行で書ける。

.. code-block:: python
   :linenos:
   :caption: 正規表現で郵便番号の形を調べる

   import re


   def is_postal_code(s: str) -> bool:
       return re.fullmatch(r"[0-9]{3}-[0-9]{4}", s) is not None

形が複雑になるほど、この差は大きくなる。一方で、正規表現は短く書ける反面、読みにくくなりやすく、使い方を誤ると性能上の問題も起こす。本書ではその両面を扱う。

本書の構成
----------

本書は次の順に進む。

* 第 2 章から第 8 章では、正規表現の構文を 1 つずつ説明する。
* 第 9 章では、Python の ``re`` モジュールが提供する関数と、その使い分けを説明する。
* 第 10 章では、ログの解析や入力値の検証など、実務でよく使うパターンを紹介する。
* 第 11 章では、性能上の問題（:term:`ReDoS`）やよくある間違い、正規表現を使うべきでない場面を説明する。
* 第 12 章では、grep、sed、JavaScript など、Python 以外の実装との違いをまとめる。

付録には、構文の早見表、用語集、参考文献を収めた。

前提とする環境
--------------

本書は Python 3.11 以降を前提とする。Python 3.11 で、:term:`強欲量指定子`\ と\ :term:`アトミックグループ`\ が ``re`` モジュールに追加されたためである。本書のサンプルコードは Python 3.14 で動作を確認した。``re`` は標準ライブラリなので、追加のインストールは不要である。

本書の表記
----------

本文中のパターンは ``\d+`` のように等幅フォントで示す。Python のコードでは、表示を行う行の末尾に ``# ->`` で始まるコメントを付け、その行を実行したときに表示される内容を示す。

.. code-block:: python
   :linenos:
   :caption: 表記の例

   print(re.findall(r"\d+", "a1b22"))  # -> ['1', '22']

ループの中で表示する場合など、表示内容が複数行になるときは、ループの後に ``# ->`` のコメントを並べて示す。

本書では、パターンと文字列の関係を「一致する」と表現する。ただし、:term:`貪欲マッチ`\ や\ :term:`最短マッチ`\ など、一般に定着している用語には「マッチ」をそのまま使う。

サンプルコード
--------------

本文で引用するコードはすべて、次のサンプルコードから抜き出したものである。各ファイルは単独で実行でき、実行するとその章のデモをすべて表示する。

.. list-table:: サンプルコードの一覧
   :header-rows: 1
   :widths: 40 60

   * - ファイル
     - 内容
   * - :download:`ch02_first_step.py <../examples/ch02_first_step.py>`
     - 第 2 章「最初の一歩」
   * - :download:`ch03_char_class.py <../examples/ch03_char_class.py>`
     - 第 3 章「文字クラス」
   * - :download:`ch04_quantifier.py <../examples/ch04_quantifier.py>`
     - 第 4 章「量指定子」
   * - :download:`ch05_anchor.py <../examples/ch05_anchor.py>`
     - 第 5 章「アンカーと境界」
   * - :download:`ch06_group.py <../examples/ch06_group.py>`
     - 第 6 章「グループと選択」
   * - :download:`ch07_lookaround.py <../examples/ch07_lookaround.py>`
     - 第 7 章「先読みと後読み」
   * - :download:`ch08_flags.py <../examples/ch08_flags.py>`
     - 第 8 章「フラグ」
   * - :download:`ch09_re_module.py <../examples/ch09_re_module.py>`
     - 第 9 章「Python の re モジュール」
   * - :download:`ch10_practical.py <../examples/ch10_practical.py>`
     - 第 10 章「実践パターン集」
   * - :download:`sample.log <../examples/sample.log>`
     - 第 10 章で解析するログファイル
   * - :download:`ch11_pitfalls.py <../examples/ch11_pitfalls.py>`
     - 第 11 章「落とし穴と性能」
   * - :download:`ch11_redos_benchmark.py <../examples/ch11_redos_benchmark.py>`
     - 第 11 章のグラフを作成するスクリプト（matplotlib が必要）
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定ファイル

各ファイルは次のように実行する。

.. code-block:: console
   :linenos:

   python ch02_first_step.py
