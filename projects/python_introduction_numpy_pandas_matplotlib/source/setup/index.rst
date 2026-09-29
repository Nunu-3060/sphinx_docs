環境構築
========

numpy、pandas、matplotlib を使い始めるための環境構築について説明します。

前提条件
--------

あらかじめ Python がインストールされている必要があります。`Python 公式サイト <https://www.python.org/>`_\ から Windows 用インストーラを入手してインストールしてください。インストーラの「Install launcher for all users (recommended)」は既定でチェックが入っており、これにより以降の手順で使用する ``py`` コマンド（py ランチャー）が有効になります。

.. code-block:: console

   > py --version

上記のコマンドでバージョンが表示されれば、Python は正しくインストールされています。

.. note::

   Python 3.10 は EOL（サポート終了）が近づいているため、これから環境を構築する場合は Python 3.11 以降のバージョンを利用することを推奨します。本ドキュメントのサンプルコードも、Python 3.11 以降での動作を前提としています。

pip を使ったインストール
-------------------------

Python のパッケージ管理ツール ``pip`` を使って、必要なライブラリをまとめてインストールします。

.. code-block:: console

   > py -m pip install numpy pandas matplotlib

インストールが完了したら、以下のコマンドで各ライブラリのバージョンを確認できます。

.. code-block:: console

   > py -c "import numpy; print(numpy.__version__)"
   > py -c "import pandas; print(pandas.__version__)"
   > py -c "import matplotlib; print(matplotlib.__version__)"

仮想環境の利用（推奨）
----------------------

プロジェクトごとに独立した環境を作るため、仮想環境の利用を推奨します。

.. code-block:: console

   > py -m venv .venv
   > .venv\Scripts\activate
   (.venv) > py -m pip install numpy pandas matplotlib

動作確認
--------

以下のスクリプトが正しく実行できれば、環境構築は完了です。

.. code-block:: python

   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt

   arr: np.ndarray = np.array([1, 2, 3])
   df: pd.DataFrame = pd.DataFrame({"a": [1, 2, 3]})

   print(arr)
   print(df)
