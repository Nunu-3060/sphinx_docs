参考文献
========

本資料の内容をさらに深く学ぶための書籍と資料です。

書籍
----

設計の全般
~~~~~~~~~~

* David Thomas、Andrew Hunt 著『達人プログラマー 熟達に向けたあなたの旅（第 2 版）』オーム社、2020 年

  DRY をはじめとする、実践的な設計と開発の心得がまとめられています。

* John Ousterhout, *A Philosophy of Software Design*, Yaknyam Press, 2018.

  複雑さを減らすことを中心に、モジュールの「深さ」や情報隠蔽について論じています。

* Frederick P. Brooks, Jr. 著『人月の神話【新装版】』丸善出版、2014 年

  本質的な複雑さと偶有的な複雑さを論じた論文「銀の弾などない」が収録されています。

オブジェクト指向設計とデザインパターン
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Erich Gamma、Richard Helm、Ralph Johnson、John Vlissides 著『オブジェクト指向における再利用のためのデザインパターン（改訂版）』ソフトバンクパブリッシング、1999 年

  23 のデザインパターンを定義した、GoF の書籍です。

* Robert C. Martin 著『Clean Architecture 達人に学ぶソフトウェアの構造と設計』アスキードワンゴ、2018 年

  SOLID 原則、コンポーネントの原則（安定度と抽象度の指標を含む）、クリーンアーキテクチャを説明しています。

アーキテクチャとドメイン駆動設計
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Eric Evans 著『エリック・エヴァンスのドメイン駆動設計』翔泳社、2011 年

  ドメイン駆動設計を提唱した書籍です。

* Harry Percival, Bob Gregory, *Architecture Patterns with Python*, O'Reilly Media, 2020.

  リポジトリ、サービス層、依存性注入などを、Python で実践する方法を説明しています。Web 上で全文を読めます（下記の Web 資料を参照）。

テストとリファクタリング
~~~~~~~~~~~~~~~~~~~~~~~~

* Martin Fowler 著『リファクタリング 既存のコードを安全に改善する（第 2 版）』オーム社、2019 年

  コードの臭いと、リファクタリングの手法を体系的にまとめています。

* Kent Beck 著『テスト駆動開発』オーム社、2017 年

  テスト駆動開発を提唱した書籍です。

* Michael C. Feathers 著『レガシーコード改善ガイド』翔泳社、2009 年

  テストのない既存のコードに、テストを加えて改善していく方法を説明しています。仕様化テストもこの書籍で紹介されています。

* Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007.

  テストダブルの分類を示した書籍です。

論文
----

* D. L. Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules", *Communications of the ACM*, Vol. 15, No. 12, pp. 1053-1058, 1972.

  情報隠蔽の考え方を示した論文です。

* T. J. McCabe, "A Complexity Measure", *IEEE Transactions on Software Engineering*, Vol. SE-2, No. 4, pp. 308-320, 1976.

  循環的複雑度を提案した論文です。

Web 資料
--------

Python
~~~~~~

* `PEP 8 – Style Guide for Python Code <https://peps.python.org/pep-0008/>`_
* `PEP 544 – Protocols: Structural subtyping (static duck typing) <https://peps.python.org/pep-0544/>`_
* `typing --- 型ヒントのサポート <https://docs.python.org/ja/3/library/typing.html>`_
* `dataclasses --- データクラス <https://docs.python.org/ja/3/library/dataclasses.html>`_
* `unittest.mock --- モックオブジェクトライブラリ <https://docs.python.org/ja/3/library/unittest.mock.html>`_
* `Cosmic Python（Architecture Patterns with Python の Web 版） <https://www.cosmicpython.com/>`_

設計とアーキテクチャ
~~~~~~~~~~~~~~~~~~~~

* `The Clean Architecture（Robert C. Martin） <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>`_
* `Hexagonal architecture（Alistair Cockburn） <https://alistair.cockburn.us/hexagonal-architecture/>`_
* `The C4 model for visualising software architecture <https://c4model.com/>`_
* `Documenting Architecture Decisions（Michael Nygard） <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>`_
* `Architectural Decision Records <https://adr.github.io/>`_
* `TechnicalDebt（Martin Fowler） <https://martinfowler.com/bliki/TechnicalDebt.html>`_
* `TestDouble（Martin Fowler） <https://martinfowler.com/bliki/TestDouble.html>`_
* `TestPyramid（Martin Fowler） <https://martinfowler.com/bliki/TestPyramid.html>`_

ツール
~~~~~~

* `flake8 <https://flake8.pycqa.org/en/latest/>`_
* `mypy <https://mypy.readthedocs.io/en/stable/>`_
* `Graphviz <https://graphviz.org/>`_
* `PlantUML <https://plantuml.com/>`_
* `Mermaid <https://mermaid.js.org/>`_
