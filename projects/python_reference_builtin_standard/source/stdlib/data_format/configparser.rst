configparser
=============

INI ファイル形式（``[section]`` とキー・バリューの組で構成される設定ファイル）
を読み書きするためのモジュール。アプリケーションの設定ファイルを扱う際によく使われる。

ConfigParser の基本
----------------------

``ConfigParser`` オブジェクトを生成し、``read`` でファイルを読み込む。
設定はセクションごとに辞書のようにアクセスできる。

.. code-block:: python

   >>> # config.ini の内容:
   >>> # [server]
   >>> # host = localhost
   >>> # port = 8080
   >>> # debug = true
   >>>
   >>> import configparser
   >>> config = configparser.ConfigParser()
   >>> config.read("config.ini", encoding="utf-8")
   ['config.ini']
   >>> config["server"]["host"]
   'localhost'
   >>> config["server"]["port"]
   '8080'

セクションとキーの一覧
--------------------------

``sections()`` でセクション名の一覧を、各セクションに対して ``options()`` や辞書メソッドでキーの一覧を取得できる。

.. code-block:: python

   >>> config.sections()
   ['server']
   >>> list(config["server"].keys())
   ['host', 'port', 'debug']
   >>> "server" in config
   True
   >>> config.has_option("server", "port")
   True

getint / getboolean による型変換
-------------------------------------

``config["section"]["key"]`` で取得した値は常に文字列になる。数値や真偽値として扱いたい場合は ``getint``、``getfloat``、``getboolean`` を使うと自動的に変換される。

.. code-block:: python

   >>> config["server"]["port"]
   '8080'
   >>> config.getint("server", "port")
   8080
   >>> config.getboolean("server", "debug")
   True

値の設定とファイルへの書き込み
------------------------------------

セクションの追加や値の変更を行い、``write`` でファイルに保存できる。

.. code-block:: python

   >>> config.add_section("client")
   >>> config["client"]["timeout"] = "30"
   >>> config["server"]["port"] = "9090"
   >>> with open("config.ini", "w", encoding="utf-8") as f:
   ...     config.write(f)
   ...

fallback とデフォルト値
--------------------------

キーが存在しない場合に備え、``get`` 系メソッドには ``fallback`` 引数でデフォルト値を指定できる。

.. code-block:: python

   >>> config.get("server", "timeout", fallback="10")
   '10'
   >>> config.getint("client", "retries", fallback=3)
   3

.. note::

   セクション名・キー名の大文字小文字の扱いなど細かな挙動は Python 公式ドキュメントの configparser モジュールの説明を参照。

.. note::

   ``ConfigParser`` は既定で ``BasicInterpolation`` が有効になっており、値の中の ``%(name)s`` を他のキーの値で置換できる。この機能のため ``%`` はテンプレート構文の特殊文字として扱われ、``value = 50%`` のように ``%`` を単体で含む値をそのまま書くと、読み込み時に ``InterpolationSyntaxError`` が発生する。``%`` そのものを値に含めたい場合は ``%%`` のように 2 つ重ねてエスケープするか、補間機能を無効にした ``configparser.ConfigParser(interpolation=None)`` を使う。

   .. code-block:: python

      >>> config = configparser.ConfigParser()
      >>> config.read_string("[server]\nvalue = 50%\n")
      >>> config["server"]["value"]  # 値を取得しようとした時点でエラーになる
      Traceback (most recent call last):
          ...
      configparser.InterpolationSyntaxError: '%' must be followed by '%' or '(', found: '%'

      >>> config = configparser.ConfigParser()
      >>> config.read_string("[server]\nvalue = 50%%\n")
      >>> config["server"]["value"]
      '50%'

      >>> config = configparser.ConfigParser(interpolation=None)
      >>> config.read_string("[server]\nvalue = 50%\n")
      >>> config["server"]["value"]
      '50%'
