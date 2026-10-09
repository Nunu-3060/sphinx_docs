"""応答をストリーミングで逐次表示するサンプル.

長い応答を生成する場合は、ストリーミングを使うと最初の文字が表示される
までの待ち時間が短くなり、HTTP のタイムアウトも避けられます。

実行例:
    python ex04_streaming.py
"""

import os

import anthropic

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")


def main() -> None:
    client = anthropic.Anthropic()

    with client.messages.stream(
        model=MODEL,
        max_tokens=16000,
        messages=[
            {
                "role": "user",
                "content": "HTTP と HTTPS の違いを 400 字程度で説明してください。",
            },
        ],
    ) as stream:
        # テキストの断片が届くたびに表示する
        for text in stream.text_stream:
            print(text, end="", flush=True)

        # ストリーム終了後、組み立て済みの完全なメッセージを取得できる
        message = stream.get_final_message()

    print()
    print("---")
    print(f"stop_reason  : {message.stop_reason}")
    print(f"output_tokens: {message.usage.output_tokens}")


if __name__ == "__main__":
    main()
