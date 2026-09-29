======================================
GUI アプリケーションの実装
======================================

本章では、Tkinter を用いた GUI 部分の実装を解説する。GUI は、入力ウィジェット（:file:`TkWidget.py`）、シミュレーション表示ウィジェット（:file:`FrameLifeGame.py`）、それらを統合するアプリケーション本体（:file:`LifeGameGUI.pyw`）の 3 つのモジュールから構成される。

部品ウィジェット（TkWidget.py）
=================================

:download:`TkWidget.py <../script/TkWidget.py>` には、シミュレーションのパラメータを指定するための、いずれも ``ttk.Frame`` を継承した専用ウィジェットが定義されている。各ウィジェットは、現在の設定値を取得する ``get`` メソッドと、外部から値を設定する ``set`` メソッドを持つという共通のインターフェースになっており、後述する :class:`~LifeGameGUI.LifeGameGUI` から統一的に扱えるようになっている。

* **FrameHSV**: 色相・彩度・明度をそれぞれスライダーで指定する。現在の色を 16 進コードのテキストとしてラベルに表示し、背景色にはその色そのものを、文字色には視認性を保つための反転色（1-h, 1-s, 1-v）を用いる。生存色・死滅色の指定に用いる。
* **FrameCheckbuttons**: 0〜8 の近傍セル数に対応する 9 個のチェックボタンを持ち、誕生条件・生存条件（:doc:`core` の ``rule`` 引数に相当）を指定する。
* **FrameLoop**: 上下（``tb``）・左右（``lr``）それぞれの境界をトーラス境界にするかどうかを切り替えるチェックボタンを持つ。
* **FrameRadioButton**: 盤面の一辺のサイズ（128 / 256 / 512）をラジオボタンで選択する。これらの選択肢は :data:`~TkWidget.DISPLAY_SIZE` （既定 512）の 1/4, 1/2, 1 倍として導出されている。
* **FrameScale**: セルの初期生存確率（0.0〜1.0）をスライダーで指定する。

いずれも、コンストラクタ内でウィジェットを生成・配置したうえで、スライダーやチェックボタンの変更イベントに応じて表示を更新する、という共通の構造になっている。

表示フレームとアニメーション（FrameLifeGame.py）
====================================================

:download:`FrameLifeGame.py <../script/FrameLifeGame.py>` の :class:`~FrameLifeGame.FrameLifeGame` は、:class:`~LifeGameImage.LifeGameImage` が生成する画像を表示し、一定間隔ごとに次の世代へ自動更新する ``ttk.Frame`` である。

.. code-block:: python

   self.image: ImageTk.PhotoImage = self.lifegameimage.image_tk()
   self.label: ttk.Label = ttk.Label(self, image=self.image)
   self.label.pack()
   self.interval: int = interval

   self._after_id: str | None = None
   self.bind("<Destroy>", self._on_destroy)
   self._after_id = self.after(self.interval, self.next)

表示には ``ttk.Label`` の ``image`` オプションを用いる。アニメーションは、Tkinter の ``after(ms, callback)`` による定期実行で実現している。``next`` メソッドの内部で ``LifeGameImage.next()`` を呼んで世代を進め、新しい画像でラベルを更新したあと、再び ``self.after(self.interval, self.next)`` を呼び出して自分自身を予約する。これにより、``next`` が自身を ``interval`` ミリ秒後の実行として繰り返し予約し続ける、コールバックベースのループが構成される（スタックを積む一般的な再帰とは異なり、Tkinter のイベントループが都度呼び出しをスケジューリングする点に注意）。

.. code-block:: python

   def next(self) -> None:
       self.lifegameimage.next()
       self.image = self.lifegameimage.image_tk()
       self.label.configure(image=self.image)
       self._after_id = self.after(self.interval, self.next)
       return None

Tkinter の ``after`` によるループは、ウィジェットが破棄された後も予約されたコールバックが呼ばれ続けてしまう問題が起きやすい。本実装では、ウィジェット自身の ``<Destroy>`` イベントに ``_on_destroy`` をバインドし、破棄時に ``after_cancel`` で予約中のコールバックを解除することで、この問題を防いでいる。

.. code-block:: python

   def _on_destroy(self, event: tk.Event) -> None:
       if event.widget is self and self._after_id is not None:
           self.after_cancel(self._after_id)
           self._after_id = None
       return None

アプリケーション統合（LifeGameGUI.pyw）
==========================================

:download:`LifeGameGUI.pyw <../script/LifeGameGUI.pyw>` の :class:`~LifeGameGUI.LifeGameGUI` は、これまでのウィジェット群を組み合わせて 1 つのアプリケーションにまとめる。

レイアウトは ``frame`` 辞書（``color``・``rule``・``loop``・``button``）で大きく 4 つの領域に分割され、各領域に対応するウィジェットが配置される。生存色・死滅色用に 2 つの :class:`~TkWidget.FrameHSV`、誕生条件・生存条件用に 2 つの :class:`~TkWidget.FrameCheckbuttons` を、それぞれ辞書で保持している。

初期値の設定は ``set_rule``・``set_color`` の 2 つのメソッドが担う。

.. code-block:: python

   def set_rule(self) -> None:
       self.rule["birth"].set([3])
       self.rule["survive"].set([2, 3])
       self.loop.set(tb=True, lr=True)
       self.size_selector.set(DISPLAY_SIZE // 2)
       self.scale.set(0.3)
       return None

これは、``LifeGame`` の既定ルール ``[[3], [2, 3]]`` （:doc:`core` を参照）と対応する初期値であり、「reset」ボタンから呼び出すことで標準ルールに戻せるようになっている。

シミュレーションの開始は ``start`` メソッドで行う。

.. code-block:: python

   def start(self) -> None:
       ...
       lgi: LifeGameImage = LifeGameImage(
           rule=[self.rule["birth"].get(), self.rule["survive"].get()],
           tb=loop.get("tb", True),
           lr=loop.get("lr", True),
           c0=self.color["dead"].get(),
           c1=self.color["live"].get(),
           width=wh,
           height=wh,
           pixel=pixel,
           probability=self.scale.get(),
       )
       self.top = tk.Toplevel(self)
       self.top.title("Conway's Game of Life")
       self.top.bind("<Destroy>", self._on_top_destroy)
       flg: FrameLifeGame = FrameLifeGame(self.top, lifegameimage=lgi)
       flg.pack()
       return None

各入力ウィジェットから ``get()`` で現在値を取得して :class:`~LifeGameImage.LifeGameImage` を構築し、新しい ``Toplevel`` ウィンドウを開いて、その中に :class:`~FrameLifeGame.FrameLifeGame` を配置する。start/stop ボタンの有効・無効は、ウィンドウの生成・破棄に合わせて切り替えられる。

また、盤面のサイズによらず表示ウィンドウの物理サイズを一定に保つため、``pixel = DISPLAY_SIZE // wh`` として拡大率を算出している（:data:`~TkWidget.DISPLAY_SIZE` を参照）。

最後に、モジュール直接実行時のエントリポイントとして ``main`` 関数が定義されている。

.. code-block:: python

   def main() -> None:
       root: tk.Tk = tk.Tk()
       root.title("Conway's Game of Life")
       LifeGameGUI(root).pack()
       root.mainloop()
       return None


   if __name__ == "__main__":
       main()

ルートウィンドウ上に :class:`~LifeGameGUI.LifeGameGUI` を配置し、``mainloop()`` によってイベントループを開始することで、アプリケーション全体が起動する。
