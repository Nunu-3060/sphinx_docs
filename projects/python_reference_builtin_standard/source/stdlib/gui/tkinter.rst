tkinter
=======

Python 標準の GUI ツールキット。Tcl/Tk をラップしており、ウィンドウやボタン、
テキスト入力欄などの基本的なウィジェットを組み合わせて簡単な GUI アプリケーションを
作成できる。標準ライブラリに含まれているため追加のインストールが不要な点が特徴。

Tk() とメインループ
--------------------

``tkinter.Tk()`` はアプリケーションのルートウィンドウを生成する。ウィジェットを
配置した後、``mainloop()`` を呼び出してイベントループを開始する。この呼び出しは
ウィンドウが閉じられるまでブロックし、その間キー入力やマウス操作などの
イベントを受け付ける。

.. code-block:: python

   import tkinter as tk

   root = tk.Tk()
   root.title("サンプルアプリ")
   root.geometry("300x150")

   root.mainloop()

基本ウィジェット: Label / Button / Entry
------------------------------------------

``Label`` はテキストや画像を表示するウィジェット、``Entry`` は1行のテキスト
入力欄、``Button`` はクリック可能なボタン。いずれもコンストラクタの第一引数に
親ウィジェット（通常はルートウィンドウ）を渡して生成し、その後ジオメトリ
マネージャで画面上に配置する。

.. code-block:: python

   import tkinter as tk

   root = tk.Tk()

   label = tk.Label(root, text="お名前を入力してください")
   entry = tk.Entry(root)
   button = tk.Button(root, text="OK")

   label.pack()
   entry.pack()
   button.pack()

   root.mainloop()

Frame によるグループ化
-------------------------

``Frame`` は見た目を持たないコンテナウィジェットで、複数のウィジェットをまとめて1つの領域として扱うために使う。画面を複数の領域に分けたい場合や、領域ごとに異なるジオメトリマネージャ（``pack()``/``grid()``）を使いたい場合に、``Frame`` の中だけで完結させることで、同じコンテナ内に ``pack()`` と ``grid()`` を混在させてしまう問題を避けられる（詳しくは次節を参照）。

.. code-block:: python

   import tkinter as tk

   root = tk.Tk()

   header = tk.Frame(root)
   header.pack(side="top", fill="x")
   tk.Label(header, text="ヘッダー領域").pack()

   body = tk.Frame(root)
   body.pack(side="top")
   tk.Label(body, text="ユーザー名").grid(row=0, column=0)
   tk.Entry(body).grid(row=0, column=1)

   root.mainloop()

ジオメトリマネージャ: pack() と grid()
------------------------------------------

ウィジェットを配置するには ``pack()`` か ``grid()`` を使うことが多い。``pack()`` はウィジェットを上下左右方向に積み重ねるように配置する簡易的な方法で、単純なレイアウトに向く。``grid()`` は行・列を指定する表形式のレイアウトで、複数のウィジェットを整然と並べたい場合に扱いやすい。同じコンテナ内で ``pack()`` と ``grid()`` を混在させることはできない。

.. code-block:: python

   import tkinter as tk

   root = tk.Tk()

   # pack(): 上から順に積み重ねる
   tk.Label(root, text="pack の例").pack(side="top")

   # grid(): 行・列を指定して配置する
   frame = tk.Frame(root)
   frame.pack()
   tk.Label(frame, text="ユーザー名").grid(row=0, column=0)
   tk.Entry(frame).grid(row=0, column=1)
   tk.Label(frame, text="パスワード").grid(row=1, column=0)
   tk.Entry(frame, show="*").grid(row=1, column=1)

   root.mainloop()

イベント処理とコールバック
-----------------------------

``Button`` の ``command`` 引数に関数を渡すと、クリック時にその関数が呼び出される。より汎用的なイベント（キー入力やマウス移動など）を扱うには ``bind()`` メソッドでイベント名とコールバック関数を対応付ける。

