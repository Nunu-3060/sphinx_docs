付録 B 数式のまとめ
===================

本資料で使った主な数式を、章ごとにまとめる。ベクトルの記号の意味は、第 9 章の表と同じである。

ベクトルと行列（第 2 章）
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 名前
     - 式
   * - ベクトルの長さ
     - :math:`|\mathbf{a}| = \sqrt{a_x^2 + a_y^2 + a_z^2}`
   * - 正規化
     - :math:`\mathrm{normalize}(\mathbf{a}) = \mathbf{a} / |\mathbf{a}|`
   * - 内積
     - :math:`\mathbf{a} \cdot \mathbf{b} = a_x b_x + a_y b_y + a_z b_z = |\mathbf{a}| |\mathbf{b}| \cos\theta`
   * - 外積
     - :math:`\mathbf{a} \times \mathbf{b} = (a_y b_z - a_z b_y,\ a_z b_x - a_x b_z,\ a_x b_y - a_y b_x)`
   * - 線形補間
     - :math:`\mathrm{lerp}(a, b, t) = a + (b - a) t`
   * - smoothstep
     - :math:`t = \mathrm{saturate}((x - a) / (b - a))` として :math:`3t^2 - 2t^3`

座標変換（第 3 章）
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 名前
     - 式
   * - モデル変換の行列
     - :math:`M = T R S`
   * - MVP 変換
     - :math:`\mathbf{p}_{CS} = P V M \mathbf{p}_{OS}`
   * - 透視除算
     - :math:`\mathbf{p}_{NDC} = (x / w,\ y / w,\ z / w)`
   * - 法線の変換
     - :math:`\mathbf{n}' = (M^{-1})^{\mathsf{T}} \mathbf{n}`

ライティング（第 9 章）
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 名前
     - 式
   * - Lambert 反射
     - :math:`I_{diffuse} = C_{base} \, C_{light} \max(0,\ \mathbf{N} \cdot \mathbf{L})`
   * - Half Lambert
     - :math:`I_{diffuse} = C_{base} \, C_{light} ((\mathbf{N} \cdot \mathbf{L}) / 2 + 1 / 2)^2`
   * - 反射ベクトル
     - :math:`\mathbf{R} = 2(\mathbf{N} \cdot \mathbf{L})\mathbf{N} - \mathbf{L}`
   * - Phong 反射
     - :math:`I_{specular} = C_{specular} \, C_{light} \max(0,\ \mathbf{R} \cdot \mathbf{V})^{s}`
   * - ハーフベクトル
     - :math:`\mathbf{H} = \mathrm{normalize}(\mathbf{L} + \mathbf{V})`
   * - Blinn-Phong 反射
     - :math:`I_{specular} = C_{specular} \, C_{light} \max(0,\ \mathbf{N} \cdot \mathbf{H})^{s}`
   * - 環境光
     - :math:`I_{ambient} = C_{base} \, C_{SH}(\mathbf{N})`
   * - 合計
     - :math:`I = I_{ambient} + I_{diffuse} + I_{specular}`

法線マップ（第 10 章）
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 名前
     - 式
   * - 法線の色への変換
     - :math:`(r, g, b) = (\mathbf{n} + 1) / 2`
   * - 従法線
     - :math:`\mathbf{B} = (\mathbf{N} \times \mathbf{T}) \, w`
   * - 接空間からワールド空間への変換
     - :math:`\mathbf{n}_{WS} = n_x \mathbf{T} + n_y \mathbf{B} + n_z \mathbf{N}`

透明（第 12 章）
----------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 名前
     - 式
   * - ブレンドの一般形
     - :math:`C = C_{src} \times F_{src} + C_{dst} \times F_{dst}`
   * - アルファブレンド
     - :math:`C = C_{src} \, \alpha_{src} + C_{dst} (1 - \alpha_{src})`

頂点アニメーション（第 13 章）
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 名前
     - 式
   * - 波の変位
     - :math:`y = A \sin(f x + s t)`
   * - 波の傾き
     - :math:`dy / dx = A f \cos(f x + s t)`
   * - 波の法線
     - :math:`\mathbf{n} = \mathrm{normalize}(-dy / dx,\ 1,\ 0)`

表現テクニックとポストエフェクト（第 14 章、第 15 章）
------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 名前
     - 式
   * - リムライト
     - :math:`I_{rim} = C_{rim} \, (1 - \max(0,\ \mathbf{N} \cdot \mathbf{V}))^{p}`
   * - Schlick の近似式
     - :math:`F = F_0 + (1 - F_0)(1 - \mathbf{N} \cdot \mathbf{V})^5`
   * - 輝度（ITU-R BT.709）
     - :math:`Y = 0.2126 R + 0.7152 G + 0.0722 B`
