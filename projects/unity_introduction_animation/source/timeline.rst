Timeline によるカットシーン
===========================

この章では、Timeline を使って、複数のオブジェクトのアニメーションや音を組み合わせたカットシーンを作成する方法を説明する。

Timeline の仕組み
-----------------

Timeline は、横軸を時間とした編集画面にトラックを並べ、各トラックにクリップを配置して演出を作る機能である。動画編集ソフトに近い操作で、複数の GameObject の動きを同じ時間軸で同期させられる。

Timeline は次の 2 つの要素で構成される。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 要素
     - 役割
   * - Timeline アセット
     - トラックとクリップの配置を記録したアセット。拡張子は .playable である。
   * - Playable Director コンポーネント
     - シーン上の GameObject に追加し、Timeline アセットを再生するコンポーネント。各トラックがどの GameObject を操作するかの対応付け（バインド）も保持する。

Timeline アセットはシーンの GameObject を直接参照せず、Playable Director のバインドを通して操作する。そのため、同じ Timeline アセットを、別の GameObject にバインドして再利用できる。

Timeline の作成
---------------

Timeline を作成する手順は次のとおりである。

#. Hierarchy ウィンドウで、カットシーンを管理する GameObject を作成して選択する（例: 空の GameObject「Cutscene」）。
#. メニューの Window > Sequencing > Timeline で Timeline ウィンドウを開く。
#. Timeline ウィンドウの Create ボタンをクリックし、Timeline アセットの保存先とファイル名を指定する。

選択していた GameObject には Playable Director コンポーネントが追加され、作成した Timeline アセットが設定される。

Playable Director の主な設定は次のとおりである。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 内容
   * - Playable
     - 再生する Timeline アセット。
   * - Update Method
     - 時間の進め方。Game Time は ``Time.timeScale`` の影響を受け、Unscaled Game Time は影響を受けない。DSP Clock は音声の時刻に合わせる。Manual はスクリプトから時刻を指定する。
   * - Play On Awake
     - 有効にすると、シーンの開始時に自動で再生する。
   * - Wrap Mode
     - 最後まで再生した後の動作。Hold は最後のフレームの状態を保つ。Loop は先頭から繰り返す。None は再生を停止する。

トラックの種類
--------------

Timeline ウィンドウの + ボタンから、次のトラックを追加できる。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - トラック
     - 内容
   * - Activation Track
     - バインドした GameObject を、クリップの区間だけアクティブにする。
   * - Animation Track
     - バインドした GameObject の Animator で、Animation Clip を再生する。
   * - Audio Track
     - Audio Clip を再生する。AudioSource をバインドする。
   * - Control Track
     - パーティクルシステムや、別の Timeline（入れ子の Timeline）の再生を制御する。
   * - Signal Track
     - 指定した時刻にイベントを発生させる。
   * - Playable Track
     - スクリプトで作成した独自のクリップを配置する。

Animation Track の使い方
------------------------

Animation Track でキャラクターを動かす手順は次のとおりである。

#. Timeline ウィンドウの + ボタンから Animation Track を追加する。
#. トラックの左側にあるバインドの欄に、Animator コンポーネントを持つ GameObject を Hierarchy ウィンドウからドラッグする。
#. Project ウィンドウから Animation Clip をトラックへドラッグして配置する。

同じトラック上で 2 つのクリップを重ねると、重なった区間で 2 つのアニメーションがブレンドされる。重なりの長さを変えることで、切り替えの滑らかさを調整できる。

トラックの録画ボタンをクリックすると、第 4 章の Animation ウィンドウと同様に、Scene ビューで GameObject を操作してキーフレームを記録できる。

Signal によるイベント通知
-------------------------

Signal は、Timeline の指定した時刻にスクリプトのメソッドを呼び出す仕組みである。「カットシーンのこの瞬間に効果音を鳴らす」「会話ウィンドウを表示する」といった、トラックだけでは表せない処理に使う。

Signal は次の 3 つの要素で構成される。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 要素
     - 役割
   * - Signal Asset
     - イベントの種類を表すアセット。「会話開始」「効果音」など、用途ごとに作成する。
   * - Signal Emitter
     - Signal Track 上に配置し、指定した時刻に Signal Asset を発信する。
   * - Signal Receiver
     - Signal Track にバインドした GameObject に追加するコンポーネント。受け取った Signal Asset ごとに、呼び出すメソッド（Reaction）を登録する。

Signal を使う手順は次のとおりである。

#. Signal Track を追加し、Signal を受け取る GameObject をバインドする。
#. Signal Track 上で、イベントを発生させたい時刻を右クリックし、Add Signal Emitter を選択する。
#. 追加した Signal Emitter を選択し、Inspector ウィンドウで Signal Asset を作成して指定する。
#. バインドした GameObject に Signal Receiver コンポーネントを追加し、Reaction に呼び出すメソッドを登録する。

次のサンプルは、Enter キーでカットシーンを再生し、Signal を受け取るとログを出力する。また、Playable Director の ``stopped`` イベントで再生の終了を検知する。このサンプルを Playable Director と同じ GameObject に追加する場合は、Signal Track にもその GameObject をバインドする。

.. literalinclude:: ../examples/CutsceneController.cs
   :language: csharp
   :caption: CutsceneController.cs

:download:`CutsceneController.cs をダウンロード <../examples/CutsceneController.cs>`

.. note::

   ``stopped`` イベントは、Wrap Mode が None の場合に最後まで再生したとき、または ``Stop`` メソッドで停止したときに発生する。Wrap Mode が Hold の場合は、最後まで再生しても停止しないため発生しない。

Animator との併用
-----------------

Animation Track で Animator Controller を持つキャラクターを動かすと、Timeline の再生中は Animation Track のアニメーションが Animator Controller のアニメーションより優先される。Timeline が停止すると、再び Animator Controller のアニメーションが再生される。

Timeline と Animator を併用する際は、次の点に注意する。

* Wrap Mode が Hold の場合、Timeline は最後のフレームを保ったまま再生を続けるため、Animator Controller のアニメーションに戻らない。カットシーンの後にゲームの操作へ戻す場合は、Wrap Mode を None にするか、スクリプトから ``Stop`` を呼ぶ。
* Animation Track の設定によっては、再生を始めたときにキャラクターが Animation Clip に記録された位置へ移動する。カットシーンをキャラクターの現在の位置から始めたい場合は、Animation Track の Inspector ウィンドウで Track Offsets を Apply Scene Offsets に設定する。
