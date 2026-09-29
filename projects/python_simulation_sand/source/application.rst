アプリケーション層: SandGUI.py
================================

``SandGUI`` は、:doc:`widgets` で解説した ``TkWidget`` の部品と ``FrameSand`` を組み合わせて、1つの操作可能なアプリケーションに仕立てるクラスです。4層構成の中で最も上位に位置し、他のすべての層を利用します。

.. note::

   実際のファイル名は ``SandGUI.pyw`` です(拡張子 ``.pyw``)。Windows ではこの拡張子のファイルをダブルクリックすると、コンソール画面を表示せずに実行されます。

画面の構成
----------

.. literalinclude:: ../script/SandGUI.pyw
   :language: python
   :pyobject: SandGUI.__init__

コンストラクタでは、次の部品を配置しています。

- ``self.scale``: 色相・彩度を選ぶ ``FrameScale`` を2つ(``"hue"`` と ``"saturation"``)
- ``self.size_selector``: グリッドサイズを選ぶ ``FrameRadioButton``
- ``self.button``: start / stop / reset / color の4つのボタン

配置後、``set_size()`` と ``set_color()`` を呼び出して、グリッドサイズを既定値に、色相をランダムな値にリセットしてから画面を表示します。

シミュレーションの開始・停止
------------------------------

.. literalinclude:: ../script/SandGUI.pyw
   :language: python
   :pyobject: SandGUI.start

``start()`` が呼ばれると、``start`` ボタンを無効化して ``stop`` ボタンを有効化したうえで、選択されているグリッドサイズ・色相・彩度をもとに新しい ``SandImage`` を作成します。次に、新しい別ウィンドウ(``Toplevel``)を開き、そこに ``FrameSand`` を配置してアニメーションを開始します。

1セルあたりの表示ピクセル数(``pixel``)は ``DISPLAY_SIZE // wh`` で計算されます。例えば ``DISPLAY_SIZE`` が 512 でグリッドサイズが 128 の場合、``pixel`` は 4 になり、常に一辺 512 ピクセルの画像として表示されます。

.. literalinclude:: ../script/SandGUI.pyw
   :language: python
   :pyobject: SandGUI.stop

``stop()`` は、開いている ``Toplevel`` が存在すればそれを破棄します。ウィンドウが破棄されると Tkinter の ``<Destroy>`` イベントが発生し、次に説明する ``_on_destroy()`` が呼ばれてボタンの状態が元に戻ります。

ウィンドウを閉じたときの状態管理
----------------------------------

.. literalinclude:: ../script/SandGUI.pyw
   :language: python
   :pyobject: SandGUI._on_destroy

``start()`` の中で ``self.top.bind("<Destroy>", self._on_destroy)`` を登録しているため、``stop`` ボタンから ``self.top.destroy()`` を呼んだ場合だけでなく、ユーザーがウィンドウのタイトルバーの閉じるボタンで直接ウィンドウを閉じた場合でも、``_on_destroy()`` が呼ばれて ``start`` / ``stop`` ボタンの有効・無効が正しく戻ります。``event.widget is self.top`` の確認は、``self.top`` の子ウィジェットが破棄されたときにも ``<Destroy>`` イベントが発生することへの対策です。

リセット・色変更
----------------

.. literalinclude:: ../script/SandGUI.pyw
   :language: python
   :pyobject: SandGUI.set_size

.. literalinclude:: ../script/SandGUI.pyw
   :language: python
   :pyobject: SandGUI.set_color

``set_size()`` はグリッドサイズの選択を既定値(``DISPLAY_SIZE // 2``)に戻します。``set_color()`` は色相をランダムな値に、彩度を既定値(``0.875``)に戻します。いずれも実行中のシミュレーションには影響せず、次回 ``start()`` が呼ばれたときの初期値を変更するだけです。

エントリーポイント: main()
----------------------------

.. literalinclude:: ../script/SandGUI.pyw
   :language: python
   :pyobject: main

``python SandGUI.pyw`` として実行された場合(あるいは Windows でダブルクリックされた場合)、``tk.Tk()`` でルートウィンドウを作成し、``SandGUI`` を配置してイベントループ(``root.mainloop()``)を開始します。

クラス・メソッドのシグネチャ一覧は :doc:`api` を参照してください。
