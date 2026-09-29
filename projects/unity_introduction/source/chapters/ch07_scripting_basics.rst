第 7 章 C# スクリプトの基礎
===========================

Unity では、GameObject の動作を C# のスクリプトで記述します。この章では、スクリプトの作成から、GameObject を動かしたり生成したりするまでの基本を説明します。

この章のサンプルコードは、``examples/chapter07`` フォルダーにあります。

最初のスクリプト
----------------

スクリプトの作成
~~~~~~~~~~~~~~~~

#. Project ウィンドウで ``Assets`` フォルダーを右クリックし、:menuselection:`Create --> Folder` で ``Scripts`` フォルダーを作成します。
#. ``Scripts`` フォルダーを右クリックし、:menuselection:`Create --> Scripting --> MonoBehaviour Script` を選びます。
#. スクリプトの名前を ``HelloUnity`` にして、:kbd:`Enter` キーを押します。
#. 作成したスクリプトをダブルクリックして、コードエディターで開きます。

スクリプトの内容を次のように書き換えて保存します。

.. literalinclude:: ../../examples/chapter07/HelloUnity.cs
   :caption: HelloUnity.cs
   :linenos:

:download:`HelloUnity.cs をダウンロード <../../examples/chapter07/HelloUnity.cs>`

.. important::

   スクリプトのファイル名（``.cs`` を除いた部分）とクラス名は、必ず同じにしてください。異なっていると、スクリプトを GameObject に付けられません。スクリプトの名前を後から変えるときは、ファイル名とクラス名の両方を変更します。

スクリプトの実行
~~~~~~~~~~~~~~~~

スクリプトはコンポーネントの一種なので、GameObject に付けて（アタッチして）初めて動作します。

#. Unity Editor に戻り、スクリプトが自動的にコンパイルされるのを待ちます。
#. :menuselection:`GameObject --> Create Empty` で空の GameObject を作成します。
#. Project ウィンドウの ``HelloUnity`` スクリプトを、Hierarchy ウィンドウの GameObject にドラッグ＆ドロップします。Inspector ウィンドウに :guilabel:`Hello Unity (Script)` コンポーネントが追加されます。
#. :guilabel:`Play` ボタンで再生すると、Console ウィンドウに ``Hello, Unity!`` と表示されます。

スクリプトに文法の誤りがあると、Console ウィンドウに赤いエラーメッセージが表示され、再生できません。エラーメッセージをダブルクリックすると、コードエディターでエラーの箇所が開きます。

コードの読み方
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - コード
     - 意味
   * - ``using UnityEngine;``
     - Unity の基本的なクラスが含まれる名前空間 ``UnityEngine`` を使うことを宣言します。
   * - ``namespace UnityIntroduction.Chapter07``
     - このクラスが属する名前空間です。他のクラスと名前が衝突するのを防ぎます。省略することもできます。
   * - ``/// <summary>`` など
     - ドキュメントコメントです。コードエディターでクラスにマウスカーソルを重ねると、この説明が表示されます。
   * - ``public class HelloUnity : MonoBehaviour``
     - ``MonoBehaviour`` を継承した ``HelloUnity`` クラスを定義します。GameObject に付けるスクリプトは、``MonoBehaviour`` を継承する必要があります。
   * - ``private void Start()``
     - 再生を開始したときに Unity から呼ばれるメソッドです。
   * - ``Debug.Log("Hello, Unity!");``
     - Console ウィンドウにメッセージを表示します。

イベント関数
------------

``Start`` のように、特定のタイミングで Unity から自動的に呼ばれるメソッドを **イベント関数** と呼びます。イベント関数は、決められた名前で ``MonoBehaviour`` を継承したクラスに定義するだけで呼ばれるようになります。``override`` などの指定は不要です。

