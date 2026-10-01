15. テスト駆動開発
==================

ここまでは、書き終えたコードに対してテストを書く流れを扱ってきた。この章では、テストを先に書き、テストに導かれてコードを書く開発の方法である\ :term:`テスト駆動開発`\ （Test-Driven Development、TDD）を学ぶ。

15.1 Red・Green・Refactor
-------------------------

テスト駆動開発では、次の 3 つの段階からなる短い周期を繰り返してコードを書く。

.. graphviz::
   :caption: テスト駆動開発の周期

   digraph tdd {
       rankdir=LR;
       node [shape=circle, style=filled, fixedsize=true, width=1.3, fontsize=13];
       red      [label="Red\n失敗する\nテストを書く", fillcolor="#fde2e1"];
       green    [label="Green\nテストを\n通す", fillcolor="#e6f4ea"];
       refactor [label="Refactor\n設計を\n整える", fillcolor="#e8f0fe"];
       red -> green -> refactor;
       refactor -> red [constraint=false];
   }

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 段階
     - 内容
   * - Red
     - これから実装する振る舞いを表すテストを 1 つ書き、実行して失敗することを確かめる。
   * - Green
     - テストが成功する最小限のコードを書く。きれいなコードでなくてもよい。
   * - Refactor
     - テストが成功する状態を保ったまま、重複を取り除くなどしてコードの設計を整える。

Red の段階で、テストが失敗することを必ず確かめる。書いたテストが最初から成功してしまう場合は、テストが何も確かめていないか、実装しようとしている振る舞いがすでにあるかのどちらかである。

Green の段階で「最小限」のコードを書くのは、テストに求められていない機能を作り込まないためである。求められていない機能のコードは、それを確かめるテストもないまま残ってしまう。

15.2 題材
---------

パスワードが次の規則を満たしているかを検査する関数 ``validate_password`` を、テスト駆動開発で作る。

* 8 文字以上である。
* 数字を含む。
* 英大文字を含む。
* 英小文字を含む。

関数は、違反している規則のメッセージのリストを返し、違反がなければ空のリストを返すものとする。

テスト駆動開発を始める前に、確かめたい振る舞いを TODO リストとして書き出しておく。

* 規則をすべて満たすパスワードでは、違反がない。
* 短すぎるパスワードでは、長さの違反になる。
* 数字がないパスワードでは、数字の違反になる。
* 英大文字、英小文字がないパスワードでは、それぞれの違反になる。

15.3 1 周目：長さの規則
-----------------------

**Red**：最初のテストを書く。

.. code-block:: python
   :caption: test_password_policy.py
   :linenos:

   from password_policy import validate_password


   def test_valid_password_has_no_error() -> None:
       assert validate_password("Secret123") == []


   def test_too_short() -> None:
       assert validate_password("Sec123") == ["8 文字以上にしてください"]

まだ ``password_policy.py`` がないため、実行すると import の段階でエラーになる。これも Red である。

**Green**：テストが成功する最小限のコードを書く。

.. code-block:: python
   :caption: password_policy.py（1 周目）
   :linenos:

   def validate_password(password: str) -> list[str]:
       if len(password) < 8:
           return ["8 文字以上にしてください"]
       return []

2 つのテストが成功する。この段階では、整えるほどのコードはないため、Refactor は行わずに次へ進む。

15.4 2 周目：数字の規則
-----------------------

**Red**：数字の規則のテストを追加する。

.. code-block:: python
   :linenos:

   def test_without_digit() -> None:
       assert validate_password("SecretPass") == ["数字を含めてください"]

実行すると、追加したテストが失敗する。

.. code-block:: text

   ..F                                                                      [100%]
   ================================== FAILURES ===================================
   _____________________________ test_without_digit ______________________________

       def test_without_digit() -> None:
   >       assert validate_password("SecretPass") == ["数字を含めてください"]
   E       AssertionError: assert [] == ['数字を含めてください']
   E
   E         Right contains one more item: '数字を含めてください'
   E         Use -v to get more diff

期待どおりの理由（数字の規則がまだないこと）で失敗していることを確かめる。想定と異なる理由で失敗している場合は、テストが誤っている可能性がある。

