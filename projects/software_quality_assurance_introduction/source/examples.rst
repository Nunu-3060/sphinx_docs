サンプルコード一覧
==================

本書で使用したサンプルコードの一覧です。ファイル名のリンクからダウンロードできます。すべてのファイルを同じフォルダーに置き、そのフォルダーで pytest、flake8、mypy、nox を実行してください。Python のファイルは、ch04_before.py（意図的な悪い例）を除き、flake8 と mypy（strict モード）の検査に合格し、型ヒントを記述しています。

Python のコード
---------------

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - ファイル
     - 章
     - 内容
   * - :download:`ch04_before.py <../examples/ch04_before.py>`
     - 第 4 章
     - 規約違反と型エラーを含む悪い例です。検査の対象から外しています。
   * - :download:`ch04_after.py <../examples/ch04_after.py>`
     - 第 4 章
     - ch04_before.py の問題を修正したコードです。
   * - :download:`test_ch04_after.py <../examples/test_ch04_after.py>`
     - 第 4 章
     - ch04_after.py のテストです。
   * - :download:`ch07_fee.py <../examples/ch07_fee.py>`
     - 第 7 章
     - 年齢から入場料金を求める関数です。
   * - :download:`test_ch07_fee.py <../examples/test_ch07_fee.py>`
     - 第 7 章
     - 境界値分析によるテストです。
   * - :download:`ch08_rle.py <../examples/ch08_rle.py>`
     - 第 8 章
     - ランレングス符号化の関数です。
   * - :download:`test_ch08_rle.py <../examples/test_ch08_rle.py>`
     - 第 8 章
     - Hypothesis によるプロパティベーステストです。
   * - :download:`ch08_weather.py <../examples/ch08_weather.py>`
     - 第 8 章
     - 依存性の注入を使って、降水確率から傘の要否を助言する関数です。
   * - :download:`test_ch08_weather.py <../examples/test_ch08_weather.py>`
     - 第 8 章
     - スタブとモックを使ったテストです。
   * - :download:`noxfile.py <../examples/noxfile.py>`
     - 第 10 章
     - 品質検査の手順を定義した nox の設定ファイルです。

設定ファイル
------------

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - ファイル
     - 章
     - 内容
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - 第 10 章
     - flake8、mypy、coverage.py の設定です。
   * - :download:`requirements-dev.txt <../examples/requirements-dev.txt>`
     - 第 11 章
     - 開発用ツールのバージョンを固定したファイルです。
   * - :download:`ch10_pre-commit-config.yaml <../examples/ch10_pre-commit-config.yaml>`
     - 第 10 章
     - pre-commit の設定ファイルです。実際に使う場合は .pre-commit-config.yaml という名前にします。
   * - :download:`ch10_github_actions.yml <../examples/ch10_github_actions.yml>`
     - 第 10 章
     - GitHub Actions のワークフロー定義です。実際に使う場合は .github/workflows に配置します。
   * - :download:`ch10_Jenkinsfile <../examples/ch10_Jenkinsfile>`
     - 第 10 章
     - Jenkins の宣言型パイプラインです。実際に使う場合は Jenkinsfile という名前にします。

実行のしかた
------------

サンプルコードのフォルダーで次のコマンドを実行すると、すべての検査を実行できます。

.. code-block:: console
   :linenos:

   $ python -m venv .venv
   $ source .venv/bin/activate      # Windows の場合は .venv\Scripts\activate
   $ python -m pip install -r requirements-dev.txt
   $ flake8 .
   $ mypy .
   $ pytest --cov=. --cov-report=term-missing

nox を使う場合は、``nox`` コマンドだけで同じ検査を実行できます（第 10 章を参照）。
