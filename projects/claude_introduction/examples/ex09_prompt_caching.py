"""プロンプトキャッシュで、共通の長い前置き部分を再利用するサンプル.

同じ長い資料に対して質問を繰り返すと、2 回目以降は資料部分が
キャッシュから読み出され、料金と応答時間が下がります。

実行例:
    python ex09_prompt_caching.py
"""

import os

import anthropic
from anthropic.types import TextBlockParam

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")

# 実際には社内規程や仕様書などの長い資料を読み込む想定。
# キャッシュされるには一定以上 (モデルにより数百から数千トークン) の長さが必要。
MANUAL = "\n".join(
    f"第 {i} 条: 申請書は所定の様式で提出し、上長の承認を得ること。"
    for i in range(1, 400)
)

QUESTIONS = [
    "第 10 条の内容を教えてください。",
    "第 200 条の内容を教えてください。",
]


def main() -> None:
    client = anthropic.Anthropic()

    # 変化しない部分 (資料) を先頭に置き、cache_control を付ける
    system: list[TextBlockParam] = [
        {"type": "text", "text": "あなたは社内規程に関する質問に答える担当者です。"},
        {
            "type": "text",
            "text": MANUAL,
            "cache_control": {"type": "ephemeral"},
        },
    ]

    for question in QUESTIONS:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": question}],
        )
        usage = response.usage
        print(f"Q: {question}")
        print(f"  キャッシュ書き込み: {usage.cache_creation_input_tokens}")
        print(f"  キャッシュ読み出し: {usage.cache_read_input_tokens}")
        print(f"  通常の入力        : {usage.input_tokens}")


if __name__ == "__main__":
    main()
