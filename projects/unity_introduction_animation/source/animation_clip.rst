Animation Clip を作る
=====================

この章では、Animation ウィンドウを使って Animation Clip を作成する方法を説明する。例として、Cube を回転させながら上下に動かす Animation Clip を作成する。

Animation ウィンドウの画面構成
------------------------------

Animation ウィンドウは、メニューの Window > Animation > Animation で開く。Hierarchy ウィンドウで GameObject を選択すると、その GameObject のアニメーションが Animation ウィンドウに表示される。

Animation ウィンドウは、主に次の領域で構成される。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 領域
     - 内容
   * - ツールバー（左上）
     - プレビュー、録画、再生などのボタンと、編集する Animation Clip の選択欄がある。
   * - プロパティ一覧（左側）
     - アニメーションさせるプロパティの一覧。Add Property ボタンでプロパティを追加する。
   * - タイムライン（右側）
     - 横軸が時間を表す。各プロパティのキーフレームが表示され、上部の時間表示をクリックすると再生位置（再生ヘッド）が移動する。
   * - 表示の切り替え（左下）
     - Dopesheet 表示と Curves 表示を切り替える。

Animation Clip の作成
---------------------

Animation Clip を作成する手順は次のとおりである。

#. Hierarchy ウィンドウで Cube を選択する。
#. Animation ウィンドウに表示される Create ボタンをクリックする。
#. 保存先とファイル名（例: CubeFloat.anim）を指定して保存する。

選択した GameObject に Animator コンポーネントが無い場合、この操作によって Animator コンポーネントが自動的に追加される。同時に、GameObject と同じ名前の Animator Controller が作成され、作成した Animation Clip が最初に再生されるステートとして登録される。そのため、この時点で再生すると Animation Clip が再生される。

キーフレームの追加
------------------

アニメーションは、ある時刻におけるプロパティの値（キーフレーム）を複数指定し、その間を補間することで作られる。キーフレームは Animation ウィンドウでひし形の印として表示される。

キーフレームを追加する方法は 2 つある。

Add Property ボタンから追加する方法
   Add Property ボタンをクリックし、アニメーションさせるプロパティ（例: Transform > Position）を選択する。先頭と末尾にキーフレームが自動的に追加されるため、再生ヘッドを移動してから、プロパティ一覧の値を直接編集する。

録画モードで追加する方法
   ツールバーの録画ボタン（赤い丸）をクリックすると録画モードになり、タイムラインが赤く表示される。この状態で再生ヘッドを移動し、Scene ビューや Inspector ウィンドウで GameObject を操作すると、その時刻にキーフレームが追加される。

例として、録画モードで次のキーフレームを追加する。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 時刻（秒）
     - Position の Y
     - Rotation の Y
   * - 0
     - 0
     - 0
   * - 1
     - 1
     - 180
   * - 2
     - 0
     - 360

追加し終えたら、録画ボタンを再度クリックして録画モードを終了する。

.. warning::

   録画モードのまま GameObject を操作すると、意図しないキーフレームが追加される。キーフレームの追加が終わったら、必ず録画モードを終了する。

Dopesheet 表示と Curves 表示
----------------------------

Animation ウィンドウには 2 種類の表示方法がある。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 表示
     - 用途
   * - Dopesheet
     - キーフレームの時刻だけを表示する。キーフレームの追加、削除、時刻の移動など、タイミングの調整に向いている。
   * - Curves
     - 横軸を時間、縦軸をプロパティの値としたカーブを表示する。キーフレーム間の補間の仕方（動きの緩急）の調整に向いている。

Curves 表示で表示されるカーブは、第 3 章で扱った ``AnimationCurve`` と同じものである。キーフレームの間がどのような形で補間されるかは、次に説明する接線で決まる。

接線と補間方法
--------------

Curves 表示でキーフレームを右クリックすると、そのキーフレームの接線（Tangent）の種類を変更できる。接線はキーフレームを通過するときのカーブの傾きを表し、動きの緩急を決める。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 種類
     - 内容
   * - Clamped Auto
     - 既定の設定。カーブが滑らかになるように接線を自動で決める。キーフレームの値を超えて行き過ぎることがない。
   * - Auto
     - 接線を自動で決める。値の行き過ぎを制限しない。
   * - Free Smooth
     - ハンドルをドラッグして接線を自由に決める。左右の接線は一直線に保たれる。
   * - Flat
     - 接線を水平にする。キーフレームの位置で動きが一瞬止まる。
   * - Broken
     - 左右の接線を別々に設定できるようにする。

