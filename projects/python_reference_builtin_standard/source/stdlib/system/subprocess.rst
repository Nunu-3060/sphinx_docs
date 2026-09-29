subprocess
==========

新しいプロセスを生成し、外部コマンドを実行してその入出力や終了コードを
扱うためのモジュール。シェルコマンドを Python から呼び出したい場合の
標準的な手段となる。

subprocess.run
--------------

外部コマンドを実行し、完了を待ってから結果を返す最も基本的な関数。
引数はコマンド名と引数を分けたリストで渡すのが標準的な方法。

.. code-block:: python

   >>> import subprocess
   >>> result = subprocess.run(["echo", "hello"])
   hello
   >>> result.returncode
   0

capture_output / text
-----------------------

``capture_output=True`` を指定すると標準出力・標準エラー出力をキャプチャできる。``text=True`` を併用すると、結果が ``bytes`` ではなく ``str`` として得られる。

.. code-block:: python

   >>> import subprocess
   >>> result = subprocess.run(
   ...     ["echo", "hello"],
   ...     capture_output=True,
   ...     text=True,
   ... )
   >>> result.stdout
   'hello\n'
   >>> result.stderr
   ''

check=True
----------

``check=True`` を指定すると、コマンドが 0 以外の終了コードで終了した
場合に ``subprocess.CalledProcessError`` 例外が送出される。エラーの
見落としを防ぐため、本番コードでは指定しておくことが望ましい。

.. code-block:: python

   >>> import subprocess
   >>> try:
   ...     subprocess.run(["false"], check=True)
   ... except subprocess.CalledProcessError as e:
   ...     print(f"コマンドが失敗しました: returncode={e.returncode}")
   コマンドが失敗しました: returncode=1

timeout（タイムアウト）
--------------------------

``run`` に ``timeout`` 引数で秒数を指定すると、コマンドがその時間内に終了
しなかった場合に ``subprocess.TimeoutExpired`` 例外が送出される。
応答が返ってこない外部コマンドに処理をブロックされ続けないようにする
ために使う。

.. code-block:: python

   >>> import subprocess
   >>> try:
   ...     subprocess.run(["ping", "-c", "10", "localhost"], timeout=1)  # doctest: +SKIP
   ... except subprocess.TimeoutExpired as e:
   ...     print(f"タイムアウトしました: {e}")  # doctest: +SKIP
   タイムアウトしました: Command '['ping', '-c', '10', 'localhost']' timed out after 1 seconds

input による標準入力の送信
------------------------------

サブプロセスの標準入力にデータを渡したい場合、``Popen`` でパイプを手動で管理しなくても、文字列（``text=True`` の場合）またはバイト列を ``run`` の ``input`` 引数に渡すだけで、そのまま標準入力として送り込める。

.. code-block:: python

   >>> import subprocess
   >>> result = subprocess.run(
   ...     ["python", "-c", "import sys; print(sys.stdin.read().strip().upper())"],
   ...     input="hello\n",
   ...     text=True,
   ...     capture_output=True,
   ... )
   >>> result.stdout
   'HELLO\n'

subprocess.Popen によるストリーミング処理
--------------------------------------------

``run`` はコマンドの完了を待って結果をまとめて返すのに対し、``Popen`` を使うとプロセスを起動したまま、出力を逐次読み取ることができる。実行に時間がかかるコマンドの進捗をリアルタイムに扱いたい場合に使う。

.. code-block:: python

   >>> import subprocess
   >>> proc = subprocess.Popen(
   ...     ["ping", "-c", "3", "localhost"],
   ...     stdout=subprocess.PIPE,
   ...     text=True,
   ... )
   >>> for line in proc.stdout:  # doctest: +SKIP
   ...     print(line, end="")
   >>> proc.wait()  # doctest: +SKIP
   0

.. note::

   出力をリアルタイムに逐次処理する必要がなく、コマンドの完了を待って
   まとめて出力を受け取るだけでよい場合は、``proc.stdout`` を手動で
   イテレートするよりも ``Popen.communicate()`` を使う方が簡単で安全
   （デッドロックの回避など）である。実質的には ``subprocess.run`` の
   内部でも ``communicate()`` が使われている。

   .. code-block:: python

      >>> proc = subprocess.Popen(
      ...     ["echo", "hello"],
      ...     stdout=subprocess.PIPE,
      ...     text=True,
      ... )
      >>> stdout, stderr = proc.communicate()
      >>> stdout
      'hello\n'

.. warning::

   ``shell=True`` を指定すると、コマンド全体をシェル経由で実行できる反面、文字列にユーザー入力をそのまま埋め込むとシェルインジェクションの脆弱性につながる。外部からの入力を含むコマンドを実行する場合は、``shell=True`` を避け、引数をリストで渡す方法を使うこと。

   .. code-block:: python

      # 危険な例: ユーザー入力をそのまま結合している
      filename = "data.txt; rm -rf /"
      subprocess.run(f"cat {filename}", shell=True)  # doctest: +SKIP

      # 安全な例: リストで渡すためシェルを介さない
      subprocess.run(["cat", filename])  # doctest: +SKIP
