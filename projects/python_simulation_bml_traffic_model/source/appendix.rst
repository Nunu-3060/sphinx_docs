======
付録
======

ソースコード一覧
================

本資料で解説した実装の全ファイルは、以下からダウンロードできます。

.. list-table:: ソースコード一覧
   :header-rows: 1
   :widths: 30 50 20

   * - ファイル
     - 役割
     - ダウンロード
   * - ``BML.py``
     - BML モデル本体
     - :download:`BML.py <../script/BML.py>`
   * - ``utility.py``
     - HSV から RGB への色変換
     - :download:`utility.py <../script/utility.py>`
   * - ``BMLImage.py``
     - 格子状態の画像化
     - :download:`BMLImage.py <../script/BMLImage.py>`
   * - ``FrameBML.py``
     - シミュレーション表示用の tkinter フレーム
     - :download:`FrameBML.py <../script/FrameBML.py>`
   * - ``TkWidget.py``
     - GUI 部品（色・サイズ・密度の設定）
     - :download:`TkWidget.py <../script/TkWidget.py>`
   * - ``BMLGUI.pyw``
     - メインアプリケーション
     - :download:`BMLGUI.pyw <../script/BMLGUI.pyw>`
   * - ``export_images.py``
     - :doc:`results` の掲載画像を出力するスクリプト
     - :download:`export_images.py <../script/export_images.py>`

参考文献
========

.. list-table:: 参考文献
   :header-rows: 1
   :widths: 70 30

   * - 文献
     - リンク
   * - O. Biham, A. A. Middleton, and D. Levine, "Self-organization and a dynamical transition in traffic-flow models," Physical Review A, 46(10), R6124, 1992.
     - （リンクなし）
   * - Biham-Middleton-Levine traffic model - Wikipedia
     - `en.wikipedia.org <https://en.wikipedia.org/wiki/Biham%E2%80%93Middleton%E2%80%93Levine_traffic_model>`_
   * - NumPy 公式ドキュメント（ ``numpy.roll`` ）
     - `numpy.org <https://numpy.org/doc/stable/reference/generated/numpy.roll.html>`_
   * - Pillow 公式ドキュメント（ ``Image`` モジュール）
     - `pillow.readthedocs.io <https://pillow.readthedocs.io/en/stable/reference/Image.html>`_
   * - Python 公式ドキュメント（ ``tkinter`` モジュール）
     - `docs.python.org <https://docs.python.org/3/library/tkinter.html>`_
