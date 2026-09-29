GUI 部品層: TkWidget.py / FrameSand.py
========================================

GUI 部品層には、``Sand`` / ``SandImage`` に依存しない汎用的な Tkinter 部品(``TkWidget``)と、``SandImage`` を一定間隔で更新しながら表示し続けるフレーム(``FrameSand``)が含まれます。いずれも :doc:`application` で解説する ``SandGUI`` から利用されます。

TkWidget.py
-----------

``TkWidget`` は、``ttk.Frame`` を継承した2つの汎用部品を提供するモジュールです。``Sand`` / ``SandImage`` を一切 import しておらず、独立した部品としてどんな Tkinter アプリケーションからでも再利用できます。

FrameRadioButton: グリッドサイズの選択
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../script/TkWidget.py
   :language: python
   :pyobject: FrameRadioButton

既定値 512 の ``DISPLAY_SIZE`` を基準に、``DISPLAY_SIZE // 4`` / ``DISPLAY_SIZE // 2`` / ``DISPLAY_SIZE`` の3つの選択肢をラジオボタンとして表示します。選択された値は ``tk.IntVar`` で保持され、``get()`` / ``set()`` で読み書きできます。

FrameScale: 0.0〜1.0 の値の選択
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../script/TkWidget.py
   :language: python
   :pyobject: FrameScale

``0.0`` 〜 ``1.0`` の範囲のスライダー(``ttk.Scale``)と、その値を表示するラベルをまとめた部品です。コンストラクタに渡した ``text`` がラベルの見出しとして使われ(例:``"hue"`` や ``"saturation"``)、スライダーを動かすたびに ``apply()`` が呼ばれてラベルの表示が更新されます。:doc:`application` では、この部品を色相用・彩度用に2つ生成して使っています。

FrameSand.py
------------

``FrameSand`` は ``SandImage`` のインスタンスを1つ保持し、Tkinter の ``after`` によるタイマーで一定間隔ごとに更新・再描画し続けるフレームです。

アニメーションの仕組み
~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../script/FrameSand.py
   :language: python
   :pyobject: FrameSand.__init__

.. literalinclude:: ../script/FrameSand.py
   :language: python
   :pyobject: FrameSand.next

コンストラクタは、渡された(または新規作成した)``SandImage`` から最初の画像を取得してラベルに表示したあと、``self.after(self.interval, self.next)`` で ``interval`` ミリ秒後に ``next()`` を呼ぶよう予約します。``next()`` は ``SandImage.next()`` で高さ場を1ステップ進め、新しい画像に差し替えたあと、自分自身を再び ``after`` で予約し直します。これにより、``next()`` が延々と呼ばれ続けるアニメーションループが実現されています。

ウィジェット破棄時の後始末
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../script/FrameSand.py
   :language: python
   :pyobject: FrameSand._on_destroy

``after`` で予約したタイマーは、ウィジェットが破棄されても自動的にはキャンセルされません。もしキャンセルせずに放置すると、``FrameSand`` が含まれるウィンドウを閉じたあとにタイマーが発火し、すでに存在しないラベルを更新しようとしてエラーになってしまいます。

これを防ぐため、コンストラクタで ``self.bind("<Destroy>", self._on_destroy)`` を登録し、ウィジェットが破棄される直前に呼ばれる ``_on_destroy()`` の中で ``self.after_cancel(self._after_id)`` を呼び、予約中のタイマーを確実にキャンセルしています。``next()`` が自分自身を再予約するたびに ``self._after_id`` を更新しているのも、常に「今まさに予約されているタイマー」を正しくキャンセルできるようにするためです。

クラス・メソッドのシグネチャ一覧は :doc:`api` を参照してください。