Left Tangent、Right Tangent、Both Tangents のメニューでは、キーフレームの左側、右側、または両側の接線を次のように設定できる。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 種類
     - 内容
   * - Free
     - ハンドルで接線を自由に決める。
   * - Linear
     - 隣のキーフレームへ直線で補間する。
   * - Constant
     - 次のキーフレームまで値を変えず、次のキーフレームで値が切り替わる。点滅やスプライトの切り替えなど、段階的に値を変えたい場合に使う。
   * - Weighted
     - 接線のハンドルの長さも変更できるようにし、カーブの曲がり方をより細かく調整する。

アニメーションできるプロパティ
------------------------------

Animation Clip では、Transform 以外にも多くのプロパティをアニメーションできる。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 対象
     - 例
   * - Transform
     - Position、Rotation、Scale
   * - GameObject
     - アクティブ状態（Is Active）
   * - コンポーネント
     - 有効・無効の切り替え（Enabled）、Light の Intensity や Color、Sprite Renderer の Sprite
   * - マテリアル
     - Renderer が使用しているマテリアルの色や数値のプロパティ
   * - 自作スクリプト
     - ``[SerializeField]`` 付き、または public の float、int、bool などのフィールド

子の GameObject のプロパティもアニメーションできる。このとき Animation Clip には、Animator コンポーネントを持つ GameObject から見た子の GameObject のパス（名前の階層）が記録される。

.. warning::

   Animation Clip は GameObject を名前のパスで特定する。アニメーションさせている子の GameObject の名前を変更したり、階層を移動したりすると、プロパティ一覧に黄色で「(Missing!)」と表示され、そのプロパティは再生されなくなる。

ループの設定
------------

Project ウィンドウで Animation Clip を選択すると、Inspector ウィンドウにループに関する設定が表示される。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 内容
   * - Loop Time
     - 有効にすると、Animation Clip の最後まで再生した後、先頭に戻って繰り返し再生する。
   * - Loop Pose
     - 有効にすると、Animation Clip の先頭と末尾の姿勢が滑らかにつながるように補正する。人型キャラクターの歩行モーションなどで使う。
   * - Cycle Offset
     - ループの開始位置をずらす。0 から 1 の割合で指定する。

一度だけ再生したい動き（扉が開くなど）では Loop Time を無効にする。Loop Time が無効な Animation Clip は、最後まで再生すると最後の姿勢のまま止まる。

FBX などのモデルファイルに含まれる Animation Clip の場合、同様の設定はモデルファイルのインポート設定の Animation タブで行う。詳しくは第 7 章で説明する。

Animation Event
---------------

Animation Event は、Animation Clip の指定した時刻に、スクリプトのメソッドを呼び出す仕組みである。足が地面に着いたときの足音、攻撃が当たる瞬間の当たり判定、エフェクトの発生など、モーションと同期させたい処理に使う。

Animation Event を追加する手順は次のとおりである。

#. Animation ウィンドウで、イベントを発生させたい時刻に再生ヘッドを移動する。
#. ツールバーの Add Event ボタンをクリックする。時間表示の下に、イベントを表す印が追加される。
#. 追加された印を選択し、Inspector ウィンドウの Function で呼び出すメソッドを選択する。必要に応じて引数の値を入力する。

呼び出せるメソッドには次の条件がある。

* Animator コンポーネントと同じ GameObject に追加されたスクリプトのメソッドであること。
* 引数が無いか、引数が 1 つで、その型が float、int、string、Object（UnityEngine.Object）、AnimationEvent のいずれかであること。

次のサンプルは、Animation Event から呼び出され、足音を再生する。

.. literalinclude:: ../examples/FootstepEvent.cs
   :language: csharp
   :caption: FootstepEvent.cs

:download:`FootstepEvent.cs をダウンロード <../examples/FootstepEvent.cs>`

.. note::

   第 5 章で扱う Blend Tree で複数の Animation Clip をブレンドしている場合、ブレンド中のすべての Animation Clip の Animation Event が呼び出される。たとえば歩行と走行をブレンドしていると、足音が二重に鳴ることがある。これを避けるには、引数を AnimationEvent 型にし、``animatorClipInfo.weight`` プロパティでその Animation Clip のブレンドの重みを確認して、重みが小さいイベントを無視する。
