乱数生成
========

サンプルデータの作成や動作確認の際、乱数を使うと便利です。numpy では ``np.random.default_rng`` で乱数生成器を作成して利用します。

.. code-block:: python

   import numpy as np

   rng: np.random.Generator = np.random.default_rng(seed=0)

``seed`` を指定すると、実行するたびに同じ乱数列を再現できます。

代表的な乱数生成
------------------

.. code-block:: python

   rng.integers(0, 10, size=5)
   # 0 以上 10 未満の整数を 5 個生成
   # array([8, 6, 5, 2, 3])

   rng.random(size=3)
   # 0.0 以上 1.0 未満の浮動小数点数を 3 個生成
   # array([0.01652764, 0.81327024, 0.91275558])

   rng.normal(loc=0, scale=1, size=5)
   # 平均 0、標準偏差 1 の正規分布に従う乱数を 5 個生成

``size`` にタプルを渡すことで、多次元配列を直接生成することもできます。

.. code-block:: python

   rng.integers(0, 10, size=(2, 3))
   # array([[0, 6, 0],
   #        [3, 8, 5]])

要素の抽出・並び替え
----------------------

既存の配列から要素をランダムに抽出したり、順序をランダムに並び替えたりする機能も用意されています。

.. code-block:: python

   rng.choice([1, 2, 3, 4, 5], size=3)
   # array([1, 4, 4])
   # 配列からランダムに 3 個を選ぶ（既定では重複あり）

   rng.choice(5, size=3, replace=False)
   # array([0, 2, 4])
   # 0〜4 の整数から重複なしで 3 個を選ぶ（replace=False）

   a: np.ndarray = np.array([1, 2, 3, 4, 5])
   rng.shuffle(a)
   print(a)
   # [3 5 4 1 2]  a 自体を並び替える（戻り値はない）

   rng.permutation(5)
   # array([3, 2, 0, 1, 4])
   # 0〜4 を並び替えた新しい配列を返す（元の配列は変更しない）

``shuffle`` は配列そのものを直接並び替える（元の配列が変更される）のに対し、``permutation`` は並び替えた新しい配列を返す点が異なります。元のデータを残しておきたい場合は ``permutation`` を使ってください。

.. note::

   古い numpy のコードでは、``np.random.seed()`` で乱数のシードを設定し、``np.random.rand()`` や ``np.random.randint()`` のように ``np.random`` モジュールの関数を直接呼び出す書き方も見られます。この書き方は現在も動作しますが、numpy の公式ドキュメントでは、このページで紹介している ``np.random.default_rng()`` で生成した ``Generator`` オブジェクト（``rng``）を使う書き方が推奨されています。``Generator`` を使うと、乱数生成器を変数として明示的に持てるため、複数の場所で乱数を使うコードでも挙動を管理しやすくなります。新しくコードを書く場合は、``default_rng`` の方を使うようにしてください。
