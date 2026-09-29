MIDI の基礎
====================================================

本章では、ジェネラティブミュージックの出力形式として広く用いられる MIDI の基礎知識と、 Python による基本的な操作方法を説明します。

MIDI とは
----------------------------------------------------

MIDI （ Musical Instrument Digital Interface ）は、電子楽器やコンピューター間で演奏情報をやり取りするための規格です。 MIDI データには、音の高さや音量、発音のタイミングといった演奏情報が含まれますが、音声そのものは含まれません。そのため、同じ MIDI データであっても、再生する音源によって異なる音色で演奏されます。

音符を表すノートナンバー
----------------------------------------------------

MIDI では、音の高さを 0 から 127 までの整数値（ ノートナンバー ）で表現します。中央のド（ C4 ）はノートナンバー 60 に対応し、値が 1 増えるごとに半音ずつ音が高くなります。

pretty_midi による MIDI ファイルの生成
----------------------------------------------------

以下は、 ``pretty_midi`` を用いて簡単な MIDI ファイルを生成するコード例です。

.. code-block:: python

   import pretty_midi

   midi_data = pretty_midi.PrettyMIDI()
   instrument = pretty_midi.Instrument(program=0)

   notes = [60, 62, 64, 65, 67, 69, 71, 72]
   start_time = 0.0
   duration = 0.5

   for note_number in notes:
       note = pretty_midi.Note(
           velocity=100,
           pitch=note_number,
           start=start_time,
           end=start_time + duration,
       )
       instrument.notes.append(note)
       start_time += duration

   midi_data.instruments.append(instrument)
   midi_data.write("output.mid")

このコードでは、ハ長調の音階（ ド・レ・ミ・ファ・ソ・ラ・シ・ド ）を、 0.5 秒間隔で並べた MIDI ファイルを生成しています。

MIDI ファイルの再生
----------------------------------------------------

生成した MIDI ファイルは、 DAW （ Digital Audio Workstation ）や、 MIDI 対応の音源ソフトで再生することができます。 Python 上でリアルタイムに再生したい場合は、 ``python-rtmidi`` を用いて MIDI 出力デバイスへメッセージを送信する方法が利用できます。
