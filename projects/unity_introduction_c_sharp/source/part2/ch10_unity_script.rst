################################################################
第 10 章 Unity スクリプトの基本
################################################################

第 2 部では、Unity でスクリプトを書くために必要な知識を学びます。この章では、Unity のシーンを構成する GameObject とコンポーネントの関係と、スクリプトがコンポーネントとして動く仕組みを説明します。

GameObject とコンポーネント
================================================================

Unity のシーンに置かれるものは、キャラクター、地面、カメラ、ライトなど、すべて GameObject です。GameObject そのものは、名前と Transform（位置など）を持つだけの入れ物にすぎません。GameObject にさまざまな機能を与えるのが、コンポーネントです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - コンポーネント
     - 機能
   * - Transform
     - 位置、回転、拡大縮小を管理します。すべての GameObject が必ず 1 つ持っています。
   * - Mesh Filter と Mesh Renderer
     - 形状（メッシュ）を持ち、画面に描画します。
   * - Collider（Box Collider など）
     - 衝突判定のための形状を持ちます（第 16 章）。
   * - Rigidbody
     - 重力や力による動きを、物理演算で計算します（第 16 章）。
   * - Camera
     - シーンを撮影し、画面に表示します。
   * - スクリプト
     - 自分で書いた C# のクラスです。

たとえば、Hierarchy ウィンドウで右クリックして 3D Object > Cube を選ぶと、Transform、Mesh Filter、Mesh Renderer、Box Collider の 4 つのコンポーネントを持つ GameObject が作られます。GameObject を選択すると、持っているコンポーネントが Inspector ウィンドウに一覧で表示されます。

このように、Unity では、GameObject にコンポーネントを組み合わせて機能を作ります。自分で書いたスクリプトも、コンポーネントの 1 つとして GameObject にアタッチします。

MonoBehaviour
================================================================

GameObject にアタッチできるスクリプトは、``MonoBehaviour`` クラスを継承したクラスです。``MonoBehaviour`` を継承すると、次のことができるようになります。

* Unity が、決まったタイミングで ``Start`` や ``Update`` などのメソッドを自動的に呼び出す（第 11 章）。
* フィールドの値を Inspector ウィンドウで設定できる（第 12 章）。
* ``transform`` や ``gameObject`` を使って、アタッチされている GameObject を操作できる（第 13 章）。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メンバー
     - 説明
   * - ``gameObject``
     - このスクリプトがアタッチされている GameObject です。
   * - ``transform``
     - このスクリプトがアタッチされている GameObject の Transform コンポーネントです。
   * - ``name``
     - GameObject の名前です。
   * - ``enabled``
     - このコンポーネントが有効かどうかです。``false`` にすると、``Update`` などが呼ばれなくなります。

スクリプトのアタッチ
================================================================

スクリプトを GameObject にアタッチするには、次のどちらかの方法を使います。

* Project ウィンドウのスクリプトを、Hierarchy ウィンドウの GameObject、または Inspector ウィンドウにドラッグする。
* GameObject を選択し、Inspector ウィンドウの Add Component ボタンを押して、スクリプトの名前を検索する。

同じスクリプトを複数の GameObject にアタッチすると、GameObject ごとに別々のインスタンスが作られます。それぞれのインスタンスは、別々のフィールドの値を持ちます。

.. warning::

   アタッチしようとしたときに「Can't add script component ... because the script class cannot be found.」と表示された場合は、次のどちらかが原因です。

   * コンパイルエラーが残っている。
   * ファイル名とクラス名が一致していない（第 1 章）。

最初のコンポーネント
================================================================

アタッチした GameObject を回転させ続けるスクリプトを作ります。Hierarchy ウィンドウで 3D Object > Cube を選んで Cube を作成し、次のスクリプトをアタッチしてから Play ボタンを押してください。

.. literalinclude:: ../../examples/ch10/Spinner.cs
   :language: csharp
   :caption: Spinner.cs

:download:`Spinner.cs をダウンロード <../../examples/ch10/Spinner.cs>`

``Update`` は、画面が 1 回更新される（1 フレーム進む）たびに呼ばれるメソッドです。``transform.Rotate`` で少しずつ回転させることで、Cube が回り続けます。``Time.deltaTime`` の意味は、第 11 章で説明します。

Inspector ウィンドウを見ると、Spinner コンポーネントに Degrees Per Second という項目が表示されています。これは ``_degreesPerSecond`` フィールドです。Unity は、フィールド名の先頭の ``_`` を取り除き、単語の区切りに空白を入れて表示します。この値を変えると、回転の速さが変わります。

.. warning::

   Play モード中に Inspector ウィンドウで変更した値は、Play モードを終了すると元に戻ります。Play モード中は試しに値を変えて調整し、決まった値は Play モードを終了してから設定し直してください。Play モード中であることに気づきやすくするために、Edit > Preferences > Colors の Playmode tint で、Play モード中のエディターの色を変えておくと便利です。

まとめ
================================================================

* シーンに置かれるものはすべて GameObject で、機能はコンポーネントとして追加します。
* スクリプトは ``MonoBehaviour`` を継承したクラスで、コンポーネントとして GameObject にアタッチします。
* ``transform`` や ``gameObject`` を使うと、アタッチされている GameObject を操作できます。
* Play モード中に変更した値は、Play モードを終了すると元に戻ります。
