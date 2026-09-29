スクリプトで動かす基礎
======================

この章では、C# スクリプトで GameObject を動かす方法を説明する。ここで扱う補間やカーブの考え方は、第 4 章以降のキーフレームアニメーションを理解するための基礎にもなる。

フレームレートに依存しない移動
------------------------------

``Update`` メソッドはフレームごとに 1 回呼び出される。1 秒あたりのフレーム数（フレームレート）は実行環境や処理負荷によって変わるため、1 フレームあたりの移動量を固定すると、フレームレートによって移動の速さが変わってしまう。

これを防ぐには、前のフレームからの経過時間（秒）を表す ``Time.deltaTime`` を移動量に掛ける。速度を :math:`\boldsymbol{v}`、経過時間を :math:`\Delta t` とすると、フレームごとの位置の更新は次の式で表される。

.. math::

   \boldsymbol{p}_{\text{new}} = \boldsymbol{p}_{\text{old}} + \boldsymbol{v} \, \Delta t

たとえば、60 fps では :math:`\Delta t \approx 0.0167` 秒、30 fps では :math:`\Delta t \approx 0.0333` 秒となる。フレームレートが半分になると 1 フレームあたりの移動量が 2 倍になるため、1 秒あたりの移動距離は変わらない。

.. literalinclude:: ../examples/MoveWithDeltaTime.cs
   :language: csharp
   :caption: MoveWithDeltaTime.cs

:download:`MoveWithDeltaTime.cs をダウンロード <../examples/MoveWithDeltaTime.cs>`

線形補間
--------

2 つの値の間を割合で指定して求めることを補間という。最も基本的な補間は線形補間（Linear Interpolation、略して Lerp）であり、開始値 :math:`\boldsymbol{p}_0`、終了値 :math:`\boldsymbol{p}_1`、割合 :math:`t` を使って次の式で表される。ここで :math:`t` は 0 以上 1 以下の値である。

.. math::

   \boldsymbol{p}(t) = (1 - t) \, \boldsymbol{p}_0 + t \, \boldsymbol{p}_1

:math:`t = 0` のとき開始値、:math:`t = 1` のとき終了値、:math:`t = 0.5` のとき中間の値となる。Unity では ``Vector3.Lerp`` や ``Mathf.Lerp`` がこの計算を行う。

回転の補間には ``Quaternion.Slerp`` を使う。Slerp（球面線形補間）は、回転の角度が一定の速さで変化するように補間する。オイラー角の各成分を個別に線形補間すると、回転の経路が不自然になる場合があるため、回転はクォータニオンで補間する。

次のサンプルは、経過時間を所要時間で割って割合 :math:`t` を求め、位置と回転を補間する。

.. literalinclude:: ../examples/LerpMover.cs
   :language: csharp
   :caption: LerpMover.cs

:download:`LerpMover.cs をダウンロード <../examples/LerpMover.cs>`

.. note::

   ``Vector3.Lerp(transform.position, target, speed * Time.deltaTime)`` のように、現在位置を開始値として毎フレーム補間する書き方もよく見られる。この書き方では目標に近づくほど遅くなる動きになるが、1 フレームあたりの補間の割合を :math:`k \, \Delta t` としているため、フレームレートによって動きが少し変わる。フレームレートに依存させたくない場合は、割合を :math:`1 - e^{-k \Delta t}` とする（:math:`k` は近づく速さを表す定数）。C# では ``1f - Mathf.Exp(-k * Time.deltaTime)`` と書ける。

イージング
----------

線形補間では、動き始めから止まるまで一定の速さで動くため、機械的な印象になる。そこで、割合 :math:`t` をそのまま使わず、関数 :math:`f(t)` で変換してから補間に使う。この関数をイージング関数という。

代表的なイージング関数を次の表に示す。いずれも :math:`f(0) = 0`、:math:`f(1) = 1` を満たすため、開始値と終了値は変わらない。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 名前
     - 式
     - 動きの特徴
   * - Linear
     - :math:`f(t) = t`
     - 等速で動く。
   * - Ease In
     - :math:`f(t) = t^2`
     - ゆっくり動き出し、だんだん速くなる。
   * - Ease Out
     - :math:`f(t) = 1 - (1 - t)^2`
     - 速く動き出し、だんだん遅くなる。
   * - Smoothstep
     - :math:`f(t) = 3t^2 - 2t^3`
     - ゆっくり動き出し、ゆっくり止まる。

Smoothstep の導関数は :math:`f'(t) = 6t - 6t^2` であり、:math:`f'(0) = f'(1) = 0` となる。つまり、開始時と終了時の速さが 0 になるため、滑らかに動き出して滑らかに止まる。

.. literalinclude:: ../examples/EasingMover.cs
   :language: csharp
   :caption: EasingMover.cs

:download:`EasingMover.cs をダウンロード <../examples/EasingMover.cs>`

このサンプルでは、イージング関数の値を ``Vector3.LerpUnclamped`` に渡している。``Vector3.Lerp`` は割合を 0 から 1 の範囲に制限するが、``Vector3.LerpUnclamped`` は制限しない。行き過ぎてから戻るような、値が 1 を超えるイージング関数を使う場合は ``LerpUnclamped`` を使う必要がある。

AnimationCurve
--------------

イージング関数を数式で書く代わりに、Inspector ウィンドウ上でグラフを描いて指定することもできる。そのためのクラスが ``AnimationCurve`` である。

``AnimationCurve`` 型のフィールドを ``[SerializeField]`` 付きで宣言すると、Inspector ウィンドウにカーブが表示され、クリックするとカーブエディターが開く。カーブエディターでは、キーの追加や移動、接線の調整をマウス操作で行える。スクリプトからは ``Evaluate`` メソッドで、横軸の値に対応する縦軸の値を取得する。

.. literalinclude:: ../examples/CurveMover.cs
   :language: csharp
   :caption: CurveMover.cs

:download:`CurveMover.cs をダウンロード <../examples/CurveMover.cs>`

このカーブエディターは、第 4 章で扱う Animation ウィンドウの Curves 表示と同じ考え方で操作する。Animation Clip も、内部ではプロパティごとに ``AnimationCurve`` を持っている。

コルーチンによる時間制御
------------------------

「0.1 秒ごとに表示を切り替える処理を 10 回繰り返す」のように、時間を空けながら順番に処理を進めたい場合は、コルーチンを使うと簡潔に書ける。

コルーチンは、戻り値の型が ``IEnumerator`` のメソッドとして定義し、``StartCoroutine`` で開始する。``yield return`` の位置で処理を中断し、指定した条件を満たすと中断した位置から再開する。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - yield return に指定する値
     - 再開するタイミング
   * - ``null``
     - 次のフレーム
   * - ``new WaitForSeconds(秒数)``
     - 指定した秒数が経過した後（``Time.timeScale`` の影響を受ける）
   * - ``new WaitForSecondsRealtime(秒数)``
     - 指定した秒数が経過した後（``Time.timeScale`` の影響を受けない）
   * - ``new WaitUntil(条件)``
     - 条件が true になった後

.. literalinclude:: ../examples/CoroutineBlink.cs
   :language: csharp
   :caption: CoroutineBlink.cs

:download:`CoroutineBlink.cs をダウンロード <../examples/CoroutineBlink.cs>`

.. warning::

   コルーチンは、それを開始した GameObject が非アクティブになると停止する。コンポーネントを無効にしただけでは停止しない。途中で止めたい場合は ``StopCoroutine`` を使う。
