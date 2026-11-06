argparse
========

コマンドラインインタフェースを構築するためのモジュール。引数の定義、型変換、デフォルト値、ヘルプメッセージの自動生成などをまとめて扱える。

argparse.ArgumentParser
-------------------------

引数解析のエントリポイントとなるパーサオブジェクトを生成する。``description`` にはプログラムの説明を指定でき、``--help`` オプション実行時に表示される。

.. code-block:: python
   :linenos:

   >>> import argparse
   >>> parser = argparse.ArgumentParser(description="ファイルをコピーするツール")

位置引数とオプション引数
--------------------------

``add_argument`` で引数を定義する。``-`` や ``--`` から始まらない名前は必須の位置引数となり、``-`` や ``--`` から始まる名前（``-v`` や ``--verbose`` など）は省略可能なオプション引数となる。

なお、対話モードで ``add_argument`` を実行すると、戻り値の ``Action`` オブジェクト（``_StoreAction(...)`` など）が表示されるが、本ページの例では省略している。

.. code-block:: python
   :linenos:

   >>> parser.add_argument("src", help="コピー元のパス")
   >>> parser.add_argument("dst", help="コピー先のパス")
   >>> parser.add_argument("--verbose", help="詳細な出力を行う")
   >>> args = parser.parse_args(["a.txt", "b.txt"])
   >>> args.src, args.dst
   ('a.txt', 'b.txt')

type と default
-----------------

``type`` を指定すると、コマンドラインの文字列を自動的に指定した型へ変換する。``default`` は引数が省略された場合に使われる値。

.. code-block:: python
   :linenos:

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument("--count", type=int, default=1, help="繰り返し回数")
   >>> args = parser.parse_args([])
   >>> args.count
   1
   >>> args = parser.parse_args(["--count", "5"])
   >>> args.count
   5

action="store_true"
----------------------

真偽値のフラグ引数を扱う場合に指定する。オプションが指定されると ``True``、指定されなければ ``False`` になり、値を別途渡す必要がない。

.. code-block:: python
   :linenos:

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument("--verbose", action="store_true", help="詳細ログを表示")
   >>> args = parser.parse_args([])
   >>> args.verbose
   False
   >>> args = parser.parse_args(["--verbose"])
   >>> args.verbose
   True

parse_args
----------

コマンドライン引数を解析し、結果を ``Namespace`` オブジェクトとして返す。通常は ``sys.argv`` を暗黙的に参照するため、スクリプト内では引数を省略して呼び出す。

.. code-block:: python
   :linenos:

   >>> import argparse
   >>> parser = argparse.ArgumentParser(description="足し算を行うツール")
   >>> parser.add_argument("x", type=int)
   >>> parser.add_argument("y", type=int)
   >>> parser.add_argument("--verbose", action="store_true")
   >>> args = parser.parse_args(["3", "4", "--verbose"])
   >>> args.x + args.y
   7
   >>> args.verbose
   True

.. note::

   実際のスクリプトでは ``args = parser.parse_args()`` のように呼び出し、``sys.argv`` の内容（``sys.argv[1:]``）を自動的に解析させるのが一般的である。

choices と required
----------------------

オプション引数には ``choices`` で受け付ける値の集合を指定できる。また ``required=True`` を指定すると、（オプション引数であっても）その指定を必須にすることができる。いずれの条件も満たさない場合、``parse_args`` はエラーメッセージを表示してプログラムを終了させる。

.. code-block:: python
   :linenos:

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument("--mode", choices=["fast", "slow"], required=True)
   >>> args = parser.parse_args(["--mode", "fast"])
   >>> args.mode
   'fast'
   >>> parser.parse_args(["--mode", "medium"])  # doctest: +SKIP
   usage: prog.py [-h] --mode {fast,slow}
   prog.py: error: argument --mode: invalid choice: 'medium' (choose from 'fast', 'slow')

add_subparsers によるサブコマンド
--------------------------------------

``git commit`` や ``git push`` のように、1 つのコマンドの下に複数のサブコマンドを持たせたい場合は ``add_subparsers()`` を使う。それぞれのサブコマンドは独立した ``ArgumentParser`` として扱われ、個別に引数を定義できる。

.. code-block:: python
   :linenos:

   >>> parser = argparse.ArgumentParser(prog="mytool")
   >>> subparsers = parser.add_subparsers(dest="command")
   >>>
   >>> add_parser = subparsers.add_parser("add", help="項目を追加する")
   >>> add_parser.add_argument("name")
   >>>
   >>> remove_parser = subparsers.add_parser("remove", help="項目を削除する")
   >>> remove_parser.add_argument("name")
   >>>
   >>> args = parser.parse_args(["add", "apple"])
   >>> args.command, args.name
   ('add', 'apple')
   >>> args = parser.parse_args(["remove", "banana"])
   >>> args.command, args.name
   ('remove', 'banana')

Python 3.14 での変更
--------------------

Python 3.14 では ``ArgumentParser`` に次の変更が加えられている。

- ``color`` 引数（既定値 ``True``）が追加され、端末に出力する場合はヘルプやエラーメッセージが色付きで表示されるようになった。環境変数 ``NO_COLOR`` などで無効化することもできる。
- ``suggest_on_error`` 引数が追加された。``True`` を指定すると、``choices`` やサブコマンド名の入力ミスに対して「もしかして」の候補を提示する（3.14 での既定値は ``False``）。

.. code-block:: python
   :linenos:

   >>> parser = argparse.ArgumentParser(prog="prog.py", suggest_on_error=True)
   >>> parser.add_argument("--mode", choices=["fast", "slow"])
   >>> parser.parse_args(["--mode", "fsat"])  # doctest: +SKIP
   usage: prog.py [-h] [--mode {fast,slow}]
   prog.py: error: argument --mode: invalid choice: 'fsat', maybe you meant 'fast'? (choose from 'fast', 'slow')
