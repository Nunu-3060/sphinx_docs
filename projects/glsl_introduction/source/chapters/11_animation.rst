第 11 章 アニメーション
=======================

シェーダーに経過時間を渡すと、形や色を時間とともに変化させるアニメーションを作れます。この章では、時間を使ったアニメーションの基本的な考え方を説明します。

時間を渡す
----------

シェーダーには時計がないため、経過時間は JavaScript から uniform 変数で渡します。ブラウザーでは、``requestAnimationFrame`` に渡した関数が画面の更新ごとに呼ばれ、その引数にページを開いてからの時刻（ミリ秒）が渡されます。

.. code-block:: javascript

   function frame(now) {
       gl.uniform1f(timeLocation, now / 1000);  // 秒に変換して渡す
       // ... 描画 ...
       requestAnimationFrame(frame);             // 次の画面の更新でも呼ぶ
   }
   requestAnimationFrame(frame);

サンプル 08 では、一時停止や速さの変更ができるように、前の画面の更新からの経過時間を求めて、自分で時間を足し合わせています。

.. literalinclude:: ../../examples/08_animation.html
   :language: javascript
   :start-after: // ---- 時間の管理 ----
   :end-before: // ---- 時間の管理ここまで ----
   :dedent: 4
   :caption: 時間の管理

.. warning::

   ``float`` の有効数字は 10 進数で 7 桁程度です。時間の値が大きくなると小数点以下の精度が失われ、``sin(uTime * 10.0)`` のような細かい変化がなめらかに動かなくなります。長時間動かし続ける場合は、時間をある周期で 0 に戻すなどの工夫が必要です。

周期的な動き
------------

時間 t を使って周期的な動きを作るには、次のような関数を使います。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 式
     - 動き
   * - ``sin(t)``
     - -1 から 1 の間をなめらかに往復します（周期 2π 秒）。
   * - ``0.5 + 0.5 * sin(t)``
     - 0 から 1 の間をなめらかに往復します。
   * - ``fract(t)``
     - 0 から 1 まで増えて 0 に戻る変化を、1 秒ごとに繰り返します。
   * - ``1.0 - abs(2.0 * fract(t) - 1.0)``
     - 0 から 1 まで増えて 0 まで減る変化（三角波）を、1 秒ごとに繰り返します。
   * - ``step(0.5, fract(t))``
     - 0 と 1 を 0.5 秒ごとに切り替えます（点滅）。

周期を変えたい場合は、t に定数を掛けます。例えば ``sin(2.0 * 3.14159265 * t / 4.0)`` は、周期 4 秒で往復します。

イージング
----------

一定の速さで動く動きは、機械的に見えがちです。動き始めや止まる直前をゆっくりにすると、自然な動きになります。このように、0 から 1 まで進む値 t を、緩急の付いた値に変換する関数をイージング関数と呼びます。

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 名前
     - 式
     - 動き
   * - linear
     - :math:`t`
     - 一定の速さ
   * - ease-in
     - :math:`t^2`
     - ゆっくり動き始め、だんだん速くなる
   * - ease-out
     - :math:`1 - (1 - t)^2`
     - 速く動き始め、だんだん遅くなる
   * - smoothstep
     - :math:`t^2 (3 - 2t)`
     - 動き始めと終わりがゆっくり

サンプル 08 の「イージング」では、4 つのイージング関数で動く円を上から順に並べて、動きを比較しています。

.. literalinclude:: ../../examples/shaders/08_animation_easing.frag
   :language: glsl
   :caption: 08_animation_easing.frag（フラグメントシェーダー）

背景の色には、コサイン関数を使ったカラーパレットを使っています。``palette(t)`` の R、G、B の各成分は、位相を 1/3 周期ずつずらしたコサイン関数なので、t が変化すると色相が連続的に変わります。

頂点アニメーション
------------------

頂点シェーダーで頂点の位置を時間とともに動かすと、形そのものを変形させられます。サンプル 08 の「頂点アニメーション」では、格子状に並べた頂点の高さを、中心からの距離 :math:`r` と時間 :math:`t` に応じて変えて、水面の波紋のような波を作っています。

.. math::

   y = A \sin(k r - \omega t)

:math:`A` は波の高さ（振幅）、:math:`k` は波数（大きいほど波の間隔が狭い）、:math:`\omega` は角速度（大きいほど波が速く進む）です。:math:`k r - \omega t` が一定の点、つまり同じ高さの点は、時間とともに :math:`r` が大きくなる方向へ移動するので、波が外側へ広がっていくように見えます。

.. literalinclude:: ../../examples/shaders/08_animation_wave.vert
   :language: glsl
   :caption: 08_animation_wave.vert（頂点シェーダー）

.. rubric:: サンプル 08：アニメーション

`ブラウザーで開く <../examples/08_animation.html>`__／:download:`ダウンロード <../../examples/08_animation.html>`／シェーダー：:download:`08_animation_wave.vert <../../examples/shaders/08_animation_wave.vert>`、:download:`08_animation_wave.frag <../../examples/shaders/08_animation_wave.frag>`、:download:`08_animation_easing.vert <../../examples/shaders/08_animation_easing.vert>`、:download:`08_animation_easing.frag <../../examples/shaders/08_animation_easing.frag>`

.. raw:: html

   <iframe src="../examples/08_animation.html" title="サンプル 08：アニメーション" loading="lazy" style="width: 100%; height: 510px; border: 1px solid #ccc;"></iframe>

.. note::

   頂点シェーダーで形を変形させると、元の法線は変形後の表面に垂直ではなくなります。変形した物体にライティングを行う場合は、法線も計算し直す必要があります。例えば、高さを :math:`y = h(x, z)` で表す場合、法線は :math:`(-\partial h / \partial x, 1, -\partial h / \partial z)` を正規化したものになります。

アニメーションの計算を CPU と GPU のどちらで行うか
--------------------------------------------------

物体全体を回転させるだけなら、JavaScript で回転行列を計算して uniform 変数で渡すほうが効率的です。行列の計算は描画 1 回につき 1 回で済みますが、同じ計算を頂点シェーダーで行うと頂点の数だけ繰り返すことになるからです。

一方、波のように頂点ごとに異なる動きをさせる場合は、頂点シェーダーで計算するのが適しています。JavaScript で計算すると、頂点データを毎回 GPU に転送し直す必要があるからです。

試してみよう
------------

* 波の頂点シェーダーの ``length(aGrid)`` を ``aGrid.x`` に変えて、平面波（一方向に進む波）にする。
* イージングのフラグメントシェーダーに、新しいイージング関数（例えば :math:`t^3`）を追加して、動きを比べる。
