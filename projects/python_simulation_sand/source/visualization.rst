可視化層: SandImage.py
========================

``SandImage`` は :doc:`model` で解説した ``Sand`` を継承し、高さ場を Pillow (PIL) の画像に変換するクラスです。継承しているため、高さ場の更新ロジック(``next()``)はそのまま ``Sand`` のものを利用し、``SandImage`` は「画像に変換する」機能だけを追加しています。

配色の初期化
------------

.. literalinclude:: ../script/SandImage.py
   :language: python
   :pyobject: SandImage.__init__

コンストラクタでは、``Sand`` のコンストラクタ(``L0`` / ``b`` / ``q`` / ``D`` / ``seed`` / ``width`` / ``height``)をそのまま呼び出したうえで、画像化のために次の3つを準備します。

- ``self.image_size``: ``pixel`` 倍に拡大した出力画像サイズ(``(pixel * width, pixel * height)``)。1セルを ``pixel`` × ``pixel`` の正方形として描画するための拡大率です。
- ``self.hue`` / ``self.saturation``: 色相(Hue)・彩度(Saturation)を格子全体(``(height, width, 3)`` の配列)に敷き詰めたもの。``hue`` に ``None`` を渡すとランダムな色相が選ばれます。彩度は ``numpy.clip`` で必ず ``[0, 1]`` の範囲に収められます。
- ``self.phase_offsets``: 後述する HSV → RGB 変換で使う、R・G・B 各チャンネルごとの位相のずれです。

色相・彩度はどちらも画像全体で一定値であり、セルごとに変化するのは高さ場(明度に対応する値)だけです。したがって、砂山が高いセルほど明るく、低いセルほど暗く表示されます。色相・彩度が空間分布を持たないにも関わらず ``(height, width, 3)`` の配列として保持しているのは、次で説明する HSV → RGB 変換をベクトル化して実装するためです。

画像への変換: image_np()
-------------------------

.. literalinclude:: ../script/SandImage.py
   :language: python
   :pyobject: SandImage.image_np

このメソッドは、高さ場を RGB の画素値(``uint8`` の NumPy 配列)に変換します。

明度の正規化
~~~~~~~~~~~~

まず、そのときの高さ場の最小値・最大値を使って、明度(Value)を ``[0, 1]`` に正規化します。

.. math::

   v_{i,j} = \frac{h_{i,j} - h_{\min}}{h_{\max} - h_{\min}}

高さ場が完全に一様で ``h_max == h_min`` となる場合は 0 除算になってしまうため、その場合は明度を一律 0 として扱います。

HSV から RGB への変換
~~~~~~~~~~~~~~~~~~~~~~

色相 :math:`H` ・彩度 :math:`S` ・明度 :math:`V` から RGB の各チャンネル :math:`c \in \{R, G, B\}` を求める計算式は、次のように実装されています。

.. math::
   :nowrap:

   \begin{align*}
   p_c &= \bigl|\, \mathrm{frac}(H + o_c) \times 6 - 3 \,\bigr| \\
   c   &= V \times \Bigl( \bigl(\mathrm{clip}(p_c - 1,\ 0,\ 1) - 1\bigr) \times S + 1 \Bigr)
   \end{align*}

ここで :math:`o_c` は ``self.phase_offsets`` にあらかじめ設定してあるチャンネルごとの位相のずれで、:math:`o_R = 0` 、:math:`o_G = 2/3` 、:math:`o_B = 1/3` です。この式は、一般的な HSV → RGB 変換をシェーダー向けに整理した式(GPU のシェーダーコードでよく使われる形)をそのまま NumPy でベクトル化したものです。

計算された値は最後に ``numpy.clip`` で ``[0, 1]`` に収め、255 倍して ``uint8`` に変換することで、通常の RGB 画素値になります。

PIL 画像・Tkinter 画像への変換
--------------------------------

.. literalinclude:: ../script/SandImage.py
   :language: python
   :pyobject: SandImage.image_pil

.. literalinclude:: ../script/SandImage.py
   :language: python
   :pyobject: SandImage.image_tk

``image_pil()`` は ``image_np()`` の結果を ``PIL.Image`` に変換したうえで、``self.image_size`` まで最近傍補間(``Image.Resampling.NEAREST``)で拡大します。最近傍補間を使っているのは、1セルを1色のくっきりした正方形として表示するためです(平滑化されたぼやけた拡大にはなりません)。

``image_tk()`` は、さらにそれを Tkinter で表示できる ``ImageTk.PhotoImage`` に変換します。この戻り値が、:doc:`widgets` で解説する ``FrameSand`` から利用されます。

クラス・メソッドのシグネチャ一覧は :doc:`api` を参照してください。
