螺旋と曲線
============

フィロタキシス
----------------

ひまわりの種やパイナップルの実、松かさの鱗片は、中心から一定の角度ずつ回転しながら外側へ広がる螺旋状に並んでいる。この配置は\ **フィロタキシス**\ （phyllotaxis、葉序）と呼ばれ、「1 点ずつ一定の角度だけ回転し、中心からの距離を少しずつ広げる」という単純な規則を繰り返すだけで再現できる。距離を点の番号の平方根に比例させるのは、外側にいくほど点の間隔が間延びしないよう、単位面積あたりの点の密度をほぼ一定に保つためである。

.. literalinclude:: ../examples/phyllotaxis.py
   :linenos:
   :language: python
   :pyobject: phyllotaxis_points
   :caption: examples/phyllotaxis.py の phyllotaxis_points 関数

回転角に何を使うかで模様の印象は大きく変わる。黄金比 :math:`\varphi = (1+\sqrt{5})/2` から作られる\ **黄金角** :math:`2\pi/\varphi^2`\ （およそ 137.5 度）を使うと、どの点も他の点とほとんど重ならず、隙間なく詰まった自然な螺旋になる。

.. literalinclude:: ../examples/phyllotaxis.py
   :linenos:
   :language: python
   :pyobject: metallic_angle
   :caption: examples/phyllotaxis.py の metallic_angle 関数

.. image:: _static/gallery/phyllotaxis_golden.png
   :alt: 黄金角による 500 点のフィロタキシス配置。隙間なく均一に詰まった螺旋になる
   :width: 350px

貴金属比の比較
----------------

黄金比は、``metallic_angle`` の式が示す通り、**貴金属比**\ と呼ばれる数列の 1 つに過ぎない。貴金属比は :math:`x^2 = nx + 1`\ （:math:`n` は正の整数）の正の解として定義され、:math:`n=1` が黄金比、:math:`n=2` が\ **白銀比** :math:`1+\sqrt{2}` になる。同じ ``metallic_angle`` 関数に白銀比を渡すだけで、全く違う印象の螺旋が得られる。

.. image:: _static/gallery/phyllotaxis_silver.png
   :alt: 白銀比による回転角で配置した 500 点のフィロタキシス。放射状の腕がはっきり見える渦巻きになる
   :width: 350px

黄金角による配置が「どこにも規則性が見えない」最密パターンになるのに対し、白銀比では明確な渦状の「腕」が浮かび上がる。これは、黄金比が連分数展開 :math:`[1; 1, 1, 1, \ldots]` を持つ、有理数によってもっとも近似しにくい「もっとも無理数的な数」であるのに対し、白銀比の連分数展開 :math:`[2; 2, 2, 2, \ldots]` はそれよりも近似されやすく、結果として点の並びに周期的な規則性が残りやすいためである。同じ仕組みでも、使う定数 1 つで生成物の性質が大きく変わる好例と言える。

対数螺旋（黄金螺旋）
----------------------

フィロタキシスは点を 1 つずつ打っていく離散的な配置だったが、同じ「角度が進むにつれて中心からの距離が増える」という発想を連続的な曲線にしたものが\ **対数螺旋**\ である。実際、黄金角のフィロタキシスの点群を外側から包むように見ると、対数螺旋（の集まり）が浮かび上がって見える。

.. math::

   r = a \, e^{b \theta}

.. literalinclude:: ../examples/polar_curves.py
   :linenos:
   :language: python
   :pyobject: logarithmic_spiral_points
   :caption: examples/polar_curves.py の logarithmic_spiral_points 関数

成長率 :math:`b` を、4 分の 1 回転（90 度）ごとに黄金比 :math:`\varphi` 倍に広がるように選ぶと、オウムガイの殻の断面としてよく紹介される、いわゆる\ **黄金螺旋**\ になる（実際のオウムガイの成長率は種や個体差があり黄金比からずれることが多く、この対応は近似的な通説として広まったものである点には注意）。

.. literalinclude:: ../examples/polar_curves.py
   :linenos:
   :language: python
   :pyobject: golden_spiral_b
   :caption: examples/polar_curves.py の golden_spiral_b 関数

.. image:: _static/gallery/logarithmic_spiral.png
   :alt: 黄金比を成長率とした対数螺旋（黄金螺旋）
   :width: 350px

