サンプルコード一覧
==================

本資料で使用した ``examples/`` 以下の Python スクリプトをまとめたページである。各章の本文では、スクリプトの一部だけを抜き出して示している。全体を通して読みたい場合は、このページを使う。

:download:`examples.zip <_static/downloads/examples.zip>` から全てのスクリプトをまとめてダウンロードできる。展開すると、``examples`` ディレクトリの中に、このページと同じ 9 個のスクリプトが入っている。

各スクリプトの実行方法は、:doc:`intro`\ の「実行環境」の節で説明している。

.. contents:: このページの目次
   :local:
   :depth: 1

color_utils.py
----------------

全ての章で使用する共通のモジュールである。色の変換（ガンマ補正、HSV、CIE XYZ、CIELAB、OKLab、OKLCH）、色域への収め方、コントラスト比の計算、画像の保存などの関数を定義している。

:download:`examples/color_utils.py <../examples/color_utils.py>`

.. literalinclude:: ../examples/color_utils.py
   :language: python
   :linenos:

color_basics.py
-----------------

:doc:`basics`\ で使用する。加法混色と減法混色、色の三属性、同時対比の図を作る。

:download:`examples/color_basics.py <../examples/color_basics.py>`

.. literalinclude:: ../examples/color_basics.py
   :language: python
   :linenos:

color_spaces.py
-----------------

:doc:`color_spaces`\ で使用する。ガンマ補正の階調、HSV と OKLCH の比較、OKLab の断面、色差の比較の図を作る。

:download:`examples/color_spaces.py <../examples/color_spaces.py>`

.. literalinclude:: ../examples/color_spaces.py
   :language: python
   :linenos:

harmony.py
------------

:doc:`harmony`\ で使用する。色相環、色相とトーンにもとづく配色、配色の面積比の図を作る。

:download:`examples/harmony.py <../examples/harmony.py>`

.. literalinclude:: ../examples/harmony.py
   :language: python
   :linenos:

palette.py
------------

:doc:`palette`\ で使用する。色空間ごとの補間、カラースケールの作成、k-means 法による配色の抽出の図を作る。カラースケールを作る関数は ``ui_colors.py`` から、夕焼けの画像を作る関数は ``print_colors.py`` から使う。

:download:`examples/palette.py <../examples/palette.py>`

.. literalinclude:: ../examples/palette.py
   :language: python
   :linenos:

dataviz.py
------------

:doc:`dataviz`\ で使用する。カラーマップの種類、jet と連続のカラーマップの比較、カテゴリの配色の図を作る。

:download:`examples/dataviz.py <../examples/dataviz.py>`

.. literalinclude:: ../examples/dataviz.py
   :language: python
   :linenos:

accessibility.py
------------------

:doc:`accessibility`\ で使用する。コントラスト比の判定、色覚の多様性のシミュレーション、色だけに頼らないグラフの図を作る。

:download:`examples/accessibility.py <../examples/accessibility.py>`

.. literalinclude:: ../examples/accessibility.py
   :language: python
   :linenos:

ui_colors.py
--------------

:doc:`ui`\ で使用する。役割ごとのカラースケール、トークンによるテーマ、ブランドカラーを組み込んだカラースケールの図を作り、コントラスト比を確かめる。

:download:`examples/ui_colors.py <../examples/ui_colors.py>`

.. literalinclude:: ../examples/ui_colors.py
   :language: python
   :linenos:

print_colors.py
-----------------

:doc:`print`\ で使用する。簡易的な式による CMYK の色分解と、ドットゲインと用紙の影響の簡易モデルの図を作る。

:download:`examples/print_colors.py <../examples/print_colors.py>`

.. literalinclude:: ../examples/print_colors.py
   :language: python
   :linenos:
