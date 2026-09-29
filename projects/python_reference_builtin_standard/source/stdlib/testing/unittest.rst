unittest
========

Python 標準のユニットテストフレームワーク。``TestCase`` を継承したクラスに
テストメソッドを書き、コードが期待通りに動作するかを自動的に検証する。
追加のインストールが不要で標準ライブラリだけで完結するため、多くの
既存プロジェクトで採用されている。

基本構造: TestCase / ``test_`` で始まるメソッド
--------------------------------------------------

テストは ``unittest.TestCase`` を継承したクラスとして書く。クラス内の ``test_`` で始まるメソッドがテストケースとして自動的に認識され、実行される。実行するには ``unittest.main()`` を呼び出すか、コマンドラインから ``python -m unittest ファイル名`` とする。

.. code-block:: python

   # test_calc.py
   import unittest


   def add(a, b):
       return a + b


   class TestCalc(unittest.TestCase):

       def test_add(self):
           self.assertEqual(add(2, 3), 5)

       def test_add_is_commutative(self):
           self.assertEqual(add(2, 3), add(3, 2))


   if __name__ == "__main__":
       unittest.main()

上記のファイルを実行すると、以下のような出力が得られる。

.. code-block:: text

   $ python -m unittest test_calc -v
   test_add (test_calc.TestCalc.test_add) ... ok
   test_add_is_commutative (test_calc.TestCalc.test_add_is_commutative) ... ok

   ----------------------------------------------------------------------
   Ran 2 tests in 0.001s

   OK

代表的なアサーションメソッド
--------------------------------

``TestCase`` は、値を検証するための多数の ``assert*`` メソッドを提供する。最もよく使うのは、値が等しいことを検証する ``assertEqual``、真偽値を検証する ``assertTrue``/``assertFalse``、そして例外の送出を検証する ``assertRaises`` である。``assertRaises`` はコンテキストマネージャとして使うと、``with`` ブロック内で対象の例外が発生したかどうかを検証できる。

.. code-block:: python

   import unittest


   def divide(a, b):
       if b == 0:
           raise ValueError("0 で割ることはできません")
       return a / b


   class TestDivide(unittest.TestCase):

       def test_divide(self):
           self.assertEqual(divide(6, 3), 2)

       def test_divide_is_positive(self):
           self.assertTrue(divide(6, 3) > 0)

       def test_divide_by_zero_raises(self):
           with self.assertRaises(ValueError):
               divide(1, 0)

.. note::

   このほかにも、値がコンテナに含まれるかを調べる ``assertIn``、``None`` であることを調べる ``assertIsNone``、浮動小数点数の近似比較を行う ``assertAlmostEqual`` など、多数のアサーションメソッドが用意されている。詳しくは公式ドキュメントの一覧を参照。

setUp / tearDown
-------------------

各テストメソッドの実行前・実行後に共通の準備・後片付けを行いたい場合は、``setUp()``/``tearDown()`` をオーバーライドする。``setUp()`` は各テストメソッドの実行前に、``tearDown()`` は実行後に、それぞれ毎回呼び出される。テスト間で状態が影響し合わないよう、テストごとに新しい状態を用意するのに使う。

.. code-block:: python

   import unittest


   class TestStack(unittest.TestCase):

       def setUp(self):
           # 各テストメソッドの実行前に毎回呼ばれる
           self.stack = [1, 2, 3]

       def tearDown(self):
           # 各テストメソッドの実行後に毎回呼ばれる（後片付け用）
           self.stack.clear()

       def test_pop(self):
           self.assertEqual(self.stack.pop(), 3)
           self.assertEqual(self.stack, [1, 2])

       def test_append(self):
           self.stack.append(4)
           self.assertEqual(self.stack, [1, 2, 3, 4])

.. note::

   実務では、より簡潔な構文（``assert`` 文をそのまま使える、フィクスチャの記述がシンプルなど）から、サードパーティ製のテストフレームワークである ``pytest`` が好まれることも多い。ただし ``unittest`` は標準ライブラリの一部であり追加のインストールが不要なこと、既存の多くのコードベースが ``unittest`` で書かれていることから、標準の選択肢として押さえておく価値がある。
