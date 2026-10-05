便利なスクリプト
================

本付録では、紅茶を淹れるときに役立つ 2 つの Python スクリプトを紹介します。どちらも Python の標準機能だけで動くため、追加のインストールは不要です。

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
   python tea_calculator.py

茶葉の量の計算（tea_calculator.py）
-----------------------------------

杯数と茶葉の種類を指定すると、茶葉の量、お湯の量、蒸らし時間の目安を表示します。計算には、「:doc:`brewing`」で紹介した式と目安を使っています。

ダウンロード：:download:`tea_calculator.py <../examples/tea_calculator.py>`

使い方
^^^^^^

引数を付けずに実行すると、杯数と茶葉の種類を順に尋ねられます。

.. code-block:: text
   :linenos:

   python tea_calculator.py

杯数と茶葉の種類を続けて指定すると、すぐに結果が表示されます。茶葉の種類には、次のいずれかを指定します。

* ``op``：OP などの大きな茶葉
* ``bop``：BOP などの細かい茶葉
* ``ctc``：BOPF や CTC などの特に細かい茶葉

例えば、BOP の茶葉で 3 杯分を淹れる場合は、次のように実行します。

.. code-block:: text
   :linenos:

   python tea_calculator.py 3 bop

実行すると、次のように表示されます。

.. code-block:: text
   :linenos:

   3 杯分（BOP などの細かい茶葉）の目安
     茶葉の量    : 9.0 g（ティースプーン約 3 杯）
     お湯の量    : 450 ml
     蒸らし時間  : 2.5〜3 分

ソースコード
^^^^^^^^^^^^

.. literalinclude:: ../examples/tea_calculator.py
   :language: python
   :linenos:

蒸らし時間のタイマー（tea_timer.py）
------------------------------------

茶葉の種類を選ぶと、その茶葉に合った蒸らし時間をカウントダウンし、時間になったら音とメッセージで知らせます。タイマーで計る時間は、「:doc:`brewing`」で紹介した蒸らし時間の目安の中間の値です。

ダウンロード：:download:`tea_timer.py <../examples/tea_timer.py>`

使い方
^^^^^^

茶葉の種類には、次のいずれかを指定します。指定しない場合は、実行後に番号で選びます。

* ``op``：OP などの大きな茶葉（3 分 30 秒）
* ``bop``：BOP などの細かい茶葉（2 分 45 秒）
* ``ctc``：BOPF や CTC などの特に細かい茶葉（1 分 45 秒）
* ``bag``：ティーバッグ（1 分 45 秒）

例えば、BOP の茶葉の蒸らし時間を計る場合は、次のように実行します。

.. code-block:: text
   :linenos:

   python tea_timer.py bop

好みの時間で計りたい場合は、``--seconds`` の後に秒数を指定します。次の例では、200 秒（3 分 20 秒）を計ります。

.. code-block:: text
   :linenos:

   python tea_timer.py --seconds 200

実行すると、残り時間が 1 秒ごとに更新され、時間になると次のように表示されます。途中でやめたい場合は、:kbd:`Ctrl+C` を押します。

.. code-block:: text
   :linenos:

   BOP などの細かい茶葉: 目安は 2.5〜3 分です。
   2 分 45 秒を計ります。Ctrl+C で中止できます。
   残り 0 分 00 秒
   蒸らし終わりました。茶こしでこしながら注ぎましょう。

ソースコード
^^^^^^^^^^^^

.. literalinclude:: ../examples/tea_timer.py
   :language: python
   :linenos:
