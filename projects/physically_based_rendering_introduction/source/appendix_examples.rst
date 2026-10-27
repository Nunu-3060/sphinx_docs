付録 B サンプルコード
=====================

本書で用いたサンプルコードの一覧と実行方法を示す。各ファイルは、以下のリンクから個別にダウンロードできる。

一括ダウンロード
----------------

すべてのサンプルコードをまとめた ZIP ファイルを用意している。

* :download:`pbr_examples.zip <_generated/pbr_examples.zip>`

動作環境
--------

* Python 3.11 以上
* NumPy、Pillow、matplotlib

必要なライブラリは、ZIP ファイルに含まれる ``requirements.txt`` を使って次のようにインストールできる。

.. code-block:: console
   :linenos:

   pip install -r requirements.txt

各スクリプトは、``examples`` フォルダで次のように実行する。``--help`` を付けて実行すると、指定できるオプションの一覧が表示される。

.. code-block:: console
   :linenos:

   python fresnel_plot.py
   python brdf_plot.py
   python monte_carlo.py
   python tone_mapping.py
   python path_tracer.py --spp 64

ファイル一覧
------------

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - ファイル
     - 内容
     - 関連する章
   * - :download:`path_tracer.py <../examples/path_tracer.py>`
     - NumPy によるミニパストレーサー
     - 「:doc:`path_tracing`」
   * - :download:`fresnel_plot.py <../examples/fresnel_plot.py>`
     - フレネル反射率と Schlick 近似の比較
     - 「:doc:`light_matter`」
   * - :download:`brdf_plot.py <../examples/brdf_plot.py>`
     - BRDF の形、GGX 分布、ラフネスを変えた球の描画
     - 「:doc:`brdf`」「:doc:`microfacet`」
   * - :download:`monte_carlo.py <../examples/monte_carlo.py>`
     - モンテカルロ積分と重点サンプリングの実験
     - 「:doc:`monte_carlo`」
   * - :download:`tone_mapping.py <../examples/tone_mapping.py>`
     - sRGB の符号化とトーンマッピングの比較
     - 「:doc:`light_and_color`」「:doc:`practical_pbr`」
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定ファイル
     - －
   * - :download:`requirements.txt <../examples/requirements.txt>`
     - 必要なライブラリの一覧
     - －

コードの検査
------------

サンプルコードは、flake8（1 行 120 文字まで許容）と mypy（strict モード）による検査で違反がないことを確認している。設定は ``setup.cfg`` にまとめてあり、``examples`` フォルダで次のように実行できる。

.. code-block:: console
   :linenos:

   python -m flake8 .
   python -m mypy .

ソースコード
------------

path_tracer.py
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/path_tracer.py
   :language: python
   :linenos:

fresnel_plot.py
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/fresnel_plot.py
   :language: python
   :linenos:

brdf_plot.py
^^^^^^^^^^^^

.. literalinclude:: ../examples/brdf_plot.py
   :language: python
   :linenos:

monte_carlo.py
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/monte_carlo.py
   :language: python
   :linenos:

tone_mapping.py
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/tone_mapping.py
   :language: python
   :linenos:

setup.cfg
^^^^^^^^^

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
