.. _ch-autodoc:

===================================
Python コードからのドキュメント生成
===================================

Python のライブラリのドキュメントでは、関数やクラスの説明を書く場面が多くあります。この章では、Python のコードに書いた :term:`docstring` から API ドキュメントを生成する :term:`autodoc` 拡張機能と、その関連機能を説明します。

この章では、図形の面積を計算する次のモジュールを題材にします。

.. literalinclude:: ../examples/sample_package/shapes.py
   :language: python
   :linenos:
   :caption: sample_package/shapes.py

このファイルは :download:`shapes.py <../examples/sample_package/shapes.py>` からダウンロードできます。パッケージの ``__init__.py`` は :download:`__init__.py <../examples/sample_package/__init__.py>` からダウンロードできます。

autodoc の仕組み
================

autodoc は、指定したモジュールを実際に ``import`` し、モジュールやクラス、関数の docstring とシグネチャを取り出してドキュメントにします。コードを実行して情報を取り出すため、次の点に注意が必要です。

- モジュールを ``import`` できるように、``sys.path`` を設定するか、パッケージをインストールしておく必要があります。
- モジュールが依存するライブラリも、ビルドする環境にインストールしておく必要があります。インストールできないライブラリは、``autodoc_mock_imports`` にモジュール名を指定すると、ダミーのモジュールで置き換えられます。
- モジュールの最上位に書いたコードは、``import`` するときに実行されます。``import`` しただけで処理が始まるモジュールは、``if __name__ == "__main__":`` の中に処理を移しておきます。

.. _sec-sys-path:

モジュールの読み込み場所の設定
==============================

ドキュメントの対象のモジュールがインストールされていない場合は、``conf.py`` で ``sys.path`` にモジュールの置き場所を追加します。本書では、``examples`` ディレクトリを次のように追加しています。

.. literalinclude:: conf.py
   :language: python
   :linenos:
   :lines: 3-8
   :caption: 本書の conf.py（抜粋）

``conf.py`` の場所を基準にパスを組み立てているため、``sphinx-build`` をどのディレクトリから実行しても同じ場所を指します。

パッケージとして開発しているライブラリであれば、``python -m pip install -e .`` で開発中のパッケージをインストールしておく方法もあります。この方法では ``sys.path`` を変更する必要がありません。

docstring の書き方
==================

docstring は、reST で書くのが基本です。引数や戻り値は、``:param:`` などのフィールドで記述します。

.. code-block:: python
   :linenos:

   def total_area(shapes: list[Shape]) -> float:
       """複数の図形の面積の合計を返します。

       :param shapes: 面積を合計する図形のリスト。
       :returns: 面積の合計。
       """

reST のフィールドは記号が多く、コードの中で読みにくいという欠点があります。``sphinx.ext.napoleon`` 拡張機能を有効にすると、読みやすい Google 形式や NumPy 形式の docstring も使えるようになります。本書のサンプルは Google 形式で書いています。

.. code-block:: python
   :linenos:
   :caption: Google 形式

   def total_area(shapes: list[Shape]) -> float:
       """複数の図形の面積の合計を返します。

       Args:
           shapes: 面積を合計する図形のリスト。

       Returns:
           面積の合計。
       """

.. code-block:: python
   :linenos:
   :caption: NumPy 形式

   def total_area(shapes: list[Shape]) -> float:
       """複数の図形の面積の合計を返します。

       Parameters
       ----------
       shapes : list[Shape]
           面積を合計する図形のリスト。

       Returns
       -------
       float
           面積の合計。
       """

