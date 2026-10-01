# 「ソフトウェア設計入門」のサンプルコード

資料の各章で使用しているサンプルコードです。Python 3.10 以降で動作し、
標準ライブラリだけを使います。

## 実行方法

このフォルダー（examples）で実行します。

```console
$ python ch03_complexity.py                          # 1 ファイルのサンプル
$ python -m ch11_hexagonal.main                      # フォルダーのサンプル
$ python -m ch16_inventory.step4.main register A-1 ボールペン
$ python -m unittest -v                              # すべてのテスト
```

## コードの検査

```console
$ python -m flake8 .
$ python -m mypy .
```

設定は setup.cfg にあります。

## ファイルの一覧

| ファイル・フォルダー | 章 | 内容 |
| --- | --- | --- |
| ch02_*.py | 2 | 1 本のスクリプトと、分割した構成の比較 |
| ch03_*.py | 3 | 結合度と循環的複雑度 |
| ch04_*.py | 4 | 関数の設計、独自の例外 |
| ch05_data.py | 5 | データクラス、値オブジェクト、列挙型 |
| ch06_composition.py | 6 | 継承とコンポジション |
| ch07_*.py | 7 | SOLID 原則 |
| ch08_*.py | 8 | デザインパターン |
| ch09_circular_bad/, ch09_circular_good/ | 9 | 循環 import とその解消 |
| ch10_dependency_injection.py | 10 | 依存性注入 |
| ch11_layered/, ch11_hexagonal/ | 11 | アーキテクチャパターン |
| ch12_domain_model/ | 12 | ドメインのモデリング |
| ch13_testing/ | 13 | テストダブル |
| ch14_refactoring/ | 14 | リファクタリング |
| ch15_*.md | 15 | ADR のテンプレートと記入例 |
| ch16_inventory/ | 16 | 総合演習（在庫管理 CLI） |
