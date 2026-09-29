第 6 章 3D 数学の基礎
=====================

ゲームで物を動かしたり向きを変えたりするには、ベクトルや回転の扱い方を知っておく必要があります。この章では、Unity のスクリプトでよく使う数学の考え方を、必要な範囲に絞って説明します。ここで説明する内容は、第 7 章以降のサンプルコードで実際に使います。

ベクトル
--------

**ベクトル** は、大きさと向きを持つ量です。Unity では、3D のベクトルを ``Vector3`` 型、2D のベクトルを ``Vector2`` 型で表します。``Vector3`` は x、y、z の 3 つの値を持ち、位置、移動量、速度、方向などを表すのに使います。

.. code-block:: csharp

   Vector3 position = new Vector3(1f, 2f, 3f);
   Vector3 up = Vector3.up;           // (0, 1, 0)
   Vector3 forward = Vector3.forward; // (0, 0, 1)

ベクトルの足し算と引き算
~~~~~~~~~~~~~~~~~~~~~~~~

ベクトル同士の足し算と引き算は、成分ごとに計算します。

.. math::

   \boldsymbol{a} + \boldsymbol{b} = (a_x + b_x,\ a_y + b_y,\ a_z + b_z)

位置に移動量を足すと、移動後の位置が求まります。また、2 つの位置の差を取ると、一方から他方へ向かうベクトルが求まります。例えば、敵の位置から自分の位置を引くと、自分から敵へ向かうベクトルになります。

.. code-block:: csharp

   Vector3 toEnemy = enemy.position - transform.position;

大きさと正規化
~~~~~~~~~~~~~~

ベクトル :math:`\boldsymbol{v} = (x, y, z)` の大きさ（長さ）\ :math:`|\boldsymbol{v}|` は、次の式で求まります。

.. math::

   |\boldsymbol{v}| = \sqrt{x^2 + y^2 + z^2}

Unity では、``magnitude`` プロパティで大きさを取得できます。2 点間の距離を求めるには、``Vector3.Distance`` を使います。

大きさが 1 のベクトルを **単位ベクトル** と呼びます。ベクトルをその大きさで割り、向きはそのままで大きさを 1 にすることを **正規化** と呼びます。

.. math::

   \hat{\boldsymbol{v}} = \frac{\boldsymbol{v}}{|\boldsymbol{v}|}

Unity では、``normalized`` プロパティで正規化したベクトルを取得できます。向きだけが必要な場合に正規化を使います。例えば、「敵の方向へ秒速 3 m で進む」という処理は、敵へ向かうベクトルを正規化してから速さを掛けて計算します。

.. code-block:: csharp

   Vector3 direction = (enemy.position - transform.position).normalized;
   Vector3 velocity = direction * 3f;

内積
~~~~

2 つのベクトル :math:`\boldsymbol{a}` と :math:`\boldsymbol{b}` の **内積** は、次の式で定義されます。:math:`\theta` は 2 つのベクトルのなす角です。

.. math::

   \boldsymbol{a} \cdot \boldsymbol{b} = a_x b_x + a_y b_y + a_z b_z = |\boldsymbol{a}|\,|\boldsymbol{b}| \cos\theta

内積の結果はベクトルではなく、1 つの数値です。:math:`\boldsymbol{a}` と :math:`\boldsymbol{b}` がどちらも単位ベクトルであれば、内積は :math:`\cos\theta` と等しくなります。そのため、内積を使うと 2 つの向きの関係を調べられます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 単位ベクトル同士の内積
     - 意味
   * - 1
     - 同じ向き
   * - 0 より大きい
     - おおむね同じ向き（なす角が 90° 未満）
   * - 0
     - 直交している（なす角が 90°）
   * - 0 より小さい
     - おおむね逆向き（なす角が 90° より大きい）
   * - -1
     - 正反対の向き

例えば、敵がプレイヤーの前方にいるかどうかは、次のように判定できます。

.. code-block:: csharp

   Vector3 toEnemy = (enemy.position - transform.position).normalized;
   bool isInFront = Vector3.Dot(transform.forward, toEnemy) > 0f;

外積
~~~~

2 つのベクトル :math:`\boldsymbol{a}` と :math:`\boldsymbol{b}` の **外積** は、次の式で定義されるベクトルです。

.. math::

   \boldsymbol{a} \times \boldsymbol{b} = (a_y b_z - a_z b_y,\ a_z b_x - a_x b_z,\ a_x b_y - a_y b_x)

外積の結果は、:math:`\boldsymbol{a}` と :math:`\boldsymbol{b}` の両方に垂直なベクトルになります。その大きさは :math:`|\boldsymbol{a}|\,|\boldsymbol{b}| \sin\theta` で、2 つのベクトルが作る平行四辺形の面積と等しくなります。

外積は、面に垂直な向き（法線）を求めたり、ある向きが別の向きの右側と左側のどちらにあるかを判定したりするのに使います。Unity は左手座標系なので、外積の向きは左手の法則に従います。例えば、``Vector3.Cross(Vector3.up, Vector3.forward)`` は ``Vector3.right`` になります。

回転の表現
----------

オイラー角
~~~~~~~~~~

Inspector ウィンドウの Transform コンポーネントの :guilabel:`Rotation` には、X 軸、Y 軸、Z 軸のまわりの回転角度が表示されます。このように、3 つの軸まわりの回転角度の組で向きを表す方法を **オイラー角** と呼びます。Unity では、Z 軸、X 軸、Y 軸の順に回転を適用します。

オイラー角は人間にとってわかりやすい反面、次のような問題があります。

* 特定の角度（例えば X 軸まわりに 90°）になると、2 つの軸の回転が同じ向きの回転になり、回転の自由度が 1 つ失われます。この現象を **ジンバルロック** と呼びます。
* 同じ向きを表す角度の組が複数あるため、2 つの向きの間をなめらかに補間するのが困難です。

クォータニオン
~~~~~~~~~~~~~~

Unity の内部では、回転を **クォータニオン**\ （四元数）で表しています。スクリプトでは ``Quaternion`` 型を使います。単位ベクトル :math:`\boldsymbol{n}` を軸として角度 :math:`\theta` だけ回転させる回転は、次のクォータニオンで表されます。

.. math::

   q = \left(n_x \sin\frac{\theta}{2},\ n_y \sin\frac{\theta}{2},\ n_z \sin\frac{\theta}{2},\ \cos\frac{\theta}{2}\right)

``Quaternion`` 型の x、y、z、w の 4 つの値は、この式の 4 つの成分に対応します。これらの値を直接操作することはほとんどありません。通常は、次のようなメソッドを使ってクォータニオンを作成します。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - メソッド
     - 機能
   * - ``Quaternion.Euler(x, y, z)``
     - オイラー角からクォータニオンを作成します。
   * - ``Quaternion.AngleAxis(angle, axis)``
     - 軸 ``axis`` のまわりに ``angle`` 度回転させるクォータニオンを作成します。
   * - ``Quaternion.LookRotation(forward)``
     - 前方が ``forward`` の向きになるクォータニオンを作成します。
   * - ``Quaternion.Slerp(a, b, t)``
     - 2 つの回転の間をなめらかに補間します。

クォータニオン同士の掛け算は、回転を続けて適用することを表します。また、クォータニオンとベクトルの掛け算は、ベクトルを回転させることを表します。

.. code-block:: csharp

   // 現在の向きから、さらに Y 軸まわりに 90° 回転させます。
   transform.rotation = transform.rotation * Quaternion.Euler(0f, 90f, 0f);

   // 前方向のベクトルを、Y 軸まわりに 45° 回転させます。
   Vector3 direction = Quaternion.Euler(0f, 45f, 0f) * Vector3.forward;

クォータニオンの掛け算は、掛ける順番によって結果が変わるので注意してください。

線形補間
--------

2 つの値の間の値を求めることを **補間** と呼びます。値 :math:`a` から値 :math:`b` までを、割合 :math:`t`\ （0 から 1）で直線的に補間する **線形補間** は、次の式で表されます。

.. math::

   \mathrm{Lerp}(a, b, t) = a + (b - a)\,t

:math:`t = 0` のとき :math:`a` に、:math:`t = 1` のとき :math:`b` に、:math:`t = 0.5` のときちょうど中間の値になります。Unity では、``Mathf.Lerp``\ （数値）、``Vector3.Lerp``\ （ベクトル）、``Color.Lerp``\ （色）などのメソッドが用意されています。これらのメソッドは、:math:`t` を 0 から 1 の範囲に制限してから計算します。

フレームレートに依存しない処理
------------------------------

ゲームの画面は、1 秒間に何十回も描き直されています。1 回の描画を **フレーム**、1 秒間のフレーム数を **フレームレート**\ （単位は fps）と呼びます。フレームレートは、コンピューターの性能や処理の重さによって変わります。

毎フレーム一定の距離だけ GameObject を動かすと、フレームレートが高いコンピューターほど速く動いてしまいます。そこで、前のフレームからの経過時間 :math:`\Delta t`\ （秒）を使って、移動量を計算します。速度を :math:`\boldsymbol{v}`\ （m/s）とすると、1 フレームでの位置 :math:`\boldsymbol{p}` の変化は次のようになります。

.. math::

   \boldsymbol{p}_{\text{次のフレーム}} = \boldsymbol{p}_{\text{現在}} + \boldsymbol{v}\,\Delta t

Unity では、:math:`\Delta t` を ``Time.deltaTime`` で取得できます。

.. code-block:: csharp

   // 毎秒 2 m の速さで前へ進みます。
   transform.position += transform.forward * 2f * Time.deltaTime;

60 fps では ``Time.deltaTime`` は約 0.0167 秒、30 fps では約 0.0333 秒になります。フレームレートが半分になると 1 フレームあたりの移動量が 2 倍になるため、1 秒あたりの移動量は変わりません。

.. note::

   ``Lerp`` を使って「現在の値を目標の値に少しずつ近づける」処理を書く場合、``Mathf.Lerp(current, target, 0.1f)`` のように :math:`t` に固定の値を使うと、フレームレートによって近づく速さが変わってしまいます。フレームレートに依存しないようにするには、近づく速さを表す係数 :math:`k` を使って、:math:`t = 1 - e^{-k \Delta t}` とします。

   .. code-block:: csharp

      float t = 1f - Mathf.Exp(-k * Time.deltaTime);
      current = Mathf.Lerp(current, target, t);
