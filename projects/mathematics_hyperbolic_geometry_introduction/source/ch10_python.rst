.. _ch10:

第 10 章 Python による計算と描画
================================

本書の図と計算結果は、すべて Python のサンプルで作成している。この章では、サンプルの共通モジュール ``hg.py`` の設計を説明し、双曲平面を数値計算するときの注意点を述べる。自分で双曲幾何学の計算や作図を行うときの出発点として使ってほしい。

サンプルの構成
--------------

サンプルは ``examples`` フォルダーにあり、次の 3 種類のファイルからなる。一覧は\ :ref:`付録 E <appendix-e>`\ にある。

.. list-table:: サンプルのファイルの種類
   :header-rows: 1
   :widths: 30 70

   * - ファイル
     - 内容
   * - ``hg.py``
     - 双曲平面の計算（距離、モデル間の変換、測地線、鏡映、角度）。NumPy だけを使う。
   * - ``hg_plot.py``
     - 図の描画の補助（日本語フォントの設定、円板や上半平面の座標軸、測地線の描画）。matplotlib を使う。
   * - ``chNN_*.py``
     - 各章のサンプル。``NN`` は章の番号である。

各章のサンプルは、図を描くものは ``create_figure()`` 関数（matplotlib の ``Figure`` を返す）を、計算結果を表示するものは ``report()`` 関数を持つ。文書のビルド時には、これらの関数が呼ばれて図と実行結果が作られる。単独で実行すると、図を画面に表示するか、結果を表示する。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python ch08_tiling.py

点の表し方
----------

``hg.py`` では、上半平面モデル、円板モデル、クラインモデルの点を Python の複素数（``complex``）で表す。複素数で表すと、メビウス変換などの式を、数式とほぼ同じ形でコードに書ける。たとえば円板モデルの距離の公式 :math:`d = 2 \artanh |(z - w) / (1 - \bar{w} z)|` は、次のようになる。

.. literalinclude:: ../examples/hg.py
   :pyobject: disk_distance
   :lineno-match:
   :caption: hg.py の disk_distance()

双曲面モデルの点は、成分 :math:`(x_0, x_1, x_2)` を持つ NumPy の配列で表す。距離はミンコフスキーの双線形形式 :math:`B` から求める。

.. literalinclude:: ../examples/hg.py
   :pyobject: hyperboloid_distance
   :lineno-match:
   :caption: hg.py の hyperboloid_distance()

:math:`B(x, y)` は理論上 1 以上だが、丸め誤差でわずかに 1 を下回ると :math:`\arcosh` が計算できない（``ValueError`` になる）。そのため、``max()`` で 1 以上に切り上げている。数値計算では、このような小さな防御が欠かせない。

中心に移して考える
------------------

円板モデルでは、任意の点を中心に移す等長変換がある（\ :ref:`第 5 章 <ch05>`\ ）。``hg.py`` の作図の関数は、すべて「中心に移して簡単な計算をし、元に戻す」という同じ考え方で書かれている。中心 :math:`0` を点 :math:`a` に移す変換 :math:`z \mapsto (z + a) / (1 + \bar{a} z)` を ``disk_translate()`` とし、:math:`a` を中心に移すときは ``disk_translate(-a, z)`` を使う。

.. literalinclude:: ../examples/hg.py
   :pyobject: disk_translate
   :lineno-match:
   :caption: hg.py の disk_translate()

2 点 :math:`a`、:math:`b` を結ぶ測地線分を描くには、:math:`a` を中心に移す。すると測地線分は中心から出る線分になり、その上に点を並べるのは簡単である。最後に、並べた点を元の位置に戻す。

.. literalinclude:: ../examples/hg.py
   :pyobject: disk_geodesic
   :lineno-match:
   :caption: hg.py の disk_geodesic()

中心から距離 :math:`t` の点は、ユークリッドの半径 :math:`\tanh(t/2)` の位置にある（\ :ref:`第 4 章 <ch04>`\ ）。``np.linspace(0.0, length, n)`` で双曲的な長さを等分してから :math:`\tanh(t/2)` に変換しているので、点は双曲的に等間隔に並ぶ。境界に近い部分でも点が粗くならず、きれいな曲線が描ける。

測地線に関する鏡映（\ :ref:`第 8 章 <ch08>`\ のタイリングで使う）と、2 本の測地線のなす角（\ :ref:`第 6 章 <ch06>`\ の検証で使う）も同じ考え方で計算できる。測地線が直径になれば鏡映は直線に関する折り返しであり、交点が中心にあれば角度は 2 本の直線の角度である。

.. literalinclude:: ../examples/hg.py
   :pyobject: disk_reflect
   :lineno-match:
   :caption: hg.py の disk_reflect()

.. literalinclude:: ../examples/hg.py
   :pyobject: disk_angle
   :lineno-match:
   :caption: hg.py の disk_angle()

この方法の利点は、測地線の円弧の中心や半径を求める必要がないことである。円弧の中心と半径を直接求める方法では、測地線が直径に近いとき（円弧の半径が非常に大きいとき）に、直径との場合分けや桁落ちの処理が必要になる。中心に移す方法では、そのような場合分けがいらない。

.. _ch10-precision:

数値計算の注意点
----------------

双曲平面の数値計算では、浮動小数点数の丸め誤差に特有の問題がある。次の 2 つの例で確かめる。

.. literalinclude:: ../build/outputs/ch10_precision.txt
   :language: text
   :caption: ch10_precision.py の実行結果

サンプルの全体：:download:`ch10_precision.py <../examples/ch10_precision.py>`

1 つ目は、円板モデルで原点から遠い点を表す例である。原点から距離 :math:`d` の点は :math:`|z| = \tanh(d/2)` の位置にあり、:math:`1 - |z| \approx 2 e^{-d}` である。倍精度の浮動小数点数（有効数字およそ 16 桁）では、:math:`1 - |z|` が :math:`10^{-16}` 程度より小さくなると表せない。そのため :math:`d = 30` あたりから距離の精度が落ち始め、:math:`d \approx 37` を超えると :math:`|z| = 1` に丸められて、境界上の点（無限遠点）になってしまう。

2 つ目は、近い 2 点の距離を :math:`\arcosh` の公式で計算する例である。距離 :math:`h` が小さいとき :math:`\cosh h \approx 1 + h^2 / 2` なので、:math:`h = 10^{-8}` では :math:`h^2/2 = 5 \times 10^{-17}` が 1 に埋もれ、:math:`\cosh h` が 1 に丸められて距離が 0 になる。同じ距離を :math:`\artanh` の公式で計算すると、:math:`h = 10^{-10}` でも正確に求まる。

これらを踏まえた指針を挙げる。

* 近い点どうしの距離には、:math:`\arcosh(1 + \cdots)` の形を避け、:math:`\artanh` の公式（または :math:`\arsinh` の公式）を使う。``hg.py`` の ``disk_distance()`` は :math:`\artanh` の公式を使っている。
* 原点から遠い点（距離が 30 程度以上）を扱う場合は、円板モデルを避け、双曲面モデルや、原点からの距離と偏角による極座標（\ :ref:`第 9 章 <ch09>`\ のランダムグラフで使った表現）で表す。
* 双曲面モデルでは、座標が :math:`e^d` 程度まで大きくなり、計算を繰り返すと :math:`B(x, x) = 1` の条件が丸め誤差で崩れていく。ときどき :math:`x_0 = \sqrt{1 + x_1^2 + x_2^2}` で計算し直して、双曲面の上に戻すとよい。
* 機械学習の双曲埋め込みで、円板（球体）モデルの点を境界のすぐ内側に戻す射影（\ :ref:`第 9 章 <ch09>`\ ）を行うのも、同じ理由による。

コードの品質の検査
------------------

サンプルは PEP 8 に従って書き、すべての関数に型ヒントを付けている。``examples`` フォルダーの ``setup.cfg`` に flake8（コーディング規約の検査、行長は 120 文字まで）と mypy（型ヒントの検査、strict モード）の設定があり、次のコマンドで違反がないことを確認できる。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python -m flake8 .
   $ python -m mypy .

この章のまとめ
--------------

* 2 次元のモデルの点は複素数で表すと、数式をそのままコードに書ける。
* 円板モデルでは、点を中心に移してから計算し、元に戻すと、作図と角度の計算が簡単になる。
* 円板モデルは原点から遠い点（距離が 30 程度以上）を正確に表せない。近い点の距離は :math:`\arcosh` の公式で桁落ちする。用途に応じて、モデルと公式を選ぶ。