対数螺旋は「:math:`r` を角度 :math:`\theta` の関数として定義する」という螺旋の作り方の 1 つの例に過ぎない。:math:`\theta` に対する増え方を変えるだけで、性質の異なる螺旋になる。**アルキメデスの螺旋** :math:`r = a + b\theta` は、対数螺旋のように指数的にではなく、:math:`\theta` に比例して線形に広がる。腕と腕の間隔が常に一定になるため、レコード盤の溝や、ノートの螺旋綴じで見かける螺旋はこちらに近い。

.. math::

   r = a + b\theta

.. literalinclude:: ../examples/polar_curves.py
   :linenos:
   :language: python
   :pyobject: archimedean_spiral_points
   :caption: examples/polar_curves.py の archimedean_spiral_points 関数

.. image:: _static/gallery/archimedean_spiral.png
   :alt: アルキメデスの螺旋。腕の間隔が常に一定になる
   :width: 300px

逆に、:math:`\theta` に反比例して :math:`r` が小さくなる\ **双曲螺旋** :math:`r = a/\theta` は、中心に近づくほどきつく巻き、外側にいくほど巻きが緩くなって、ある直線（漸近線）に近づいていく。:math:`\theta \to 0` で :math:`r \to \infty` に発散してしまうため、原点のごく近くは評価対象から外している。

.. math::

   r = \frac{a}{\theta}

.. literalinclude:: ../examples/polar_curves.py
   :linenos:
   :language: python
   :pyobject: hyperbolic_spiral_points
   :caption: examples/polar_curves.py の hyperbolic_spiral_points 関数

.. image:: _static/gallery/hyperbolic_spiral.png
   :alt: 双曲螺旋。中心付近はきつく巻き、外側では直線に近づいていく
   :width: 300px

指数的に広がる対数螺旋、線形に広がるアルキメデスの螺旋、反比例して収束していく双曲螺旋は、いずれも :math:`r(\theta)` の式を 1 つ変えるだけの違いでしかないが、生まれる曲線の印象は大きく異なる。

サイクロイドとスピログラフ
-----------------------------

円が直線や別の円に沿って滑らずに転がるとき、円周上の 1 点が描く軌跡を\ **サイクロイド族**\ の曲線と呼ぶ。もっとも単純な例が、直線上を転がる円の軌跡である\ **サイクロイド**\ である。

.. math::

   x = r(t - \sin t)

.. math::

   y = r(1 - \cos t)

.. literalinclude:: ../examples/spirograph.py
   :linenos:
   :language: python
   :pyobject: cycloid_points
   :caption: examples/spirograph.py の cycloid_points 関数

.. image:: _static/gallery/cycloid.png
   :alt: 直線上を転がる円の軌跡であるサイクロイド曲線
   :width: 350px

直線の代わりに、固定した円の内側・外側を転がる円を考えると、いわゆる「スピログラフ」のおもちゃと同じ模様が描ける。転がる円の中心からペン先までの距離 :math:`d` を、転がる円の半径そのものではなく自由なパラメータにしておくと、尖った星形から輪が連なるループ状まで多様な模様を作れる（この一般化はハイポトロコイド／エピトロコイドと呼ばれる）。

.. literalinclude:: ../examples/spirograph.py
   :linenos:
   :language: python
   :pyobject: hypotrochoid_points
   :caption: examples/spirograph.py の hypotrochoid_points 関数

.. literalinclude:: ../examples/spirograph.py
   :linenos:
   :language: python
   :pyobject: epitrochoid_points
   :caption: examples/spirograph.py の epitrochoid_points 関数

固定円の半径・転がる円の半径の比によって、曲線が何周してから閉じるかが決まる（最大公約数を使って必要な周回数を求めている）。同じ半径の組み合わせ (5, 3) でも、内側を転がるか外側を転がるかで全く違う模様になる。

.. image:: _static/gallery/hypotrochoid.png
   :alt: 固定円の内側を転がる円によるハイポトロコイド。5 つの頂点を持つ星形になる
   :width: 300px

.. image:: _static/gallery/epitrochoid.png
   :alt: 固定円の外側を転がる円によるエピトロコイド。花びら状の模様になる
   :width: 300px

フィロタキシスが「1 点ずつ増える離散的な点の集まり」だったのに対し、サイクロイド族は「時刻 :math:`t` を細かく振って求めた 1 本の連続した曲線」である点が対照的である。どちらも、単純な式を NumPy でベクトル化して一括計算するだけで、複雑に見える模様が得られる。

