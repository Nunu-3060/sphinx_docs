付録 C　サンプルコード
======================

本書のサンプルコードの全体を掲載する。サンプルコードと素材は、次のリンクから zip ファイルでまとめてダウンロードできる。

* `examples.zip <downloads/examples.zip>`__

リソースファイルと、ブラウザ版の完成版ゲームは次のリンクからダウンロードできる。

* :download:`cosmo_rush.pyxres <../examples/assets/cosmo_rush.pyxres>`\ （素材のリソースファイル）
* `cosmo_rush.pyxapp <downloads/cosmo_rush.pyxapp>`__\ （完成版の Pyxel アプリケーションファイル。``pyxel play cosmo_rush.pyxapp`` で実行する）
* `cosmo_rush.html <play/cosmo_rush.html>`__\ （完成版のブラウザ版）

ファイルの一覧
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ファイル
     - 内容
   * - :ref:`setup.cfg <sample-setup-cfg>`
     - flake8、mypy、pytest の設定
   * - :ref:`ch01_hello/main.py <sample-ch01-hello-main-py>`
     - 第 1 章：最小構成のプログラム
   * - :ref:`ch03_basics/draw_demo.py <sample-ch03-basics-draw-demo-py>`
     - 第 3 章：図形と文字の描画
   * - :ref:`ch03_basics/input_demo.py <sample-ch03-basics-input-demo-py>`
     - 第 3 章：キー入力の取得
   * - :ref:`ch03_basics/motion_demo.py <sample-ch03-basics-motion-demo-py>`
     - 第 3 章：速度と加速度による動き
   * - :ref:`ch03_basics/collision_demo.py <sample-ch03-basics-collision-demo-py>`
     - 第 3 章：当たり判定
   * - :ref:`ch03_basics/random_demo.py <sample-ch03-basics-random-demo-py>`
     - 第 3 章：乱数とタイマー
   * - :ref:`assets/make_assets.py <sample-assets-make-assets-py>`
     - 第 4 章、第 5 章：素材を生成するスクリプト
   * - :ref:`ch06_step1/main.py <sample-ch06-step1-main-py>`
     - 第 6 章のステップ 1：自機を表示して動かす
   * - :ref:`ch06_step2/main.py <sample-ch06-step2-main-py>`
     - 第 6 章のステップ 2：弾を撃つ
   * - :ref:`ch06_step3/main.py <sample-ch06-step3-main-py>`
     - 第 6 章のステップ 3：敵と当たり判定
   * - :ref:`ch06_step4/main.py <sample-ch06-step4-main-py>`
     - 第 6 章のステップ 4：スコア、残機、ゲームオーバー
   * - :ref:`ch07_step5/main.py <sample-ch07-step5-main-py>`
     - 第 7 章のステップ 5：シーンの切り替え
   * - :ref:`ch07_step6/main.py <sample-ch07-step6-main-py>`
     - 第 7 章のステップ 6：スプライトで描く
   * - :ref:`ch07_step7/main.py <sample-ch07-step7-main-py>`
     - 第 7 章のステップ 7：背景のスクロール
   * - :ref:`ch07_step8/main.py <sample-ch07-step8-main-py>`
     - 第 7 章のステップ 8：効果音と BGM
   * - :ref:`ch07_step9/main.py <sample-ch07-step9-main-py>`
     - 第 7 章のステップ 9：演出
   * - :ref:`cosmo_rush/main.py <sample-cosmo-rush-main-py>`
     - 第 7 章：完成版
   * - :ref:`tests/test_cosmo_rush.py <sample-tests-test-cosmo-rush-py>`
     - 第 8 章：単体テスト

.. _sample-setup-cfg:

setup.cfg
---------

flake8、mypy、pytest の設定。:download:`setup.cfg をダウンロード <../examples/setup.cfg>`

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
   :caption: setup.cfg

.. _sample-ch01-hello-main-py:

ch01_hello/main.py
------------------

第 1 章：最小構成のプログラム。:download:`main.py をダウンロード <../examples/ch01_hello/main.py>`

.. literalinclude:: ../examples/ch01_hello/main.py
   :language: python
   :linenos:
   :caption: ch01_hello/main.py

.. _sample-ch03-basics-draw-demo-py:

ch03_basics/draw_demo.py
------------------------

第 3 章：図形と文字の描画。:download:`draw_demo.py をダウンロード <../examples/ch03_basics/draw_demo.py>`

.. literalinclude:: ../examples/ch03_basics/draw_demo.py
   :language: python
   :linenos:
   :caption: ch03_basics/draw_demo.py

.. _sample-ch03-basics-input-demo-py:

ch03_basics/input_demo.py
-------------------------

第 3 章：キー入力の取得。:download:`input_demo.py をダウンロード <../examples/ch03_basics/input_demo.py>`

.. literalinclude:: ../examples/ch03_basics/input_demo.py
   :language: python
   :linenos:
   :caption: ch03_basics/input_demo.py

.. _sample-ch03-basics-motion-demo-py:

ch03_basics/motion_demo.py
--------------------------

第 3 章：速度と加速度による動き。:download:`motion_demo.py をダウンロード <../examples/ch03_basics/motion_demo.py>`

