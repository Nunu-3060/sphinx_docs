===========
Sphinx 入門
===========

本書は、ドキュメント生成ツール Sphinx の基本的な使い方を解説する入門書です。インストールから reST の記法、Python のコードからの API ドキュメントの生成、ドキュメントの公開までを、実際の作業の順に説明します。

本書について
============

対象読者
--------

Python の基本的な知識があり、pip や仮想環境を使ったことがあるエンジニアを対象とします。Python の文法やパッケージ管理の説明は省略し、Sphinx 固有の考え方や記法の説明に重点を置きます。

動作確認環境
------------

本書の内容は、次の環境で動作を確認しています。

.. list-table:: 動作確認環境
   :header-rows: 1
   :widths: 40 60

   * - ソフトウェア
     - バージョン
   * - Python
     - 3.14
   * - Sphinx
     - 9.1
   * - sphinx_rtd_theme
     - 3.1
   * - sphinx-copybutton
     - 0.5

本書で使うサンプル
------------------

本文で紹介するサンプルは、次のリンクからダウンロードできます。各サンプルの内容は、対応する章で説明します。

.. list-table:: サンプルの一覧
   :header-rows: 1
   :widths: 30 35 35

   * - ファイル
     - 内容
     - 解説している章
   * - :download:`minimal_project.zip <../examples/minimal_project.zip>`
     - 最小構成の Sphinx プロジェクト
     - :ref:`ch-install`
   * - :download:`build_html_example.bat <../build_html_example.bat>`
     - HTML をビルドするバッチファイル
     - :ref:`ch-install`
   * - :download:`rest_sample.rst <../examples/rest_sample.rst>`
     - reST の記法のサンプル
     - :ref:`ch-rest-basics`
   * - :download:`conf_sample.py <../examples/conf_sample.py>`
     - conf.py のサンプル
     - :ref:`ch-configuration`
   * - :download:`shapes.py <../examples/sample_package/shapes.py>`
     - autodoc の題材にする Python モジュール
     - :ref:`ch-autodoc`
   * - :download:`my_extension.py <../examples/my_extension.py>`
     - 自作の拡張機能
     - :ref:`ch-extensions`
   * - :download:`workflow_sample.yml <../examples/workflow_sample.yml>`
     - GitHub Actions のワークフロー
     - :ref:`ch-output-publish`
   * - :download:`readthedocs_sample.yaml <../examples/readthedocs_sample.yaml>`
     - Read the Docs の設定ファイル
     - :ref:`ch-output-publish`

表記について
------------

本書では、次の表記を使います。

- コマンドやファイル名、設定値の名前は ``conf.py`` のように等幅フォントで表します。
- コードの例には行番号を付けています。行番号はコードの一部ではありません。コードの右上に表示されるボタンでコピーすると、行番号を除いたコードだけがコピーされます。
- 本書の用語は\ :ref:`ch-glossary`\ にまとめています。本文中の用語のリンクから、用語集の説明へ移動できます。

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: 目次

   introduction
   install
   rest_basics
   directives_roles
   cross_reference
   configuration
   autodoc
   extensions
   output_publish
   tips
   glossary
   references
