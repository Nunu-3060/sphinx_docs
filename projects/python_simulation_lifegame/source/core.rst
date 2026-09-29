=====================================
コアロジックの実装（LifeGame.py）
=====================================

本章では、ライフゲームの中核となる :class:`~LifeGame.LifeGame` クラス（:download:`LifeGame.py <../script/LifeGame.py>`）の実装を解説する。

格子の表現と初期化
===================

格子の状態は、``height`` × ``width`` の 2 次元 NumPy 配列 ``self.lattice`` として表現される。各要素は 0（死）または 1（生）の値を取り、型は ``int64`` である。

.. code-block:: python

   self.lattice: np.typing.NDArray[np.int64] = np.zeros((height, width), dtype=np.int64)
   self.lattice[rng.random(size=self.lattice.shape) < probability] = 1

``np.random.Generator.random`` によって各セルに独立な一様乱数を割り当て、``probability`` を下回った位置のセルを「生」として初期化している。ループを使わず、配列全体に対する比較演算と一括代入だけで初期状態を生成している点がポイントである。

また、コンストラクタの ``rule`` 引数には誕生・生存条件のリストを渡す。

.. code-block:: python

   if rule is None:
       rule = [[3], [2, 3]]
   self.rule: list[list[int]] = rule

``rule`` は ``[誕生条件, 生存条件]`` という形式のリストであり、既定値 ``[[3], [2, 3]]`` は後述する標準的なライフゲームのルール（誕生: 3、生存: 2 または 3）に対応する。この形式にすることで、標準ルール以外の任意のセルオートマトンルールも表現できるようになっている。

近傍セル数の計算
=================

格子を次世代に進める処理は :meth:`~LifeGame.LifeGame.next` メソッドが担う。ここから 2 節にわたって、``next`` メソッドの内部処理を順に見ていく。

各セルの次の状態は、8 近傍（ムーア近傍）に存在する生きたセルの数によって決まる。素朴に実装するとセルごとにループを回して近傍を数える必要があるが、本実装では ``np.roll`` を使うことで、ループを使わずに格子全体の近傍セル数を一括計算している。

.. code-block:: python

   neighbour: np.typing.NDArray[np.int64] = (
       np.roll(self.lattice, shift=(-1, -1), axis=(0, 1)) +
       np.roll(self.lattice, shift=( 1, -1), axis=(0, 1)) +
       np.roll(self.lattice, shift=(-1,  1), axis=(0, 1)) +
       np.roll(self.lattice, shift=( 1,  1), axis=(0, 1)) +
       np.roll(self.lattice, shift=( 0, -1), axis=(0, 1)) +
       np.roll(self.lattice, shift=( 0,  1), axis=(0, 1)) +
       np.roll(self.lattice, shift=(-1,  0), axis=(0, 1)) +
       np.roll(self.lattice, shift=( 1,  0), axis=(0, 1))
   )

``np.roll(self.lattice, shift=(di, dj), axis=(0, 1))`` は、格子全体を縦方向に ``di``、横方向に ``dj`` だけずらした配列を返す。これを 8 方向すべてについて足し合わせることで、各セル位置における「8 近傍の生存セル数」を、格子全体について一度に得ることができる。この処理では、Python レベルのループを 8 近傍分（=8回）しか使わない。残りの計算はすべて NumPy の C 実装に委ねられるため、格子サイズが大きくなってもループで実装する場合に比べて高速に動作する。

ルールの適用
=============

近傍セル数 ``neighbour`` が求まったら、``self.rule`` に従って次世代の格子を構築する。

.. code-block:: python

   lattice: np.typing.NDArray[np.int64] = np.zeros_like(self.lattice)
   for i, neighbour_counts in enumerate(self.rule):
       b: np.typing.NDArray[np.bool] = self.lattice == i
       for j in neighbour_counts:
           lattice[b & (neighbour == j)] = 1
   self.lattice = lattice

外側のループの添字 ``i`` は現在のセルの状態（0: 死、1: 生）に対応し、``neighbour_counts`` はその状態のセルが次世代で「生」になるために必要な近傍セル数のリストである。内側のループでは、``self.lattice == i`` （現在の状態が ``i`` である位置）と ``neighbour == j`` （近傍セル数がちょうど ``j`` である位置）の論理積を取り、該当するセルを新しい格子で「生」にする。

既定値 ``rule = [[3], [2, 3]]`` の場合、

* ``i = 0`` （死んでいるセル）: 近傍が 3 のとき誕生する
* ``i = 1`` （生きているセル）: 近傍が 2 または 3 のとき生存する

となり、これは標準的なライフゲームのルールである :math:`B3/S23` （:doc:`theory` を参照）と一致する。すべての更新が更新前の ``self.lattice`` と ``neighbour`` のみを参照して行われ、最後にまとめて ``self.lattice`` を置き換えることで、:doc:`theory` で述べた同期更新を実現している。

境界条件の実装
===============

格子の端のセルは、8 近傍の一部が格子の外側にはみ出す。``np.roll`` は配列を循環的にずらすため、何も手を加えなければ上端の外側は下端、左端の外側は右端とみなされ、格子全体がトーラス状の周期境界条件になる。

固定境界条件（外側を常に「死」とみなす条件）を再現したい場合は、コンストラクタの ``tb`` （top-bottom）・``lr`` （left-right）引数を ``False`` に指定する。

.. code-block:: python

   if not tb:
       def deco(func: Callable[[], None]) -> Callable[[], None]:
           self.lattice[0, :] = 0
           self.lattice[-1, :] = 0

           def tmp() -> None:
               func()
               self.lattice[0, :] = 0
               self.lattice[-1, :] = 0
               return None
           return tmp
       self.next = deco(self.next)

   if not lr:
       def deco(func: Callable[[], None]) -> Callable[[], None]:
           self.lattice[:, 0] = 0
           self.lattice[:, -1] = 0

           def tmp() -> None:
               func()
               self.lattice[:, 0] = 0
               self.lattice[:, -1] = 0
               return None
           return tmp
       self.next = deco(self.next)

この ``deco`` 関数は、元の ``next`` メソッドを、実行後に最外周の行（``tb`` の場合）または列（``lr`` の場合）を強制的に 0 にする処理で包むデコレータになっている。``tb`` は行（``self.lattice[0, :]``・``self.lattice[-1, :]``）を、``lr`` は列（``self.lattice[:, 0]``・``self.lattice[:, -1]``）を対象にしている点以外、2 つの ``deco`` は同じ構造である。初期化時に一度、以後は ``next`` が呼ばれるたびに最外周が 0 にリセットされるため、外側は常に死んでいる状態が保たれ、実質的に固定境界条件を模することができる。``tb``・``lr`` はそれぞれ独立に指定できるため、上下だけ、あるいは左右だけを固定境界にするといった組み合わせも可能である。