.. literalinclude:: ../examples/ch03_basics/motion_demo.py
   :language: python
   :linenos:
   :caption: ch03_basics/motion_demo.py

.. _sample-ch03-basics-collision-demo-py:

ch03_basics/collision_demo.py
-----------------------------

第 3 章：当たり判定。:download:`collision_demo.py をダウンロード <../examples/ch03_basics/collision_demo.py>`

.. literalinclude:: ../examples/ch03_basics/collision_demo.py
   :language: python
   :linenos:
   :caption: ch03_basics/collision_demo.py

.. _sample-ch03-basics-random-demo-py:

ch03_basics/random_demo.py
--------------------------

第 3 章：乱数とタイマー。:download:`random_demo.py をダウンロード <../examples/ch03_basics/random_demo.py>`

.. literalinclude:: ../examples/ch03_basics/random_demo.py
   :language: python
   :linenos:
   :caption: ch03_basics/random_demo.py

.. _sample-assets-make-assets-py:

assets/make_assets.py
---------------------

第 4 章、第 5 章：素材を生成するスクリプト。:download:`make_assets.py をダウンロード <../examples/assets/make_assets.py>`

.. literalinclude:: ../examples/assets/make_assets.py
   :language: python
   :linenos:
   :caption: assets/make_assets.py

.. _sample-ch06-step1-main-py:

ch06_step1/main.py
------------------

第 6 章のステップ 1：自機を表示して動かす。:download:`main.py をダウンロード <../examples/ch06_step1/main.py>`

.. literalinclude:: ../examples/ch06_step1/main.py
   :language: python
   :linenos:
   :caption: ch06_step1/main.py

.. _sample-ch06-step2-main-py:

ch06_step2/main.py
------------------

第 6 章のステップ 2：弾を撃つ。:download:`main.py をダウンロード <../examples/ch06_step2/main.py>`

.. literalinclude:: ../examples/ch06_step2/main.py
   :language: python
   :linenos:
   :caption: ch06_step2/main.py

.. _sample-ch06-step3-main-py:

ch06_step3/main.py
------------------

第 6 章のステップ 3：敵と当たり判定。:download:`main.py をダウンロード <../examples/ch06_step3/main.py>`

.. literalinclude:: ../examples/ch06_step3/main.py
   :language: python
   :linenos:
   :caption: ch06_step3/main.py

.. _sample-ch06-step4-main-py:

ch06_step4/main.py
------------------

第 6 章のステップ 4：スコア、残機、ゲームオーバー。:download:`main.py をダウンロード <../examples/ch06_step4/main.py>`

.. literalinclude:: ../examples/ch06_step4/main.py
   :language: python
   :linenos:
   :caption: ch06_step4/main.py

.. _sample-ch07-step5-main-py:

ch07_step5/main.py
------------------

第 7 章のステップ 5：シーンの切り替え。:download:`main.py をダウンロード <../examples/ch07_step5/main.py>`

.. literalinclude:: ../examples/ch07_step5/main.py
   :language: python
   :linenos:
   :caption: ch07_step5/main.py

.. _sample-ch07-step6-main-py:

ch07_step6/main.py
------------------

第 7 章のステップ 6：スプライトで描く。:download:`main.py をダウンロード <../examples/ch07_step6/main.py>`

.. literalinclude:: ../examples/ch07_step6/main.py
   :language: python
   :linenos:
   :caption: ch07_step6/main.py

.. _sample-ch07-step7-main-py:

ch07_step7/main.py
------------------

第 7 章のステップ 7：背景のスクロール。:download:`main.py をダウンロード <../examples/ch07_step7/main.py>`

.. literalinclude:: ../examples/ch07_step7/main.py
   :language: python
   :linenos:
   :caption: ch07_step7/main.py

.. _sample-ch07-step8-main-py:

ch07_step8/main.py
------------------

第 7 章のステップ 8：効果音と BGM。:download:`main.py をダウンロード <../examples/ch07_step8/main.py>`

.. literalinclude:: ../examples/ch07_step8/main.py
   :language: python
   :linenos:
   :caption: ch07_step8/main.py

.. _sample-ch07-step9-main-py:

ch07_step9/main.py
------------------

第 7 章のステップ 9：演出。:download:`main.py をダウンロード <../examples/ch07_step9/main.py>`

.. literalinclude:: ../examples/ch07_step9/main.py
   :language: python
   :linenos:
   :caption: ch07_step9/main.py

.. _sample-cosmo-rush-main-py:

cosmo_rush/main.py
------------------

第 7 章：完成版。:download:`main.py をダウンロード <../examples/cosmo_rush/main.py>`

.. literalinclude:: ../examples/cosmo_rush/main.py
   :language: python
   :linenos:
   :caption: cosmo_rush/main.py

.. _sample-tests-test-cosmo-rush-py:

tests/test_cosmo_rush.py
------------------------

第 8 章：単体テスト。:download:`test_cosmo_rush.py をダウンロード <../examples/tests/test_cosmo_rush.py>`

.. literalinclude:: ../examples/tests/test_cosmo_rush.py
   :language: python
   :linenos:
   :caption: tests/test_cosmo_rush.py

