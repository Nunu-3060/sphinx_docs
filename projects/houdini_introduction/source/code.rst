サンプルコード一覧
==================

本資料で使用した ``examples`` ディレクトリのファイルをまとめたページである。各章の本文では、ファイルの一部だけを示していることがある。全体を通して読みたい場合は、このページを使う。

:download:`examples.zip <_static/downloads/examples.zip>` から全てのファイルをまとめてダウンロードできる。展開すると ``examples`` ディレクトリができ、その中に Python のスクリプト 14 個、``vex`` ディレクトリに VEX のコード 7 個、静的検査の設定ファイル ``setup.cfg`` が入っている。

スクリプトの実行方法は、:doc:`intro` の「サンプルコードの使い方」で説明している。全ての Python のスクリプトは、flake8（1 行 120 文字まで）と mypy（``strict = True``）の検査で違反が無いことを確かめている。

.. contents:: このページの目次
   :local:
   :depth: 2

Python のスクリプト
-------------------

common.py
^^^^^^^^^

全てのスクリプトで使う共通の関数を定義したモジュールである。同じ名前のノードを作り直す関数、VEX のファイルを読む関数、エラーを確かめる関数、hip ファイルを保存する関数がある。単独では実行しない。

:download:`examples/common.py <../examples/common.py>`

.. literalinclude:: ../examples/common.py
   :language: python
   :linenos:

build_table.py
^^^^^^^^^^^^^^

:doc:`modeling` の机を作る。

:download:`examples/build_table.py <../examples/build_table.py>`

.. literalinclude:: ../examples/build_table.py
   :language: python
   :linenos:

build_attributes.py
^^^^^^^^^^^^^^^^^^^

:doc:`attributes` の、起伏のある地形に色を付ける例を作る。

:download:`examples/build_attributes.py <../examples/build_attributes.py>`

.. literalinclude:: ../examples/build_attributes.py
   :language: python
   :linenos:

build_expressions.py
^^^^^^^^^^^^^^^^^^^^

:doc:`expressions` の、弾みながら回るボールを作る。

:download:`examples/build_expressions.py <../examples/build_expressions.py>`

.. literalinclude:: ../examples/build_expressions.py
   :language: python
   :linenos:

build_vex_examples.py
^^^^^^^^^^^^^^^^^^^^^

:doc:`vex` の 4 つの例を作る。VEX のコードは ``vex`` ディレクトリのファイルから読み込む。

:download:`examples/build_vex_examples.py <../examples/build_vex_examples.py>`

.. literalinclude:: ../examples/build_vex_examples.py
   :language: python
   :linenos:

build_stairs.py
^^^^^^^^^^^^^^^

:doc:`procedural` の階段を作る。

:download:`examples/build_stairs.py <../examples/build_stairs.py>`

.. literalinclude:: ../examples/build_stairs.py
   :language: python
   :linenos:

build_city.py
^^^^^^^^^^^^^

:doc:`procedural` の建物群を作る。

:download:`examples/build_city.py <../examples/build_city.py>`

.. literalinclude:: ../examples/build_city.py
   :language: python
   :linenos:

inspect_geometry.py
^^^^^^^^^^^^^^^^^^^

:doc:`python` で使う。ノードの出力のジオメトリの中身を表示する。

:download:`examples/inspect_geometry.py <../examples/inspect_geometry.py>`

.. literalinclude:: ../examples/inspect_geometry.py
   :language: python
   :linenos:

python_sop_wave.py
^^^^^^^^^^^^^^^^^^

:doc:`python` で使う。Python SOP の :guilabel:`Python Code` に貼り付けるコードである。

:download:`examples/python_sop_wave.py <../examples/python_sop_wave.py>`

.. literalinclude:: ../examples/python_sop_wave.py
   :language: python
   :linenos:

build_python_sop.py
^^^^^^^^^^^^^^^^^^^

:doc:`python` で使う。``python_sop_wave.py`` のコードを設定した Python SOP を作る。

