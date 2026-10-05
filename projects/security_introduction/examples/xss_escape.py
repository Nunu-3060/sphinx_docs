"""クロスサイトスクリプティング（XSS）と出力エスケープのサンプル.

利用者の入力をそのまま HTML に埋め込むと、入力に含まれるスクリプトが
ブラウザーで実行されます。HTML に出力する前にエスケープします。

実行方法:
    python xss_escape.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import html


def render_unsafe(comment: str) -> str:
    """入力をそのまま HTML に埋め込む（悪い例）."""
    return f"<p>{comment}</p>"


def render_safe(comment: str) -> str:
    """入力をエスケープしてから HTML に埋め込む（良い例）."""
    return f"<p>{html.escape(comment)}</p>"


def render_attribute_safe(url: str) -> str:
    """属性値に埋め込む場合も引用符で囲み、エスケープする.

    ただし javascript: で始まる URL はエスケープしても実行されるため、
    URL のスキームは許可リストで別途検証する必要がある。
    """
    if not url.startswith(("https://", "http://")):
        url = "#"
    return f'<a href="{html.escape(url, quote=True)}">リンク</a>'


def main() -> None:
    attack = '<script>alert("XSS")</script>'

    print(f"悪い例: {render_unsafe(attack)}")
    print(f"良い例: {render_safe(attack)}")

    print(f"属性値: {render_attribute_safe('https://example.com/?q=1&r=2')}")
    print(f"属性値: {render_attribute_safe('javascript:alert(1)')}")
    print(f"属性値: {render_attribute_safe('https://x/" onclick="evil()')}")


if __name__ == "__main__":
    main()
