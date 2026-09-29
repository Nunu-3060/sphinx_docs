unittest.mock
=============

テストの中で、外部への依存（ネットワークアクセス、データベース、他の
関数呼び出しなど）を偽物のオブジェクトに置き換えるためのモジュール。
本物を用意する代わりに ``Mock`` オブジェクトを使うことで、外部要因に
左右されない高速で再現性の高いテストが書ける。

Mock
----

``Mock`` は、どんな属性アクセスやメソッド呼び出しにも応答する汎用的なモックオブジェクト。呼び出されると自動的にその呼び出し内容（引数や呼び出し回数）を記録するため、後から「期待通りに呼ばれたか」を検証できる。``assert_called_once_with()`` は、指定した引数でちょうど1回だけ呼ばれたことを検証するメソッドで、``call_count``/``call_args`` からは呼び出し回数や実際に渡された引数を直接参照できる。

.. code-block:: python

   from unittest.mock import Mock

   mock = Mock()
   mock(1, 2, key="value")

   print(mock.call_count)  # 1
   print(mock.call_args)   # call(1, 2, key='value')

   mock.assert_called_once_with(1, 2, key="value")  # 検証成功（何も起きない）

   # 期待と異なる引数で検証すると AssertionError が送出される
   mock.assert_called_once_with(9, 9)
   # AssertionError: expected call not found.
   # Expected: mock(9, 9)
   #   Actual: mock(1, 2, key='value')

MagicMock
---------

``MagicMock`` は ``Mock`` を継承しており、それに加えて ``__len__``/``__iter__`` のようなマジックメソッド（特殊メソッド）もあらかじめ実装している。``len()`` や ``for`` 文でイテレートする対象など、マジックメソッド経由でアクセスされる可能性があるオブジェクトを置き換える場合は ``MagicMock`` が必要になる。後述する ``patch()`` は、明示的に指定しない限りデフォルトで ``MagicMock`` を使ってオブジェクトを置き換える。

.. code-block:: python

   from unittest.mock import MagicMock

   m = MagicMock()
   m.__len__.return_value = 3

   print(len(m))  # 3

patch()
-------

``patch()`` は、テストの実行中だけ対象のオブジェクトを ``MagicMock`` に一時的に置き換え、テスト終了後に自動的に元へ戻すための仕組みで、``unittest.mock`` の中でも最もよく使われる機能。デコレータとして使う方法と、``with`` 文のコンテキストマネージャとして使う方法があり、どちらも置き換え対象は文字列で「その名前が参照されている場所」を指定する（定義元ではなく、テスト対象のモジュールから見た参照先を指定する点に注意）。

以下は、外部 API を呼び出す ``requests.get`` をパッチして、実際には
ネットワークアクセスを行わずにテストする例。

.. code-block:: python

   # myapp.py
   import requests


   def get_weather(city):
       response = requests.get(f"https://api.example.com/weather/{city}")
       response.raise_for_status()
       return response.json()["temperature"]

.. code-block:: python

   # test_myapp.py
   import unittest
   from unittest.mock import patch

   import myapp


   class TestGetWeather(unittest.TestCase):

       # デコレータとして使う場合、パッチ対象の Mock がテストメソッドの
       # 引数として渡される
       @patch("myapp.requests.get")
       def test_get_weather_decorator(self, mock_get):
           mock_get.return_value.json.return_value = {"temperature": 21.5}

           result = myapp.get_weather("Tokyo")

           self.assertEqual(result, 21.5)
           mock_get.assert_called_once_with(
               "https://api.example.com/weather/Tokyo"
           )

       # コンテキストマネージャとして使う場合、with ブロックの中だけ
       # パッチが有効になる
       def test_get_weather_context_manager(self):
           with patch("myapp.requests.get") as mock_get:
               mock_get.return_value.json.return_value = {"temperature": 18.0}

               result = myapp.get_weather("Osaka")

               self.assertEqual(result, 18.0)


   if __name__ == "__main__":
       unittest.main()

return_value / side_effect
------------------------------

モックが呼び出されたときの振る舞いは、``return_value``/``side_effect`` で細かく制御できる。``return_value`` は呼び出し時に返す値をそのまま指定する。``side_effect`` には例外オブジェクトや呼び出し可能オブジェクトを指定でき、例外オブジェクトを指定すればモック呼び出し時にその例外が送出され、関数を指定すればモック呼び出し時にその関数が実際に呼ばれてその戻り値が返される（引数ごとに異なる値を返したい場合や、副作用を再現したい場合に便利）。

.. code-block:: python

   from unittest.mock import Mock

   # return_value: 呼び出されたときに返す値を固定する
   mock = Mock(return_value=42)
   print(mock())  # 42

   # side_effect に例外を渡すと、呼び出し時にその例外が送出される
   mock2 = Mock(side_effect=ConnectionError("接続失敗"))
   try:
       mock2()
   except ConnectionError as e:
       print("raised:", e)  # raised: 接続失敗

   # side_effect に関数を渡すと、呼び出し時にその関数が実行される
   def fake_add(a, b):
       return a + b + 100

   mock3 = Mock(side_effect=fake_add)
   print(mock3(1, 2))  # 103

.. note::

   ``patch()`` にも ``return_value``/``side_effect`` を直接渡せる
   （例: ``@patch("myapp.requests.get", side_effect=TimeoutError)``）。
   モックの戻り値を1行で設定したいだけの単純なケースでは、
   パッチ後に別途属性を設定するよりも簡潔に書ける。