:download:`examples/build_python_sop.py <../examples/build_python_sop.py>`

.. literalinclude:: ../examples/build_python_sop.py
   :language: python
   :linenos:

shelf_tool_add_out.py
^^^^^^^^^^^^^^^^^^^^^

:doc:`python` で使う。シェルフツールの :guilabel:`Script` タブに貼り付けるコードである。

:download:`examples/shelf_tool_add_out.py <../examples/shelf_tool_add_out.py>`

.. literalinclude:: ../examples/shelf_tool_add_out.py
   :language: python
   :linenos:

build_hda.py
^^^^^^^^^^^^

:doc:`hda` の、階段のデジタルアセットを作る。

:download:`examples/build_hda.py <../examples/build_hda.py>`

.. literalinclude:: ../examples/build_hda.py
   :language: python
   :linenos:

build_render.py
^^^^^^^^^^^^^^^

:doc:`rendering` の、机をレンダリングする LOP のネットワークを作る。

:download:`examples/build_render.py <../examples/build_render.py>`

.. literalinclude:: ../examples/build_render.py
   :language: python
   :linenos:

build_rbd.py
^^^^^^^^^^^^

:doc:`simulation` の、箱の壁を崩す剛体シミュレーションを作る。

:download:`examples/build_rbd.py <../examples/build_rbd.py>`

.. literalinclude:: ../examples/build_rbd.py
   :language: python
   :linenos:

VEX のコード
------------

Attribute Wrangle の :guilabel:`VEXpression` に貼り付けて使う。``ch`` 系の関数が読むパラメーターは、:guilabel:`VEXpression` の右にあるボタンで作る（:doc:`vex` を参照）。

wave.vex
^^^^^^^^

:doc:`vex` の例 1。

:download:`examples/vex/wave.vex <../examples/vex/wave.vex>`

.. literalinclude:: ../examples/vex/wave.vex
   :language: vex
   :linenos:

noise_displace.vex
^^^^^^^^^^^^^^^^^^

:doc:`vex` の例 2。

:download:`examples/vex/noise_displace.vex <../examples/vex/noise_displace.vex>`

.. literalinclude:: ../examples/vex/noise_displace.vex
   :language: vex
   :linenos:

spiral.vex
^^^^^^^^^^

:doc:`vex` の例 3。

:download:`examples/vex/spiral.vex <../examples/vex/spiral.vex>`

.. literalinclude:: ../examples/vex/spiral.vex
   :language: vex
   :linenos:

nearest_color.vex
^^^^^^^^^^^^^^^^^

:doc:`vex` の例 4。

:download:`examples/vex/nearest_color.vex <../examples/vex/nearest_color.vex>`

.. literalinclude:: ../examples/vex/nearest_color.vex
   :language: vex
   :linenos:

stairs_points.vex
^^^^^^^^^^^^^^^^^

:doc:`procedural` の階段で、段ごとのポイントを作る。

:download:`examples/vex/stairs_points.vex <../examples/vex/stairs_points.vex>`

.. literalinclude:: ../examples/vex/stairs_points.vex
   :language: vex
   :linenos:

lot_attributes.vex
^^^^^^^^^^^^^^^^^^

:doc:`procedural` の建物群で、区画ごとの高さを決める。

:download:`examples/vex/lot_attributes.vex <../examples/vex/lot_attributes.vex>`

.. literalinclude:: ../examples/vex/lot_attributes.vex
   :language: vex
   :linenos:

building_color.vex
^^^^^^^^^^^^^^^^^^

:doc:`procedural` の建物群で、高さに応じて色を付ける。

:download:`examples/vex/building_color.vex <../examples/vex/building_color.vex>`

.. literalinclude:: ../examples/vex/building_color.vex
   :language: vex
   :linenos:

setup.cfg
---------

flake8 と mypy の設定ファイルである。``examples`` ディレクトリで ``python -m flake8`` と ``python -m mypy .`` を実行すると、この設定で検査される。

:download:`examples/setup.cfg <../examples/setup.cfg>`

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
