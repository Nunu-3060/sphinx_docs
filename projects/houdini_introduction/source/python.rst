Python による操作
=================

Houdini は Python で操作できる。画面で行うほとんどの操作（ノードの作成、接続、パラメーターの設定、ファイルの保存など）を、Python のコードで行える。この章では、Houdini の Python API である ``hou`` モジュールの使い方と、Python を使う 4 つの場面（Python Shell、Python SOP、シェルフツール、hython）を説明する。

hou モジュール
--------------

Houdini の Python API は、``hou`` という名前のモジュールで提供されている。HOM（Houdini Object Model）とも呼ぶ。Houdini 22.0 には Python 3.13 が付属していて、Houdini の中で動く Python のコードは、全てこの Python で実行される。

Houdini の中の Python Shell やパラメーターの式では、``hou`` は最初から読み込まれている。自分で作ったモジュール（ファイル）の中では、``import hou`` と書く。

.. list-table:: hou モジュールの主なクラスと関数
   :header-rows: 1
   :widths: 35 65

   * - クラス、関数
     - 内容
   * - ``hou.node(パス)``
     - パスを指定してノードを取得する。見つからなければ ``None`` を返す。
   * - ``hou.Node``
     - ノード。``createNode()``、``setInput()``、``parm()``、``children()`` などのメソッドを持つ。SOP のノードは ``hou.SopNode`` で、``geometry()`` で出力のジオメトリを取得できる。
   * - ``hou.Parm``、``hou.ParmTuple``
     - パラメーター、パラメーターのタプル。``eval()`` で値を読み、``set()`` で値を書く。``setExpression()`` で式を設定する。
   * - ``hou.Geometry``
     - ジオメトリ。``points()``、``prims()``、``pointAttribs()`` などで中身を読む。
   * - ``hou.Point``、``hou.Prim``、``hou.Vertex``
     - ポイント、プリミティブ、バーテックス。``attribValue()`` でアトリビュートの値を読む。
   * - ``hou.hipFile``
     - hip ファイルの保存（``save()``）と読み込み（``load()``）。
   * - ``hou.frame()``、``hou.setFrame()``
     - 現在のフレームの取得と変更。

全てのクラスと関数は、ヘルプの HOM のリファレンスで調べられる。

Python Shell で試す
-------------------

:menuselection:`Windows --> Python Shell` で Python Shell を開き、次のコードを 1 行ずつ入力する。

.. code-block:: python
   :linenos:

   geo = hou.node("/obj").createNode("geo", "hello")
   box = geo.createNode("box")
   box.parmTuple("size").set((2, 1, 1))
   xform = geo.createNode("xform")
   xform.setFirstInput(box)
   xform.parm("ry").set(45)
   xform.setDisplayFlag(True)
   print(len(xform.geometry().points()))
   print([n.name() for n in geo.children()])

1 行目で ``/obj`` に Geometry ノード ``hello`` を作り、2 行目でその中に Box ノードを作っている。``createNode()`` の 1 番目の引数はノードの種類の内部名、2 番目の引数はノードの名前である。名前を省略すると、``box1`` のような名前が自動的に付く。4 行目の ``"xform"`` は Transform ノードの内部名である。ノードの種類の内部名は、Tab メニューでノードを作った後に、Python Shell で ``hou.node("ノードのパス").type().name()`` を実行すると確かめられる。

8 行目は、Transform ノードの出力のポイントの数（8）を表示する。9 行目は ``['box1', 'transform1']`` を表示する。ネットワークエディターで ``/obj/hello`` を開くと、2 個のノードがつながっていることを確かめられる。

画面で操作したことをコードで書くときは、次の方法で必要な名前を調べる。

* パラメーターの内部名: パラメーターのラベルにマウスを重ねる。
* メニューの値: Python Shell で ``node.parm("名前").parmTemplate().menuItems()`` を実行すると、メニューの選択肢の内部名が分かる。