**Green**：規則の違反を複数返せるように、リストに追加していく形に変える。

.. code-block:: python
   :caption: password_policy.py（2 周目）
   :linenos:

   def validate_password(password: str) -> list[str]:
       errors: list[str] = []
       if len(password) < 8:
           errors.append("8 文字以上にしてください")
       if not any(c.isdigit() for c in password):
           errors.append("数字を含めてください")
       return errors

3 つのテストがすべて成功する。1 周目のテストも再び実行されるため、長さの規則を壊していないことも同時に確かめられる。

15.5 3 周目：英大文字と英小文字の規則
-------------------------------------

同じように、英大文字と英小文字の規則のテストを 1 つずつ追加し、Red と Green を繰り返す。その結果、次のコードになる。

.. code-block:: python
   :caption: password_policy.py（3 周目）
   :linenos:

   def validate_password(password: str) -> list[str]:
       errors: list[str] = []
       if len(password) < 8:
           errors.append("8 文字以上にしてください")
       if not any(c.isdigit() for c in password):
           errors.append("数字を含めてください")
       if not any(c.isupper() for c in password):
           errors.append("英大文字を含めてください")
       if not any(c.islower() for c in password):
           errors.append("英小文字を含めてください")
       return errors

**Refactor**：同じ形の ``if`` 文が 4 つ並んだ。規則が増えるたびに ``if`` 文を増やすのではなく、「判定の関数とメッセージの組」の一覧として規則を表すように整える。あわせて、最小の長さを定数にする。テストがすべて成功する状態を保ったまま変更し、変更のたびにテストを実行する。

.. literalinclude:: ../examples/ch15_tdd/password_policy.py
   :language: python
   :caption: ch15_tdd/password_policy.py（最終版）
   :linenos:

リファクタリングの前後で、テストは 1 行も変えていない。テストがあるため、振る舞いを変えずに設計を変えられたことを確信できる。

15.6 テストを見直す
-------------------

TODO リストをすべて実装したら、4 章の技法でテストの抜けを探す。長さの規則には境界があるため、境界値分析により、ちょうど 8 文字のパスワードのテストを追加する。また、複数の規則に同時に違反する場合のテストも追加する。最終的なテストは次のとおりである。

.. literalinclude:: ../examples/ch15_tdd/test_password_policy.py
   :language: python
   :caption: ch15_tdd/test_password_policy.py（最終版）
   :linenos:

テスト駆動開発は、テスト設計の技法の代わりにはならない。TODO リストを作るときや、実装を終えた後に、設計技法を使ってテストケースを補う。

15.7 テスト駆動開発の効果と向き不向き
-------------------------------------

テスト駆動開発には、次の効果がある。

* **テストのないコードが生まれない**：すべてのコードは、それを求めるテストの後に書かれる。
* **使う側の視点で設計できる**：テストを先に書くと、関数の名前や引数、戻り値を、呼び出す側の立場で考えることになる。10 章で見たテストしやすい設計にも自然となる。
* **安心してリファクタリングできる**：常にテストが成功する状態から始めるため、変更で何かを壊せばすぐに分かる。
* **進み具合が分かる**：周期が短く、成功するテストが 1 つずつ増えていくため、どこまでできたかが明確である。

一方で、次のような場合は、テスト駆動開発を厳密に適用しにくい。

* 何を作るべきかがはっきりしない、試行錯誤の段階のコード
* 画面の見た目のように、期待結果を事前にコードで表しにくいもの
* 使い方がよく分からない外部のライブラリを試す場合

このような場合は、先に試作して理解を深め、振る舞いが固まってからテストを書いたり、試作のコードを捨ててテスト駆動開発で作り直したりする方法がある。

15.8 まとめ
-----------

* テスト駆動開発では、Red（失敗するテストを書く）、Green（最小限のコードで通す）、Refactor（設計を整える）の周期を繰り返す。
* Red の段階で、テストが期待どおりの理由で失敗することを確かめる。
* テストがあることで、振る舞いを変えずに設計を変えるリファクタリングを安心して行える。
* テスト駆動開発で作ったテストも、テスト設計の技法で見直して補う。
