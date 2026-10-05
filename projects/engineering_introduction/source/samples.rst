サンプルコード
==============

本書で使用したサンプルコードの一覧です。ファイル名のリンクからダウンロードできます。実行環境と実行方法は\ :doc:`introduction`\ を参照してください。

一覧
----

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - ファイル
     - 章
     - 内容
   * - :download:`ch02_dimension.py <../examples/ch02_dimension.py>`
     - :doc:`units`
     - 次元を持つ量を計算し、次元の不一致を検出する
   * - :download:`ch03_pendulum.py <../examples/ch03_pendulum.py>`
     - :doc:`modeling`
     - 振り子の非線形モデルと線形モデルを比較する
   * - :download:`ch03_state_machine.py <../examples/ch03_state_machine.py>`
     - :doc:`modeling`
     - 状態機械で電気ポットの制御をモデル化する
   * - :download:`ch03_overfitting.py <../examples/ch03_overfitting.py>`
     - :doc:`modeling`
     - 過学習を確かめ、交差検証でモデルの複雑さを選ぶ
   * - :download:`ch04_least_squares.py <../examples/ch04_least_squares.py>`
     - :doc:`measurement`
     - 最小二乗法で直線を当てはめ、係数の不確かさを求める
   * - :download:`ch04_benchmark.py <../examples/ch04_benchmark.py>`
     - :doc:`measurement`
     - 処理時間を繰り返し測定し、ばらつきを要約する
   * - :download:`ch05_float.py <../examples/ch05_float.py>`
     - :doc:`numerical`
     - 浮動小数点数と固定幅の整数の落とし穴を確かめる
   * - :download:`ch05_derivative.py <../examples/ch05_derivative.py>`
     - :doc:`numerical`
     - 数値微分と数値積分の誤差を確かめる
   * - :download:`ch05_ode.py <../examples/ch05_ode.py>`
     - :doc:`numerical`
     - 常微分方程式の数値解法（オイラー法、ホイン法、RK4）を比較する
   * - :download:`ch05_complexity.py <../examples/ch05_complexity.py>`
     - :doc:`numerical`
     - 計算量の違いが処理時間に与える影響を確かめる
   * - :download:`ch06_step_response.py <../examples/ch06_step_response.py>`
     - :doc:`dynamics_control`
     - 1 次遅れ系と 2 次系のステップ応答を描く
   * - :download:`ch06_frequency_response.py <../examples/ch06_frequency_response.py>`
     - :doc:`dynamics_control`
     - 2 次系のボード線図を描き、共振を確かめる
   * - :download:`ch06_pid.py <../examples/ch06_pid.py>`
     - :doc:`dynamics_control`
     - PID 制御のシミュレーションを行う
   * - :download:`ch06_jitter.py <../examples/ch06_jitter.py>`
     - :doc:`dynamics_control`
     - 周期処理のジッターとドリフトを測定する
   * - :download:`ch07_aliasing.py <../examples/ch07_aliasing.py>`
     - :doc:`signals`
     - エイリアシングを確かめる
   * - :download:`ch07_quantization.py <../examples/ch07_quantization.py>`
     - :doc:`signals`
     - A/D 変換の量子化雑音を確かめる
   * - :download:`ch07_fft_filter.py <../examples/ch07_fft_filter.py>`
     - :doc:`signals`
     - 振幅スペクトルを求め、移動平均フィルターの効果を確かめる
   * - :download:`ch08_thermal.py <../examples/ch08_thermal.py>`
     - :doc:`energy_heat`
     - 熱抵抗を使って半導体の温度を見積もり、放熱器を選ぶ
   * - :download:`ch09_decision_matrix.py <../examples/ch09_decision_matrix.py>`
     - :doc:`design_process`
     - 重み付き評価マトリクスで設計案を比較し、感度分析を行う
   * - :download:`ch09_schedule.py <../examples/ch09_schedule.py>`
     - :doc:`design_process`
     - 3 点見積もりとモンテカルロ法で開発期間の分布を求める
   * - :download:`ch10_gradient_descent.py <../examples/ch10_gradient_descent.py>`
     - :doc:`optimization`
     - 最急降下法で最小値を探し、学習率の影響を確かめる
   * - :download:`ch10_pareto.py <../examples/ch10_pareto.py>`
     - :doc:`optimization`
     - 片持ち梁の設計でパレート最適解を求める
   * - :download:`ch11_statistics.py <../examples/ch11_statistics.py>`
     - :doc:`statistics`
     - 信頼区間と並べ替え検定を計算する
   * - :download:`ch11_doe.py <../examples/ch11_doe.py>`
     - :doc:`statistics`
     - 要因実験の主効果と交互作用を求める
   * - :download:`ch11_tolerance.py <../examples/ch11_tolerance.py>`
     - :doc:`statistics`
     - 寸法公差の積み上げを 3 つの方法で見積もる
   * - :download:`ch11_control_chart.py <../examples/ch11_control_chart.py>`
     - :doc:`statistics`
     - 管理図で工程の変化を検出する
   * - :download:`ch12_boundary_test.py <../examples/ch12_boundary_test.py>`
     - :doc:`verification`
     - 同値分割と境界値分析に基づいて単体試験を書く
   * - :download:`ch13_reliability.py <../examples/ch13_reliability.py>`
     - :doc:`reliability`
     - システムの信頼度とアベイラビリティを計算し、バスタブ曲線を描く
   * - :download:`ch13_fatigue.py <../examples/ch13_fatigue.py>`
     - :doc:`reliability`
     - S-N 曲線とマイナー則で疲労寿命を見積もる
   * - :download:`ch14_fault_tree.py <../examples/ch14_fault_tree.py>`
     - :doc:`safety`
     - フォールトツリーから頂上事象の発生確率を計算する
   * - :download:`ch15_chart_makeover.py <../examples/ch15_chart_makeover.py>`
     - :doc:`communication`
     - 同じデータの悪い示し方と良い示し方を比べる

コードの確認に使った設定ファイルは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - ファイル
     - 内容
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 の設定（1 行の最大文字数 79）
   * - :download:`mypy.ini <../examples/mypy.ini>`
     - mypy の設定（strict モード）

サンプルコードを置いたフォルダーで次のコマンドを実行すると、規約違反と型の誤りがないことを確かめられます。

.. code-block:: console
   :linenos:

   python -m pip install flake8 mypy
   python -m flake8 .
   python -m mypy .

ソースコード
------------

各サンプルコードの全文を示します。

ch02_dimension.py
^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch02_dimension.py
   :language: python
   :linenos:

ch03_pendulum.py
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch03_pendulum.py
   :language: python
   :linenos:

ch03_state_machine.py
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch03_state_machine.py
   :language: python
   :linenos:

ch03_overfitting.py
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch03_overfitting.py
   :language: python
   :linenos:

ch04_least_squares.py
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch04_least_squares.py
   :language: python
   :linenos:

ch04_benchmark.py
^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch04_benchmark.py
   :language: python
   :linenos:

ch05_float.py
^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch05_float.py
   :language: python
   :linenos:

ch05_derivative.py
^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch05_derivative.py
   :language: python
   :linenos:

ch05_ode.py
^^^^^^^^^^^

.. literalinclude:: ../examples/ch05_ode.py
   :language: python
   :linenos:

ch05_complexity.py
^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch05_complexity.py
   :language: python
   :linenos:

ch06_step_response.py
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch06_step_response.py
   :language: python
   :linenos:

ch06_frequency_response.py
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch06_frequency_response.py
   :language: python
   :linenos:

ch06_pid.py
^^^^^^^^^^^

.. literalinclude:: ../examples/ch06_pid.py
   :language: python
   :linenos:

ch06_jitter.py
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch06_jitter.py
   :language: python
   :linenos:

ch07_aliasing.py
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch07_aliasing.py
   :language: python
   :linenos:

ch07_quantization.py
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch07_quantization.py
   :language: python
   :linenos:

ch07_fft_filter.py
^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch07_fft_filter.py
   :language: python
   :linenos:

ch08_thermal.py
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch08_thermal.py
   :language: python
   :linenos:

ch09_decision_matrix.py
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch09_decision_matrix.py
   :language: python
   :linenos:

ch09_schedule.py
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch09_schedule.py
   :language: python
   :linenos:

ch10_gradient_descent.py
^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch10_gradient_descent.py
   :language: python
   :linenos:

ch10_pareto.py
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch10_pareto.py
   :language: python
   :linenos:

ch11_statistics.py
^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch11_statistics.py
   :language: python
   :linenos:

ch11_doe.py
^^^^^^^^^^^

.. literalinclude:: ../examples/ch11_doe.py
   :language: python
   :linenos:

ch11_tolerance.py
^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch11_tolerance.py
   :language: python
   :linenos:

ch11_control_chart.py
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch11_control_chart.py
   :language: python
   :linenos:

ch12_boundary_test.py
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch12_boundary_test.py
   :language: python
   :linenos:

ch13_reliability.py
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch13_reliability.py
   :language: python
   :linenos:

ch13_fatigue.py
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch13_fatigue.py
   :language: python
   :linenos:

ch14_fault_tree.py
^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch14_fault_tree.py
   :language: python
   :linenos:

ch15_chart_makeover.py
^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch15_chart_makeover.py
   :language: python
   :linenos:
