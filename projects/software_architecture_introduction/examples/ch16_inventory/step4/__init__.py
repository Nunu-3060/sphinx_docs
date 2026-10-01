"""段階 4: レイヤーに分け、依存性注入とテストを加える.

* domain: 商品と在庫の規則、リポジトリのインターフェース
* repository: 商品の保存の実装（JSON ファイル版とメモリ版）
* service: ユースケース
* cli: コマンドライン引数の解析と表示
* main: オブジェクトの組み立て（コンポジションルート）
* test_service: domain、service、repository、cli のテスト

実行方法（examples フォルダーで実行します）::

    python -m ch16_inventory.step4.main register A-1 ボールペン
    python -m ch16_inventory.step4.main list
    python -m ch16_inventory.step4.main --file stock.json register B-1 ノート
    python -m ch16_inventory.step4.main --file stock.json list
    python -m unittest ch16_inventory.step4.test_service -v
"""
