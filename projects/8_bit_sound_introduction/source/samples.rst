.. _ch-samples:

サンプルコード一覧
==================

本書のサンプルコードの一覧である。ファイル名のリンクからダウンロードできる。すべてのファイルを同じフォルダに置いて使うこと。

動作に必要なライブラリと実行方法は「:ref:`ch-introduction`」を参照すること。

.. list-table:: サンプルコードの一覧
   :header-rows: 1
   :widths: 30 70

   * - ファイル
     - 内容
   * - :download:`wav_io.py <../examples/wav_io.py>`
     - WAV ファイルの書き出しと音量の調整を行う共通モジュール。
   * - :download:`waveforms.py <../examples/waveforms.py>`
     - 矩形波・三角波・ノイズの生成、音名と周波数の変換。
   * - :download:`envelope.py <../examples/envelope.py>`
     - エンベロープ、ピッチスイープ、ビブラート、アルペジオ、疑似エコー。
   * - :download:`sound_effects.py <../examples/sound_effects.py>`
     - 効果音の作例と、乱数による効果音の生成。
   * - :download:`sequencer.py <../examples/sequencer.py>`
     - テキストの楽譜から複数チャンネルの曲を合成する簡易シーケンサ。
   * - :download:`bgm_example.py <../examples/bgm_example.py>`
     - 4 チャンネル構成のループ BGM の作例。
   * - :download:`pyxel_sound.py <../examples/pyxel_sound.py>`
     - Pyxel の音源機能でジングルを作る例。
   * - :download:`play_pygame.py <../examples/play_pygame.py>`
     - pygame-ce で BGM と効果音を鳴らす例。
   * - :download:`make_all.py <../examples/make_all.py>`
     - 本書で使うすべての音声ファイルを一括で生成する。
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定ファイル。

すべてのコードは flake8（行の長さの上限 120 文字）と mypy（``strict = True``）の検査を通過している。検査は ``setup.cfg`` を置いたフォルダで次のように実行する。

.. code-block:: bat
   :linenos:

   python -m flake8
   python -m mypy .

wav_io.py
---------

WAV ファイルの書き出しと音量の調整を行う共通モジュール。

.. literalinclude:: ../examples/wav_io.py
   :language: python
   :linenos:
   :caption: wav_io.py

waveforms.py
------------

矩形波・三角波・ノイズの生成、音名と周波数の変換。

.. literalinclude:: ../examples/waveforms.py
   :language: python
   :linenos:
   :caption: waveforms.py

envelope.py
-----------

エンベロープ、ピッチスイープ、ビブラート、アルペジオ、疑似エコー。

.. literalinclude:: ../examples/envelope.py
   :language: python
   :linenos:
   :caption: envelope.py

sound_effects.py
----------------

効果音の作例と、乱数による効果音の生成。

.. literalinclude:: ../examples/sound_effects.py
   :language: python
   :linenos:
   :caption: sound_effects.py

sequencer.py
------------

テキストの楽譜から複数チャンネルの曲を合成する簡易シーケンサ。

.. literalinclude:: ../examples/sequencer.py
   :language: python
   :linenos:
   :caption: sequencer.py

bgm_example.py
--------------

4 チャンネル構成のループ BGM の作例。

.. literalinclude:: ../examples/bgm_example.py
   :language: python
   :linenos:
   :caption: bgm_example.py

pyxel_sound.py
--------------

Pyxel の音源機能でジングルを作る例。

.. literalinclude:: ../examples/pyxel_sound.py
   :language: python
   :linenos:
   :caption: pyxel_sound.py

play_pygame.py
--------------

pygame-ce で BGM と効果音を鳴らす例。

.. literalinclude:: ../examples/play_pygame.py
   :language: python
   :linenos:
   :caption: play_pygame.py

make_all.py
-----------

本書で使うすべての音声ファイルを一括で生成する。

.. literalinclude:: ../examples/make_all.py
   :language: python
   :linenos:
   :caption: make_all.py

setup.cfg
---------

flake8 と mypy の設定ファイル。``mypy_path`` は、ほかのモジュールを読み込むための設定である。

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
   :caption: setup.cfg
