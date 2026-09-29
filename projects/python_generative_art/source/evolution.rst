進化的アルゴリズム
====================

変異と選択による探索
------------------------

:doc:`intro`\ で触れた通り、ジェネラティブアートの生成手法には、乱数・ノイズ関数・セルオートマトン・L-system と並んで\ **進化的アルゴリズム**\ （evolutionary algorithm）が数えられる。ここまでの章で扱った手法は、いずれも「決まった手続きを 1 回（あるいは反復）適用すれば結果が決まる」ものだった。進化的アルゴリズムはこれとは異なり、次の 2 つの操作を繰り返すことで、設計者が正解の手続きを直接書かなくても解を徐々に洗練させていく。

変異（mutation）
   現在の解に、ランダムな小さな変化を加える。

選択（selection）
   変異前後を何らかの\ **適応度**\ （fitness、目的に対する「良さ」）で比較し、良くなっていれば採用し、そうでなければ棄てる。

生物の進化になぞらえてこう呼ばれるが、必要なのは「適応度を数値で測れること」と「小さな変異を加えられること」だけであり、対象は絵でも音楽でもパラメータの組でも構わない。本章では、多数の半透明三角形を重ね合わせて 1 枚の目標画像に近づける、という単純な題材を通してこの考え方を実装する。

個体の表現と描画
------------------

個体（genome）を「三角形のリスト」として表現する。三角形はそれぞれ 3 頂点の座標と、RGBA の色（アルファ値を低めに抑えた半透明）を持つ。

.. literalinclude:: ../examples/evolution.py
   :language: python
   :pyobject: random_triangle
   :caption: examples/evolution.py の random_triangle 関数

個体を描画する際は、三角形ごとに画素が内部にあるかどうかを判定し、アルファ値で重みづけしながら白いキャンバスに重ね合わせる。内外判定には、3 辺それぞれについて「画素がその辺のどちら側にあるか」を表す符号付き面積（edge function）を使い、3 辺全てで符号がそろっている画素だけを内部とする。画素グリッド全体に対する 1 回の NumPy 演算で判定できるため、世代ごとに個体を描き直す本章の用途に向いている。

.. literalinclude:: ../examples/evolution.py
   :language: python
   :pyobject: triangle_mask
   :caption: examples/evolution.py の triangle_mask 関数

.. literalinclude:: ../examples/evolution.py
   :language: python
   :pyobject: render_genome
   :caption: examples/evolution.py の render_genome 関数

目標画像との差を測る
----------------------

外部の画像ファイルに頼らず、空のグラデーション・太陽・山という 3 種類の平坦な図形だけで目標画像を合成する。少数の三角形でも近似の様子が分かりやすい題材になっている。

.. literalinclude:: ../examples/evolution.py
   :language: python
   :pyobject: make_target
   :caption: examples/evolution.py の make_target 関数

.. image:: _static/gallery/evolution_target.png
   :alt: 近似の目標にする、空のグラデーション・太陽・2 つの山から成る単純な画像
   :width: 240px

適応度は、目標画像との平均二乗誤差（小さいほど良い）で測る。

.. literalinclude:: ../examples/evolution.py
   :language: python
   :pyobject: fitness
   :caption: examples/evolution.py の fitness 関数

(1+1) 進化戦略
----------------

集団（population）を持たず、「現在の 1 個体（親）」から変異させた「候補 1 個体（子）」だけを毎世代比較する、実装がもっとも単純な進化的アルゴリズムを **(1+1) 進化戦略**\ と呼ぶ（名前の「1+1」は、親 1 個体・子 1 個体という個体数の内訳を表す）。変異は、三角形を 1 枚追加・削除する、頂点を 1 つ少しずらす、色を少し変える、のいずれかをランダムに選んで行う。

.. literalinclude:: ../examples/evolution.py
   :language: python
   :pyobject: mutate
   :caption: examples/evolution.py の mutate 関数

変異させた個体を描画して適応度を測り、現在の個体より良くなっていれば採用し、そうでなければ棄てて元の個体に戻る、という選択を指定世代数だけ繰り返す。

.. literalinclude:: ../examples/evolution.py
   :language: python
   :pyobject: evolve
   :caption: examples/evolution.py の evolve 関数

世代を追うごとに三角形の集合が目標画像に近づいていく様子は、次のようになる（左から世代 30・300・1500・5999）。

.. image:: _static/gallery/evolution_progress.png
   :alt: 世代 30・300・1500・5999 における個体の描画結果を並べた画像。世代が進むにつれてノイズ状の重なりから山と太陽の輪郭が徐々に浮かび上がる
   :width: 600px

6000 世代まで進めた最終結果を目標画像と比べると、三角形の粗い集合だけで山の稜線と太陽の位置がおおむね再現されているのが分かる。

.. image:: _static/gallery/evolution_result.png
   :alt: 6000 世代の進化を経た最終結果。目標画像の山と太陽のシルエットがおおむね再現されている
   :width: 240px

本来の遺伝的アルゴリズムは、集団の中の複数個体を適応度に応じて選び出し、2 個体の遺伝子を組み合わせる交叉（crossover）を行うことで、より効率的に探索空間を進む。本章の (1+1) 進化戦略はそれを持たない最小構成だが、「改善する変異だけを採用する」という選択の核心部分は共通している。:doc:`fractals`\ の IFS が「あらかじめ選んだ変換をランダムに適用し続けると自然に収束する」手法だったのに対し、進化的アルゴリズムは「試行錯誤の結果を毎回評価し、良かったものだけを次に引き継ぐ」という、フィードバックを伴う探索である点が対照的である。
