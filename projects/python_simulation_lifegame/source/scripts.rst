==============
スクリプト一覧
==============

本資料で解説に用いるスクリプトの一覧である。各スクリプトは、ファイル名のリンクからダウンロードできるほか、本ページ内でソースコード全体を確認できる。

utility.py
==========

``hsv2rgb`` 関数を提供する共通ユーティリティモジュール。他のどのモジュールにも依存せず、:file:`LifeGameImage.py` と :file:`TkWidget.py` の双方から利用される。

:download:`ダウンロード <../script/utility.py>`

.. literalinclude:: ../script/utility.py
   :language: python
   :linenos:

LifeGame.py
===========

ライフゲームの中核となるロジックを実装したモジュール。格子の状態（``lattice``）の保持、近傍セル数の計算、次世代への更新（:meth:`~LifeGame.LifeGame.next`）、周期境界条件・固定境界条件の切り替えを行う。

:download:`ダウンロード <../script/LifeGame.py>`

.. literalinclude:: ../script/LifeGame.py
   :language: python
   :linenos:

LifeGameImage.py
=================

``LifeGame`` を継承し、格子の状態を色付き画像（PIL の :class:`~PIL.Image.Image` および Tkinter 表示用の :class:`~PIL.ImageTk.PhotoImage`）として出力する機能を追加したモジュール。配色に用いる ``hsv2rgb`` 関数は :file:`utility.py` からインポートして利用している。

:download:`ダウンロード <../script/LifeGameImage.py>`

.. literalinclude:: ../script/LifeGameImage.py
   :language: python
   :linenos:

FrameLifeGame.py
=================

``LifeGameImage`` が生成する画像を Tkinter の ``ttk.Frame`` 上に表示し、一定間隔ごとに次世代へ自動更新するウィジェットを実装したモジュール。

:download:`ダウンロード <../script/FrameLifeGame.py>`

.. literalinclude:: ../script/FrameLifeGame.py
   :language: python
   :linenos:

TkWidget.py
============

GUI アプリケーションで使用する各種入力ウィジェット（色相・彩度・明度の指定、誕生条件・生存条件のチェックボックス、境界条件の切り替え、盤面サイズの選択、初期生存確率のスケールなど）を実装したモジュール。

:download:`ダウンロード <../script/TkWidget.py>`

.. literalinclude:: ../script/TkWidget.py
   :language: python
   :linenos:

LifeGameGUI.pyw
================

上記の各モジュールを組み合わせ、ルール・色・境界条件・盤面サイズなどを GUI 上で設定してライフゲームを実行できるアプリケーション本体。

:download:`ダウンロード <../script/LifeGameGUI.pyw>`

.. literalinclude:: ../script/LifeGameGUI.pyw
   :language: python
   :linenos:

参考スクリプト
================

以下は、GUI アプリケーション本体では使用しないが、:doc:`summary` の「さらなる高速化」で触れている高速化の検討に使われた参考スクリプトである。

LifeGame_scipy.py
------------------

``LifeGame`` の近傍セル数計算を ``np.roll`` の代わりに ``scipy.signal.convolve2d`` で行う代替実装。クラス名・インターフェースは ``LifeGame.py`` と同一である。

:download:`ダウンロード <../script/LifeGame_scipy.py>`

.. literalinclude:: ../script/LifeGame_scipy.py
   :language: python
   :linenos:

lifegame_fullHD_0001.py
-------------------------

``LifeGame.py`` （``np.roll`` 版）と ``LifeGame_scipy.py`` （``convolve2d`` 版）とで、盤面サイズを変えながら処理速度を比較するベンチマークスクリプト。

:download:`ダウンロード <../script/lifegame_fullHD_0001.py>`

.. literalinclude:: ../script/lifegame_fullHD_0001.py
   :language: python
   :linenos:

lifegame_fullHD_0000.py
-------------------------

``LifeGame`` でフル HD 解像度のシミュレーションを実行し、各セルが生存していた世代数の割合を明度に変換して 1 枚の静止画として書き出すスクリプト。

:download:`ダウンロード <../script/lifegame_fullHD_0000.py>`

.. literalinclude:: ../script/lifegame_fullHD_0000.py
   :language: python
   :linenos:
