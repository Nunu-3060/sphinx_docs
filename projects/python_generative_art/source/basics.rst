基礎編：ジェネラティブアート特有の設計方針
============================================

Python・NumPy・Pillow・matplotlib 自体の使い方には立ち入らず、ジェネラティブアート作品を作る上で共通して必要になる設計上の考え方をまとめる。

座標系の正規化
--------------

作品のロジックを ``800 x 800`` のような特定の解像度に結びつけて書くと、後から出力サイズを変えたくなったときに、拡大縮小や余白の計算をあちこちに書き足す羽目になる。座標を最初から ``[0, 1]`` あるいは ``[-1, 1]`` のような正規化された範囲で組み立て、実際にピクセル配列や画像へ書き出す最後の段階だけでピクセル座標に変換すると、解像度の変更が「最後の変換関数に渡す ``width`` / ``height`` を変えるだけ」で済むようになる。

本資料のサンプルコードでは、簡潔さを優先してピクセル座標を直接扱っている箇所も多いが（:doc:`noise`\ のノイズ画像など）、複数の解像度で書き出したい作品や、印刷用に大きな解像度が必要になる作品では、正規化座標を採用する価値がある。

.. code-block:: python
   :linenos:

   def to_pixel(u: float, v: float, width: int, height: int) -> tuple[int, int]:
       """正規化座標 (u, v) （それぞれ0〜1）をピクセル座標に変換する。"""
       x: int = round(u * width)
       y: int = round(v * height)
       return x, y

シードと再現性
----------------

ジェネラティブアートは乱数を多用するため、シードを固定しない限り実行のたびに違う結果になる。これは狙った効果である一方、「さっき気に入った出力をもう一度得たい」「1 つのパラメータだけを変えて見た目の違いを比較したい」といった場面では、同じシードから同じ乱数列を再現できることが重要になる。実際、本資料の\ :doc:`noise`\ の作例でも、``make_permutation(seed=...)`` に固定のシードを渡すことで、生成される画像を再現可能にしている。

``np.random.seed`` のようにグローバルな乱数状態を書き換える方式は、モジュールをまたいで暗黙の状態を共有してしまうため、複数の作品や複数のパーティクル群を同時に扱うコードでは思わぬ干渉が起きやすい。``np.random.default_rng(seed)`` でジェネレータのインスタンスを明示的に作り、それを関数の引数として持ち回す方式のほうが、「このシードでこのジェネレータから生成した」という対応関係がコード上に残り、再現性・独立性の両面で扱いやすい。

.. code-block:: python
   :linenos:

   import numpy as np

   rng: np.random.Generator = np.random.default_rng(seed=42)

.. _basics-composition:

構図とレイヤーの考え方
------------------------

1 枚の絵を「1 つの決め打ちの手続き」として書くのではなく、「パラメータを受け取って画像（または画像の一部）を返す関数」として設計しておくと、同じコードから多様なバリエーションを生み出せる。本資料の作例でも、:doc:`noise`\ の ``fbm2d`` / ``domain_warp2d`` は座標配列とシード・オクターブ数などのパラメータを受け取り、:doc:`fractals`\ の ``draw_l_system`` は axiom・書き換え規則・角度を受け取る、というように、いずれも「描画関数 + パラメータ」の形をとっている。

この形にしておくと、少なくとも 2 つの組み立て方ができるようになる。

グリッド配置
   パラメータ（シード、色相、角度など）を格子状に少しずつ変えながら同じ描画関数を繰り返し呼び出し、結果を並べて 1 枚の画像に敷き詰める。バリエーションを一覧して比較したいときや、パラメータが作品の見た目にどう影響するかを把握したいときに向く。

レイヤー合成
   同じ座標系に対して、性質の異なる描画関数を複数回呼び出し、その結果を重ね合わせる。例えば背景をノイズで塗り、その上にパーティクルシステムの軌跡を重ね、さらにフラクタルの輪郭を重ねる、といった組み合わせが考えられる。Pillow であれば ``Image.alpha_composite`` やアルファブレンドで、透明度を持たせながら重ねられる。

いずれの場合も、「1 回描画する処理」と「複数の結果を並べる・重ねる処理」を分けて実装しておくことが鍵になる。前者を作品ごとに使い回し、後者はグリッド配置・レイヤー合成のどちらにも共通して使える汎用的なユーティリティとして持っておくとよい。

.. _easing:

補間とイージング関数
----------------------

