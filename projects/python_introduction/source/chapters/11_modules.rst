第 11 章 モジュールとパッケージ
===============================

モジュールとは
--------------

モジュールとは、関数やクラスなどをまとめて記述した、1 つの Python ファイルのことである。処理を複数のファイルに分けて整理することで、コードの見通しがよくなり、他のプログラムからも再利用しやすくなる。

標準ライブラリのインポート
--------------------------

Python には、あらかじめ多くのモジュールが標準ライブラリとして用意されている。標準ライブラリのモジュールを利用するには、``import`` 文を使用する。

.. code-block:: python
   :linenos:

   import math

   print(math.sqrt(16))  # 4.0
   print(math.pi)         # 3.141592653589793

モジュールの中から特定の関数だけを取り出してインポートしたい場合は、``from`` を使用する。

.. code-block:: python
   :linenos:

   from math import sqrt

   print(sqrt(16))  # 4.0

自作モジュールの作成
--------------------

自分で作成した Python ファイルも、モジュールとしてインポートできる。次のような ``rectangle.py`` というファイルがあるとする。

.. code-block:: python
   :linenos:

   # rectangle.py
   def calculate_area(width: float, height: float) -> float:
       return width * height

同じフォルダにある別のファイルからは、次のようにインポートして利用できる。

.. code-block:: python
   :linenos:

   from rectangle import calculate_area

   print(calculate_area(4.0, 3.0))  # 12.0

パッケージとは
--------------

パッケージとは、複数のモジュールをフォルダにまとめたものである。パッケージとして扱うフォルダには、``__init__.py`` という名前のファイルを置く。``__init__.py`` はパッケージが読み込まれたときに実行されるファイルで、パッケージ内のモジュールをまとめて公開する役割を持たせることもできる。

``__init__.py`` の中から、同じパッケージ内にある別のモジュールをインポートする場合は、次のようにモジュール名の前に ``.`` を付ける。

.. code-block:: python
   :linenos:

   # shapes/__init__.py
   from .rectangle import calculate_area

先頭の ``.`` は、同じパッケージの中を指す相対インポートという書き方である。パッケージの外にある ``main.py`` などから ``shapes`` パッケージをインポートするときは、これまでどおり ``from shapes import calculate_area`` のように ``.`` を付けずに書く。

``__init__.py`` では、次のように ``__all__`` という変数を定義することもある。

.. code-block:: python
   :linenos:

   # shapes/__init__.py
   from .rectangle import calculate_area

   __all__ = ["calculate_area"]

``__all__`` は、そのパッケージを外部に公開する際の一覧を表すリストである。``__init__.py`` の中で ``import`` した関数やクラスは、そのままでは「読み込んだだけで使われていない」と誤って判断されることがあるが、``__all__`` に名前を含めておくことで、それらが意図的に外部へ公開されていることを明示できる。

外部ライブラリのインストール（pip）
-----------------------------------

標準ライブラリに含まれていない機能を利用したい場合は、外部ライブラリをインストールして使用する。第 2 章で確認した ``pip`` は、この外部ライブラリをインストールするためのツールである。次のコマンドを実行すると、指定した名前の外部ライブラリ（この例では、Web へのアクセスを簡単にする ``requests``）をインストールできる。

.. code-block:: console

   $ python -m pip install requests

インストールした外部ライブラリは、標準ライブラリや自作モジュールと同じように、``import`` 文で読み込んで利用できる。第 1 章で紹介した Web アプリケーション開発やデータ分析用のライブラリも、``pip`` を使ってインストールしたうえで利用する。

仮想環境（venv）
----------------

外部ライブラリをパソコン全体の Python に直接インストールすると、プログラムごとに必要なライブラリやそのバージョンが異なる場合に、互いに影響し合ってしまう。また、macOS や Linux の環境によっては、OS が管理する Python を保護するために、``pip`` によるインストールがエラー（``externally-managed-environment``）になることがある。

そのため、外部ライブラリを使う場合は、標準ライブラリの ``venv`` モジュールで仮想環境を作成し、その中にインストールするのが一般的である。仮想環境とは、プログラムごとに独立したライブラリの置き場所を持つ Python の実行環境である。次のコマンドを実行すると、現在のフォルダに ``.venv`` という名前のフォルダが作成され、その中に仮想環境が用意される。

.. code-block:: console

   $ python -m venv .venv

作成した仮想環境を使うには、仮想環境を有効にする（アクティベートする）。有効にするコマンドは OS によって異なる。

.. code-block:: console

   $ .venv\Scripts\activate

上記は Windows の場合である。macOS や Linux では、次のコマンドを実行する。

.. code-block:: console

   $ source .venv/bin/activate

仮想環境を有効にすると、コマンドラインの先頭に ``(.venv)`` と表示される。この状態で ``python -m pip install`` を実行すると、外部ライブラリは仮想環境の中にインストールされ、パソコン全体の Python には影響しない。仮想環境での作業を終えるときは、``deactivate`` コマンドを実行する。

なお、本資料のサンプルコードは標準ライブラリだけを使用しているため、仮想環境を作成しなくても実行できる。

サンプルコード
--------------

長方形の面積と周囲の長さを計算する ``shapes`` パッケージと、それを利用する ``main.py`` のサンプルコードである。次の 3 つのファイルを、下記のフォルダ構成のとおりに保存する。

.. code-block:: text

   ch11_modules/
   ├── main.py
   └── shapes/
       ├── __init__.py
       └── rectangle.py

:download:`main.py <../../examples/ch11_modules/main.py>`
:download:`shapes/__init__.py <../../examples/ch11_modules/shapes/__init__.py>`
:download:`shapes/rectangle.py <../../examples/ch11_modules/shapes/rectangle.py>`

main.py
^^^^^^^

.. literalinclude:: ../../examples/ch11_modules/main.py
   :language: python3
   :linenos:

shapes/__init__.py
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../examples/ch11_modules/shapes/__init__.py
   :language: python3
   :linenos:

shapes/rectangle.py
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../examples/ch11_modules/shapes/rectangle.py
   :language: python3
   :linenos:

上記のファイルを同じフォルダ構成のまま保存し、``main.py`` があるフォルダで ``python main.py`` を実行すると、``shapes`` パッケージの関数を利用した計算結果が表示される。
