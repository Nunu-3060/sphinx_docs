サンプルコード一覧
==================

本資料で使用しているサンプルコードの一覧です。各章のサンプルコードの全文は、表の「全文」の列のリンク先で閲覧でき、そこから 1 ファイルずつダウンロードできます。

すべてのサンプルコードは、zip ファイルにまとめてダウンロードすることもできます。

* :download:`examples.zip <../build/zip/examples.zip>`

複数のファイルからなるサンプル（フォルダーになっているもの）は、フォルダーごと必要になるので、zip ファイルでダウンロードしてください。

一覧
----

.. list-table::
   :header-rows: 1
   :widths: 32 46 22

   * - ファイル・フォルダー
     - 内容
     - 全文
   * - ``ch02_report_script.py``
     - 売上レポートを 1 本のスクリプトで出力します（悪い例）。
     - :doc:`samples/ch02`
   * - ``ch02_report_structured.py``
     - 同じ売上レポートを、役割ごとの関数に分けて出力します。
     - :doc:`samples/ch02`
   * - ``ch03_coupling.py``
     - 結合度の高い実装と低い実装を比べます。
     - :doc:`samples/ch03`
   * - ``ch03_complexity.py``
     - 循環的複雑度の高い実装を、表を使って書き換えます。
     - :doc:`samples/ch03`
   * - ``ch04_functions.py``
     - 引数を書き換えない関数、計算と入出力の分離、フラグ引数の除去の例です。
     - :doc:`samples/ch04`
   * - ``ch04_exceptions.py``
     - 独自の例外の階層を設計します。
     - :doc:`samples/ch04`
   * - ``ch05_data.py``
     - 辞書で表した注文を、値オブジェクト、列挙型、データクラスで書き換えます。
     - :doc:`samples/ch05`
   * - ``ch06_composition.py``
     - 継承で機能を追加した通知を、コンポジションで書き換えます。
     - :doc:`samples/ch06`
   * - ``ch07_srp.py`` など 5 ファイル
     - SOLID 原則の、原則ごとの違反例と改善例です。
     - :doc:`samples/ch07`
   * - ``ch08_strategy.py`` など 7 ファイル
     - Strategy、Factory、Adapter、Decorator、Observer、Template Method、State の各パターンの例です。
     - :doc:`samples/ch08`
   * - ``ch09_circular_bad/``
     - 循環 import が起きるパッケージです（実行するとエラーになります）。
     - :doc:`samples/ch09`
   * - ``ch09_circular_good/``
     - 循環 import を解消したパッケージです。
     - :doc:`samples/ch09`
   * - ``ch10_dependency_injection.py``
     - 依存性注入とコンポジションルートの例です。
     - :doc:`samples/ch10`
   * - ``ch11_layered/``
     - レイヤードアーキテクチャで構成した ToDo アプリです。
     - :doc:`samples/ch11`
   * - ``ch11_hexagonal/``
     - ヘキサゴナルアーキテクチャで構成した ToDo アプリです。
     - :doc:`samples/ch11`
   * - ``ch12_domain_model/``
     - 注文のドメインモデルと、メモリ版と SQLite 版のリポジトリです。
     - :doc:`samples/ch12`
   * - ``ch13_testing/``
     - テストしやすい会計の処理と、テストダブルを使った単体テストです。
     - :doc:`samples/ch13`
   * - ``ch14_refactoring/``
     - 請求書を作る処理のリファクタリングの前後と、仕様化テストです。
     - :doc:`samples/ch14`
   * - ``ch15_adr_template.md``、``ch15_adr_0001_example.md``
     - ADR のテンプレートと、記入例です。
     - :doc:`samples/ch15`
   * - ``ch16_inventory/``
     - 総合演習の在庫管理 CLI です（段階 1 から段階 4）。
     - :doc:`samples/ch16`
   * - ``setup.cfg``
     - flake8 と mypy の設定です。
     - このページの下部

実行方法
--------

1 ファイルのサンプル
~~~~~~~~~~~~~~~~~~~~

ファイル名が ``ch`` と数字で始まる 1 ファイルのサンプルは、そのファイルのあるフォルダーで次のように実行します。

.. code-block:: console

   $ python ch03_complexity.py

フォルダーのサンプル
~~~~~~~~~~~~~~~~~~~~

フォルダーになっているサンプルは、Python のパッケージです。zip ファイルを展開してできる ``examples`` フォルダーで、``-m`` オプションを付けて実行します。

.. code-block:: console

   $ python -m ch11_hexagonal.main
   $ python -m ch12_domain_model.main

総合演習の段階 1 から 3 は、1 ファイルのスクリプトなので、ファイルを直接実行します。在庫のデータは、実行したフォルダーの ``inventory.json`` に保存されます。

.. code-block:: console

   $ python ch16_inventory/step1/inventory.py register A-1 ボールペン
   $ python ch16_inventory/step1/inventory.py list

段階 4 はパッケージなので、``-m`` オプションを付けて実行します。

.. code-block:: console

   $ python -m ch16_inventory.step4.main register A-1 ボールペン
   $ python -m ch16_inventory.step4.main list

.. note::

   Windows の一部の環境では、日本語の出力が文字化けすることがあります。その場合は、環境変数 ``PYTHONUTF8`` に ``1`` を設定してから実行してください（PowerShell では ``$env:PYTHONUTF8 = "1"``）。

テストの実行
~~~~~~~~~~~~

``examples`` フォルダーで次のように実行すると、すべてのテストを実行します。

.. code-block:: console

   $ python -m unittest -v

コードの検査
------------

サンプルコードは、flake8（PEP 8 への準拠の検査）と mypy（型の検査、``--strict`` 相当の設定）で、問題が検出されないことを確認しています。検査の設定は ``setup.cfg`` に書かれています。

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :caption: setup.cfg

:download:`setup.cfg <../examples/setup.cfg>`

``examples`` フォルダーで次のように実行します。flake8 と mypy は、あらかじめ ``pip install flake8 mypy`` でインストールしておきます。

.. code-block:: console

   $ python -m flake8 .
   $ python -m mypy .

各章のサンプルコードの全文
--------------------------

各章のサンプルコードの全文は、次のページで閲覧できます。

.. toctree::
   :maxdepth: 1

   samples/ch02
   samples/ch03
   samples/ch04
   samples/ch05
   samples/ch06
   samples/ch07
   samples/ch08
   samples/ch09
   samples/ch10
   samples/ch11
   samples/ch12
   samples/ch13
   samples/ch14
   samples/ch15
   samples/ch16