主なイベント関数と呼ばれるタイミングは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - イベント関数
     - 呼ばれるタイミングと主な用途
   * - ``Awake``
     - GameObject が読み込まれた直後に 1 回だけ呼ばれます。GameObject が無効な状態で読み込まれた場合は、有効になったときに呼ばれます。自分自身のコンポーネントの取得など、他の GameObject に依存しない初期化に使います。
   * - ``OnEnable``
     - コンポーネントが有効になるたびに呼ばれます。イベントの購読の開始（:doc:`ch08_scripting_advanced` を参照）などに使います。
   * - ``Start``
     - 最初の ``Update`` の直前に 1 回だけ呼ばれます。他の GameObject を参照する初期化に使います。
   * - ``FixedUpdate``
     - 物理演算の更新に合わせて一定の間隔（初期設定では 0.02 秒）で呼ばれます。``Rigidbody`` に力を加える処理などに使います。
   * - ``Update``
     - 毎フレーム 1 回呼ばれます。入力の読み取りや、GameObject の移動など、ほとんどの処理はここに書きます。
   * - ``LateUpdate``
     - すべての ``Update`` が呼ばれた後に、毎フレーム 1 回呼ばれます。カメラの追従など、他の GameObject の移動が終わった後に行う処理に使います。
   * - ``OnDisable``
     - コンポーネントが無効になるたびに呼ばれます。イベントの購読の解除などに使います。
   * - ``OnDestroy``
     - GameObject やコンポーネントが破棄される直前に呼ばれます。

シーンを読み込んだときは、シーン内のすべての GameObject の ``Awake`` と ``OnEnable`` が呼ばれた後に、各 GameObject の ``Start`` が呼ばれます。そのため、``Awake`` で自分の初期化を済ませ、``Start`` で他の GameObject を参照するようにすると、初期化の順番による問題を避けられます。

``FixedUpdate`` は、フレームレートとは関係なく一定の間隔で呼ばれます。フレームレートが高いときは 1 フレームの間に 1 回も呼ばれないことがあり、低いときは 1 フレームの間に複数回呼ばれることがあります。

次のスクリプトを GameObject に付けて再生すると、イベント関数が呼ばれる順番を確認できます。再生を終えると、``OnDisable`` と ``OnDestroy`` も表示されます。

.. literalinclude:: ../../examples/chapter07/LifecycleLogger.cs
   :caption: LifecycleLogger.cs
   :linenos:

:download:`LifecycleLogger.cs をダウンロード <../../examples/chapter07/LifecycleLogger.cs>`

GameObject を動かす
-------------------

次のスクリプトは、GameObject を一定の速度で動かします。

.. literalinclude:: ../../examples/chapter07/Mover.cs
   :caption: Mover.cs
   :linenos:

:download:`Mover.cs をダウンロード <../../examples/chapter07/Mover.cs>`

``transform`` は、スクリプトを付けた GameObject の Transform コンポーネントを表すプロパティです。``transform.position`` に値を足すことで、GameObject を移動させています。``Time.deltaTime`` を掛ける理由は、:doc:`ch06_math` の「フレームレートに依存しない処理」で説明したとおりです。

Inspector ウィンドウへの公開
----------------------------

``Mover`` スクリプトを GameObject に付けると、Inspector ウィンドウに :guilabel:`Velocity` という項目が表示されます。これは、``_velocity`` フィールドに ``[SerializeField]`` 属性を付けているためです。``[SerializeField]`` のように、``[ ]`` で囲んでクラスやフィールド、メソッドに付ける目印を **属性** と呼びます。Inspector ウィンドウで値を変えると、スクリプトを書き換えずに動作を調整できます。

フィールドを Inspector ウィンドウに表示する方法は 2 つあります。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 書き方
     - 特徴
   * - ``[SerializeField] private float _speed;``
     - Inspector ウィンドウに表示されますが、他のクラスからは変更できません。
   * - ``public float Speed;``
     - Inspector ウィンドウに表示され、他のクラスからも自由に変更できます。

意図しない場所から値を変更されるのを防ぐため、本資料では ``[SerializeField]`` と ``private`` を組み合わせる書き方を使います。なお、Inspector ウィンドウに表示される名前は、フィールド名の先頭の ``_`` が取り除かれ、単語の区切りで空白が入り、先頭が大文字になります。例えば、``_moveSpeed`` は :guilabel:`Move Speed` と表示されます。

.. warning::

   Inspector ウィンドウで設定した値は、シーンや Prefab に保存され、スクリプトに書いた初期値よりも優先されます。スクリプトの初期値を後から変更しても、既に GameObject に付けてあるコンポーネントの値は変わりません。初期値に戻したい場合は、Inspector ウィンドウのコンポーネント名の右にあるメニュー（⋮）から :guilabel:`Reset` を選びます。

