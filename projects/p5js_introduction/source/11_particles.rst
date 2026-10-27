ベクトルとオブジェクト指向
==========================

この章では、位置や速度をまとめて扱う ``p5.Vector`` と、JavaScript のクラスを組み合わせて、多数の粒子が動く :term:`パーティクル` を作ります。

p5.Vector
---------

:doc:`07_animation` では、位置と速度を ``x``、``y``、``vx``、``vy`` という別々の変数で扱いました。動かす物体が増えたり、力を扱ったりするようになると、変数が増えてコードが読みにくくなります。

``p5.Vector`` は、x 成分と y 成分をまとめて 1 つの :term:`ベクトル` として扱うクラスです。``createVector()`` で作成します。

.. code-block:: javascript
   :linenos:

   const position = createVector(100, 200);
   const velocity = createVector(3, -2);
   position.add(velocity);       // position は (103, 198) になる
   console.log(position.x, position.y);

主なメソッドを次の表に示します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メソッド
     - 動作
   * - ``v.add(w)``
     - ``v`` に ``w`` を加える。
   * - ``v.sub(w)``
     - ``v`` から ``w`` を引く。
   * - ``v.mult(s)``
     - ``v`` を ``s`` 倍する。
   * - ``v.mag()``
     - ``v`` の大きさ（長さ）を返す。
   * - ``v.normalize()``
     - ``v`` の向きを変えずに、大きさを 1 にする。
   * - ``v.limit(max)``
     - ``v`` の大きさが ``max`` を超えないように制限する。
   * - ``v.heading()``
     - ``v`` の向き（x 軸からの角度）を返す。
   * - ``v.copy()``
     - ``v`` の複製を返す。

``add()`` や ``mult()`` などのメソッドは、新しいベクトルを返すのではなく、``v`` 自身の値を書き換えます。元のベクトルを残したいときは、``v.copy().add(w)`` のように複製してから計算するか、``p5.Vector.add(v, w)`` のように静的メソッドを使います。静的メソッドは、計算結果を新しいベクトルとして返します。

位置・速度・加速度
------------------

ベクトルを使うと、重力などの力を受けて動く物体を簡潔に表現できます。フレームごとに、次の順で値を更新します。

.. math::

   \boldsymbol{v} \leftarrow \boldsymbol{v} + \boldsymbol{a}, \quad
   \boldsymbol{p} \leftarrow \boldsymbol{p} + \boldsymbol{v}

ここで :math:`\boldsymbol{p}` は位置、:math:`\boldsymbol{v}` は速度、:math:`\boldsymbol{a}` は加速度です。重力のように一定の加速度を加え続けると、物体は放物線を描いて落下します。

クラスで粒子を表す
------------------

1 つの粒子が持つデータ（位置、速度、寿命）と処理（更新、描画）を、クラスにまとめます。

.. literalinclude:: ../examples/ch11_particles/sketch.js
   :language: javascript
   :linenos:
   :lines: 7-31
   :lineno-start: 7
   :caption: ch11_particles/sketch.js（Particle クラス）

``this.life`` は粒子の残りの寿命で、フレームごとに 3 ずつ減ります。この値を透明度にも使っているため（24 行目）、粒子は時間とともに薄くなって消えていきます。

配列で多数の粒子を管理する
--------------------------

粒子は配列に入れて管理します。毎フレーム新しい粒子を追加し、寿命が尽きた粒子を配列から削除します。

配列から要素を削除するには ``splice(添字, 個数)`` を使います。ループの途中で要素を削除すると、それより後ろの要素の添字が 1 つずつ前にずれます。前から順に処理していると、削除した要素の次の要素が処理されずに飛ばされてしまいます。そのため、配列の後ろから前に向かって処理します。

サンプル
--------

噴水のように粒子が噴き出すサンプルです。マウスボタンを押している間は、マウスの位置から粒子が出ます。

.. literalinclude:: ../examples/ch11_particles/sketch.js
   :language: javascript
   :linenos:
   :caption: ch11_particles/sketch.js

* `実行する <examples/ch11_particles/index.html>`__
* ダウンロード：:download:`index.html <../examples/ch11_particles/index.html>`、:download:`sketch.js <../examples/ch11_particles/sketch.js>`

5 行目の ``gravity`` は、宣言だけを関数の外で行い、値は ``setup()`` の中で代入しています（35 行目）。``createVector()`` は p5.js の初期化が終わってから使える関数であるため、関数の外では呼べないからです。

左上に表示される粒子の数は、追加と削除がつり合うと一定になります。寿命を 255 から 3 ずつ減らしているため、1 つの粒子は 85 フレームで消えます。毎フレーム 3 個ずつ追加するので、画面上の粒子はおよそ :math:`85 \times 3 = 255` 個で安定します。
