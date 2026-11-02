# todo-cli

コマンドラインでタスクを管理するツール。

## 必要な環境

- Python 3.10 以上

## インストール

```bash
pip install todo-cli
```

## 使い方

| コマンド | 動作 |
| --- | --- |
| `todo add "タスク"` | タスクを追加する |
| `todo list` | タスクの一覧を表示する |
| `todo done 番号` | 指定した番号のタスクを完了にする |

実行例：

```console
$ todo add "牛乳を買う"
タスク 1 を追加した：牛乳を買う
$ todo list
[ ] 1. 牛乳を買う
$ todo done 1
タスク 1 を完了にした：牛乳を買う
```

> [!NOTE]
> データはホームフォルダの `.todo.json` に保存される。

## ライセンス

[MIT License](LICENSE)