他のコンポーネントを使う
------------------------

同じ GameObject に付いている他のコンポーネントを使うには、``GetComponent`` メソッドで取得します。次のスクリプトは、Renderer コンポーネントを取得して、表示の色を変化させます。

.. literalinclude:: ../../examples/chapter07/ColorChanger.cs
   :caption: ColorChanger.cs
   :linenos:

:download:`ColorChanger.cs をダウンロード <../../examples/chapter07/ColorChanger.cs>`

``GetComponent`` は、コンポーネントを探すための処理を伴います。毎フレーム呼ぶのではなく、この例のように ``Awake`` で 1 回だけ取得してフィールドに保持しておくのが一般的です。

クラスに付けた ``[RequireComponent(typeof(MeshRenderer))]`` は、このスクリプトが Mesh Renderer コンポーネントを必要とすることを表します。このスクリプトを GameObject に付けると、Mesh Renderer コンポーネントがない場合は自動的に追加されます。また、Mesh Renderer コンポーネントを誤って削除することも防げます。ただし、``Renderer`` や ``Collider`` のような抽象クラス（それ自体はコンポーネントとして追加できないクラス）を指定した場合は、自動的には追加されません。その場合は、先に Mesh Renderer や Box Collider などの具体的なコンポーネントを付けておきます。

別の GameObject のコンポーネントを使う場合は、``[SerializeField]`` を付けたフィールドを用意し、Inspector ウィンドウで対象をドラッグ＆ドロップして設定するのが最も簡単で確実な方法です。

.. code-block:: csharp

   [SerializeField]
   private Transform _target;  // Inspector ウィンドウで追従する対象を設定します。

GameObject の生成と破棄
-----------------------

ゲームの実行中に GameObject を生成するには ``Instantiate`` メソッドを、破棄するには ``Destroy`` メソッドを使います。次のスクリプトは、Inspector ウィンドウで指定した Prefab を一定の間隔で生成し、一定時間後に破棄します。

.. literalinclude:: ../../examples/chapter07/Spawner.cs
   :caption: Spawner.cs
   :linenos:

:download:`Spawner.cs をダウンロード <../../examples/chapter07/Spawner.cs>`

使い方は次のとおりです。

#. :menuselection:`GameObject --> 3D Object --> Sphere` で球を作成し、Project ウィンドウにドラッグ＆ドロップして Prefab にします。シーンに残った球は削除します。
#. 空の GameObject を作成し、``Spawner`` スクリプトを付けます。
#. Inspector ウィンドウの :guilabel:`Prefab` に、作成した球の Prefab をドラッグ＆ドロップします。
#. 再生すると、1 秒ごとに球が現れ、3 秒後に消えます。

``Instantiate`` は、元になる GameObject（ここでは Prefab）を複製し、指定した位置と回転で配置します。``Destroy`` は、第 2 引数に秒数を指定すると、その時間が経過した後に GameObject を破棄します。

``Start`` では、Prefab が設定されていない場合に警告を表示し、``enabled = false`` でこのコンポーネントを無効にしています。無効にしたコンポーネントの ``Update`` は呼ばれなくなります。

ログの出力
----------

``Debug`` クラスには、Console ウィンドウにメッセージを表示するメソッドがあります。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - メソッド
     - 用途
   * - ``Debug.Log``
     - 通常のメッセージを表示します。
   * - ``Debug.LogWarning``
     - 警告を黄色のアイコンで表示します。
   * - ``Debug.LogError``
     - エラーを赤色のアイコンで表示します。

第 2 引数に ``this`` などのオブジェクトを渡すと、Console ウィンドウでメッセージをクリックしたときに、そのオブジェクトが Hierarchy ウィンドウで強調表示されます。``Spawner`` の ``Debug.LogWarning("Prefab が設定されていません。", this)`` がその例です。どの GameObject がメッセージを出したのかを調べるのに役立ちます。

``Debug.Log`` はビルドしたアプリケーションでも実行されるため、毎フレーム大量に呼ぶと処理が重くなります。調査が終わったログは削除してください。
