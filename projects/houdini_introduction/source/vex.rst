VEX 入門
========

VEX は、Houdini の中でジオメトリやボリュームを処理するための言語である。文法は C 言語に似ている。VEX のコードは、ポイントやプリミティブの 1 個 1 個に対して並列に実行される。そのため、大量の要素を高速に処理できる。この章では、Attribute Wrangle ノードで VEX を使う方法を説明する。

Attribute Wrangle
-----------------

Attribute Wrangle ノードは、:guilabel:`VEXpression` パラメーターに書いた VEX のコードを、入力のジオメトリの要素ごとに実行するノードである。コードを実行する要素の種類は、:guilabel:`Run Over` パラメーターで選ぶ。

.. list-table:: Run Over の選択肢
   :header-rows: 1
   :widths: 30 70

   * - 選択肢
     - コードを実行する回数と単位
   * - :guilabel:`Points`\ （既定）
     - ポイントごとに 1 回ずつ
   * - :guilabel:`Primitives`
     - プリミティブごとに 1 回ずつ
   * - :guilabel:`Vertices`
     - バーテックスごとに 1 回ずつ
   * - :guilabel:`Detail (only once)`
     - ジオメトリ全体に対して 1 回だけ。入力が無くても実行される。
   * - :guilabel:`Numbers`
     - 指定した回数

例えば、Grid ノードの後ろに Attribute Wrangle ノードをつなぎ、:guilabel:`VEXpression` に次の 1 行を書く。

.. code-block:: vex
   :linenos:

   @P.y = sin(@P.x * 2.0) * 0.3;

:guilabel:`Run Over` が :guilabel:`Points` なので、この行はグリッドの全てのポイントに対して 1 回ずつ実行される。``@P`` は処理中のポイントの位置であり、その y 成分を x 座標の正弦波にしている。結果として、グリッドが波打つ。Python で書くなら次のループに相当するが、VEX ではループを書かない。ループは Houdini が並列に実行する。

.. code-block:: python
   :linenos:

   for point in geo.points():
       pos = point.position()
       pos[1] = math.sin(pos[0] * 2.0) * 0.3
       point.setPosition(pos)

基本の文法
----------

VEX の文法は C 言語に近い。

* 文の終わりにはセミコロン（``;``）が必要である。
* コメントは ``//`` から行末まで、または ``/*`` と ``*/`` の間である。
* 変数は、型を付けて宣言する。``int count = 10;`` のように書く。
* ``if``、``for``、``while``、``foreach`` などの制御文を使える。
* 三角関数の角度はラジアンで指定する。

.. list-table:: VEX の主な型
   :header-rows: 1
   :widths: 25 75

   * - 型
     - 内容
   * - ``int``
     - 整数
   * - ``float``
     - 浮動小数点数
   * - ``vector2``、``vector``、``vector4``
     - 2 個、3 個、4 個の浮動小数点数。``vector`` は位置、方向、色に使う。
   * - ``matrix3``、``matrix``
     - 3 x 3、4 x 4 の行列
   * - ``string``
     - 文字列
   * - ``dict``
     - 辞書
   * - 配列
     - ``int[]``、``vector[]`` のように、型の後ろに ``[]`` を付ける。

ベクトルの成分は、``v.x``、``v.y``、``v.z`` で読み書きする。色として使うときは ``v.r``、``v.g``、``v.b`` とも書ける。

ベクトルを作るには 2 つの書き方がある。

.. code-block:: vex
   :linenos:

   vector a = {1, 0, 0};          // 波かっこ: 定数だけ書ける
   float h = 2.0;
   vector b = set(0, h, 0);       // set(): 変数や式を書ける
   // vector c = {0, h, 0};       // エラーになる

波かっこ（``{}``）の中には定数しか書けない。変数や式を含むベクトルは ``set()`` 関数で作る。これは間違えやすい点である。

アトリビュートの読み書き
------------------------

``@`` の後にアトリビュートの名前を書くと、処理中の要素のアトリビュートを読み書きできる。存在しないアトリビュートに書き込むと、新しく作られる。

``@`` の前に 1 文字を付けて、アトリビュートの型を指定する。

.. list-table:: アトリビュートの型の指定
   :header-rows: 1
   :widths: 25 25 50

   * - 書き方
     - 型
     - 例
   * - ``f@name``
     - ``float``
     - ``f@height = 1.5;``
   * - ``i@name``
     - ``int``
     - ``i@floors = 3;``
   * - ``v@name``
     - ``vector``
     - ``v@scale = {1, 2, 1};``
   * - ``p@name``
     - ``vector4``
     - ``p@orient = {0, 0, 0, 1};``
   * - ``s@name``
     - ``string``
     - ``s@name = "roof";``
   * - ``u@name``
     - ``vector2``
     - ``u@st = {0.5, 0.5};``
   * - ``4@name``
     - ``matrix``
     - ``4@xform = ident();``

型を省略すると ``float`` とみなされる。ただし、``P``、``N``、``Cd``、``v``、``uv``、``scale`` などの決まったアトリビュートは、型を省略してもベクトルとして扱われる。``id`` は整数、``name`` は文字列として扱われる。自分で作るアトリビュートには、型を明示する習慣を付けるとよい。``@height`` と書いたつもりで ``height`` をベクトルとして作ってしまう、といった間違いを防げる。

アトリビュートのほかに、次の変数を使える。

.. list-table:: よく使う組み込みの変数
   :header-rows: 1
   :widths: 30 70

   * - 変数
     - 意味
   * - ``@ptnum``
     - 処理中のポイントの番号
   * - ``@numpt``
     - ポイントの総数
   * - ``@primnum``
     - 処理中のプリミティブの番号
   * - ``@numprim``
     - プリミティブの総数
   * - ``@Time``
     - 現在の時刻（秒）
   * - ``@Frame``
     - 現在のフレーム番号

パラメーターを読む
------------------

コードの中の定数を後から調整できるように、パラメーターにしておくと便利である。VEX では ``chf("名前")``\ （浮動小数点数）、``chi("名前")``\ （整数）、``chv("名前")``\ （ベクトル）、``chramp("名前", 位置)``\ （ランプ）で、ノードのパラメーターを読める。

``chf("amplitude")`` のように書いた後、:guilabel:`VEXpression` の右にあるボタン（ツールチップは「Creates spare parameters for each unique call of ch()」）を押すと、コードの中の ``ch`` 系の関数の呼び出しに対応するパラメーターが、ノードに自動的に追加される。このように後から追加したパラメーターを、スペアパラメーターと呼ぶ。

よく使う関数
------------

VEX には多くの関数が用意されている。よく使うものを挙げる。全ての関数は、ヘルプの VEX の関数の一覧で調べられる。

.. list-table:: VEX でよく使う関数
   :header-rows: 1
   :widths: 35 65

   * - 関数
     - 機能
   * - ``fit(v, a, b, c, d)``、``fit01(v, c, d)``
     - 値 ``v`` を範囲 a から b（``fit01`` では 0 から 1）から、範囲 c から d に換算する。
   * - ``lerp(a, b, t)``
     - a と b を t の割合で混ぜる（線形補間）。
   * - ``clamp(v, a, b)``
     - 値を a から b の範囲に収める。
   * - ``rand(seed)``
     - 0 から 1 の乱数。同じ ``seed`` には同じ値を返す。
   * - ``noise(pos)``
     - 位置に応じて滑らかに変化する乱数（ノイズ）。
   * - ``sin()``、``cos()``
     - 三角関数（ラジアン）。
   * - ``length(v)``、``normalize(v)``
     - ベクトルの長さ、長さ 1 にしたベクトル。
   * - ``distance(a, b)``
     - 2 点の距離。
   * - ``dot(a, b)``、``cross(a, b)``
     - 内積、外積。
   * - ``point(input, "名前", ptnum)``
     - 入力のジオメトリの、指定したポイントのアトリビュートを読む。
   * - ``nearpoint(input, pos)``
     - 位置 ``pos`` に最も近いポイントの番号を返す。
   * - ``addpoint(0, pos)``
     - ポイントを追加し、その番号を返す。
   * - ``addprim(0, "poly")``、``addvertex(0, prim, pt)``
     - プリミティブを追加する。プリミティブにポイントをつなぐ。
   * - ``removepoint(0, ptnum)``、``removeprim(0, primnum, 1)``
     - ポイント、プリミティブを削除する。
   * - ``setpointattrib(0, "名前", ptnum, 値)``
     - 指定したポイントのアトリビュートを書く。

関数の最初の引数の数字（``input``）は、ノードの入力の番号である。0 が 1 番目の入力、1 が 2 番目の入力を表す。``addpoint`` などのジオメトリを変更する関数の 0 は、このノードが出力するジオメトリを表す。

入力のジオメトリと出力のジオメトリ
----------------------------------

VEX のコードは、全ての要素で同時に（並列に）実行される。そのため、コードの中では次の 2 つを区別する必要がある。

* ``point(0, "P", n)`` のような関数が読むのは、ノードに入力された（変更される前の）ジオメトリである。他の要素がコードの中で書き換えた値は読めない。
* ``@P = ...`` や ``setpointattrib()`` で書いた値と、``addpoint()`` で追加したポイントは、全ての要素の処理が終わった後で出力のジオメトリに反映される。

