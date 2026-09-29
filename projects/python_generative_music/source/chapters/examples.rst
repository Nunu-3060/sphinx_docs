実装例
====================================================

本章では、これまでに解説した内容を踏まえた、 4 つの実装例を紹介します。いずれのサンプルコードも、本文中で内容を確認できるほか、各節の末尾に掲載したリンクからファイルをダウンロードすることができます。いずれのコードも PEP 8 に準拠し、 ``flake8`` および ``mypy`` によるチェックを通過しています。

ランダムメロディジェネレーター
----------------------------------------------------

もっとも基本的な例として、乱数を用いてハ長調のメジャースケールからランダムに音を選び、旋律を生成するプログラムです。各音符の長さは、 4 分音符または 8 分音符の中からランダムに選択されます。

.. literalinclude:: ../../examples/random_melody_generator.py
   :language: python
   :linenos:

``generate_melody`` 関数では、あらかじめ定義した音階 ``SCALE`` と、音の長さの候補 ``DURATIONS`` の中から、それぞれランダムに値を選択し、指定した数の音符からなる旋律を生成しています。 ``melody_to_midi`` 関数では、生成した旋律のリストを ``pretty_midi.Note`` オブジェクトへ変換した上で、 MIDI ファイルとして出力しています。

このサンプルコードは :download:`random_melody_generator.py <../../examples/random_melody_generator.py>` からダウンロードできます。実行すると、スクリプトと同じディレクトリに ``random_melody.mid`` という MIDI ファイルが生成されます。

.. code-block:: bash

   python random_melody_generator.py

マルコフ連鎖メロディジェネレーター
----------------------------------------------------

「アルゴリズム作曲の手法」の章で紹介したマルコフ連鎖を用いて、旋律を生成するプログラムです。 ``TRANSITION_TABLE`` には、各音符から遷移しうる次の音符の候補があらかじめ定義されており、 ``generate_melody`` 関数がその候補の中から乱数を用いて次の音を選択します。

.. literalinclude:: ../../examples/markov_melody_generator.py
   :language: python
   :linenos:

ランダムメロディジェネレーターと比較すると、音の並びに一定の傾向が生まれ、より旋律らしい印象になることが確認できます。このサンプルコードは :download:`markov_melody_generator.py <../../examples/markov_melody_generator.py>` からダウンロードできます。実行すると、 ``markov_melody.mid`` という MIDI ファイルが生成されます。

.. code-block:: bash

   python markov_melody_generator.py

ユークリッドリズムジェネレーター
----------------------------------------------------

「アルゴリズム作曲の手法」の章で紹介したユークリッドリズムを実装し、ドラムパターンとして MIDI ファイルへ出力するプログラムです。 ``euclidean_rhythm`` 関数が Bjorklund のアルゴリズムによってリズムパターンを計算し、 ``pattern_to_midi`` 関数がそのパターンをキック（ バスドラム ）の MIDI ノートへ変換します。

.. literalinclude:: ../../examples/euclidean_rhythm.py
   :language: python
   :linenos:

既定の設定では、 8 ステップの中に 5 拍を配置したパターンを、 4 小節分繰り返した MIDI ファイル ``euclidean_rhythm.mid`` を生成します。 ``euclidean_rhythm`` 関数の引数を変更することで、さまざまな拍数とステップ数の組み合わせを試すことができます。このサンプルコードは :download:`euclidean_rhythm.py <../../examples/euclidean_rhythm.py>` からダウンロードできます。

.. code-block:: bash

   python euclidean_rhythm.py

サイン波シンセサイザー
----------------------------------------------------

「音声合成の基礎」の章で紹介した内容に基づき、サイン波に ADSR エンベロープを適用して WAV ファイルへ出力するプログラムです。 ``generate_sine_wave`` 関数で波形を生成し、 ``apply_adsr_envelope`` 関数で音量変化を適用した後、 ``write_wav`` 関数で 16 ビット PCM の WAV ファイルとして書き出します。

.. literalinclude:: ../../examples/sine_wave_synthesis.py
   :language: python
   :linenos:

実行すると、 440 Hz のサイン波（ 音楽で用いられる基準音、いわゆる A4 の音 ）を 2 秒間鳴らした ``sine_wave.wav`` が生成されます。このサンプルコードは :download:`sine_wave_synthesis.py <../../examples/sine_wave_synthesis.py>` からダウンロードできます。

.. code-block:: bash

   python sine_wave_synthesis.py

サンプルコードの検証方法
----------------------------------------------------

ここまでに紹介した 4 つのサンプルコードは、以下のコマンドで静的解析を行うことができます。 ``mypy`` の実行には、 :download:`mypy.ini <../../examples/mypy.ini>` をダウンロードし、各サンプルコードと同じディレクトリへ配置した上で使用します。

.. code-block:: bash

   pip install flake8 mypy
   flake8 random_melody_generator.py markov_melody_generator.py euclidean_rhythm.py sine_wave_synthesis.py
   mypy --config-file mypy.ini random_melody_generator.py markov_melody_generator.py euclidean_rhythm.py sine_wave_synthesis.py