どの形式でも、1 行目には関数の概要を 1 文で書き、空行を挟んで詳しい説明を書くのが慣例です。この慣例は :pep:`257` で定められています。docstring の中で ``\pi`` のようにバックスラッシュを使う場合は、サンプルの 93 行目のように raw 文字列（``r"""``）にします。

型ヒントの表示
==============

autodoc は、関数の型ヒントもドキュメントに反映します。表示する場所は ``autodoc_typehints`` で指定します。

.. list-table:: autodoc_typehints の値
   :header-rows: 1
   :widths: 30 70

   * - 値
     - 説明
   * - ``"signature"``
     - シグネチャの中に型ヒントを表示します。既定値です。
   * - ``"description"``
     - 引数や戻り値の説明の中に型ヒントを表示します。
   * - ``"both"``
     - シグネチャと説明の両方に表示します。
   * - ``"none"``
     - 型ヒントを表示しません。

型ヒントが長いとシグネチャが読みにくくなるため、本書では ``"description"`` を指定しています。型ヒントを書いておけば、docstring の中に型を書く必要はありません。

autodoc のディレクティブ
========================

autodoc は、ドキュメントの対象ごとにディレクティブを提供しています。

.. list-table:: autodoc の主なディレクティブ
   :header-rows: 1
   :widths: 30 70

   * - ディレクティブ
     - 対象
   * - ``automodule``
     - モジュール
   * - ``autoclass``
     - クラス
   * - ``autofunction``
     - 関数
   * - ``automethod``
     - メソッド
   * - ``autodata``
     - モジュールの変数

``automodule`` や ``autoclass`` では、既定では指定したオブジェクト自身の docstring だけが表示されます。メンバーも表示するには、オプションを指定します。

.. list-table:: automodule と autoclass の主なオプション
   :header-rows: 1
   :widths: 30 70

   * - オプション
     - 説明
   * - ``:members:``
     - docstring のあるメンバーを表示します。``:members: area, perimeter`` のように、表示するメンバーを指定することもできます。
   * - ``:undoc-members:``
     - docstring のないメンバーも表示します。
   * - ``:show-inheritance:``
     - 基底クラスを表示します。
   * - ``:member-order:``
     - メンバーの並び順を、``alphabetical``\ （名前順）、``bysource``\ （ソースコードの順）、``groupwise``\ （種類ごと）のいずれかで指定します。

すべての ``automodule`` に同じオプションを指定する場合は、``conf.py`` の ``autodoc_default_options`` に書いておくと便利です。

.. _sec-api-reference:

API リファレンスの例
====================

次のように書くと、``sample_package.shapes`` モジュールの API リファレンスが生成されます。

.. code-block:: rst
   :linenos:

   .. automodule:: sample_package.shapes
      :members:

このソースファイルは、次のように表示されます。各項目の右側にある「[ソース]」は、:ref:`sec-viewcode`\ で説明するソースコードへのリンクです。

.. automodule:: sample_package.shapes
   :members:

.. note::

   サンプルの ``Rectangle`` クラスと ``Circle`` クラスは、docstring の ``Attributes`` セクションに属性を書いています。``napoleon`` はこのセクションから属性の説明を作るため、``:undoc-members:`` を指定しなくても属性が表示されます。本書では ``conf.py`` に ``napoleon_use_ivar = True`` と書いて、属性をクラスの説明の中の「変数」欄にまとめて表示しています。

一覧表の生成（autosummary）
===========================

``sphinx.ext.autosummary`` 拡張機能を使うと、モジュールのクラスや関数の一覧表を作れます。一覧表の各項目には、docstring の 1 行目が概要として表示されます。

.. code-block:: rst
   :linenos:

   .. currentmodule:: sample_package.shapes

   .. autosummary::

      Rectangle
      Circle
      total_area

このソースファイルは、次のように表示されます。

.. currentmodule:: sample_package.shapes

.. autosummary::

   Rectangle
   Circle
   total_area

``:toctree:`` オプションに出力先のディレクトリを指定すると、一覧表の項目ごとに autodoc のディレクティブを書いたソースファイルが自動で生成され、一覧表からそれぞれのページへリンクされます。大きなパッケージの API リファレンスを作るときに便利です。

.. _sec-viewcode:

ソースコードへのリンク（viewcode）
==================================

``sphinx.ext.viewcode`` 拡張機能を有効にすると、autodoc で生成した各項目に「[ソース]」というリンクが付き、強調表示された Python のソースコードのページへ移動できます。ソースコードのページには、ドキュメントの対象のモジュールだけが出力されます。

コード例のテスト（doctest）
===========================

docstring やドキュメントに書いたコード例は、コードを変更したときに更新を忘れがちです。``sphinx.ext.doctest`` 拡張機能を有効にすると、ドキュメントの中の ``>>>`` で始まるコード例を実行し、表示されている結果と一致するかを確認できます。確認には ``doctest`` ビルダーを使います。

.. code-block:: text
   :linenos:

   sphinx-build -b doctest source build/doctest

autodoc で取り込んだ docstring のコード例も確認の対象になります。ただし、コード例はドキュメントの対象のモジュールの中ではなく、独立した環境で実行されます。そのため、コード例で使うクラスや関数は、``conf.py`` の ``doctest_global_setup`` で ``import`` しておく必要があります。本書では、次のように設定しています。

.. code-block:: python
   :linenos:

   doctest_global_setup = (
       "from sample_package.shapes import Circle, Rectangle, total_area"
   )

``doctest_global_setup`` に書いたコードは、各コード例の前に実行されます。本書のサンプルのコード例も、この設定で確認しています。結果が一致しない場合は、ビルダーが失敗として報告し、結果は ``build/doctest/output.txt`` に書き出されます。
