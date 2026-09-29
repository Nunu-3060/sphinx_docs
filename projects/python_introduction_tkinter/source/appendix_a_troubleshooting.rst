付録 A よくあるトラブル
=======================

A.1 tkinter を import できない
------------------------------

``ModuleNotFoundError: No module named 'tkinter'`` や ``No module named '_tkinter'`` が表示される場合は、Python に tkinter が含まれていません。環境に応じて、次の方法でインストールしてください。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 環境
     - 対処方法
   * - Windows（python.org のインストーラー）
     - 従来のインストーラーの場合は、インストーラーを再度実行して「Modify」を選び、「tcl/tk and IDLE」にチェックを入れます。Python インストールマネージャーでインストールした場合は、tkinter が含まれています。
   * - Debian、Ubuntu
     - ``sudo apt install python3-tk`` を実行します。
   * - Fedora
     - ``sudo dnf install python3-tkinter`` を実行します。
   * - macOS（Homebrew の Python）
     - ``brew install python-tk`` を実行します。

A.2 ウィンドウが表示されない、すぐに消える
------------------------------------------

スクリプトの最後で ``mainloop`` を呼び出しているかを確認してください。``mainloop`` を呼び出さないと、スクリプトの終了とともにウィンドウも閉じます（:doc:`第 2 章 <02_first_window>`\ 参照）。

また、``geometry`` で画面の外の位置を指定していないかも確認してください。

A.3 ウィジェットが表示されない
------------------------------

ウィジェットを作成した後、``pack``、``grid``、``place`` のいずれかで配置しているかを確認してください。作成しただけのウィジェットは表示されません。

``_tkinter.TclError: cannot use geometry manager grid inside . which already has slaves managed by pack`` のようなエラーが表示される場合は、同じ親ウィジェットの中で ``pack`` と ``grid`` を混在させています（:doc:`第 4 章 <04_layout>`\ 参照）。

A.4 ボタンを押す前に関数が実行される
------------------------------------

``command=on_click()`` のように、関数名の後に丸かっこを付けていないかを確認してください。丸かっこを付けると、ウィジェットの作成時に関数が実行されます。``command=on_click`` と書くのが正しい指定です（:doc:`第 3 章 <03_basic_widgets>`\ 参照）。

A.5 画像が表示されない
----------------------

``tk.PhotoImage`` で読み込んだ画像は、Python 側のオブジェクトがどこからも参照されなくなると破棄され、表示されなくなります。関数の中で画像を読み込んだ場合は、ウィジェットの属性に保存するなどして参照を保持してください。

.. code-block:: python

   def create_logo(parent: tk.Misc) -> ttk.Label:
       photo = tk.PhotoImage(file="logo.png")
       label = ttk.Label(parent, image=photo)
       label.image = photo  # 参照を保持する
       return label

``tk.PhotoImage`` が読み込める形式は、PNG、GIF、PPM/PGM です。JPEG などを表示するには、Pillow ライブラリの ``ImageTk.PhotoImage`` を使います。

A.6 Windows で文字がぼやける
----------------------------

Windows のディスプレイの拡大率を 100% より大きくしていると、tkinter のウィンドウ全体が拡大されて、文字がぼやけることがあります。この場合は、``tk.Tk()`` を呼び出す前に次のコードを実行すると、くっきりと表示されます。

.. code-block:: python

   import ctypes
   import sys

   if sys.platform == "win32":
       ctypes.windll.shcore.SetProcessDpiAwareness(1)

この設定をすると、ポイント単位で指定したフォントは拡大率に合わせた大きさで表示されますが、ピクセル単位で指定したウィンドウの大きさや余白は相対的に小さく見えます。必要に応じて値を調整してください。

A.7 処理中に画面が固まる
------------------------

コールバック関数の中で時間のかかる処理を実行していないかを確認してください。対処方法は\ :doc:`第 10 章 <10_long_task>`\ で説明しています。

A.8 エラーが表示されずに処理が止まる
------------------------------------

コールバック関数の中で例外が発生すると、tkinter はトレースバックを標準エラー出力に表示し、アプリケーションの実行を続けます。そのため、``pythonw`` でコンソールなしに起動した場合などは、エラーに気付きにくくなります。

``report_callback_exception`` を置き換えると、コールバック関数の中で発生した例外をダイアログで表示できます。

.. code-block:: python

   import traceback
   from tkinter import messagebox
   from types import TracebackType


   def show_error(
       exc_type: type[BaseException],
       exc_value: BaseException,
       exc_traceback: TracebackType | None,
   ) -> None:
       message = "".join(
           traceback.format_exception(exc_type, exc_value, exc_traceback)
       )
       messagebox.showerror("エラー", message)


   root = tk.Tk()
   root.report_callback_exception = show_error

A.9 日本語を入力できない
------------------------

Windows と macOS では、Entry や Text で日本語入力（IME）を使えます。Linux では、入力メソッドの設定によっては日本語を入力できないことがあります。その場合は、入力メソッドのフレームワーク（Fcitx や IBus など）が XIM に対応するよう設定されているかを確認してください。