リサージュ曲線とハーモノグラフ
---------------------------------

x 軸・y 軸それぞれに周波数の異なる正弦振動を与えると、その軌跡は周波数比に応じて様々な閉曲線を描く。これを\ **リサージュ曲線**\ と呼ぶ。オシロスコープに 2 つの交流信号を入力したときに現れる図形としても知られる。なお、周波数比がちょうど 1:1 のときは、位相差に応じて直線・楕円・円（振幅が等しく位相差が 90 度の場合）のいずれかになる。8 の字やより複雑な模様が現れるのは、周波数比が 1:1 からずれている場合である。

.. math::

   x = \sin(f_x t + \phi), \quad y = \sin(f_y t)

.. literalinclude:: ../examples/lissajous.py
   :linenos:
   :language: python
   :pyobject: lissajous_points
   :caption: examples/lissajous.py の lissajous_points 関数

.. image:: _static/gallery/lissajous.png
   :alt: 周波数比 3:2 のリサージュ曲線
   :width: 350px

振幅が時間とともに指数的に減衰する効果を加えると、実際に 2 つの振り子を直交させてペン先の軌跡を記録する「ハーモノグラフ」という装置と同じ軌跡が再現できる。周波数をわずかに整数比からずらす（例えば 3 ではなく 3.01 にする）と、実際の振り子が持つわずかな誤差を模した、渦を巻きながら中心に収束していくより有機的な軌跡になる。

.. literalinclude:: ../examples/lissajous.py
   :linenos:
   :language: python
   :pyobject: harmonograph_points
   :caption: examples/lissajous.py の harmonograph_points 関数

.. image:: _static/gallery/harmonograph.png
   :alt: 周波数をわずかにずらし、振幅を減衰させたハーモノグラフの軌跡
   :width: 350px

バラ曲線
----------

**バラ曲線**\ （rhodonea curve）は、極座標で :math:`r = \cos(k\theta)` と表される、花びら状の曲線である。フィロタキシスや対数螺旋と同じく、距離を角度の関数として定義する極座標の発想に基づく。

.. math::

   r = \cos(k\theta)

.. literalinclude:: ../examples/polar_curves.py
   :linenos:
   :language: python
   :pyobject: rose_curve_points
   :caption: examples/polar_curves.py の rose_curve_points 関数

花びらの枚数は :math:`k` の値によって決まり、:math:`k` が奇数なら :math:`k` 枚、偶数なら :math:`2k` 枚になる（:math:`\cos` が負の値を取る半周期でも、極座標では原点を挟んだ反対側に点が打たれるため、偶数のときは花びらの数が 2 倍になる）。

.. image:: _static/gallery/rose_5.png
   :alt: k=5 のバラ曲線。花びらが 5 枚になる
   :width: 300px

.. image:: _static/gallery/rose_4.png
   :alt: k=4 のバラ曲線。花びらが 8 枚になる
   :width: 300px

スーパーフォーミュラ
-----------------------

バラ曲線は :math:`r = \cos(k\theta)` という 1 つの式の :math:`k` を変えるだけで花びらの数を操作できたが、この発想をさらに推し進め、円・多角形・星形・歯車状・花びら状といった質的に異なる輪郭までも 1 つの式から作り分けられるようにしたのが、Johan Gielis が 2003 年の論文で提案した\ **スーパーフォーミュラ**\ （superformula）である。

.. math::

   r(\theta) = \left(
       \left|\frac{\cos(m\theta/4)}{a}\right|^{n_2}
       + \left|\frac{\sin(m\theta/4)}{b}\right|^{n_3}
   \right)^{-1/n_1}

対称性の次数 :math:`m` は花びらや角の数を、指数 :math:`n_1, n_2, n_3` は輪郭の丸み・尖り具合を決める。:math:`a, b` は横方向・縦方向それぞれの伸び率で、既定値の 1 のままなら円対称、値を変えれば横長・縦長に引き伸ばした輪郭になる（本節の作例ではいずれも 1 のまま使う）。指数を全て :math:`n_1=n_2=n_3=2` にすると :math:`m` の値によらず :math:`\cos^2+\sin^2=1` が恒等的に成り立つため厳密に半径 1 の円になる（:math:`m` は角の数ではなく角速度を変えるだけなので、この恒等式には影響しない）。:math:`m=4` のまま 3 つの指数をそろえて大きくしていくと、角の丸い正方形である超楕円（squircle）を経て正方形に近づく。もとは植物の葉や貝殻、珪藻の殻など自然界の輪郭を少数のパラメータで統一的に表現する目的で考案された式だが、パラメータの組み合わせ次第で人工的な幾何学模様も自在に作れる。

