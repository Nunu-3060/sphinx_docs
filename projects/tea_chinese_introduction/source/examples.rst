便利なスクリプト
================

本付録では、中国茶を淹れるときに役立つ 2 つの Python スクリプトを紹介します。どちらも Python の標準機能だけで動くため、追加のインストールは不要です。

動かすための準備
----------------

スクリプトを動かすには、Python 3.10 以上が必要です。Python は、`Python の公式サイト <https://www.python.org/downloads/>`_\ からダウンロードしてインストールできます。

スクリプトは、次の手順で実行します。

#. 本ページのリンクからスクリプトをダウンロードします。
#. Windows では「コマンドプロンプト」、macOS では「ターミナル」を開きます。
#. ``cd`` コマンドで、スクリプトを保存したフォルダーに移動します。
#. ``python`` コマンドの後にスクリプトのファイル名を付けて実行します。

例えば、ダウンロードフォルダーに保存した場合は、次のように入力します。macOS では ``python`` の代わりに ``python3`` と入力してください。

.. code-block:: text
   :linenos:

   cd Downloads
   python brewing_guide.py

どちらのスクリプトでも、茶類は次の名前で指定します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 指定する名前
     - 茶類
   * - ``green``
     - 緑茶
   * - ``white``
     - 白茶
   * - ``yellow``
     - 黄茶
   * - ``oolong``
     - 青茶（烏龍茶）
   * - ``black``
     - 紅茶
   * - ``dark``
     - 黒茶（プーアル茶）
   * - ``jasmine``
     - 花茶（ジャスミン茶）

淹れ方の目安の表示（brewing_guide.py）
--------------------------------------

茶類と器の容量を指定すると、茶葉の量、湯温、煎ごとの浸出時間の目安を表示します。計算には、「:doc:`brewing`」で紹介した、蓋碗や茶壺で淹れる場合の目安と式を使っています。

ダウンロード：:download:`brewing_guide.py <../examples/brewing_guide.py>`

使い方
^^^^^^

引数を付けずに実行すると、茶類と器の容量を順に尋ねられます。

.. code-block:: text
   :linenos:

   python brewing_guide.py

茶類と器の容量（ml）を続けて指定すると、すぐに結果が表示されます。器の容量には、30〜500 の整数を指定します。例えば、容量 120 ml の蓋碗で青茶を淹れる場合は、次のように実行します。

.. code-block:: text
   :linenos:

   python brewing_guide.py oolong 120

実行すると、次のように表示されます。

.. code-block:: text
   :linenos:

   青茶（烏龍茶）を 120 ml の器で淹れる目安
     茶葉の量  : 7.2 g
     湯温      : 95〜100 ℃
     浸出時間  :
       1 煎目  0 分 30 秒
       2 煎目  0 分 40 秒
       3 煎目  0 分 50 秒
       4 煎目  1 分 00 秒
       5 煎目  1 分 10 秒
       6 煎目  1 分 20 秒

ソースコード
^^^^^^^^^^^^

.. literalinclude:: ../examples/brewing_guide.py
   :language: python
   :linenos:

煎ごとのタイマー（infusion_timer.py）
-------------------------------------

茶類を指定すると、1 煎目から順に浸出時間をカウントダウンします。煎を重ねるごとに浸出時間が延びる、中国茶の淹れ方に合わせたタイマーです。計る時間は、brewing_guide.py で表示される浸出時間と同じです。

ダウンロード：:download:`infusion_timer.py <../examples/infusion_timer.py>`

使い方
^^^^^^

茶類を指定しない場合は、実行後に番号で選びます。例えば、ジャスミン茶の浸出時間を計る場合は、次のように実行します。

.. code-block:: text
   :linenos:

   python infusion_timer.py jasmine

お湯を注いだら :kbd:`Enter` キーを押すと、カウントダウンが始まります。時間になると、音とメッセージで知らせます。続けて次の煎のお湯を注いだら、もう一度 :kbd:`Enter` キーを押します。途中で終わりたい場合は、:kbd:`Enter` キーの代わりに :kbd:`q` を入力して :kbd:`Enter` キーを押すか、:kbd:`Ctrl+C` を押します。

途中の煎から計りたい場合は、``-s`` の後に煎数を指定します。次の例では、ジャスミン茶の 2 煎目から計ります。

.. code-block:: text
   :linenos:

   python infusion_timer.py jasmine -s 2

実行すると、次のように表示されます。残り時間は、1 秒ごとに同じ行で更新されます。

.. code-block:: text
   :linenos:

   花茶（ジャスミン茶）: 3 煎目まで計ります。Ctrl+C で中止できます。
   2 煎目: お湯を注いだら Enter を押してください（q で終了）:
     残り 0 分 00 秒
     2 煎目の時間です。茶海に注ぎ切りましょう。
   3 煎目: お湯を注いだら Enter を押してください（q で終了）:
     残り 0 分 00 秒
     3 煎目の時間です。茶海に注ぎ切りましょう。
   目安の煎数に達しました。味が薄くなるまで楽しめます。

ソースコード
^^^^^^^^^^^^

.. literalinclude:: ../examples/infusion_timer.py
   :language: python
   :linenos:
