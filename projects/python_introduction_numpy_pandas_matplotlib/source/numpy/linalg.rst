線形代数（np.linalg）
========================

numpy には、線形代数（ベクトルや行列に関する計算）のための機能が ``np.linalg`` モジュールにまとめられています。ここでは、内積・行列積、逆行列、行列式、連立一次方程式の解法という基本的なトピックを紹介します。

内積・行列積
--------------

ベクトルの内積は ``np.dot`` で計算できます。

.. code-block:: python

   import numpy as np

   a: np.ndarray = np.array([1, 2, 3])
   b: np.ndarray = np.array([4, 5, 6])

   np.dot(a, b)
   # 32  1*4 + 2*5 + 3*6

行列（2 次元配列）に対して ``np.dot`` を使うと、行列積（行列の掛け算）になります。これは「:doc:`operations`」で紹介した ``@`` 演算子と同じ結果です。

.. code-block:: python

   A: np.ndarray = np.array([[1, 2], [3, 4]])
   B: np.ndarray = np.array([[5, 6], [7, 8]])

   np.dot(A, B)
   # array([[19, 22],
   #        [43, 50]])

   A @ B
   # array([[19, 22],
   #        [43, 50]])
   # np.dot(A, B) と同じ結果

.. note::

   ベクトル同士では ``np.dot`` は内積になりますが、行列同士では行列積になります。行列に対して行列積を計算したいという意図が明確な場合は、``np.dot`` よりも ``@`` 演算子（または ``np.matmul``）を使う方が読みやすいコードになります。

逆行列
--------

正方行列（行数と列数が同じ行列）に対して、掛け合わせると単位行列（対角成分が 1 で他が 0 の行列）になる行列を「逆行列」と呼びます。逆行列は ``np.linalg.inv`` で計算できます。

.. code-block:: python

   A: np.ndarray = np.array([[1, 2], [3, 4]])

   np.linalg.inv(A)
   # array([[-2. ,  1. ],
   #        [ 1.5, -0.5]])

   A @ np.linalg.inv(A)
   # array([[1.0000000e+00, 0.0000000e+00],
   #        [8.8817842e-16, 1.0000000e+00]])
   # 単位行列に近い結果になる（浮動小数点演算の誤差でわずかにずれる）

.. note::

   逆行列を持たない行列（後述する行列式が 0 になる行列）に対して ``np.linalg.inv`` を呼び出すと、``numpy.linalg.LinAlgError`` が発生します。

行列式
--------

正方行列から計算される、行列の性質を表す 1 つの数値を「行列式」と呼びます。行列式は ``np.linalg.det`` で計算できます。

.. code-block:: python

   A: np.ndarray = np.array([[1, 2], [3, 4]])

   np.linalg.det(A)
   # -2.0000000000000004  浮動小数点演算の誤差で -2 からわずかにずれる

行列式が 0 になる行列は逆行列を持ちません。``np.linalg.inv`` を使う前に行列式を確認する、という使い方もできます。

連立一次方程式を解く
----------------------

``np.linalg.solve`` を使うと、連立一次方程式を解くことができます。たとえば次の連立方程式を考えます。

.. math::

   \begin{cases}
   2x + y = 5 \\
   x + 3y = 10
   \end{cases}

この方程式は、係数を行列 ``Aeq``、右辺の値をベクトル ``beq`` として ``Aeq @ x = beq`` の形で表せます。

.. code-block:: python

   Aeq: np.ndarray = np.array([[2, 1], [1, 3]])
   beq: np.ndarray = np.array([5, 10])

   x: np.ndarray = np.linalg.solve(Aeq, beq)
   print(x)
   # [1. 3.]  x = 1, y = 3

   Aeq @ x
   # array([ 5., 10.])  元の式に戻ることを確認できる

``np.linalg.solve(Aeq, beq)`` は、逆行列を使って ``np.linalg.inv(Aeq) @ beq`` と書いても同じ結果になりますが、``solve`` を使った方が計算効率がよく、数値誤差も小さくなるため、連立方程式を解く場合は ``solve`` を使うことが推奨されます。
