第 12 章 UI
===========

この章では、スコアの表示やボタンなど、ゲーム画面に重ねて表示する UI（ユーザーインターフェイス）の作り方を説明します。

この章のサンプルコードは、``examples/chapter12`` フォルダーにあります。

UI のしくみ
-----------

Unity には、UI を作るしくみが 2 つあります。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - しくみ
     - 特徴
   * - uGUI（Unity UI）
     - GameObject とコンポーネントで UI を作ります。Scene ビューで配置を確認しながら作れるため、Unity の操作に慣れていれば直感的に扱えます。ゲームの UI で広く使われています。
   * - UI Toolkit
     - Web ページの HTML と CSS に似た方式（UXML と USS）で UI を作ります。多くの項目を持つメニュー画面や、エディター拡張のウィンドウに向いています。

本資料では、GameObject とコンポーネントの知識をそのまま生かせる uGUI を使います。

Canvas
------

uGUI の UI 要素は、すべて **Canvas** の子として配置します。例えば、:menuselection:`GameObject --> UI --> Text - TextMeshPro` を選ぶと、シーンに Canvas がない場合は、次の GameObject が自動的に作成されます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - GameObject
     - 役割
   * - Canvas
     - UI を描画する領域です。
   * - EventSystem
     - マウスのクリックやタッチなどの入力を UI に伝えます。Input System を使うプロジェクトでは、``Input System UI Input Module`` コンポーネントが付きます。
   * - Text (TMP)
     - テキストを表示する UI 要素です。Canvas の子として作成されます。

.. note::

   プロジェクトで初めて TextMeshPro を使うときは、:guilabel:`TMP Importer` ウィンドウが表示されます。:guilabel:`Import TMP Essentials` をクリックして、TextMeshPro に必要なアセットを読み込んでください。

Canvas Scaler による画面サイズへの対応
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ゲームを動かす画面の解像度は、プレイヤーの環境によって異なります。Canvas に付いている **Canvas Scaler** コンポーネントを次のように設定すると、どの解像度でも UI が同じような大きさで表示されます。

#. :guilabel:`UI Scale Mode` を :guilabel:`Scale With Screen Size` にします。
#. :guilabel:`Reference Resolution` に、UI を作るときの基準の解像度（例えば X が 1920、Y が 1080）を入力します。
#. :guilabel:`Match` を、画面の幅と高さのどちらを基準に拡大縮小するかに応じて設定します。0 で幅、1 で高さが基準になります。

RectTransform とアンカー
------------------------

UI 要素には、Transform の代わりに **RectTransform** が付いています。RectTransform は、位置と大きさを、親の長方形の中のどこを基準にするかで指定します。この基準を **アンカー** と呼びます。

例えば、スコアを画面の左上に表示したい場合は、アンカーを左上に設定します。すると、画面の大きさが変わっても、スコアは常に画面の左上からの同じ位置に表示されます。

アンカーは、Inspector ウィンドウの RectTransform の左上にある四角いアイコン（Anchor Presets）をクリックして選べます。:kbd:`Shift` を押しながら選ぶと、UI 要素の中心点（Pivot）も同じ位置に設定されます。:kbd:`Alt` を押しながら選ぶと、UI 要素の位置もアンカーの位置に移動します。

テキストの表示
--------------

テキストの表示には **TextMeshPro**\ （TMP）を使います。TextMeshPro は、拡大しても文字がぼやけにくく、縁取りや影などの装飾も簡単に設定できます。

スクリプトからテキストを変更するには、``TMPro`` 名前空間の ``TextMeshProUGUI`` 型のフィールドを用意し、``text`` プロパティに文字列を設定します。

.. literalinclude:: ../../examples/chapter12/ScoreView.cs
   :caption: ScoreView.cs
   :linenos:

:download:`ScoreView.cs をダウンロード <../../examples/chapter12/ScoreView.cs>`

.. important::

   TextMeshPro の既定のフォントには、日本語の文字が含まれていません。日本語を表示すると、文字の代わりに四角形が表示されます。日本語を表示するには、まず、日本語を含むフォントファイル（``.ttf`` や ``.otf``）をプロジェクトに追加します。次に、Project ウィンドウでそのフォントを右クリックし、:menuselection:`Create --> TextMeshPro` の下にある Font Asset の作成メニューを選びます。最後に、作成したフォントアセットを TextMeshPro の :guilabel:`Font Asset` に設定します。フォントのライセンスで、ゲームへの組み込みが許可されていることも確認してください。

ボタン
------

ボタンは、:menuselection:`GameObject --> UI --> Button - TextMeshPro` で作成します。ボタンがクリックされたときの処理は、次の 2 つの方法で設定できます。

Inspector ウィンドウで設定する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Button コンポーネントの :guilabel:`On Click ()` の欄にある :guilabel:`+` をクリックします。
#. 追加された欄に、呼び出したいメソッドを持つ GameObject をドラッグ＆ドロップします。
#. 右側の一覧から、コンポーネントとメソッドを選びます。

この方法で呼び出せるのは、``public`` で、引数がないか、引数が 1 つ（``int``、``float``、``string``、``bool``、Unity のオブジェクトのいずれか）のメソッドです。

スクリプトで設定する
~~~~~~~~~~~~~~~~~~~~

Button コンポーネントの ``onClick`` に、``AddListener`` でメソッドを登録します。

.. literalinclude:: ../../examples/chapter12/ClickCounter.cs
   :caption: ClickCounter.cs
   :linenos:

:download:`ClickCounter.cs をダウンロード <../../examples/chapter12/ClickCounter.cs>`

使い方は次のとおりです。

#. Canvas に、テキスト（Text (TMP)）とボタン（Button）を 1 つずつ作成します。
#. テキストの GameObject に ``ScoreView`` を付け、:guilabel:`Score Text` にテキスト自身をドラッグ＆ドロップします。
#. ボタンの GameObject に ``ClickCounter`` を付け、:guilabel:`Button` にボタン自身を、:guilabel:`Score View` にテキストの GameObject をドラッグ＆ドロップします。
#. 再生してボタンをクリックすると、クリックした回数が表示されます。

Inspector ウィンドウで設定する方法は手軽ですが、どこで何が呼ばれるのかがスクリプトからはわかりません。スクリプトで設定する方法は、処理の流れをコードで追えるという利点があります。

UI Toolkit
----------

UI Toolkit は、UI の構造を UXML、見た目を USS というファイルで記述するしくみです。UI Builder というツールを使って、画面上で UI を組み立てることもできます。多くのボタンや一覧を持つ設定画面のように、要素の数が多い UI を作る場合や、見た目をスタイルシートでまとめて管理したい場合に向いています。

UI Toolkit の使い方は本資料の範囲を超えるため、詳しくは `Unity マニュアルの UI Toolkit のページ <https://docs.unity3d.com/Manual/UIElements.html>`_ を参照してください。
