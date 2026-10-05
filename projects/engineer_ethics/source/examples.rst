サンプルコード一覧
==================

本資料で紹介したサンプルコードの全体を掲載します。各ファイルは、見出しの下のリンクからダウンロードできます。

すべてのサンプルは Python 3.10 以降の標準ライブラリだけで動作し、追加のパッケージは不要です。ダウンロードしたフォルダーで、次のように実行します。

.. code-block:: console
   :linenos:

   python pii_masking.py

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - ファイル
     - 内容
     - 関連する章
   * - ``pii_masking.py``
     - ログに出力する個人情報のマスキング
     - :doc:`07_privacy`
   * - ``password_hashing.py``
     - パスワードの安全な保存と照合
     - :doc:`06_security`
   * - ``sql_injection.py``
     - SQL インジェクションの危険性と対策の比較
     - :doc:`06_security`
   * - ``fairness_check.py``
     - 選考結果の公平性の指標の計算
     - :doc:`10_ai_ethics`
   * - ``pseudonymize.py``
     - HMAC による識別子の仮名化
     - :doc:`07_privacy`
   * - ``license_report.py``
     - インストール済みパッケージのライセンスの一覧表示
     - :doc:`08_intellectual_property`
   * - ``contrast_check.py``
     - 文字色と背景色のコントラスト比の判定
     - :doc:`09_user_respect`

個人情報のマスキング
--------------------

ダウンロード：:download:`pii_masking.py <../examples/pii_masking.py>`

.. literalinclude:: ../examples/pii_masking.py
   :language: python
   :linenos:

パスワードの安全な保存
----------------------

ダウンロード：:download:`password_hashing.py <../examples/password_hashing.py>`

.. literalinclude:: ../examples/password_hashing.py
   :language: python
   :linenos:

SQL インジェクションの比較
--------------------------

ダウンロード：:download:`sql_injection.py <../examples/sql_injection.py>`

.. literalinclude:: ../examples/sql_injection.py
   :language: python
   :linenos:

公平性の指標の計算
------------------

ダウンロード：:download:`fairness_check.py <../examples/fairness_check.py>`

.. literalinclude:: ../examples/fairness_check.py
   :language: python
   :linenos:

識別子の仮名化
--------------

ダウンロード：:download:`pseudonymize.py <../examples/pseudonymize.py>`

.. literalinclude:: ../examples/pseudonymize.py
   :language: python
   :linenos:

ライセンスの一覧表示
--------------------

ダウンロード：:download:`license_report.py <../examples/license_report.py>`

.. literalinclude:: ../examples/license_report.py
   :language: python
   :linenos:

コントラスト比の判定
--------------------

ダウンロード：:download:`contrast_check.py <../examples/contrast_check.py>`

.. literalinclude:: ../examples/contrast_check.py
   :language: python
   :linenos:
