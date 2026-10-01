12. さまざまなテスト手法
========================

ここまでは、入力と期待結果を 1 つずつ書く、例に基づくテストを扱ってきた。この章では、それを補う手法として、doctest、プロパティベーステスト、ゴールデンテスト、ミューテーションテストを紹介する。

12.1 doctest
------------

:term:`doctest` は、docstring に書いた対話モードの実行例を、テストとして実行する仕組みである。Python の標準ライブラリに含まれている。

.. literalinclude:: ../examples/ch12_techniques/text_utils.py
   :language: python
   :caption: ch12_techniques/text_utils.py
   :linenos:

``>>>`` で始まる行が実行するコード、その次の行が期待される出力である。例外が送出されることは、``Traceback (most recent call last):`` の行と、最後の例外の行で表す（17～19 行目）。途中の行は ``...`` で省略できる。

pytest では、``--doctest-modules`` オプションを付けると doctest を実行できる。

.. code-block:: console
   :linenos:

   $ python -m pytest --doctest-modules -v ch12_techniques/text_utils.py

.. code-block:: text

   ch12_techniques/text_utils.py::text_utils.format_price PASSED            [ 50%]
   ch12_techniques/text_utils.py::text_utils.format_zip_code PASSED         [100%]

   ============================== 2 passed in 0.49s ==============================

doctest の利点は、使い方の例が常に正しく動くことを保証できる点にある。文書に書いた例が、コードの変更に追従せず古くなる問題を防げる。一方で、多くの場合分けを doctest で書くと docstring が長くなり、読みにくくなる。doctest は代表的な使い方の例にとどめ、網羅的なテストは通常のテストファイルに書くとよい。

12.2 プロパティベーステスト
---------------------------

例に基づくテストでは、入力と期待結果の組をテストを書く人が選ぶ。そのため、書いた人が想定しなかった入力は試されない。:term:`プロパティベーステスト`\ は、「どのような入力に対しても成り立つべき性質（プロパティ）」を書き、入力はツールに大量に生成させる手法である。

題材として、ランレングス符号化を使う。ランレングス符号化は、同じ文字の連続を「文字と個数」の組で表す方法で、たとえば ``"aaab"`` を ``[("a", 3), ("b", 1)]`` に変換する。

.. literalinclude:: ../examples/ch12_techniques/run_length.py
   :language: python
   :caption: ch12_techniques/run_length.py
   :linenos:

この関数には、次のような性質があるはずである。

* 符号化してから復元すると、元の文字列に戻る。
* 符号化の結果で、隣り合う組の文字は異なり、個数は 1 以上である。

Python では、Hypothesis というライブラリでプロパティベーステストを書ける。

.. literalinclude:: ../examples/ch12_techniques/test_run_length_properties.py
   :language: python
   :caption: ch12_techniques/test_run_length_properties.py
   :linenos:

``@given(st.text())``\ （10 行目）は、任意の文字列を生成してテスト関数の引数 ``text`` に渡すことを表す。Hypothesis は、既定では 1 つのテストにつき 100 通りの入力を生成する。空文字列、非常に長い文字列、制御文字や絵文字を含む文字列など、人が思いつきにくい入力も積極的に生成される。``st``\ （strategies）には、整数、真偽値、リスト、辞書などを生成する関数が用意されている。

3 つ目のテスト（24～32 行目）は、題材の送料計算についての性質である。「注文金額が増えても送料は増えない」という性質は、個々の入力と期待値の組を並べるよりも、仕様の意図を直接表している。

12.3 失敗の縮小
---------------

プロパティベーステストの強みは、欠陥を見つけたときに、失敗する入力を最も単純な形に縮めて報告することである。これを\ :term:`縮小`\ （shrinking）と呼ぶ。

符号化の結果を ``"a3b1"`` のような文字列で表す版を書いたとする。この版には、元の文字列に数字が含まれると正しく復元できない欠陥がある。

.. literalinclude:: ../examples/ch12_techniques/buggy_codec_example.py
   :language: python
   :caption: ch12_techniques/buggy_codec_example.py（10 行目以降）
   :linenos:
   :lines: 10-
   :lineno-start: 10

.. code-block:: console
   :linenos:

   $ python -m pytest ch12_techniques/buggy_codec_example.py

.. code-block:: text

   text = '0'

       @given(st.text())
       def test_roundtrip(text: str) -> None:
   >       assert decode_from_str(encode_to_str(text)) == text
   E       AssertionError: assert '' == '0'
   E
   E         - 0
   E       Failing test case: test_roundtrip(
   E           text='0',
   E       )

Hypothesis は、失敗する入力として ``'0'`` を報告している。最初に見つかった失敗の入力は、数字を含む長く複雑な文字列だったかもしれない。Hypothesis はそれを少しずつ単純にしながら、失敗が再現する最小の入力を探す。この例では、「数字 1 文字だけで失敗する」ことが分かるため、原因をすぐに推測できる。

見つかった失敗の入力は、``.hypothesis`` フォルダーに保存され、次回の実行で最初に試される。修正した後は、その入力を ``@example`` デコレーターで明示的に追加しておくと、回帰テストになる。

12.4 標準ライブラリだけで行う方法
---------------------------------

Hypothesis を使えない環境でも、``random`` モジュールで入力を生成すれば、簡易なプロパティベーステストを書ける。

.. literalinclude:: ../examples/ch12_techniques/test_run_length_random.py
   :language: python
   :caption: ch12_techniques/test_run_length_random.py
   :linenos:

乱数のシードを固定しているため（15 行目）、失敗したときに同じ入力を再現できる。また、``assert`` 文にメッセージを付けて、失敗した入力を表示するようにしている（18 行目）。ただし、失敗の縮小は行われない。文字の種類を ``"aab"`` に絞っているのは、同じ文字が連続する入力を作りやすくするためである。このように、入力の生成方法を工夫しないと、重要な場合がほとんど試されないことがある。

12.5 ゴールデンテスト
---------------------

領収書やレポートのように、出力が長い文字列の場合、期待値をテストコードの中に書くと読みにくい。:term:`ゴールデンテスト`\ （スナップショットテスト）は、期待される出力をファイル（ゴールデンファイル）として保存しておき、実際の出力と比べる手法である。

.. literalinclude:: ../examples/ch12_techniques/receipt.py
   :language: python
   :caption: ch12_techniques/receipt.py
   :linenos:

.. literalinclude:: ../examples/ch12_techniques/golden/receipt.txt
   :language: text
   :caption: ch12_techniques/golden/receipt.txt
   :linenos:

.. literalinclude:: ../examples/ch12_techniques/test_receipt_golden.py
   :language: python
   :caption: ch12_techniques/test_receipt_golden.py
   :linenos:

出力の形式を意図して変えた場合は、環境変数 ``UPDATE_GOLDEN`` に ``1`` を設定してテストを実行すると、ゴールデンファイルが新しい出力で上書きされる（25～26 行目）。

ゴールデンテストは、出力の予期しない変化を検出するのに役立つ。一方で、ゴールデンファイルを更新するときに、差分をよく確かめずに上書きすると、誤った出力が正解として保存されてしまう。ゴールデンファイルはバージョン管理に含め、更新したときは差分をレビューする。

12.6 ミューテーションテスト
---------------------------

5 章で見たとおり、カバレッジはコードが実行されたかどうかしか測らず、テストが結果を十分に確かめているかは分からない。:term:`ミューテーションテスト`\ は、テスト対象のコードにわざと小さな変更（ミュータント）を加え、テストがその変更を検出できるかによって、テストの質を評価する手法である。

たとえば、送料計算の ``>=`` を ``>`` に変えたミュータントを作る。

.. code-block:: python
   :linenos:

   # 元のコード（shop/shipping.py の 34 行目）
   fee = 0 if subtotal >= threshold else BASE_FEE
   # ミュータント
   fee = 0 if subtotal > threshold else BASE_FEE

このミュータントに対して、8 章のテストを実行すると、次の結果になる。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - テスト
     - 結果
   * - デシジョンテーブルのテスト（``test_decision_table``\ ）
     - 8 つすべて成功する。注文金額に 2,000、4,000、6,000 を使っており、境界の値を試していないため、変更を検出できない。
   * - 境界値のテスト（``test_boundary_for_regular_member`` など）
     - 5,000 と 3,000 のテストが失敗する。変更を検出できる。

テストが失敗してミュータントを検出できた場合を「ミュータントを殺した」、検出できなかった場合を「ミュータントが生き残った」と表現する。生き残ったミュータントは、テストが不足している箇所を示している。この例は、4 章で境界値分析をデシジョンテーブルと組み合わせる必要があった理由を、別の角度から示している。

ミュータントの作成とテストの実行を手作業で繰り返すのは現実的でないため、実際にはツールを使う。Python では mutmut や Cosmic Ray などのツールがある。ミュータントの数だけテストを実行するため時間がかかるが、重要なモジュールに絞って使うと、テストの弱点を効率よく見つけられる。

12.7 まとめ
-----------

* doctest は、docstring の実行例をテストとして実行し、文書の例が正しいことを保証する。
* プロパティベーステストは、成り立つべき性質を書き、入力をツールに大量に生成させる。Hypothesis は失敗した入力を最小の形に縮小して報告する。
* ゴールデンテストは、長い出力を保存したファイルと比べる。更新するときは差分を必ず確かめる。
* ミューテーションテストは、コードにわざと加えた変更をテストが検出できるかで、テストの質を評価する。
