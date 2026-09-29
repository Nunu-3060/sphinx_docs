========================================
可視化の実装（LifeGameImage.py）
========================================

本章では、:class:`~LifeGame.LifeGame` を継承して格子の状態を色付き画像として可視化する :class:`~LifeGameImage.LifeGameImage` クラス（:download:`LifeGameImage.py <../script/LifeGameImage.py>`）の実装を解説する。

セルの配色
===========

生きたセルと死んだセルをそれぞれ異なる色で表示するため、色相（hue）・彩度（saturation）・明度（value）で色を指定できる ``hsv2rgb`` 関数を、共通ユーティリティモジュール :download:`utility.py <../script/utility.py>` に用意している。``LifeGameImage.py`` だけでなく、後述する :doc:`gui` の :class:`~TkWidget.FrameHSV` からも同じ関数が利用される。

.. code-block:: python

   def hsv2rgb(
       h: np.typing.NDArray[np.float64] | float,
       s: np.typing.NDArray[np.float64] | float,
       v: np.typing.NDArray[np.float64] | float,
   ) -> np.typing.NDArray[np.uint8]:
       phase_offsets: np.typing.NDArray[np.float64]
       rgb: np.typing.NDArray[np.float64]
       if isinstance(h, float) and isinstance(s, float) and isinstance(v, float):
           phase_offsets = np.array([0, 2/3, 1/3], np.float64)
           rgb = ((np.clip(np.abs(np.mod(h + phase_offsets, 1) * 6 - 3) - 1, 0, 1) - 1) * s + 1) * v
       elif isinstance(h, np.ndarray) and isinstance(s, np.ndarray) and isinstance(v, np.ndarray):
           if h.shape != s.shape or h.shape != v.shape:
               raise TypeError("adjust the array lengths to be the same.")
           elif len(h.shape) != 2:
               raise TypeError("input 2D numpy array.")
           phase_offsets = np.zeros((h.shape[0], h.shape[1], 3), np.float64)
           phase_offsets[:, :, 1] = 2 / 3
           phase_offsets[:, :, 2] = 1 / 3
           hue: np.typing.NDArray[np.float64] = h[:, :, None]
           saturate: np.typing.NDArray[np.float64] = s[:, :, None]
           value: np.typing.NDArray[np.float64] = v[:, :, None]
           rgb = ((np.clip(np.abs(np.mod(hue + phase_offsets, 1) * 6 - 3) - 1, 0, 1) - 1) * saturate + 1) * value
       else:
           text: str = "\n".join([
               "h, s, and v must all be float or np.ndarray.",
               f"h: {type(h).__name__}",
               f"s: {type(s).__name__}",
               f"v: {type(v).__name__}",
           ])
           raise TypeError(text)
       rgb = np.clip(rgb, 0, 1)
       return (rgb * 255).round(0).astype(np.uint8)

一般的な HSV→RGB 変換は場合分けを伴う実装になることが多い。これに対し、この関数は色相・彩度・明度それぞれの値ごとの場合分けを行わず、R・G・B の 3 成分を色相環上で 120°（=2/3, 1/3）ずつずらした位相として一括に計算する閉形式の式になっている。``np.mod`` で色相の周期性を扱い、``np.clip`` で各成分を三角波状の波形に整形することで、単一の数式で 3 チャンネル分の RGB 値を同時に得ている。``h``・``s``・``v`` には ``float`` のほか、同じ形状の 2 次元 ``np.ndarray`` をまとめて渡すこともでき、この場合は格子と同じ形状の RGB 画像を一括で計算できる（形状が一致しない場合や 2 次元でない場合は ``TypeError`` になる）。``h``・``s``・``v`` の型が ``float`` と ``np.ndarray`` で混在している場合や、それ以外の型が渡された場合も同様に ``TypeError`` を送出する。

:class:`~LifeGameImage.LifeGameImage` のコンストラクタでは、生存色・死滅色が指定されなかった場合、ランダムに選んだ色相をもとに、同じ色相で明度だけが異なる 2 色（死滅色 ``c0`` を暗めに、生存色 ``c1`` を明るめに）を自動生成する。

.. code-block:: python

   if c0 is None or c1 is None:
       rng: np.random.Generator = np.random.default_rng()
       hue: float = float(rng.random())
       saturation: float = 0.875
       value: float = 0.875
       c0 = hsv2rgb(hue, saturation, 1-value)
       c1 = hsv2rgb(hue, saturation, value)

これにより、実行するたびに配色が変化しつつも、生存セルと死滅セルの色相は揃っているため統一感のある表示になる。

画像への変換
=============

コンストラクタでは、画像化用の RGB 配列 ``self.image_array`` （``height`` × ``width`` × 3 の ``uint8`` 配列）を ``np.zeros`` で、拡大後の画像サイズ ``self.image_size`` （``pixel`` 倍した ``(width, height)``）をあらかじめ用意している。格子の状態から実際の画像を生成する処理は、配列生成を担う ``image_np`` メソッドと、それを Pillow 画像に変換する ``image_pil`` メソッドの 2 段階に分かれている。

.. code-block:: python

   def image_np(self) -> np.typing.NDArray[np.uint8]:
       self.image_array[self.lattice == 0] = self.c0
       self.image_array[self.lattice == 1] = self.c1
       return self.image_array

   def image_pil(self) -> Image.Image:
       im: Image.Image = Image.fromarray(self.image_np())
       return im.resize(self.image_size, resample=Image.Resampling.NEAREST)

まず ``image_np`` が、``height`` × ``width`` × 3（RGB）の ``uint8`` 配列 ``self.image_array`` に対して、格子が 0 のセルには死滅色 ``c0``、1 のセルには生存色 ``c1`` をブールインデックスで一括代入し、格子と同じ解像度の RGB 配列を返す。次に ``image_pil`` が、``Image.fromarray`` によってこの NumPy 配列から Pillow の :class:`~PIL.Image.Image` を生成し、``resize`` で ``self.image_size`` に拡大する。補間方式に ``NEAREST`` （最近傍補間）を指定しているため、セル同士の境界がぼやけることなく、1 セル 1 マスのドット絵のような見た目になる。``image_np`` を独立したメソッドとして切り出しているため、Pillow 画像を経由せず NumPy 配列そのものを利用したい場合にも流用できる。

最後に、Tkinter 上で画像を表示するために ``image_tk`` メソッドで Tkinter 用の :class:`~PIL.ImageTk.PhotoImage` に変換する。

.. code-block:: python

   def image_tk(self) -> ImageTk.PhotoImage:
       return ImageTk.PhotoImage(self.image_pil())

この ``image_tk`` メソッドは、:doc:`gui` で解説する :class:`~FrameLifeGame.FrameLifeGame` から、世代が更新されるたびに呼び出される。