ジェネラティブアートでは、「2 つの値の間をなめらかにつなぐ」処理が至るところに現れる。2 色の間のグラデーション、図形の大きさを中心から外側へ変化させる処理、格子点の値からその間の値を求めるノイズの計算などは、いずれも ``t``\ （0〜1）を使った補間として書ける。もっとも単純なのは、``t`` に比例して値を変化させる線形補間（lerp）である。

.. math::

   \mathrm{lerp}(a, b, t) = a + (b - a)\,t

線形補間は変化の速さが常に一定であるため、両端で変化が急に始まり急に止まる、機械的な印象になりやすい。そこで、``t`` をいったん\ **イージング関数** :math:`f(t)`\ （:math:`f(0) = 0`、:math:`f(1) = 1` を満たす関数）に通してから補間に使うと、変化の緩急を自由に設計できる。

.. math::

   \mathrm{lerp}\bigl(a, b, f(t)\bigr)

代表的なイージング関数には次のようなものがある。

.. list-table::
   :header-rows: 1

   * - 名前
     - 式
     - 変化の特徴
   * - linear
     - :math:`f(t) = t`
     - 一定の速さで変化する（線形補間そのもの）。
   * - ease-in（3 次）
     - :math:`f(t) = t^3`
     - 始まりがゆっくりで、終わりに向かって加速する。
   * - ease-out（3 次）
     - :math:`f(t) = 1 - (1 - t)^3`
     - 始まりが速く、終わりに向かって減速する。
   * - smoothstep
     - :math:`f(t) = 3t^2 - 2t^3`
     - 両端でゆっくり、中央で速く変化する（ease-in-out）。両端で 1 階微分が 0 になる。
   * - smootherstep
     - :math:`f(t) = 6t^5 - 15t^4 + 10t^3`
     - smoothstep と同様の形で、両端で 1 階・2 階微分がともに 0 になる。

.. literalinclude:: ../examples/easing.py
   :linenos:
   :language: python
   :pyobject: smoothstep
   :caption: examples/easing.py の smoothstep 関数

.. literalinclude:: ../examples/easing.py
   :linenos:
   :language: python
   :pyobject: smootherstep
   :caption: examples/easing.py の smootherstep 関数

上の表の関数を、横軸を ``t``、縦軸を出力として左から順に描くと次のようになる。薄い対角線は比較用の線形補間である。

.. image:: _static/gallery/easing_curves.png
   :alt: linear・ease-in・ease-out・smoothstep・smootherstep の 5 つのイージング関数のグラフを横に並べた図
   :width: 600px

イージング関数は、UI やアニメーションで「動きの緩急」を付けるための道具として知られているが、本資料で扱う静止画でも、補間の割合 ``t`` を空間上の位置と見なせばそのまま使える。例えば、同じ 2 色の間のグラデーションを、イージング関数だけを変えて補間すると、色の変化が画像のどこに集中するかが変わる（上から linear・ease-in・ease-out・smoothstep・smootherstep の順）。

.. literalinclude:: ../examples/easing.py
   :linenos:
   :language: python
   :pyobject: render_eased_gradient
   :caption: examples/easing.py の render_eased_gradient 関数

.. image:: _static/gallery/easing_gradient.png
   :alt: 同じ 2 色の間を 5 種類のイージング関数で補間したグラデーションを縦に並べた画像
   :width: 600px

同様に、図形を並べる間隔をイージング関数で決めれば、間隔の疎密で奥行きや集中を表現できる。次の 2 枚は、同心円の半径を等間隔の ``t`` から求めたもの（左、linear）と、ease-in に通してから求めたもの（右）である。ease-in では中心付近の円が密に、外側の円が疎になり、中心に向かって吸い込まれるような印象になる。

.. literalinclude:: ../examples/easing.py
   :linenos:
   :language: python
   :pyobject: render_eased_rings
   :caption: examples/easing.py の render_eased_rings 関数

.. image:: _static/gallery/easing_rings_linear.png
   :alt: 半径を等間隔に取った同心円
   :width: 300px

.. image:: _static/gallery/easing_rings_ease_in.png
   :alt: 半径を ease-in で決めた同心円。中心付近が密で外側ほど間隔が広い
   :width: 300px

本資料の他の章にも、イージング関数は名前を変えて登場する。:doc:`noise`\ のパーリンノイズで格子点の値を補間する fade 関数は smootherstep そのものであり、:doc:`shapes`\ で SDF の輪郭をアンチエイリアスする処理や等高線を描く処理には smoothstep を使っている。いずれも「両端で傾きが 0 になる」性質を利用して、隣り合う領域の継ぎ目を目立たなくしている。

