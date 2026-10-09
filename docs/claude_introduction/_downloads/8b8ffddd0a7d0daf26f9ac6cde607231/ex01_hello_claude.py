"""最小構成で Claude にメッセージを送るサンプル.

実行前に環境変数 ANTHROPIC_API_KEY を設定してください。
使用するモデルは環境変数 CLAUDE_MODEL で変更できます。

実行例:
    python ex01_hello_claude.py
"""

import os

import anthropic

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")


def main() -> None:
    # API キーは環境変数 ANTHROPIC_API_KEY から自動的に読み込まれる
    client = anthropic.Anthropic()

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Python の特徴を 3 行で説明してください。"},
        ],
    )

    # 応答はコンテンツブロックのリスト。テキストブロックだけを表示する
    for block in response.content:
        if block.type == "text":
            print(block.text)

    print("---")
    print(f"stop_reason  : {response.stop_reason}")
    print(f"input_tokens : {response.usage.input_tokens}")
    print(f"output_tokens: {response.usage.output_tokens}")


if __name__ == "__main__":
    main()
