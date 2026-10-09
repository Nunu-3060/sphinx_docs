# プロジェクト概要

社内向け在庫管理 Web アプリケーション。バックエンドは Python (FastAPI)、
フロントエンドは TypeScript (React)。

# よく使うコマンド

- 開発サーバー起動: `make dev`
- テスト: `pytest -q` (個別に実行する場合は `pytest tests/test_xxx.py -q`)
- 静的解析: `flake8 src && mypy src`

# コーディング規約

- Python は PEP 8 に従い、すべての関数に型ヒントを付ける
- 例外は握りつぶさず、ログに出力してから再送出する
- データベースへのアクセスは `src/repository/` 配下に集約する

# 作業時の注意

- `migrations/` 配下のファイルは手で編集しない (`make migrate-new` で生成する)
- 変更後は必ずテストと静的解析を実行し、結果を報告する
- `.env` には本番の認証情報が含まれるため、読み取らない