.. literalinclude:: ../examples/polar_curves.py
   :linenos:
   :language: python
   :pyobject: superformula_points
   :caption: examples/polar_curves.py の superformula_points 関数

:math:`m, n_1, n_2, n_3` の 4 つだけを変えて 4 種類の輪郭を描くと、同じ式とは思えないほど印象の異なる形状が並ぶ。

.. image:: _static/gallery/superformula.png
   :alt: スーパーフォーミュラのパラメータを変えて生成した 4 種類の輪郭。丸みを帯びた三角形・6 枚花びら・歯車状の星形・4 本腕の星形が並ぶ
   :width: 400px

.. _bezier:

ベジェ曲線とスプライン曲線
----------------------------

ここまでの曲線は、いずれも式で形が決まり、パラメータを変えることで形を操作していた。一方で、「この点から出発し、あの点のあたりを通って、ここで終わる」というように、形そのものを直接指定したい場合もある。そうした用途で広く使われているのが\ **ベジェ曲線**\ （Bézier curve）である。ベクター描画ソフトのペンツール、フォントの輪郭、:doc:`intro`\ で触れた pycairo の ``curve_to`` など、曲線を扱う多くの場面で標準的に使われている。

ベジェ曲線の形は、並べた\ **制御点** :math:`P_0, P_1, \ldots, P_n` で決まる（:math:`n` を曲線の次数と呼ぶ）。曲線は始点 :math:`P_0` と終点 :math:`P_n` を通るが、途中の制御点は通らず、曲線をその方向へ引き寄せる役割を持つ。曲線上の点は、次の **de Casteljau のアルゴリズム**\ で求められる。

1. 隣り合う制御点どうしを、パラメータ :math:`t`\ （0〜1）の割合で線形補間する。点が 1 つ少ない点列ができる。
2. できた点列に対して、同じ線形補間を繰り返す。
3. 点が 1 つになったら、それが :math:`t` における曲線上の点である。

:math:`t` を 0 から 1 まで動かすと、始点から終点までの曲線が得られる。次の図は、4 つの制御点（灰色）で決まる 3 次ベジェ曲線（青）と、:math:`t = 0.4` における作図の途中経過である。灰色の線分をそれぞれ 0.4 の割合で分けた点が緑、緑の線分を同じ割合で分けた点が橙で、橙の線分を分けた赤い点が曲線上の点になる。

.. image:: _static/gallery/bezier_construction.png
   :alt: 4 つの制御点による 3 次ベジェ曲線と、t=0.4 における de Casteljau のアルゴリズムの作図。制御点を結ぶ灰色の折れ線、緑と橙の途中経過の線分、曲線上の赤い点が描かれている
   :width: 350px

実装では、全ての :math:`t` についての計算をまとめて NumPy の配列演算で行っている。

.. literalinclude:: ../examples/bezier.py
   :linenos:
   :language: python
   :pyobject: de_casteljau
   :caption: examples/bezier.py の de_casteljau 関数

3 次の場合、この線形補間の繰り返しを展開すると、制御点の重み付き和として書ける。

.. math::

   B(t) = (1-t)^3 P_0 + 3(1-t)^2 t\,P_1 + 3(1-t)\,t^2 P_2 + t^3 P_3

各制御点に掛かる重みは\ **バーンスタイン基底多項式**\ と呼ばれ、どの :math:`t` でも全て 0 以上で、合計は 1 になる。そのため、曲線は常に制御点を囲む凸多角形（凸包）の内側に収まる。また、始点での曲線の向きは :math:`P_0` から :math:`P_1` へ向かう方向、終点での向きは :math:`P_2` から :math:`P_3` へ向かう方向に一致する。

この式の制御点に、座標ではなく 1 つの数値を入れると、:ref:`easing`\ で扱ったイージング関数が現れる。例えば 0, 0, 1, 1 を入れると :math:`3t^2 - 2t^3`\ （smoothstep）に、0, 0, 0, 1 を入れると :math:`t^3`\ （3 次の ease-in）になる。線形補間そのものも、制御点が 2 つの 1 次ベジェ曲線にあたる。実際、CSS の ``cubic-bezier()`` のように、イージング関数を 3 次ベジェ曲線の制御点で指定する方式も広く使われている。

