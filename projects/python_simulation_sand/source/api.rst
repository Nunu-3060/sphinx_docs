API リファレンス
==================

各モジュールのクラス・関数のシグネチャ一覧です。処理内容の詳しい解説は :doc:`model` / :doc:`visualization` / :doc:`widgets` / :doc:`application` を参照してください。

.. note::

   見出しの ``[source]`` リンクから、各モジュールのソースコードをブラウザ上でそのまま閲覧できます。また、各モジュールの見出しの下にあるリンクからスクリプトファイル自体をダウンロードできます。

モデル層
--------

:download:`Sand.py をダウンロード <../script/Sand.py>`

.. automodule:: Sand
   :members:

可視化層
--------

:download:`SandImage.py をダウンロード <../script/SandImage.py>`

.. automodule:: SandImage
   :members:

GUI 部品層
----------

:download:`TkWidget.py をダウンロード <../script/TkWidget.py>`

.. automodule:: TkWidget
   :members:

:download:`FrameSand.py をダウンロード <../script/FrameSand.py>`

.. automodule:: FrameSand
   :members:

アプリケーション層
------------------

:download:`SandGUI.pyw をダウンロード <../script/SandGUI.pyw>`

.. automodule:: SandGUI
   :members:

バッチ実行用スクリプト
-----------------------

GUI を起動せずに、フルHD相当の画像を1枚生成して保存するスクリプトです。上記の4層構成には含まれず、``SandImage`` を直接利用する独立したエントリポイントという位置付けです。

:download:`sand_fullHD_0000.py をダウンロード <../script/sand_fullHD_0000.py>`

.. automodule:: sand_fullHD_0000
   :members:
