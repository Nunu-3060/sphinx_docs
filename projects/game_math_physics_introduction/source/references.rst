付録 C 参考文献
===============

本書の内容をさらに詳しく学ぶための文献と資料を挙げる。ウェブページの内容は 2026 年 10 月時点で確認したものである。

書籍
----

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 文献
     - 内容
   * - Fletcher Dunn, Ian Parberry, *3D Math Primer for Graphics and Game Development*, 2nd ed., CRC Press, 2011.
     - ゲームのためのベクトル・行列・回転（オイラー角、クォータニオン）を丁寧に解説している。第 4 章～第 7 章の発展。オンライン版が `gamemath.com <https://gamemath.com/>`__ で公開されている
   * - Eric Lengyel, *Mathematics for 3D Game Programming and Computer Graphics*, 3rd ed., Course Technology, 2011.
     - 3D のゲームと CG に必要な数学を、証明を含めて網羅的に扱っている
   * - Christer Ericson, *Real-Time Collision Detection*, Morgan Kaufmann, 2004.
     - 衝突判定の定番の書籍。さまざまな形状の組み合わせの判定、分離軸定理、空間分割を詳しく扱っている。第 11 章の発展
   * - Ian Millington, *Game Physics Engine Development*, 2nd ed., Morgan Kaufmann, 2010.
     - 物理エンジンを一から作りながら、剛体の運動と衝突応答を学べる。第 10 章・第 12 章・第 14 章の発展
   * - Robert Nystrom, *Game Programming Patterns*, Genever Benning, 2014.
     - ゲームループ、オブジェクトプールなど、ゲームのプログラムの設計パターン。`Web 版 <https://gameprogrammingpatterns.com/>`__\ が公開されている

講演・論文
----------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 文献
     - 内容
   * - Kyle Pittman, "Math for Game Programmers: Building a Better Jump", Game Developers Conference, 2016.
     - ジャンプの高さと時間から重力と初速を求める方法、下降中の重力の調整など。第 10 章のジャンプの設計のもとになった考え方
   * - Squirrel Eiserloh, "Math for Game Programmers: Juicing Your Cameras With Math", Game Developers Conference, 2016.
     - trauma の 2 乗に比例させた画面の揺れ、ノイズによる揺れなど、カメラの演出の数学。第 9 章・第 15 章
   * - Thomas Jakobsen, "Advanced Character Physics", Game Developers Conference, 2001.
     - 位置ベルレ法と、位置を直接動かして拘束を満たす方法。第 13 章のロープと布のもとになった手法
   * - Ken Perlin, "Improving Noise", ACM Transactions on Graphics, 21(3), 2002.
     - パーリンノイズの改良版。5 次の補間の重み 6t\ :sup:`5` − 15t\ :sup:`4` + 10t\ :sup:`3` が提案された。第 9 章

ウェブ上の資料
--------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 資料
     - 内容
   * - Glenn Fiedler, `Fix Your Timestep! <https://gafferongames.com/post/fix_your_timestep/>`__
     - 固定タイムステップと描画の補間について、最もよく参照される解説。第 3 章
   * - Robert Nystrom, `Game Loop <https://gameprogrammingpatterns.com/game-loop.html>`__\ （*Game Programming Patterns* より）
     - ゲームループと時間の扱い方の比較。第 3 章
   * - `Easing Functions Cheat Sheet <https://easings.net/>`__
     - 代表的なイージング関数のグラフと式の一覧。第 8 章
   * - Amit Patel, `Red Blob Games <https://www.redblobgames.com/>`__
     - ノイズによる地形の生成、グリッド、経路探索などを、動かせる図で解説している。第 9 章、第 15 章の「次のステップ」
   * - `pygame-ce のドキュメント <https://pyga.me/docs/>`__
     - 本書のサンプルコードで使った pygame-ce の公式ドキュメント
   * - `pymunk のドキュメント <https://www.pymunk.org/>`__
     - 第 14 章で使った pymunk の公式ドキュメント
   * - `Box2D <https://box2d.org/>`__
     - 2D の物理エンジン Box2D の公式サイト。作者の Erin Catto による物理エンジンの講演資料も公開されている。第 14 章
   * - `random — 擬似乱数を生成する <https://docs.python.org/ja/3/library/random.html>`__\ （Python のドキュメント）
     - Python の擬似乱数の使い方。第 9 章

関連する文書
------------

本書の範囲から外れる内容や、前提となる内容は、次の文書で扱っている。

- 「ゲーム作成入門」: ゲーム制作の全体の流れ（企画、エンジンの選定、アセット、公開）
- 「コンピューターグラフィックス入門」: 3D の描画の仕組み
- 「線形代数入門」: ベクトルと行列の数学的な理論
- 「Python 入門」: 本書のサンプルコードを読むための Python の基礎
