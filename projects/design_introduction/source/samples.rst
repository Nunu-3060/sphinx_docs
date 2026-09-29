サンプルコード
==============

本書で使用したサンプルコードの一覧です。ファイル名のリンクからダウンロードできます。各サンプルの実行方法は\ :doc:`introduction`\ を参照してください。

一覧
----

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - ファイル
     - 章
     - 内容
   * - :download:`ch01_principles.py <../examples/ch01_principles.py>`
     - :doc:`principles`
     - 4 原則を適用する前後のカードを描画する
   * - :download:`ch02_color_scheme.py <../examples/ch02_color_scheme.py>`
     - :doc:`color`
     - 基準色から配色パターンを生成する
   * - :download:`ch02_color_contrast.py <../examples/ch02_color_contrast.py>`
     - :doc:`color`
     - コントラスト比を計算する
   * - :download:`ch02_color_vision.py <../examples/ch02_color_vision.py>`
     - :doc:`color`
     - 色覚の違いによる見え方をシミュレーションする
   * - :download:`ch03_typography.py <../examples/ch03_typography.py>`
     - :doc:`typography`
     - ジャンプ率と行送りを比較する
   * - :download:`ch04_layout_grid.py <../examples/ch04_layout_grid.py>`
     - :doc:`layout`
     - グリッドシステムに沿って配置する
   * - :download:`ch05_chart_before_after.py <../examples/ch05_chart_before_after.py>`
     - :doc:`dataviz`
     - 折れ線グラフを改善する
   * - :download:`ch05_colormap.py <../examples/ch05_colormap.py>`
     - :doc:`dataviz`
     - カラーマップの明度を比較する
   * - :download:`ch06_icon_grid.py <../examples/ch06_icon_grid.py>`
     - :doc:`icons_images`
     - グリッドに沿ってアイコンを描画する
   * - :download:`ch06_image_processing.py <../examples/ch06_image_processing.py>`
     - :doc:`icons_images`
     - 写真のトリミング・縮小・文字の重ね方を比較する
   * - :download:`ch07_tkinter_form.py <../examples/ch07_tkinter_form.py>`
     - :doc:`ui`
     - tkinter の入力フォームを比較する
   * - :download:`ch08_design_tokens.py <../examples/ch08_design_tokens.py>`
     - :doc:`design_system`
     - デザイントークンを matplotlib と tkinter に適用する
   * - :download:`ch09_report_makeover.py <../examples/ch09_report_makeover.py>`
     - :doc:`practice`
     - 月次報告の資料を改善する

コードの確認に使った設定ファイルは次のとおりです。サンプルコードと同じフォルダーに置き、そのフォルダーで ``flake8 .`` と ``mypy .`` を実行します。pandas は型情報を同梱していないため、mypy の設定で型チェックの対象外にしています。pandas-stubs をインストールしている場合は、この設定は不要です。

* :download:`setup.cfg <../examples/setup.cfg>`：flake8 の設定
* :download:`mypy.ini <../examples/mypy.ini>`：mypy の設定

ソースコード
------------

ch01_principles.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch01_principles.py
   :language: python
   :linenos:

ch02_color_scheme.py
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch02_color_scheme.py
   :language: python
   :linenos:

ch02_color_contrast.py
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch02_color_contrast.py
   :language: python
   :linenos:

ch02_color_vision.py
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch02_color_vision.py
   :language: python
   :linenos:

ch03_typography.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch03_typography.py
   :language: python
   :linenos:

ch04_layout_grid.py
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch04_layout_grid.py
   :language: python
   :linenos:

ch05_chart_before_after.py
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch05_chart_before_after.py
   :language: python
   :linenos:

ch05_colormap.py
~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch05_colormap.py
   :language: python
   :linenos:

ch06_icon_grid.py
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch06_icon_grid.py
   :language: python
   :linenos:

ch06_image_processing.py
~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch06_image_processing.py
   :language: python
   :linenos:

ch07_tkinter_form.py
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch07_tkinter_form.py
   :language: python
   :linenos:

ch08_design_tokens.py
~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch08_design_tokens.py
   :language: python
   :linenos:

ch09_report_makeover.py
~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch09_report_makeover.py
   :language: python
   :linenos:
