copy
====

オブジェクトのコピーを作成するためのモジュール。単純な代入 ``b = a`` は同じオブジェクトを指す別名を作るだけだが、``copy`` モジュールを使うと実体そのものを複製できる。複製の深さによって ``copy()``\ （浅いコピー）と ``deepcopy()``\ （深いコピー）を使い分ける。

copy() による浅いコピー
--------------------------

``copy.copy()`` は新しいオブジェクトを作成するが、その中身がリストや辞書などのミュータブルなオブジェクトである場合、内部の要素までは複製せず元のオブジェクトと共有する。

.. code-block:: python
   :linenos:

   >>> import copy
   >>> a = [1, 2, [3, 4]]
   >>> b = copy.copy(a)
   >>> b is a
   False
   >>> b[0] = 100
   >>> a
   [1, 2, [3, 4]]

deepcopy() による深いコピー
-------------------------------

``copy.deepcopy()`` はネストされた要素も再帰的にすべて複製する。元のオブジェクトと複製後のオブジェクトが、内部の要素も含めて完全に独立したものになる。

.. code-block:: python
   :linenos:

   >>> a = [1, 2, [3, 4]]
   >>> c = copy.deepcopy(a)
   >>> c[2] is a[2]
   False
   >>> c[2][0] = 999
   >>> a
   [1, 2, [3, 4]]
   >>> c
   [1, 2, [999, 4]]

浅いコピーが問題になる例
--------------------------

浅いコピーでは、ネストしたミュータブルなオブジェクト（リストの中のリストなど）が元のオブジェクトと共有されたままになるため、片方を変更するともう片方にも影響が及んでしまう。

.. code-block:: python
   :linenos:

   >>> original = [1, 2, [3, 4]]
   >>> shallow = copy.copy(original)
   >>> shallow[2].append(5)  # ネストしたリストを変更
   >>> original
   [1, 2, [3, 4, 5]]
   >>> shallow
   [1, 2, [3, 4, 5]]

このように、内側のリストは ``original`` と ``shallow`` の両方から参照されている同一オブジェクトである。ネストした構造を独立に扱いたい場合は ``deepcopy()`` を使う必要がある。

.. note::

   イミュータブルな要素（数値や文字列など）だけで構成されたリストの場合は、浅いコピーでも実質的に独立したコピーとして扱える。深いコピーが本当に必要かどうかは、扱っているデータの構造次第である。

__copy__ / __deepcopy__ によるコピー処理のカスタマイズ
--------------------------------------------------------------

ファイルハンドルやキャッシュなど、複製すべきでない外部リソースを持つ自作クラスでは、``__copy__``/``__deepcopy__`` メソッドを定義することで、``copy.copy()``/``copy.deepcopy()`` が呼ばれた際の振る舞いを自分で制御できる。

.. code-block:: python
   :linenos:

   class Cache:
       def __init__(self, data):
           self.data = data
           self.connection = object()  # 複製したくない外部リソースの例

       def __deepcopy__(self, memo):
           new = Cache(copy.deepcopy(self.data, memo))
           new.connection = self.connection  # 接続オブジェクトは共有する
           return new

``__deepcopy__`` の引数 ``memo`` は、コピー済みのオブジェクトを記録しておく辞書で、循環参照があっても無限に再帰しないようにするために使われる。内部の要素を ``deepcopy()`` する際は、受け取った ``memo`` をそのまま渡す。

copy.replace() による一部の属性を変更した複製
------------------------------------------------

Python 3.13 で追加された ``copy.replace()`` は、オブジェクトを複製しつつ、指定した属性だけを新しい値に置き換える。dataclass や ``collections.namedtuple``、``datetime`` オブジェクトなど、``__replace__()`` メソッドを実装した型で使える。特に、属性を直接変更できないイミュータブルなオブジェクトから「一部だけ異なるもの」を作りたい場合に便利である。

.. code-block:: python
   :linenos:

   >>> from dataclasses import dataclass
   >>> @dataclass(frozen=True)
   ... class Point:
   ...     x: int
   ...     y: int
   ...
   >>> p = Point(1, 2)
   >>> copy.replace(p, x=10)
   Point(x=10, y=2)
   >>> p
   Point(x=1, y=2)
