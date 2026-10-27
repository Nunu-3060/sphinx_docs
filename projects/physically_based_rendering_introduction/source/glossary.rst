用語集
======

本書で用いた主な用語を五十音順（英字で始まるものは先頭）にまとめる。括弧内は英語表記（記載のあるもの）と、主に説明している章である。

.. glossary::

   BRDF
      双方向反射率分布関数（Bidirectional Reflectance Distribution Function）。ある方向から入射した光が、別の方向へどれだけ反射されるかを表す関数。単位は 1/sr。（「:doc:`brdf`」）

   BSDF
      反射を表す BRDF と透過を表す BTDF をまとめた関数（Bidirectional Scattering Distribution Function）。（「:doc:`advanced`」）

   GGX
      マイクロファセット理論で使われる法線分布関数の 1 つ。Trowbridge-Reitz 分布とも呼ぶ。裾が長く、実際の材料の測定結果とよく一致する。（「:doc:`microfacet`」）

   HDR
      高ダイナミックレンジ（High Dynamic Range）。ディスプレイで表示できる範囲を超える、広い範囲の明るさを持つこと。（「:doc:`light_and_color`」）

   IBL
      イメージベースドライティング（Image Based Lighting）。全方向の光の分布を記録した環境マップを光源として使う方法。（「:doc:`practical_pbr`」）

   PBR
      物理ベースレンダリング（Physically Based Rendering）。光の放射、反射、伝達を物理法則に基づいてモデル化するレンダリングの考え方。（「:doc:`introduction`」）

   spp
      1 画素あたりのサンプル数（samples per pixel）。パストレーシングでは、1 画素あたりに追跡するパスの本数を指す。（「:doc:`path_tracing`」）

   sRGB
      パソコンやウェブで標準的に使われる色空間。原色、白色点、伝達関数を定める。（「:doc:`light_and_color`」）

   アルベド
      表面に入射した光のうち、反射される光の割合。ある入射方向に対する値を方向アルベドと呼ぶ。（「:doc:`brdf`」）

   拡散反射
      物体の内部で散乱した光が、あらゆる方向にほぼ均等に出ていく反射（diffuse reflection）。物体固有の色が付く。（「:doc:`light_matter`」）

   幾何減衰項
      マイクロファセットが、ほかのマイクロファセットに遮られて光が届かない、あるいは見えない効果を表す項。記号 G。（「:doc:`microfacet`」）

   鏡面反射
      表面で直接反射する光（specular reflection）。誘電体では色が付かず、金属では色が付くことがある。（「:doc:`light_matter`」）

   金属
      内部に自由電子を持ち、内部に入った光をすぐに吸収する物質。導体とも呼ぶ。見た目は表面での反射だけで決まる。（「:doc:`light_matter`」）

   次イベント推定
      パスの各交点で光源上の点を選び、直接届く光を明示的に計算する手法（Next Event Estimation、NEE）。（「:doc:`path_tracing`」）

   重点サンプリング
      被積分関数の値が大きいところを重点的にサンプリングすることで、モンテカルロ積分の分散を減らす手法（importance sampling）。（「:doc:`monte_carlo`」）

   スループット
      パストレーシングで、パスに沿って掛け合わされていく係数（BRDF × cos / 確率密度）の積。（「:doc:`path_tracing`」）

   大域照明
      物体の間での光の相互反射（間接照明）まで含めて計算する照明（global illumination）。（「:doc:`overview`」）

   多重重点サンプリング
      複数のサンプリング手法で得たサンプルを重みを付けて組み合わせる手法（Multiple Importance Sampling、MIS）。（「:doc:`monte_carlo`」）

   トーンマッピング
      HDR の値を、ディスプレイで表示できる範囲の値に変換する処理（tone mapping）。（「:doc:`practical_pbr`」）

   ハーフベクトル
      光源の方向と観測者の方向の中間の方向を表す単位ベクトル。（「:doc:`microfacet`」）

   パストレーシング
      レンダリング方程式を、各交点で方向を 1 つずつ選ぶモンテカルロ積分で解く手法（path tracing）。（「:doc:`path_tracing`」）

   表面下散乱
      物体の内部に入った光が、内部を移動してから入射点と異なる場所から出てくる現象（subsurface scattering）。（「:doc:`light_matter`」）

   フレネル反射率
      境界面に当たった光のうち、反射される光の割合。屈折率と入射角で決まり、浅い角度ほど大きい。（「:doc:`light_matter`」）

   放射輝度
      単位投影面積・単位立体角あたりの放射束（radiance）。単位は W/(m²·sr)。カメラの画素が測る量であり、光線に沿って変化しない。（「:doc:`radiometry`」）

   放射強度
      光源から単位立体角あたりに放たれる放射束（radiant intensity）。主に点光源に対して用いる。単位は W/sr。（「:doc:`radiometry`」）

   放射照度
      表面の単位面積あたりに入射する放射束（irradiance）。単位は W/m²。（「:doc:`radiometry`」）

   放射束
      単位時間あたりに流れる光のエネルギー（radiant flux）。単位は W。（「:doc:`radiometry`」）

   法線分布関数
      マイクロファセットの法線の向きの分布を表す関数（Normal Distribution Function、NDF）。記号 D。（「:doc:`microfacet`」）

   マイクロファセット
      粗い表面を構成するとみなす、微小な鏡面（microfacet）。微小面とも呼ぶ。（「:doc:`microfacet`」）

   メタリック／ラフネスワークフロー
      ベースカラー、メタリック、ラフネスの 3 つのパラメーターで材質を表す PBR のワークフロー。（「:doc:`practical_pbr`」）

   モンテカルロ積分
      乱数を使って積分を推定する手法。誤差はサンプル数の平方根に反比例して減り、その速さは積分の次元によらない。（「:doc:`monte_carlo`」）

   誘電体
      ガラス、水、プラスチックなど、金属以外の物質。表面での反射は弱く色が付かない。（「:doc:`light_matter`」）

   ラフネス
      表面の粗さを表すパラメーター（roughness）。0 が滑らか、1 が粗い。（「:doc:`microfacet`」）

   ランバート BRDF
      どの方向にも同じ値 :math:`\rho / \pi` を持つ BRDF。理想的な拡散反射を表す。（「:doc:`brdf`」）

   立体角
      方向の広がりを表す量。単位球面上の面積で測る。単位はステラジアン（sr）。（「:doc:`radiometry`」）

   リニアワークフロー
      光の計算を線形な値で行い、表示の直前に符号化する手順。（「:doc:`light_and_color`」）

   レイ
      レイトレーシングで追跡する半直線（ray）。始点と方向で表す。（「:doc:`overview`」）

   レンダリング方程式
      ある点から出ていく放射輝度を、自ら放つ光と、入射光を BRDF に従って反射した光の和として表す積分方程式。（「:doc:`rendering_equation`」）

   ロシアンルーレット
      パスを確率的に打ち切り、継続したパスの重みを増やすことで、推定に偏りを生じさせずに計算量を減らす手法。（「:doc:`path_tracing`」）