スクリプトでネットワークを組む
------------------------------

本資料のサンプルコードの ``build_*.py`` は、全てこの方法でネットワークを組み立てている。例えば ``build_table.py`` の、天板を作る部分は次のとおりである。

.. literalinclude:: ../examples/build_table.py
   :language: python
   :start-at: def build()
   :end-before: # 配線用の穴
   :linenos:

``recreate_geo()`` は、``examples/common.py`` で定義した関数で、同じ名前のノードがあれば削除してから Geometry ノードを作る。こうしておくと、スクリプトを何度実行しても同じ結果になる。

``"polybevel::3.0"`` の ``::3.0`` は、ノードの種類のバージョンである。Houdini では、ノードの仕様を大きく変えるときに、古いバージョンを残したまま新しいバージョンを追加する。Tab メニューで作っても、``createNode("polybevel")`` のようにバージョンを省略しても、その時点の最新のバージョンが作られる。ただし、Houdini を更新して新しいバージョンが追加されると、同じスクリプトから別のバージョンのノードが作られ、パラメーターの名前が変わることがある。本資料のスクリプトでは、結果を再現できるようにバージョンを明示している。ノードのバージョンは、Python Shell で ``node.type().name()`` を実行すると分かる。

スクリプトでネットワークを組む利点は、次のとおりである。

* 手順が正確に記録され、同じものを何度でも作れる。
* Git などのバージョン管理システムで差分を確認できる。hip ファイルはバイナリなので差分が読めない。
* パラメーターを変えたバリエーションを、ループで大量に作れる。

ジオメトリを読む
----------------

``hou.Geometry`` を使うと、ノードの出力の中身を Python で調べられる。サンプルコードの ``inspect_geometry.py`` は、ジオメトリの要素の数、アトリビュートの一覧、先頭のポイントの位置を表示する。

.. literalinclude:: ../examples/inspect_geometry.py
   :language: python
   :pyobject: describe
   :linenos:

``build_table.py`` で机を作った後に ``inspect_geometry.describe("/obj/table/OUT")`` を実行すると、次のように表示される。

.. code-block:: none
   :linenos:

   == /obj/table/OUT (null) ==
   ポイント: 104, プリミティブ: 74, バーテックス: 340
   ポイントアトリビュート: P(Floatx3)
   バーテックスアトリビュート: なし
   プリミティブアトリビュート: なし
   ディテールアトリビュート: なし
     ポイント 0: P = (0.595, 0.685, -0.350)
     ポイント 1: P = (0.595, 0.680, -0.345)
     ポイント 2: P = (0.600, 0.685, -0.345)
     ポイント 3: P = (0.595, 0.720, -0.345)
     ポイント 4: P = (0.595, 0.715, -0.350)

Python SOP
----------

Python SOP は、Python のコードでジオメトリを作ったり変更したりする SOP である。:guilabel:`Python Code` パラメーターに書いたコードが、ノードがクックされるたびに実行される。コードの中では、``hou.pwd()`` がこの Python SOP 自身を表し、``hou.pwd().geometry()`` が出力するジオメトリを表す。入力がつながっていれば、出力のジオメトリは最初は入力のコピーであり、それを変更する。入力が無ければ空のジオメトリから始まる。

サンプルコードの ``python_sop_wave.py`` は、ポイントとポリゴンを作って波打つ面を作る。

.. literalinclude:: ../examples/python_sop_wave.py
   :language: python
   :linenos:

``createPoints()`` は、位置のリストからまとめてポイントを作り、作ったポイントのリストを返す。``createPolygons()`` は、ポイントの組のリストからまとめてポリゴンを作る。:doc:`cg_basics` で説明したとおり、Houdini では面を表から見て時計回りにポイントを並べる。逆に並べると、面が下を向いてしまう。

このコードを Python SOP に貼り付けるには、``build_python_sop.py`` を実行するか、Python SOP を作って :guilabel:`Python Code` にファイルの中身を貼り付ける。``hou.frame()`` を使っているので、再生すると波が動く。

