14. カバレッジの計測
====================

5 章では、テストがコードをどれだけ実行したかを表すカバレッジの考え方を学んだ。この章では、coverage.py を使って Python のコードのカバレッジを計測し、その結果をテストの改善に活かす方法を学ぶ。

14.1 coverage.py
----------------

coverage.py は、Python のプログラムの実行中に、どの行とどの分岐が実行されたかを記録するツールである。pytest と組み合わせて、テストのカバレッジを計測できる。

計測の設定は、``pyproject.toml`` に書ける。本書のサンプルコードでは、次の設定を使っている。

.. literalinclude:: ../examples/pyproject.toml
   :language: toml
   :caption: pyproject.toml（coverage.py の設定の部分）
   :lines: 32-
   :lineno-start: 32
   :linenos:

``branch = true``\ （33 行目）は、命令網羅だけでなく分岐網羅も計測することを表す。``source``\ （34 行目）は、計測の対象とするパッケージである。テストコードそのものは計測の対象から外し、題材の ``shop`` パッケージだけを計測する。

14.2 計測の手順
---------------

5 章の ``member_rank`` を、次の不十分なテストで計測してみる。

.. literalinclude:: ../examples/ch14_coverage/test_member_rank_partial.py
   :language: python
   :caption: ch14_coverage/test_member_rank_partial.py
   :linenos:

計測は、``coverage run`` で pytest を実行し、``coverage report`` で結果を表示するという 2 段階で行う。

.. code-block:: console
   :linenos:

   $ python -m coverage run -m pytest ch14_coverage/test_member_rank_partial.py
   $ python -m coverage report -m --include=shop/member.py

1 行目では、``python -m pytest`` の代わりに ``python -m coverage run -m pytest`` と書くことで、coverage.py の計測の下で pytest を実行する。計測結果は、``.coverage`` という名前のファイルに保存される。2 行目の ``-m`` オプションは、実行されなかった行の番号を表示することを、``--include`` オプションは、表示する対象のファイルを絞ることを表す。

.. code-block:: text

   Name             Stmts   Miss Branch BrPart  Cover   Missing
   ------------------------------------------------------------
   shop\member.py       6      1      4      1    80%   17
   ------------------------------------------------------------
   TOTAL                6      1      4      1    80%

各列の意味は次のとおりである。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 列
     - 意味
   * - Stmts
     - 実行できる文の数
   * - Miss
     - 実行されなかった文の数
   * - Branch
     - 分岐の数（判定ごとの真と偽の行き先の数）
   * - BrPart
     - 真と偽の一方しか実行されなかった判定の数
   * - Cover
     - カバレッジ（文と分岐を合わせて計算した割合）
   * - Missing
     - 実行されなかった行の番号と、実行されなかった分岐

Cover の値は、次の式で計算される。

.. math::

   \text{Cover} = \frac{(\text{Stmts} - \text{Miss}) + (\text{実行された分岐の数})}{\text{Stmts} + \text{Branch}} \times 100\ [\%]

この例では、6 つの文のうち 5 つ、4 つの分岐のうち 3 つが実行されたため、:math:`(5 + 3) / (6 + 4) = 80\ \%` となる。Missing の 17 は、``member.py`` の 17 行目（\ ``return "silver"``\ ）が実行されなかったことを示す。gold と bronze のテストしかないため、silver の場合が抜けていることが分かる。

14.3 HTML のレポート
--------------------

``coverage html`` を実行すると、ソースコードに実行の有無を色で重ねて表示する HTML のレポートを作る。

.. code-block:: console
   :linenos:

   $ python -m coverage html

``htmlcov`` フォルダーの ``index.html`` をブラウザーで開くと、ファイルごとのカバレッジの一覧が表示される。ファイル名を選ぶと、実行された行が緑、実行されなかった行が赤、一方の分岐しか実行されなかった判定の行が黄色で表示される。どこにテストが足りないかを、コードを見ながら確かめられる。

14.4 不足したテストを補う
-------------------------

5.6 節で設計した MC/DC を満たすテストケースを実装し、計測し直す。

