"""注文のドメインモデルの例.

* model: 値オブジェクト（Money, OrderLine）、エンティティで集約ルートの
  Order、ドメインサービスの shipping_fee、リポジトリのインターフェース
  OrderRepository
* repository: リポジトリの実装（メモリ版と SQLite 版）
* service: ユースケースを実装するアプリケーションサービス

実行方法（examples フォルダーで実行します）::

    python -m ch12_domain_model.main
"""
