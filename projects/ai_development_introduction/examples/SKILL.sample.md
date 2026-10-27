---
name: add-endpoint
description: 注文管理 API に新しいエンドポイントを追加する手順。API の追加や変更を頼まれたときに使う。
---

# エンドポイントの追加手順

1. `docs/specs/` に仕様書があるか確認する。なければ作業を止めて、仕様書の作成を提案する
2. `src/app/schemas/` にリクエストとレスポンスの Pydantic モデルを追加する
3. `src/app/repositories/` に DB アクセスを追加する
4. `src/app/routers/` にエンドポイントを追加する
5. `tests/api/` に正常系と異常系（400、404）のテストを追加する
6. `python -m pytest -q tests/api` と `mypy src` が成功するまで修正する
7. `docs/api.md` のエンドポイント一覧を更新する
