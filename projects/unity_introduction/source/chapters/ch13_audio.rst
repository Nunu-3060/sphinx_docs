第 13 章 オーディオ
===================

この章では、効果音や BGM を再生する方法を説明します。

この章のサンプルコードは、``examples/chapter13`` フォルダーにあります。

AudioClip、AudioSource、AudioListener
-------------------------------------

Unity で音を扱うには、次の 3 つの要素を使います。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 要素
     - 役割
   * - AudioClip
     - 音声ファイル（``.wav``、``.mp3``、``.ogg`` など）をプロジェクトに読み込んだアセットです。
   * - AudioSource
     - AudioClip を再生するコンポーネントです。音を出したい GameObject に付けます。
   * - AudioListener
     - 音を聞くコンポーネントです。人間の耳にあたります。通常は Main Camera に付いています。

AudioListener は、シーンに 1 つだけ置きます。複数あると、Console ウィンドウに警告が表示されます。

AudioSource の主なプロパティ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - プロパティ
     - 意味
   * - :guilabel:`Audio Resource`
     - 再生する AudioClip などの音声のアセットです。
   * - :guilabel:`Play On Awake`
     - GameObject が有効になったときに自動的に再生するかどうかです。
   * - :guilabel:`Loop`
     - 最後まで再生したら、最初から繰り返すかどうかです。BGM では有効にします。
   * - :guilabel:`Volume`
     - 音量（0 から 1）です。
   * - :guilabel:`Pitch`
     - 再生速度と音の高さです。1 が元の速さです。
   * - :guilabel:`Spatial Blend`
     - 0 で 2D の音、1 で 3D の音になります（後述）。

BGM の再生
----------

BGM は、スクリプトを書かなくても再生できます。

#. 空の GameObject を作成し、名前を ``BGM`` にします。
#. :guilabel:`Add Component` で AudioSource を追加します。
#. :guilabel:`Audio Resource` に BGM の AudioClip を設定します。
#. :guilabel:`Play On Awake` と :guilabel:`Loop` を有効にします。

再生すると、BGM が繰り返し流れます。

効果音の再生
------------

効果音は、スクリプトから再生するのが一般的です。

.. literalinclude:: ../../examples/chapter13/SoundPlayer.cs
   :caption: SoundPlayer.cs
   :linenos:

:download:`SoundPlayer.cs をダウンロード <../../examples/chapter13/SoundPlayer.cs>`

使い方は次のとおりです。

#. 空の GameObject を作成し、名前を ``SoundPlayer`` にして、``SoundPlayer`` スクリプトを付けます。
#. 同じ GameObject に AudioSource を 2 つ追加します。1 つ目は効果音用で、:guilabel:`Play On Awake` を無効にします。2 つ目は BGM 用で、:guilabel:`Audio Resource` に BGM を設定し、:guilabel:`Play On Awake` と :guilabel:`Loop` を有効にします。
#. ``SoundPlayer`` の :guilabel:`Sfx Source` に 1 つ目の AudioSource を、:guilabel:`Bgm Source` に 2 つ目の AudioSource を、:guilabel:`Click Sound` に効果音の AudioClip を、それぞれドラッグ＆ドロップします。

AudioSource で音を再生するメソッドには、次のものがあります。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - メソッド
     - 特徴
   * - ``Play()``
     - :guilabel:`Audio Resource` に設定した音を再生します。再生中の音は止めて、最初から再生し直します。
   * - ``PlayOneShot(clip)``
     - 引数の AudioClip を再生します。再生中の音を止めずに重ねて再生するため、連続して鳴る効果音に向いています。
   * - ``AudioSource.PlayClipAtPoint(clip, position)``
     - 指定した位置に一時的な AudioSource を作成して、音を再生します。再生が終わると自動的に削除されます。音を鳴らす GameObject がすぐに破棄される場合に使います。

``SoundPlayer`` の ``PlayClickSound`` を、:doc:`ch12_ui` で説明したボタンの :guilabel:`On Click ()` に設定すると、ボタンをクリックしたときに効果音が鳴ります。``FadeOutBgm`` は、コルーチンを使って BGM の音量を徐々に下げてから停止します。

3D サウンド
-----------

AudioSource の :guilabel:`Spatial Blend` を 1 にすると、音が **3D サウンド** になります。3D サウンドでは、AudioListener（通常はカメラ）との位置関係によって、音の大きさと左右の聞こえ方が変わります。例えば、画面の右側にある滝の音は右から聞こえ、遠ざかると小さくなります。

音が聞こえる範囲は、:guilabel:`3D Sound Settings` の :guilabel:`Min Distance` と :guilabel:`Max Distance` で設定します。:guilabel:`Min Distance` までは最大の音量で聞こえ、それより遠くなるにつれて小さくなります。

BGM や UI の効果音のように、位置に関係なく同じように聞こえてほしい音は、:guilabel:`Spatial Blend` を 0（2D）のままにしておきます。

音量の管理
----------

BGM と効果音の音量を別々に調整できるようにしたい場合は、**Audio Mixer** を使います。Audio Mixer では、AudioSource の出力先をグループ（BGM、効果音など）に分け、グループごとに音量やエフェクトを設定できます。Audio Mixer は、Project ウィンドウを右クリックし、:menuselection:`Create --> Audio --> Audio Mixer` で作成します。
