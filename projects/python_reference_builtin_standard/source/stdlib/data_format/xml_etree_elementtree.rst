xml.etree.ElementTree
======================

XML 文書を要素（``Element``）のツリー構造として扱うためのモジュール。XML の解析・構築・出力を、比較的シンプルな API で行うことができる。CI ツール（Jenkins など）が読み書きする JUnit 形式のテストレポート（``<testsuite><testcase .../></testsuite>``）のような、実務でよく出くわす XML フォーマットを扱う際に特に有用。

ElementTree.parse / fromstring
--------------------------------

XML ファイルを解析するには ``parse()``、文字列を解析するには ``fromstring()`` を使う。``parse()`` は ``ElementTree`` オブジェクトを返し、``getroot()`` でルート要素を取得する。``fromstring()`` はルート要素（``Element``）を直接返す。

.. code-block:: python

   >>> import xml.etree.ElementTree as ET
   >>> xml_str = """<testsuite name="mytests" tests="2">
   ...     <testcase classname="tests.test_math" name="test_add" time="0.001"/>
   ...     <testcase classname="tests.test_math" name="test_sub" time="0.002">
   ...         <failure message="assertion failed">AssertionError: 1 != 2</failure>
   ...     </testcase>
   ... </testsuite>"""
   >>> root = ET.fromstring(xml_str)
   >>> root
   <Element 'testsuite' at ...>

   >>> tree = ET.parse("report.xml")  # doctest: +SKIP
   >>> root = tree.getroot()  # doctest: +SKIP

要素の参照
------------

各 ``Element`` は、タグ名を表す ``.tag``、属性を辞書として保持する ``.attrib``、開始タグ直後のテキストを表す ``.text`` を持つ。子要素はそのまま ``for`` 文で反復できる。

.. code-block:: python

   >>> root.tag
   'testsuite'
   >>> root.attrib
   {'name': 'mytests', 'tests': '2'}
   >>> for child in root:
   ...     print(child.tag, child.attrib)
   ...
   testcase {'classname': 'tests.test_math', 'name': 'test_add', 'time': '0.001'}
   testcase {'classname': 'tests.test_math', 'name': 'test_sub', 'time': '0.002'}

find / findall
----------------

``find()`` は最初に一致した子要素を、``findall()`` は一致した子要素すべてをリストで返す。引数には単純な XPath 風のパスを指定でき、``.//tag`` と書くとその階層より下を再帰的に検索する。

.. code-block:: python

   >>> [tc.get("name") for tc in root.findall("testcase")]
   ['test_add', 'test_sub']
   >>> root.find("testcase").attrib
   {'classname': 'tests.test_math', 'name': 'test_add', 'time': '0.001'}
   >>> [f.text for f in root.findall(".//failure")]
   ['AssertionError: 1 != 2']

.. note::

   属性値を取得する際は ``element.attrib["name"]`` の代わりに ``element.get("name")`` を使うと、属性が存在しない場合に ``KeyError`` ではなく ``None`` （またはデフォルト値）を返すため安全。

Element / SubElement による構築と出力
----------------------------------------

新しく XML を組み立てる場合は ``Element()`` でルート要素を作り、``SubElement()`` で子要素を追加していく。組み立てた要素は ``tostring()`` で文字列に、``ElementTree(root).write()`` でファイルに出力できる。``ET.indent()`` を使うと出力を整形できる。

.. code-block:: python

   >>> new_root = ET.Element("testsuite", name="mytests", tests="2")
   >>> tc1 = ET.SubElement(new_root, "testcase",
   ...                      classname="tests.test_math", name="test_add", time="0.001")
   >>> tc2 = ET.SubElement(new_root, "testcase",
   ...                      classname="tests.test_math", name="test_sub", time="0.002")
   >>> failure = ET.SubElement(tc2, "failure", message="assertion failed")
   >>> failure.text = "AssertionError: 1 != 2"
   >>> ET.indent(new_root)
   >>> print(ET.tostring(new_root, encoding="unicode"))
   <testsuite name="mytests" tests="2">
     <testcase classname="tests.test_math" name="test_add" time="0.001" />
     <testcase classname="tests.test_math" name="test_sub" time="0.002">
       <failure message="assertion failed">AssertionError: 1 != 2</failure>
     </testcase>
   </testsuite>

   >>> tree = ET.ElementTree(new_root)
   >>> tree.write("report.xml", encoding="utf-8", xml_declaration=True)  # doctest: +SKIP

.. note::

   ここで組み立てているのは JUnit 形式のテストレポートそのもの。``pytest --junitxml=report.xml`` のようなオプションで各種テストフレームワークが出力するファイルもこの構造を持っており、Jenkins などの CI システムはこれを解析してテスト結果を可視化する。手元で独自の集計ツールを書く場合も、同じ形式で読み書きできる。

.. warning::

   ``xml.etree.ElementTree`` は、外部エンティティ参照の膨張攻撃
   （いわゆる「XML 爆弾」）などの悪意あるデータに対して安全に
   設計されていない。信頼できないソース（外部から受け取った
   ファイルやリクエストボディなど）を解析する場合は、サードパーティ
   の `defusedxml <https://pypi.org/project/defusedxml/>`_ パッケージ
   の利用を検討すること。
