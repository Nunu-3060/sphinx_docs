"""Flask による Web アプリケーションの基本的なセキュリティ対策のサンプル.

次の対策を 1 つのアプリケーションにまとめています。

* テンプレートの自動エスケープによる XSS 対策（比較用に脆弱なページもある）
* CSRF トークンによる CSRF 対策
* セッション Cookie の属性（HttpOnly、SameSite、Secure）
* セキュリティ関連の HTTP レスポンスヘッダー

実行方法:
    python flask_security_demo.py
    起動後、ブラウザーで http://127.0.0.1:5000/ を開きます。
    終了するにはコンソールで Ctrl+C を押します。

注意:
    脆弱なページを含むため、127.0.0.1 以外では待ち受けないでください。

必要なライブラリ:
    Flask（python -m pip install Flask）
"""

import os
import secrets

from flask import Flask, Response, abort, render_template_string, request
from flask import session

app = Flask(__name__)

# 秘密鍵はソースコードに書かず、環境変数から読み込む。
# 未設定の場合は起動のたびに生成する（再起動するとセッションは無効になる）
app.secret_key = os.environ.get("DEMO_SECRET_KEY") or secrets.token_hex(32)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,  # JavaScript から Cookie を読めなくする
    SESSION_COOKIE_SAMESITE="Lax",  # 他サイトからの POST に Cookie を付けない
    # 本番環境（HTTPS）では True にする。このデモは HTTP で動かすため False
    SESSION_COOKIE_SECURE=False,
)

PAGE = """<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>セキュリティ対策のデモ</title></head>
<body>
  <h1>セキュリティ対策のデモ</h1>
  <h2>検索（自動エスケープあり）</h2>
  <form action="/search"><input name="q"><button>検索</button></form>
  <p>比較用の脆弱なページ:
    <a href="/search-unsafe?q=%3Cb%3Ebold%3C%2Fb%3E">/search-unsafe</a></p>
  <h2>送金（CSRF 対策あり）</h2>
  <form method="post" action="/transfer">
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
    送金先 <input name="to"> 金額 <input name="amount">
    <button>送金</button>
  </form>
  {% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>
"""


def get_csrf_token() -> str:
    """セッションに CSRF トークンがなければ生成し、返す."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    token: str = session["csrf_token"]
    return token


@app.after_request
def set_security_headers(response: Response) -> Response:
    """すべてのレスポンスにセキュリティ関連のヘッダーを付ける."""
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; frame-ancestors 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # HTTPS で配信する場合は Strict-Transport-Security も付ける
    return response


@app.get("/")
def index() -> str:
    """トップページ."""
    return render_template_string(PAGE, csrf_token=get_csrf_token(),
                                  message=None)


@app.get("/search")
def search() -> str:
    """検索語をテンプレートで表示する（自動エスケープされる）."""
    query = request.args.get("q", "")
    return render_template_string(
        PAGE, csrf_token=get_csrf_token(),
        message=f"「{query}」の検索結果は 0 件です。",
    )


@app.get("/search-unsafe")
def search_unsafe() -> str:
    """検索語を文字列連結で HTML に埋め込む（悪い例）."""
    query = request.args.get("q", "")
    return f"<p>「{query}」の検索結果は 0 件です。</p>"


@app.post("/transfer")
def transfer() -> str:
    """CSRF トークンを検証してから送金処理を行う."""
    sent = request.form.get("csrf_token", "")
    if not secrets.compare_digest(sent, get_csrf_token()):
        abort(403)
    to = request.form.get("to", "")
    amount = request.form.get("amount", "")
    return render_template_string(
        PAGE, csrf_token=get_csrf_token(),
        message=f"{to} さんに {amount} 円を送金しました（デモ）。",
    )


if __name__ == "__main__":
    # デバッグモードは任意のコードを実行できる機能を持つため、無効にする
    app.run(host="127.0.0.1", port=5000, debug=False)
