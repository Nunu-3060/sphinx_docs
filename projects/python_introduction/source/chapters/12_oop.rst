第 12 章 クラスとオブジェクト指向
=================================

クラスとは
----------

クラスとは、関連するデータ（属性）と処理（メソッド）をひとまとめにした設計図のようなものである。クラスから作られた実体のことを、インスタンスと呼ぶ。同じクラスから複数のインスタンスを作成でき、それぞれのインスタンスは独立した属性の値を持つ。

クラスの定義
------------

Python では、``class`` キーワードを使ってクラスを定義する。インスタンスが作成される際に自動的に呼び出される特別なメソッドを ``__init__`` メソッドと呼び、属性の初期化に使用する。クラスの定義の直後や、``__init__`` メソッドをはじめとする各メソッドの定義の直後には、第 7 章で説明した docstring を書ける。

.. code-block:: python
   :linenos:

   class BankAccount:
       """銀行口座を表すクラス。"""

       def __init__(self, owner: str, balance: int = 0) -> None:
           """口座の名義人と残高を初期化する。"""
           self.owner: str = owner
           self.balance: int = balance

       def deposit(self, amount: int) -> None:
           """口座に指定した金額を入金する。"""
           self.balance += amount

   account: BankAccount = BankAccount("伊藤", 1000)
   account.deposit(500)
   print(account.balance)  # 1500

``self`` は、メソッドが呼び出されたインスタンス自身を指す引数である。クラス内のメソッドを定義する際は、第 1 引数として必ず ``self`` を書く。``self.owner`` や ``self.balance`` のように、属性にも型ヒントを付けられる。また、``account: BankAccount`` のように、クラス自体を型ヒントとして使うこともできる。この書き方により、``account`` に対して ``BankAccount`` クラスにない属性やメソッドを使おうとした場合に、``mypy`` で誤りを検出できるようになる。

特殊メソッド
------------

Python のクラスには、``__str__`` のように前後にアンダースコアを 2 つ付けた特殊メソッドを定義できる。``__str__`` メソッドを定義すると、``print`` 関数でインスタンスを表示したときに、その戻り値が表示されるようになる。

.. code-block:: python
   :linenos:

   class BankAccount:
       def __init__(self, owner: str, balance: int = 0) -> None:
           self.owner: str = owner
           self.balance: int = balance

       def __str__(self) -> str:
           return f"{self.owner} の口座残高: {self.balance} 円"

   account = BankAccount("伊藤", 1000)
   print(account)  # 伊藤 の口座残高: 1000 円

特殊メソッドは、``__init__`` や ``__str__`` のほかにも数多く用意されており、決められた名前と書き方に従うことで、Python の組み込みの構文や関数からクラスを扱えるようになる。代表的なものを次に示す。

.. list-table::
   :header-rows: 1

   * - 特殊メソッド
     - 呼び出される場面
   * - ``__init__``
     - インスタンスが作成されたとき
   * - ``__str__``
     - ``print`` 関数や ``str`` 関数で文字列に変換するとき
   * - ``__eq__``
     - ``==`` 演算子でインスタンス同士を比較するとき
   * - ``__len__``
     - ``len`` 関数でインスタンスの長さを取得するとき

本資料では ``__init__`` と ``__str__`` のみを扱う。これら以外の特殊メソッドについては、必要に応じて Python 公式ドキュメントで調べるとよい。

継承
----

継承とは、既存のクラスの属性やメソッドを引き継いで、新しいクラスを定義する仕組みである。継承元のクラスを親クラス（基底クラス）、継承先のクラスを子クラス（派生クラス）と呼ぶ。子クラスでは、``super()`` を使って親クラスの ``__init__`` メソッドを呼び出せる。

.. code-block:: python
   :linenos:

   class SavingsAccount(BankAccount):
       def __init__(self, owner: str, balance: int = 0, interest_rate: float = 0.01) -> None:
           super().__init__(owner, balance)
           self.interest_rate: float = interest_rate

       def add_interest(self) -> None:
           self.balance += int(self.balance * self.interest_rate)

``SavingsAccount`` クラスは ``BankAccount`` クラスを継承しているため、``BankAccount`` クラスに定義されているメソッド（これまでの例で定義した ``deposit`` メソッドや ``__str__`` メソッドなど）を、定義し直さずにそのまま利用できる。``super()`` は親クラスを指し、``super().__init__(owner, balance)`` によって、名義人と残高の初期化を親クラスの ``__init__`` メソッドに任せている。

サンプルコード
--------------

銀行口座を表すクラスと、それを継承した貯蓄口座のクラスをまとめたサンプルコードである。

:download:`oop.py <../../examples/ch12_oop/oop.py>`

.. literalinclude:: ../../examples/ch12_oop/oop.py
   :language: python3
   :linenos:
