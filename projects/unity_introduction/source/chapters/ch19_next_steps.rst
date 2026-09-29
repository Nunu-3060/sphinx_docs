第 19 章 次のステップ
=====================

本資料では、Unity の基本的な機能を使って、簡単なゲームを完成させるまでを説明しました。この章では、さらに学習を進めるための情報を紹介します。

公式の情報源
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 情報源
     - 内容
   * - `Unity マニュアル <https://docs.unity3d.com/Manual/index.html>`_
     - Unity Editor の機能や、各コンポーネントの使い方の説明です。
   * - `Unity スクリプトリファレンス <https://docs.unity3d.com/ScriptReference/index.html>`_
     - Unity の C# のクラスやメソッドの説明です。メソッドの引数や使用例を調べるときに使います。
   * - `Unity Learn <https://learn.unity.com/>`_
     - Unity が提供している無料の学習サイトです。チュートリアルや講座が多数公開されています。
   * - `Unity Discussions <https://discussions.unity.com/>`_
     - Unity のユーザー同士が質問や情報交換をするための公式のフォーラムです。
   * - `C# のドキュメント <https://learn.microsoft.com/ja-jp/dotnet/csharp/>`_
     - Microsoft による C# の言語の説明です。

マニュアルやスクリプトリファレンスは、ページの左上でバージョンを切り替えられます。お使いの Unity のバージョンに合ったページを参照してください。

Asset Store
-----------

`Asset Store <https://assetstore.unity.com/>`_ では、3D モデル、テクスチャ、音声、エフェクト、ツールなどのアセットが、無料または有料で公開されています。学習や試作の段階では、無料のアセットを使うと、見た目の良いゲームを手軽に作れます。

購入したアセットは、Unity Editor の Package Manager ウィンドウの :guilabel:`My Assets` から、プロジェクトに読み込めます。

アセットを使うときは、次の点に注意してください。

* 対応している Unity のバージョンと、レンダーパイプライン（:doc:`ch11_graphics` を参照）を確認します。
* ライセンスの条件（商用利用の可否、クレジットの表記の要否など）を確認します。

発展的なトピック
----------------

本資料で扱わなかった機能のうち、次に学ぶと役立つものを紹介します。多くはパッケージとして提供されており、Package Manager ウィンドウからインストールできます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - トピック
     - 内容
   * - エディター拡張
     - :doc:`ch08_scripting_advanced` で紹介したメニューの追加に加えて、独自のウィンドウ（``EditorWindow``）や、Inspector の表示の変更（``[CustomEditor]``）などで、作業を効率化するツールを作れます。詳しくは、`Unity マニュアルのエディターの拡張のページ <https://docs.unity3d.com/Manual/ExtendingTheEditor.html>`_ を参照してください。
   * - Shader Graph
     - ノードをつなぐ操作で、コードを書かずにシェーダーを作れます。
   * - Visual Effect Graph
     - GPU を使って、大量のパーティクルによるエフェクトを作れます（:doc:`ch11_graphics` を参照）。
   * - Cinemachine
     - カメラの追従や切り替えを、スクリプトを書かずに設定できます。
   * - Timeline
     - アニメーション、音声、カメラの動きなどを時間軸に沿って並べ、ムービーシーンなどを作れます。
   * - AI Navigation
     - 地形から歩ける範囲（NavMesh）を計算し、敵のキャラクターなどに障害物を避けながら目的地まで移動させられます。
   * - Terrain
     - 山や谷のある広い地形を、ブラシで描くように作れます。
   * - ProBuilder
     - Unity Editor の中で、簡単な 3D モデルを作れます。ステージの試作に便利です。
   * - Addressables
     - アセットを必要なときに読み込み、不要になったら解放するしくみです。大規模なゲームのメモリ管理や、ダウンロードによるコンテンツの追加に使います。
   * - Netcode for GameObjects
     - 複数のプレイヤーが同時に遊ぶ、マルチプレイヤーのゲームを作るためのパッケージです。
   * - XR Interaction Toolkit
     - VR や AR のアプリケーションで、物をつかむ、ボタンを押すなどの操作を実装するためのパッケージです。
   * - Unity Test Framework
     - スクリプトの動作を自動的に確認するテストを書くためのパッケージです。
   * - Entities（ECS）
     - 大量のオブジェクトを高速に処理するための、GameObject とは異なる設計のしくみです。

おわりに
--------

ゲーム開発の技術は、実際に作ってみることで身に付きます。まずは :doc:`ch16_tutorial` の発展課題のように、完成したゲームを少しずつ改造することから始めてみてください。わからないことがあれば、マニュアルやスクリプトリファレンスで調べ、試しながら理解を深めていきましょう。
