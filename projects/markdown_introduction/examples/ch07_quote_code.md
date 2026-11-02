# エラーの報告

## 発生した現象

テストを実行すると、次のエラーが表示される。

```text
ModuleNotFoundError: No module named 'requests'
```

## 再現する手順

```bash
python -m venv .venv
python main.py
```

## 期待する結果

エラーが表示されずに、プログラムが起動する。

## 実行環境

- Windows 11
- Python 3.12

## 参考

公式ドキュメントには次のように書かれている。

> 仮想環境を作成した後は、必要なパッケージをインストールすること。

---

報告者：山田