:doc:`vex` で見たとおり、Python SOP は要素の多い処理では VEX よりずっと遅い。Python SOP は、ファイルや外部のライブラリからデータを読み込んでジオメトリにする場合など、Python でなければ書けない処理に使う。

シェルフツール
--------------

シェルフツールは、シェルフに置くボタンで、押すと Python のスクリプトが実行される。よく行う操作を 1 回のクリックで実行できるようにする。

#. シェルフのタブの空いている所で RMB をクリックし、:guilabel:`New Tool` を選ぶ。
#. 開いたウィンドウの :guilabel:`Options` タブで、:guilabel:`Name`\ （内部名）と :guilabel:`Label`\ （表示名）を入力する。
#. :guilabel:`Script` タブに Python のコードを書き、:guilabel:`Accept` を押す。

サンプルコードの ``shelf_tool_add_out.py`` は、選択している SOP のノードの後ろに、出力用の Null ノード ``OUT`` を追加するツールである。ファイルの中身を :guilabel:`Script` タブにそのまま貼り付けて使う。

.. literalinclude:: ../examples/shelf_tool_add_out.py
   :language: python
   :linenos:

``hou.selectedNodes()`` は、ネットワークエディターで選択しているノードのリストを返す。``hou.ui.displayMessage()`` は、メッセージのウィンドウを表示する。``hou.ui`` は画面に関する機能なので、画面の無い hython では使えない。

hython
------

hython は、Houdini に付属する Python のインタープリターで、``hou`` モジュールを最初から使える。Houdini の画面を開かずに、hip ファイルの読み込み、ノードのクック、ファイルの書き出し、レンダリングなどを実行できる。大量のファイルを一括で処理したり、夜間に自動でレンダリングしたりするのに使う。

hython の実行ファイルは、Houdini のインストール先の ``bin`` ディレクトリにある。

.. code-block:: bat
   :linenos:

   "C:\Program Files\Side Effects Software\Houdini 22.0.466\bin\hython.exe" build_city.py city.hipnc

本資料のサンプルコードの ``build_*.py`` は、hython で実行すると、ネットワークを組み立ててエラーが無いかを確かめ、結果の一部を表示する。コマンドライン引数でファイル名を渡すと、シーンを hip ファイルに保存する。この部分は、各スクリプトの ``main()`` 関数に書いてある。

hython は、Apprentice のライセンスでも動作する（本資料の執筆時に確認した）。ただし、保存されるファイルは Apprentice の形式（非商用）になる。

型ヒントと静的検査
------------------

``hou`` モジュールは Houdini の中でしか読み込めず、型の情報（スタブ）も付属していない。そのため、Houdini の外で mypy などの型検査を実行すると、``hou`` を読み込めないというエラーになる。本資料のサンプルコードでは、``examples/setup.cfg`` に次の設定を書き、``hou`` に関する値を ``Any`` 型として扱わせている。

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:

この設定で、``hou`` 以外の部分（自分で書いた関数の引数や戻り値）は厳密に型検査される。``setup.cfg`` に日本語のコメントを書くと、Windows では mypy が設定ファイルを読めずにエラーになるため、英語で書いている。

モジュールの名前に注意する
--------------------------

自分で作った Python のファイルの名前が、Houdini が内部で使うモジュールの名前と同じだと、Houdini がそちらを誤って読み込むことがある。Python は、実行したスクリプトのあるディレクトリや ``sys.path`` に追加したディレクトリから、先にモジュールを探すためである。

本資料の執筆中にも、hython で試験用に作った ``dbg.py`` が Houdini の内部のモジュール ``dbg`` の代わりに読み込まれ、マテリアルの変換が黙って失敗して、レンダリング結果から色が消える現象が起きた。エラーの表示はほとんど無かった。自分のファイルには、``build_table.py`` のように用途の分かる、他と重なりにくい名前を付けるとよい。
