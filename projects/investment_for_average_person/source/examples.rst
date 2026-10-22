サンプルコード
==============

本書で紹介した試算を、自分の条件で試すための Python のスクリプトを掲載する。各ファイルは、見出しの下のリンクからダウンロードできる。

試算の結果は、毎年一定の利回りで運用できたと仮定した場合の目安である。実際の運用成果は毎年大きく上下するため、将来の成果を示すものではない。

実行の方法
----------

すべてのスクリプトは Python 3.10 以降の標準ライブラリだけで動作し、追加のパッケージは不要である。ダウンロードしたフォルダで、次のように実行する。

.. code-block:: console
   :linenos:

   python accumulation_simulation.py
   python accumulation_simulation.py --monthly 20000 --rate 4 --years 25

``--help`` を付けて実行すると、指定できる条件の一覧が表示される。

``cost_comparison.py`` は ``accumulation_simulation.py`` の関数を使うため、2 つのファイルを同じフォルダに置いて実行する。

.. list-table:: サンプルコードの一覧
   :header-rows: 1
   :widths: 35 40 25

   * - ファイル
     - 内容
     - 関連する章
   * - ``accumulation_simulation.py``
     - 毎月の積立投資の結果の試算
     - :doc:`04_money_basics`
   * - ``cost_comparison.py``
     - 運用コストの違いによる最終残高の比較
     - :doc:`04_money_basics`
   * - ``withdrawal_simulation.py``
     - 定額方式と定率方式の取り崩しの比較
     - :doc:`13_continuing`

積立投資の試算
--------------

ダウンロード：\ :download:`accumulation_simulation.py <../examples/accumulation_simulation.py>`

毎月の積立額、コストを引く前の年率リターン、年率コスト、積立期間を指定すると、各年末の元本・残高・運用益を表示する。既定の条件（毎月 3 万円、年 5 %、コスト年 0.1 %、30 年）で実行した結果は次のとおりである。

.. code-block:: text
   :linenos:

   毎月 30,000 円、年率 5.0 % (コスト 0.1 %)、30 年間の試算
      年      元本 (円)      残高 (円)    運用益 (円)
      5      1,800,000      2,037,564        237,564
     10      3,600,000      4,625,710      1,025,710
     15      5,400,000      7,913,214      2,513,214
     20      7,200,000     12,089,052      4,889,052
     25      9,000,000     17,393,267      8,393,267
     30     10,800,000     24,130,764     13,330,764

.. literalinclude:: ../examples/accumulation_simulation.py
   :language: python
   :linenos:

運用コストの比較
----------------

ダウンロード：\ :download:`cost_comparison.py <../examples/cost_comparison.py>`

積立の条件を同じにして、年率コストだけを変えたときの最終残高を比べる。``--costs`` に比べたいコスト（%）を空白で区切って指定する。

.. literalinclude:: ../examples/cost_comparison.py
   :language: python
   :linenos:

取り崩しの比較
--------------

ダウンロード：\ :download:`withdrawal_simulation.py <../examples/withdrawal_simulation.py>`

取り崩し開始時の資産、運用の年率リターン、定額方式で毎年引き出す額、定率方式で毎年引き出す割合を指定すると、2 つの方式の引き出し額と残高を並べて表示する。

.. literalinclude:: ../examples/withdrawal_simulation.py
   :language: python
   :linenos:
