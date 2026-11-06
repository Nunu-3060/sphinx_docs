venv
====

Python に標準で付属する、軽量な仮想環境を作成するためのモジュール。プロジェクトごとに独立した Python 実行環境・パッケージ群を用意することで、異なるプロジェクト間での依存パッケージのバージョン衝突を防ぐ。

仮想環境の作成
--------------

``python -m venv`` コマンドに続けてディレクトリ名を指定すると、その場所に新しい仮想環境が作成される。作成されたディレクトリには、Python 本体への参照や ``pip``、専用の ``site-packages`` などが含まれる。Python 3.13 以降では、仮想環境のディレクトリ内に、その中身全体を Git の管理対象から外す ``.gitignore`` も自動的に作成される。

.. code-block:: text
   :linenos:

   $ python -m venv myenv

仮想環境の有効化
----------------

作成しただけでは仮想環境は使われない。有効化（activate）することで、シェルの ``PATH`` が書き換えられ、``python`` や ``pip`` コマンドが仮想環境内のものを指すようになる。有効化スクリプトは OS によって呼び出し方が異なる。

.. code-block:: text
   :linenos:

   # Windows (コマンドプロンプト)
   myenv\Scripts\activate

   # Windows (PowerShell)
   myenv\Scripts\Activate.ps1

   # macOS / Linux
   source myenv/bin/activate

有効化すると、以降その端末で実行する ``python`` や ``pip`` は、システムに直接インストールされたものではなく仮想環境内のものが優先される。``deactivate`` コマンドを実行すると有効化が解除される。

なお、有効化は必須ではない。``myenv/bin/python``\ （Windows では ``myenv\Scripts\python.exe``）のように仮想環境内のインタプリタをパスで直接実行しても、その仮想環境が使われる。スクリプトや CI から利用する場合はこの方法が便利である。

仮想環境が分離するもの
----------------------

仮想環境は、それぞれ独自の ``site-packages``\ （サードパーティパッケージのインストール先）を持つ。そのため、仮想環境内で ``pip install`` を実行しても、システム全体の Python 環境や他のプロジェクトの仮想環境には一切影響しない。プロジェクトごとに異なるバージョンのライブラリを使い分けたい場合や、環境を汚さずに試したいパッケージがある場合に有用。

.. code-block:: text
   :linenos:

   (myenv) $ pip install requests
   (myenv) $ pip list
   Package            Version
   ------------------ ---------
   certifi            2025.10.5
   charset-normalizer 3.4.4
   idna               3.11
   pip                25.3
   requests           2.32.5
   urllib3            2.5.0

``requests`` が依存するパッケージも、仮想環境の ``site-packages`` に一緒にインストールされている（バージョンは実行時期によって異なる）。

venv.create
-----------

シェルコマンドとしてだけでなく、Python コードから仮想環境を作成することもできる。``with_pip=True`` を指定すると、作成した仮想環境に ``pip`` も同時にインストールされる。

.. code-block:: python
   :linenos:

   >>> import venv
   >>> venv.create("myenv", with_pip=True)  # doctest: +SKIP

より詳細な制御が必要な場合は ``EnvBuilder`` クラスを使う。こちらは ``create`` のオプションをまとめて指定するだけでなく、サブクラス化して仮想環境作成後の処理をカスタマイズすることもできる。

.. code-block:: python
   :linenos:

   >>> from venv import EnvBuilder
   >>> builder = EnvBuilder(with_pip=True, clear=True)
   >>> builder.create("myenv")  # doctest: +SKIP

.. note::

   ``venv`` は Python 本体に同梱されているため、原則として追加のインストール作業なしにすぐ使える（ただし Debian / Ubuntu などのシステム付属の Python では、``python3-venv`` パッケージを別途インストールする必要がある場合がある）。一方、サードパーティの ``virtualenv`` はより古い Python のバージョンにも対応しており、動作も高速な場合が多い。また、Poetry や uv のようなプロジェクト管理ツールは、仮想環境の作成・管理に加えて依存パッケージのバージョン固定やビルド・公開まで一括で扱えるが、その分ツール自体の学習コストが必要になる。