.. code-block:: python

   import tkinter as tk

   def on_click():
       label["text"] = f"こんにちは、{entry.get()} さん"

   root = tk.Tk()

   entry = tk.Entry(root)
   entry.pack()

   button = tk.Button(root, text="挨拶する", command=on_click)
   button.pack()

   label = tk.Label(root, text="")
   label.pack()

   # Enter キー押下でも同じ処理を実行する
   entry.bind("<Return>", lambda event: on_click())

   root.mainloop()

StringVar / IntVar による制御変数
-------------------------------------

前のイベント処理の例では ``label["text"] = ...`` のようにウィジェットの属性を直接書き換えていたが、より tkinter らしい方法として、``StringVar``/``IntVar`` のような制御変数を使うやり方がある。ウィジェットの ``textvariable``/``variable`` 引数にこれらを渡して結びつけておくと、変数の値を ``set()`` するだけでウィジェット側の表示が自動的に更新され、複数のウィジェットで同じ値を共有することも簡単になる。

.. code-block:: python

   import tkinter as tk

   root = tk.Tk()

   greeting = tk.StringVar(value="")

   def on_click():
       greeting.set(f"こんにちは、{entry.get()} さん")

   entry = tk.Entry(root)
   entry.pack()

   button = tk.Button(root, text="挨拶する", command=on_click)
   button.pack()

   # label["text"] を直接更新する代わりに、変数を textvariable で結びつける
   label = tk.Label(root, textvariable=greeting)
   label.pack()

   root.mainloop()

``IntVar`` も同様に、数値を扱うウィジェットと結びつけて使う。以下は
ボタンを押すたびに値が 1 増えるカウンタの例。

.. code-block:: python

   import tkinter as tk

   root = tk.Tk()

   count = tk.IntVar(value=0)

   def increment():
       count.set(count.get() + 1)

   label = tk.Label(root, textvariable=count)
   label.pack()

   button = tk.Button(root, text="+1", command=increment)
   button.pack()

   root.mainloop()

.. note::

   制御変数以外にも、ユーザーへの通知や入力を手軽に行う手段として、ダイアログ用のモジュールが用意されている。確認・警告・エラーなどのメッセージボックス用の ``tkinter.messagebox``、ファイル選択ダイアログ用の ``tkinter.filedialog`` などがある。

ttk によるテーマ付きウィジェット
-----------------------------------

``tkinter.ttk`` は、OS ネイティブに近い見た目のテーマが適用されたウィジェット群を提供するサブモジュール。``Label``/``Button``/``Entry`` などに対応する ``ttk.Label``/``ttk.Button``/``ttk.Entry`` が用意されており、API はほぼ同じまま見た目だけが改善される。新しいコードでは、素の ``tkinter`` ウィジェットの代わりに ``ttk`` を使うことが推奨されることが多い。

.. code-block:: python

   import tkinter as tk
   from tkinter import ttk

   root = tk.Tk()

   ttk.Label(root, text="お名前を入力してください").pack()
   ttk.Entry(root).pack()
   ttk.Button(root, text="OK").pack()

   root.mainloop()

.. note::

   ``ttk`` にはコンボボックス（``ttk.Combobox``）やプログレスバー
   （``ttk.Progressbar``）など、素の ``tkinter`` には無いウィジェットも
   含まれている。一方 ``Frame`` は ``ttk.Frame`` としても提供されており、
   見た目の統一のためにコンテナも ``ttk`` 側に揃えることが多い。

まとめ
--------

.. note::

   この手軽さから、tkinter は社内向けの小さなツールや、スクリプトに簡単な操作画面を付けたい場合の第一候補になりやすい。一方で、モダンな見た目や高度なレイアウト、モバイル対応などが求められる大規模な GUI アプリケーションでは、PyQt/PySide や Kivy といった他のフレームワークが選ばれることも多い。
