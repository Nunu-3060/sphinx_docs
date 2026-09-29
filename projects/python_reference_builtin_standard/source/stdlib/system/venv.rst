venv
====

Python に標準で付属する、軽量な仮想環境を作成するためのモジュール。
プロジェクトごとに独立した Python 実行環境・パッケージ群を用意することで、
異なるプロジェクト間での依存パッケージのバージョン衝突を防ぐ。

仮想環境の作成
--------------

``python -m venv`` コマンドに続けてディレクトリ名を指定すると、その場所に
新しい仮想環境が作成される。作成されたディレクトリには、Python 本体への
参照や ``pip``、専用の ``site-packages`` などが含まれる。

.. code-block:: text

   $ python -m venv myenv

仮想環境の有効化
----------------

作成しただけでは仮想環境は使われない。有効化（activate）することで、
シェルの ``PATH`` が書き換えられ、``python`` や ``pip`` コマンドが
仮想環境内のものを指すようになる。有効化スクリプトは OS によって
呼び出し方が異なる。

.. code-block:: text

   # Windows (コマンドプロンプト)
   myenv\Scripts\activate

   # Windows (PowerShell)
   myenv\Scripts\Activate.ps1

   # macOS / Linux
   source myenv/bin/activate

有効化すると、以降その端末で実行する ``python`` や ``pip`` は、
システムに直接インストールされたものではなく仮想環境内のものが優先される。

仮想環境が分離するもの
----------------------

仮想環境は、それぞれ独自の ``site-packages``（サードパーティパッケージの
インストール先）を持つ。そのため、仮想環境内で ``pip install`` を実行
しても、システム全体の Python 環境や他のプロジェクトの仮想環境には
一切影響しない。プロジェクトごとに異なるバージョンのライブラリを
使い分けたい場合や、環境を汚さずに試したいパッケージがある場合に有用。

.. code-block:: text

   (myenv) $ pip install requests
   (myenv) $ pip list
   Package    Version
   ---------- -------
   pip        24.0
   requests   2.31.0

venv.create
-----------

シェルコマンドとしてだけでなく、Python コードから仮想環境を作成することもできる。``with_pip=True`` を指定すると、作成した仮想環境に ``pip`` も同時にインストールされる。

.. code-block:: python

   >>> import venv
   >>> venv.create("myenv", with_pip=True)  # doctest: +SKIP

より詳細な制御が必要な場合は ``EnvBuilder`` クラスを使う。こちらは ``create`` のオプションをまとめて指定するだけでなく、サブクラス化して仮想環境作成後の処理をカスタマイズすることもできる。

.. code-block:: python

   >>> from venv import EnvBuilder
   >>> builder = EnvBuilder(with_pip=True, clear=True)
   >>> builder.create("myenv")  # doctest: +SKIP

.. note::

   ``venv`` は Python 本体に同梱されているため、追加のインストール作業なしにすぐ使える。一方、サードパーティの ``virtualenv`` はより古い Python のバージョンにも対応しており、動作も高速な場合が多い。また、Poetry や uv のようなプロジェクト管理ツールは、仮想環境の作成・管理に加えて依存パッケージのバージョン固定やビルド・公開まで一括で扱えるが、その分ツール自体の学習コストが必要になる。
