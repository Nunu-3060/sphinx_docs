付録 D サンプルコード一覧
=========================

本書のサンプルコードは、次のリンクからダウンロードできる。ファイル名のリンクを開くとダウンロードでき、「全文」のリンクを開くとこのページの下の方でコード全体を読める。すべてのファイルを同じフォルダーに置いて使う。

ダウンロード
------------

.. list-table:: デモとモジュール
   :header-rows: 1
   :widths: 30 10 50 10

   * - ファイル
     - 章
     - 内容
     - 全文
   * - :download:`float_precision.py <../examples/float_precision.py>`
     - 2
     - 座標の変換と浮動小数点数の誤差（コンソールに表示）
     - :ref:`表示 <src-float_precision>`
   * - :download:`game_loop.py <../examples/game_loop.py>`
     - 3
     - フレーム数を基準にした移動と、デルタタイムを基準にした移動の比較
     - :ref:`表示 <src-game_loop>`
   * - :download:`fixed_timestep.py <../examples/fixed_timestep.py>`
     - 3
     - 固定タイムステップと描画の補間
     - :ref:`表示 <src-fixed_timestep>`
   * - :download:`vec2.py <../examples/vec2.py>`
     - 4
     - 自作の 2 次元ベクトルのクラス
     - :ref:`表示 <src-vec2>`
   * - :download:`vectors_demo.py <../examples/vectors_demo.py>`
     - 4
     - 正規化・内積・外積を使った移動と視界の判定
     - :ref:`表示 <src-vectors_demo>`
   * - :download:`reflect_demo.py <../examples/reflect_demo.py>`
     - 4
     - 反射ベクトル
     - :ref:`表示 <src-reflect_demo>`
   * - :download:`turret.py <../examples/turret.py>`
     - 5
     - atan2 でマウスの方向を向く砲台と、円運動
     - :ref:`表示 <src-turret>`
   * - :download:`homing.py <../examples/homing.py>`
     - 5
     - 旋回速度に上限があるホーミング弾
     - :ref:`表示 <src-homing>`
   * - :download:`transform2d.py <../examples/transform2d.py>`
     - 6
     - 2D のアフィン変換の行列のクラス（arm_demo.py、camera_demo.py が使う）
     - :ref:`表示 <src-transform2d>`
   * - :download:`arm_demo.py <../examples/arm_demo.py>`
     - 6
     - 親子関係のある変換で動かすロボットアーム
     - :ref:`表示 <src-arm_demo>`
   * - :download:`camera_demo.py <../examples/camera_demo.py>`
     - 6
     - 2D カメラとクリック位置の逆変換
     - :ref:`表示 <src-camera_demo>`
   * - :download:`quaternion.py <../examples/quaternion.py>`
     - 7
     - 自作のクォータニオンのクラスと球面線形補間（cube_demo.py が使う）
     - :ref:`表示 <src-quaternion>`
   * - :download:`cube_demo.py <../examples/cube_demo.py>`
     - 7
     - クォータニオンで回して透視投影で描く立方体
     - :ref:`表示 <src-cube_demo>`
   * - :download:`easing.py <../examples/easing.py>`
     - 8
     - 線形補間、イージング関数、damp
     - :ref:`表示 <src-easing>`
   * - :download:`curves.py <../examples/curves.py>`
     - 8
     - ベジェ曲線、Catmull-Rom スプライン、弧長による等速移動
     - :ref:`表示 <src-curves>`
   * - :download:`random_tools.py <../examples/random_tools.py>`
     - 9
     - 重み付き抽選、袋方式、円内の点、確率の計算（コンソールに表示）
     - :ref:`表示 <src-random_tools>`
   * - :download:`noise.py <../examples/noise.py>`
     - 9
     - バリューノイズ、パーリンノイズ、フラクタルノイズ、ノイズによる揺れ
     - :ref:`表示 <src-noise>`
   * - :download:`integrators.py <../examples/integrators.py>`
     - 10
     - 数値積分の方法の比較（コンソールに表示）
     - :ref:`表示 <src-integrators>`
   * - :download:`jump.py <../examples/jump.py>`
     - 10
     - ジャンプの設計と、ゲームらしい調整
     - :ref:`表示 <src-jump>`
   * - :download:`collision.py <../examples/collision.py>`
     - 11
     - 衝突判定の関数集（collision_demo.py、response.py、platformer.py が使う）
     - :ref:`表示 <src-collision>`
   * - :download:`collision_demo.py <../examples/collision_demo.py>`
     - 11
     - 衝突判定を目で確かめるデモ
     - :ref:`表示 <src-collision_demo>`
   * - :download:`spatial_grid.py <../examples/spatial_grid.py>`
     - 11
     - 一様グリッドによるブロードフェーズ（コンソールに表示）
     - :ref:`表示 <src-spatial_grid>`
   * - :download:`response.py <../examples/response.py>`
     - 12
     - 力積による衝突応答
     - :ref:`表示 <src-response>`
   * - :download:`spring.py <../examples/spring.py>`
     - 13
     - ばねとダンパー
     - :ref:`表示 <src-spring>`
   * - :download:`rope.py <../examples/rope.py>`
     - 13
     - ベルレ法と距離拘束によるロープと布
     - :ref:`表示 <src-rope>`
   * - :download:`particles.py <../examples/particles.py>`
     - 13
     - パーティクル
     - :ref:`表示 <src-particles>`
   * - :download:`pymunk_demo.py <../examples/pymunk_demo.py>`
     - 14
     - 物理エンジン pymunk の基本
     - :ref:`表示 <src-pymunk_demo>`
   * - :download:`platformer.py <../examples/platformer.py>`
     - 15
     - 総合演習の 2D プラットフォーマー
     - :ref:`表示 <src-platformer>`