.. literalinclude:: ../examples/ch14_coverage/test_member_rank_mcdc.py
   :language: python
   :caption: ch14_coverage/test_member_rank_mcdc.py
   :linenos:

.. code-block:: console
   :linenos:

   $ python -m coverage run -m pytest ch14_coverage/test_member_rank_mcdc.py
   $ python -m coverage report -m --include=shop/member.py

.. code-block:: text

   Name             Stmts   Miss Branch BrPart  Cover   Missing
   ------------------------------------------------------------
   shop\member.py       6      0      4      0   100%
   ------------------------------------------------------------
   TOTAL                6      0      4      0   100%

すべての文と分岐が実行され、カバレッジは 100 % になった。

ただし、coverage.py が計測するのは命令網羅と分岐網羅であり、条件網羅や MC/DC は計測できない。たとえば、gold（150,000 円、5 年）、silver（80,000 円、1 年）、bronze（1,000 円、1 年）の 3 つのテストケースでも、カバレッジは 100 % になる。しかし、この 3 つでは、判定 2 の条件 D（会員歴が 5 年以上）が真になる場合が試されておらず、MC/DC は満たされない。カバレッジが 100 % になった後も、5 章の網羅基準や 4 章の技法に照らして、テストケースが十分かを考える必要がある。

14.5 サンプルコード全体の計測
-----------------------------

引数を指定せずに pytest を実行すると、``pyproject.toml`` の ``testpaths`` のすべてのテストが実行され、``shop`` パッケージ全体のカバレッジが計測される。

.. code-block:: console
   :linenos:

   $ python -m coverage run -m pytest
   $ python -m coverage report -m

.. code-block:: text

   Name               Stmts   Miss Branch BrPart  Cover   Missing
   --------------------------------------------------------------
   shop\__init__.py       0      0      0      0   100%
   shop\cart.py          18      0      2      0   100%
   shop\member.py         6      0      4      0   100%
   shop\order.py         25      0      2      0   100%
   shop\shipping.py      16      0      4      0   100%
   --------------------------------------------------------------
   TOTAL                 65      0     12      0   100%

pytest のプラグインである pytest-cov をインストールすると、``python -m pytest --cov=shop --cov-branch --cov-report=term-missing`` のように、pytest のオプションとして計測することもできる。

14.6 カバレッジの目標値
-----------------------

カバレッジの目標値を決めるときは、次の点に注意する。

* **目標値を目的にしない**：カバレッジの数値だけを目標にすると、``assert`` のないテストや、意味の薄いテストで数値を上げることが起きる。5.8 節で述べたとおり、カバレッジはテストの不足を見つけるための道具である。
* **一律の値にこだわらない**：業務の計算のように重要で複雑なコードは高い値を目指し、単純な設定の読み込みなどは低くてもよい。全体で 80 % 前後を一つの目安とするプロジェクトが多いが、値そのものより、実行されていない箇所がなぜ実行されていないかを確かめることが重要である。
* **下がったことに気付けるようにする**：17 章の継続的インテグレーションで、カバレッジが一定の値を下回ったらテストを失敗させると、テストのない変更が紛れ込むのを防げる。coverage.py では、``coverage report --fail-under=90`` のように指定する。

テストする価値がないと判断したコード（デバッグ用の処理など）は、行の末尾に ``# pragma: no cover`` というコメントを付けると、計測の対象から外せる。ただし、多用するとカバレッジの数値が実態を表さなくなるため、理由がはっきりしている場合に限って使う。

14.7 まとめ
-----------

* coverage.py は、``coverage run -m pytest`` で計測し、``coverage report -m`` で結果を表示する。``branch = true`` で分岐網羅も計測する。
* Missing の列や HTML のレポートで、実行されなかった行と分岐を確かめ、不足したテストを補う。
* coverage.py は条件網羅や MC/DC を計測できない。カバレッジが 100 % でも、テストケースが十分とは限らない。
* カバレッジの目標値は目的ではなく、テストの不足に気付くための目安として使う。