ベジェ曲線は途中の制御点を通らないため、「与えた点を全て通るなめらかな曲線」を引きたい場合には扱いにくい。そのような曲線には、**Catmull-Rom スプライン**\ がよく使われる。点 :math:`P_i` から :math:`P_{i+1}` までの区間を、各点での接線を前後の点の差の半分（:math:`P_i` では :math:`(P_{i+1} - P_{i-1})/2`）とした 3 次曲線で結ぶ方法である。3 次ベジェ曲線の始点での接線は :math:`3(P_1 - P_0)` なので、各区間は次の 4 点を制御点とする 3 次ベジェ曲線に変換できる。

.. math::

   P_i,\quad P_i + \frac{P_{i+1} - P_{i-1}}{6},\quad P_{i+1} - \frac{P_{i+2} - P_i}{6},\quad P_{i+1}

隣り合う区間は、共有する点で接線が一致するため、折れ目なくつながる。変換した後は、先ほどの ``de_casteljau`` で区間ごとに点を求めて並べればよい。

.. literalinclude:: ../examples/bezier.py
   :linenos:
   :language: python
   :pyobject: catmull_rom_to_bezier
   :caption: examples/bezier.py の catmull_rom_to_bezier 関数

.. literalinclude:: ../examples/bezier.py
   :linenos:
   :language: python
   :pyobject: sample_bezier_segments
   :caption: examples/bezier.py の sample_bezier_segments 関数

例として、円周上に等間隔で置いた 9 個の点の半径をランダムに伸び縮みさせ、直線で結んだもの（左）と、Catmull-Rom スプラインで結んだもの（右）を比べる。同じ点を通っていても、スプラインでは角が取れ、有機的な塊（ブロブ）になる。:doc:`shapes`\ の SDF によるブロブは輪郭全体をノイズで歪めていたが、こちらは曲線が通る点を直接指定できるため、形を思い通りに制御しやすい。

.. literalinclude:: ../examples/bezier.py
   :linenos:
   :language: python
   :pyobject: random_blob_points
   :caption: examples/bezier.py の random_blob_points 関数

.. image:: _static/gallery/spline_polygon.png
   :alt: 半径をランダムに伸び縮みさせた 9 個の点を直線で結んだ多角形
   :width: 300px

.. image:: _static/gallery/spline_blob.png
   :alt: 同じ 9 個の点を Catmull-Rom スプラインで結んだ、角のないなめらかな塊
   :width: 300px

多数の 3 次ベジェ曲線を少しずつ変えながら重ねると、髪や草のような線の束を描ける。各曲線の内側の制御点を横にずらす量を、曲線の番号に対する正弦波で決めると、隣り合う曲線どうしが似た形になり、全体として波打つ流れが生まれる。:doc:`noise`\ のフローフィールドも流れる線の束を作るが、あちらはベクトル場に沿って線を少しずつ伸ばすのに対し、こちらは 1 本ずつの形を制御点で決める点が異なる。

.. literalinclude:: ../examples/bezier.py
   :linenos:
   :language: python
   :pyobject: render_strands
   :caption: examples/bezier.py の render_strands 関数

.. image:: _static/gallery/bezier_strands.png
   :alt: 下端から上端へ伸びる 120 本の 3 次ベジェ曲線を重ねた線の束。全体が波打つように流れている
   :width: 400px

Pillow の ``ImageDraw`` にはベジェ曲線を直接描く機能がないため、本節の作例では曲線上の点を細かく求め、折れ線として描いている。拡大しても劣化しない曲線として出力したい場合は、pycairo の ``curve_to`` に制御点をそのまま渡せばよい。なお、スプライン曲線には、与えた点を通らない代わりに曲率の変化までなめらかにつながる B スプラインなど、ほかにも多くの種類がある。

スーパーフォーミュラまでの曲線は、どれもたった 1 つか 2 つのパラメータ（周波数比、成長率、転がる円の半径比など）を変えるだけで見た目が大きく変わる。値を少しずつ振って並べてみる、あるいは色を変えてみる、といった探索そのものが、これらの技法を使った制作の醍醐味と言える。一方、ベジェ曲線とスプライン曲線は式ではなく制御点で形を決めるため、作りたい形に合わせて点を置くことも、点の配置そのものを乱数やほかの技法で生成することもできる。