この仕組みにより、要素の処理の順序を気にせずにコードを書ける。逆に、「隣のポイントを先に動かし、その結果を使って自分を動かす」ような逐次的な処理は、1 個の Wrangle では書けない。その場合は Wrangle を 2 個に分けるか、:guilabel:`Detail (only once)` で全ての要素をループで処理する。

作例
----

サンプルコードの ``build_vex_examples.py`` は、``/obj/vex_examples`` の中に次の 4 つの例を作る。VEX のコードは ``examples/vex`` ディレクトリにあり、Attribute Wrangle の :guilabel:`VEXpression` にそのまま貼り付けて使える。各コードの ``ch`` 系の関数が読むパラメーターは、前述のボタンで作る。スクリプトで作った場合は、スペアパラメーターも作られる。

.. graphviz::
   :caption: VEX の作例のネットワーク
   :name: fig-vex-network

   digraph vex {
     node [shape=box, style="rounded,filled", fillcolor="#d4e8f7", fontsize=11];
     grid [label="grid（Grid）"];
     wave [label="wave\n（Attribute Wrangle）"];
     sphere [label="sphere（Sphere）"];
     normal [label="normal（Normal）"];
     noise [label="noise_displace\n（Attribute Wrangle）"];
     spiral [label="spiral\n（Attribute Wrangle）"];
     nearest [label="nearest_color\n（Attribute Wrangle）"];
     o1 [label="OUT_wave", fillcolor="#fff3b0"];
     o2 [label="OUT_noise", fillcolor="#fff3b0"];
     o3 [label="OUT_spiral", fillcolor="#fff3b0"];
     o4 [label="OUT_nearest", fillcolor="#fff3b0"];
     grid -> wave -> o1;
     sphere -> normal -> noise -> o2;
     spiral -> o3;
     grid -> nearest; spiral -> nearest;
     nearest -> o4;
   }

例 1: 波打つグリッド
^^^^^^^^^^^^^^^^^^^^

:guilabel:`Run Over` は :guilabel:`Points` である。``@Time`` を使っているので、再生すると波が流れる。

.. literalinclude:: ../examples/vex/wave.vex
   :language: vex
   :linenos:

例 2: でこぼこの球
^^^^^^^^^^^^^^^^^^

:guilabel:`Run Over` は :guilabel:`Points` である。法線 ``@N`` の向きに、ノイズの値だけポイントを動かす。入力の球には、Normal ノードで法線を付けておく。

.. literalinclude:: ../examples/vex/noise_displace.vex
   :language: vex
   :linenos:

例 3: らせんを描く
^^^^^^^^^^^^^^^^^^

:guilabel:`Run Over` は :guilabel:`Detail (only once)` で、入力は無い。``addprim`` でポリライン（折れ線）のプリミティブを 1 個作り、``for`` ループで作ったポイントを ``addvertex`` で順につないでいく。``PI`` は円周率を表す定数である。

.. literalinclude:: ../examples/vex/spiral.vex
   :language: vex
   :linenos:

例 4: 最も近いポイントまでの距離で色を付ける
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:guilabel:`Run Over` は :guilabel:`Points` である。1 番目の入力にグリッドを、2 番目の入力に例 3 のらせんをつなぐ。グリッドの各ポイントについて、らせんの最も近いポイントを ``nearpoint(1, @P)`` で探し、その距離で色を決める。らせんの真下が赤く、離れるほど青くなる。

.. literalinclude:: ../examples/vex/nearest_color.vex
   :language: vex
   :linenos:

VEX と Python の速さ
--------------------

VEX は、コンパイルされてから、CPU の複数のコアで並列に実行される。Python の Python SOP（:doc:`python`）でも同じ処理を書けるが、ポイントを 1 個ずつ順に処理するため、ずっと遅い。本資料の環境（16 スレッドの CPU）で、25 万個のポイントを持つグリッドに本章の最初の例と同じ波の計算をしたところ、Attribute Wrangle は約 2 ミリ秒、Python SOP は約 1.8 秒かかった。

要素ごとの計算は VEX で書き、Python はネットワークの操作やファイルの入出力に使うのが基本である。

VOP
---

VOP は、VEX のプログラムをノードで組み立てる仕組みである。Attribute VOP ノードの中で、``sin`` や ``noise`` などの関数を表すノードをつないで処理を作ると、Houdini がそれを VEX のコードに変換して実行する。コードを書くか、ノードをつなぐかの違いで、できることはほぼ同じである。マテリアル（:doc:`rendering`）も VOP のネットワークで定義する。
