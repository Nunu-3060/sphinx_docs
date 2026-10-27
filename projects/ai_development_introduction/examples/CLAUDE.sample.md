# 注文管理 API

FastAPI で作った注文管理の Web API。DB は PostgreSQL。

## よく使うコマンド

- テスト: `python -m pytest -q`（DB を使うテストは先に `docker compose up -d db`）
- 静的解析: `flake8 src tests` と `mypy src`
- 開発サーバー: `uvicorn app.main:app --reload`

## 規約

- 型ヒントを必ず書く。mypy の strict モードを通すこと
- DB へのアクセスは `src/app/repositories/` に閉じ込め、API 層から直接 SQL を書かない
- 金額は `Decimal` で扱う。`float` を使わない

## 作業の進め方

- 実装の前に、変更方針を箇条書きで示して確認を取る
- 振る舞いを変えたらテストを追加し、`python -m pytest -q` が成功するまで修正する
- 仕様は `docs/specs/` にある。仕様と実装が食い違ったら、実装せずに報告する

## してはいけないこと

- `migrations/` 配下の既存ファイルを編集しない（新しいマイグレーションを追加する）
- `.env` を読まない、コミットしない
