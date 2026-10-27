サンプルコード
==============

本書で紹介した Python のサンプルコードとサンプルデータを、次の表に示す。ファイル名をクリックするとダウンロードできる。

.. list-table:: サンプルコードとサンプルデータ
   :header-rows: 1
   :widths: 30 50 20

   * - ファイル
     - 内容
     - 説明している章
   * - :download:`break_timer.py <../examples/break_timer.py>`
     - 作業と休止の時刻を知らせる休憩タイマー
     - :doc:`sedentary`
   * - :download:`activity_calc.py <../examples/activity_calc.py>`
     - 1 週間の活動記録から身体活動量と消費エネルギーを計算し、推奨量と比べる
     - :doc:`exercise`
   * - :download:`activity_sample.csv <../examples/activity_sample.csv>`
     - activity_calc.py 用のサンプルデータ（1 週間の活動記録）
     - :doc:`exercise`
   * - :download:`sleep_log.py <../examples/sleep_log.py>`
     - 睡眠記録を集計し、睡眠時間や社会的時差ぼけを計算する。睡眠の時間帯をグラフにする
     - :doc:`habits`
   * - :download:`sleep_log_sample.csv <../examples/sleep_log_sample.csv>`
     - sleep_log.py 用のサンプルデータ（2 週間の睡眠記録）
     - :doc:`habits`

実行環境
--------

* Python 3.10 以降で動作する。
* break_timer.py と activity_calc.py は、Python の標準ライブラリだけで動作する。
* sleep_log.py でグラフを作る（``--plot`` を指定する）場合は、matplotlib が必要である。matplotlib は次のようにインストールできる。

.. code-block:: console
   :linenos:

   python -m pip install matplotlib

実行のしかた
------------

ダウンロードしたファイルを同じフォルダに置き、そのフォルダで端末を開いて実行する。各スクリプトのオプションは、``--help`` を付けて実行すると表示される。

.. code-block:: console
   :linenos:

   python break_timer.py --help
   python activity_calc.py activity_sample.csv --weight 65
   python sleep_log.py sleep_log_sample.csv --plot sleep_log.png

自分の記録を集計するには、サンプルデータと同じ形式の CSV ファイルを作り、そのファイル名を指定する。CSV ファイルは、文字コードを UTF-8 にして保存する。表計算ソフトで作る場合は、保存するときの形式に「CSV UTF-8」などを選ぶ。

.. note::

   出力には日本語の記号（「〜」や「±」）が含まれる。Windows で出力をファイルにリダイレクトするときに文字コードのエラーが出る場合は、環境変数 ``PYTHONUTF8`` に 1 を設定してから実行する。

コードの品質
------------

サンプルコードは、PEP 8 に沿って書き、すべての関数に型ヒントを付けている。flake8（1 行の長さは 120 文字まで許容）と mypy（\ ``strict = True``\ ）で検査し、違反がないことを確認している。