.. _animation:

時間変化の表現：静止画とアニメーション
------------------------------------------

本資料で扱う技法の多くは、本来は時間とともに変化するものである。セルオートマトンや反応拡散系は世代ごとに状態が更新され、パーティクルシステムや Boids は 1 ステップごとに粒子が動き、進化的アルゴリズムは世代を重ねるごとに目標へ近づいていく。本資料はこれらを 1 枚の静止画として示しており、その方法は大きく 2 つに分かれる。

最終状態を描く
   十分なステップ数だけ進めた時点の状態を 1 枚にする。:doc:`automata`\ の反応拡散系や、:doc:`evolution`\ の最終結果がこれにあたる。

軌跡を重ねる
   各ステップの状態を 1 枚に重ね合わせる（古いステップほど薄くする場合もある）。:doc:`automata`\ のライフゲームの軌跡や、:doc:`noise`\ のフローフィールドがこれにあたり、時間の流れを空間上の模様として表現できる。

一方で、変化そのものを見せたい場合は、各ステップの画像（フレーム）を順に並べたアニメーションとして書き出せばよい。:ref:`構図とレイヤーの考え方 <basics-composition>`\ で述べた通り、本資料の作例はどれも「パラメータや状態を受け取って 1 枚の画像を返す関数」として書かれているため、その関数を時刻ごとに繰り返し呼び出すだけでフレームの列が得られる。フレームの作り方には、次の 2 通りがある。

状態を更新する
   シミュレーションを 1 ステップ進めるごとに、その時点の状態を 1 フレームとして描く。セルオートマトンやパーティクルシステムのように、次の状態が現在の状態から決まる系に向く。

時刻をパラメータとして渡す
   時刻 :math:`t` を描画関数のパラメータ（位相・角度・ノイズの座標など）に対応させ、:math:`t` を少しずつ変えながら描く。:math:`t` の関数として周期的なもの（:math:`\sin(2\pi t)` や、角度として使う :math:`2\pi t` など）を選べば、最後のフレームから最初のフレームへなめらかにつながる、継ぎ目のないループアニメーションになる。動きに緩急を付けたい場合は、:ref:`easing`\ で扱ったイージング関数に :math:`t` を通してから使えばよい。

Pillow は複数の画像をアニメーション GIF として保存できるため、追加のライブラリなしで書き出せる。

.. literalinclude:: ../examples/animation.py
   :linenos:
   :language: python
   :pyobject: save_gif
   :caption: examples/animation.py の save_gif 関数

「状態を更新する」例として、:doc:`automata`\ のライフゲームの ``simulate_life`` が返す履歴を、1 世代ずつフレームにする。静止画の作例では同じ履歴を 1 枚に重ね合わせていたが、ここでは時間方向に並べる。

.. literalinclude:: ../examples/animation.py
   :linenos:
   :language: python
   :pyobject: life_frames
   :caption: examples/animation.py の life_frames 関数

.. image:: _static/gallery/animation_life.gif
   :alt: ライフゲームを 120 世代分、1 世代ずつフレームにしたアニメーション
   :width: 270px

「時刻をパラメータとして渡す」例として、:doc:`spirals`\ のリサージュ曲線の位相 :math:`\phi` を :math:`2\pi t` として 1 周期分動かす。位相は :math:`2\pi` を周期とするため、最後のフレームの次に最初のフレームへ戻っても変化がつながる。

.. literalinclude:: ../examples/animation.py
   :linenos:
   :language: python
   :pyobject: lissajous_loop_frames
   :caption: examples/animation.py の lissajous_loop_frames 関数

.. image:: _static/gallery/animation_lissajous.gif
   :alt: 周波数比 3:2 のリサージュ曲線の位相を 1 周期分動かした、継ぎ目のないループアニメーション
   :width: 240px

GIF は 1 フレームあたり 256 色までしか扱えず、フレーム数や画像サイズを増やすとファイルサイズも急速に大きくなる。本節の作例は、フレーム数・画像サイズを小さく抑えている。なめらかなグラデーションを含む作品や長いアニメーションを書き出す場合は、フレームを連番の PNG として保存し、動画編集ソフトや ffmpeg などで動画に変換する方法が向く。また、マウス操作に反応させるなど、実行中にリアルタイムで描画し続ける作品には、:doc:`intro`\ で触れた py5 のようなフレームベースの描画環境が適している。本資料では、アニメーションについてはここで述べた書き出し方の基本にとどめ、以降の章の作例は静止画で示す。
