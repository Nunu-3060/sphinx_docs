環境構築
========

numpy、pandas、matplotlib を使い始めるための環境構築について説明する。

前提条件
--------

あらかじめ Python がインストールされている必要がある。`Python 公式サイト <https://www.python.org/>`_\ から Windows 用インストーラを入手してインストールすること。インストーラの「Install launcher for all users (recommended)」は既定でチェックが入っており、これにより以降の手順で使用する ``py`` コマンド（py ランチャー）が有効になる。

.. code-block:: console

   > py --version

上記のコマンドでバージョンが表示されれば、Python は正しくインストールされている。

.. note::

   Python 3.10 は 2026 年 10 月に EOL（サポート終了）を迎え、セキュリティ修正も提供されなくなった。これから環境を構築する場合は Python 3.11 以降、できれば最新の安定版を利用すること。なお、Python 3.11 も 2027 年 10 月に EOL を迎える予定である。本ドキュメントのサンプルコードは Python 3.11 以降での動作を前提としており、Python 3.14、numpy 2.5、pandas 3.1、matplotlib 3.11 で動作を確認している。

pip を使ったインストール
-------------------------

Python のパッケージ管理ツール ``pip`` を使って、必要なライブラリをまとめてインストールする。

.. code-block:: console

   > py -m pip install numpy pandas matplotlib

インストールが完了したら、以下のコマンドで各ライブラリのバージョンを確認できる。

.. code-block:: console

   > py -c "import numpy; print(numpy.__version__)"
   > py -c "import pandas; print(pandas.__version__)"
   > py -c "import matplotlib; print(matplotlib.__version__)"

仮想環境の利用（推奨）
----------------------

プロジェクトごとに独立した環境を作るため、仮想環境の利用を推奨する。

.. code-block:: console

   > py -m venv .venv
   > .venv\Scripts\activate
   (.venv) > py -m pip install numpy pandas matplotlib

上の手順はコマンドプロンプトを想定している。PowerShell では ``.venv\Scripts\Activate.ps1`` で仮想環境を有効にする。スクリプトの実行が許可されていないというエラーが出る場合は、``Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`` で実行ポリシーを変更する。

動作確認
--------

以下のスクリプトが正しく実行できれば、環境構築は完了である。

.. code-block:: python

   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt

   arr: np.ndarray = np.array([1, 2, 3])
   df: pd.DataFrame = pd.DataFrame({"a": [1, 2, 3]})

   print(arr)
   print(df)