.. list-table:: テストと設定ファイル
   :header-rows: 1
   :widths: 30 60 10

   * - ファイル
     - 内容
     - 全文
   * - :download:`test_vec2.py <../examples/test_vec2.py>`
     - vec2.py の単体テスト
     - :ref:`表示 <src-test_vec2>`
   * - :download:`test_math_tools.py <../examples/test_math_tools.py>`
     - 第 2 章・第 5 章～第 9 章のサンプルコードの単体テスト
     - :ref:`表示 <src-test_math_tools>`
   * - :download:`test_physics.py <../examples/test_physics.py>`
     - 第 3 章・第 4 章・第 10 章～第 13 章のサンプルコードの単体テスト
     - :ref:`表示 <src-test_physics>`
   * - :download:`test_platformer.py <../examples/test_platformer.py>`
     - platformer.py の単体テスト
     - :ref:`表示 <src-test_platformer>`
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定ファイル
     - :ref:`表示 <src-setup_cfg>`

実行に必要なライブラリー
------------------------

pygame-ce と pymunk が必要である。pymunk を使うのは ``pymunk_demo.py`` だけである。

.. code-block:: powershell
   :linenos:
   :caption: ライブラリーのインストール

   py -m pip install pygame-ce pymunk

テストとコードの検査
--------------------

テストは、ダウンロードしたフォルダーで次のコマンドを実行する。画面は開かない。

.. code-block:: powershell
   :linenos:
   :caption: すべてのテストの実行

   py -m unittest

サンプルコードは、PEP 8 に沿って書き、すべての関数に型ヒントを付けている。flake8（1 行 120 文字まで許容）と mypy（strict モード）で検査できる。どちらも設定は ``setup.cfg`` に書いてある。

.. code-block:: powershell
   :linenos:
   :caption: サンプルコードの検査

   py -m pip install flake8 mypy
   py -m flake8
   py -m mypy .

全文
----

.. _src-float_precision:

float_precision.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/float_precision.py
   :language: python
   :linenos:

.. _src-game_loop:

game_loop.py
~~~~~~~~~~~~

.. literalinclude:: ../examples/game_loop.py
   :language: python
   :linenos:

.. _src-fixed_timestep:

fixed_timestep.py
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/fixed_timestep.py
   :language: python
   :linenos:

.. _src-vec2:

vec2.py
~~~~~~~

.. literalinclude:: ../examples/vec2.py
   :language: python
   :linenos:

.. _src-vectors_demo:

vectors_demo.py
~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/vectors_demo.py
   :language: python
   :linenos:

.. _src-reflect_demo:

reflect_demo.py
~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/reflect_demo.py
   :language: python
   :linenos:

.. _src-turret:

turret.py
~~~~~~~~~

.. literalinclude:: ../examples/turret.py
   :language: python
   :linenos:

.. _src-homing:

homing.py
~~~~~~~~~

.. literalinclude:: ../examples/homing.py
   :language: python
   :linenos:

.. _src-transform2d:

transform2d.py
~~~~~~~~~~~~~~

.. literalinclude:: ../examples/transform2d.py
   :language: python
   :linenos:

.. _src-arm_demo:

arm_demo.py
~~~~~~~~~~~

.. literalinclude:: ../examples/arm_demo.py
   :language: python
   :linenos:

.. _src-camera_demo:

camera_demo.py
~~~~~~~~~~~~~~

.. literalinclude:: ../examples/camera_demo.py
   :language: python
   :linenos:

.. _src-quaternion:

quaternion.py
~~~~~~~~~~~~~

.. literalinclude:: ../examples/quaternion.py
   :language: python
   :linenos:

.. _src-cube_demo:

cube_demo.py
~~~~~~~~~~~~

.. literalinclude:: ../examples/cube_demo.py
   :language: python
   :linenos:

.. _src-easing:

easing.py
~~~~~~~~~

.. literalinclude:: ../examples/easing.py
   :language: python
   :linenos:

.. _src-curves:

curves.py
~~~~~~~~~

.. literalinclude:: ../examples/curves.py
   :language: python
   :linenos:

.. _src-random_tools:

random_tools.py
~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/random_tools.py
   :language: python
   :linenos:

.. _src-noise:

noise.py
~~~~~~~~

.. literalinclude:: ../examples/noise.py
   :language: python
   :linenos:

.. _src-integrators:

integrators.py
~~~~~~~~~~~~~~

.. literalinclude:: ../examples/integrators.py
   :language: python
   :linenos:

.. _src-jump:

jump.py
~~~~~~~

.. literalinclude:: ../examples/jump.py
   :language: python
   :linenos:

.. _src-collision:

collision.py
~~~~~~~~~~~~

.. literalinclude:: ../examples/collision.py
   :language: python
   :linenos:

.. _src-collision_demo:

collision_demo.py
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/collision_demo.py
   :language: python
   :linenos:

.. _src-spatial_grid:

spatial_grid.py
~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/spatial_grid.py
   :language: python
   :linenos:

.. _src-response:

response.py
~~~~~~~~~~~

.. literalinclude:: ../examples/response.py
   :language: python
   :linenos:

.. _src-spring:

spring.py
~~~~~~~~~

.. literalinclude:: ../examples/spring.py
   :language: python
   :linenos:

.. _src-rope:

rope.py
~~~~~~~

.. literalinclude:: ../examples/rope.py
   :language: python
   :linenos:

.. _src-particles:

particles.py
~~~~~~~~~~~~

.. literalinclude:: ../examples/particles.py
   :language: python
   :linenos:

.. _src-pymunk_demo:

pymunk_demo.py
~~~~~~~~~~~~~~

.. literalinclude:: ../examples/pymunk_demo.py
   :language: python
   :linenos:

.. _src-platformer:

platformer.py
~~~~~~~~~~~~~

.. literalinclude:: ../examples/platformer.py
   :language: python
   :linenos:

.. _src-test_vec2:

test_vec2.py
~~~~~~~~~~~~

.. literalinclude:: ../examples/test_vec2.py
   :language: python
   :linenos:

.. _src-test_math_tools:

test_math_tools.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/test_math_tools.py
   :language: python
   :linenos:

.. _src-test_physics:

test_physics.py
~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/test_physics.py
   :language: python
   :linenos:

.. _src-test_platformer:

test_platformer.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/test_platformer.py
   :language: python
   :linenos:

.. _src-setup_cfg:

setup.cfg
~~~~~~~~~

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
