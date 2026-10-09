"""システムプロンプトで Claude の役割と出力形式を指定するサンプル.

同じ質問に対して、システムプロンプトの有無で応答がどう変わるかを比較します。

実行例:
    python ex02_system_prompt.py
"""

import os

import anthropic

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")

SYSTEM_PROMPT = """\
あなたは社内向けの Python コードレビュー担当者です。
以下のルールに従って回答してください。

- 指摘は重要度の高い順に箇条書きで示す
- 各指摘には修正後のコードを付ける
- 問題がなければ「指摘なし」とだけ答える
"""

CODE = """\
def average(values):
    return sum(values) / len(values)
"""


def ask(client: anthropic.Anthropic, system: str | None) -> str:
    """CODE のレビューを依頼し、応答テキストを返す."""
    question = f"次のコードをレビューしてください。\n\n{CODE}"
    if system is None:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            messages=[{"role": "user", "content": question}],
        )
    else:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": question}],
        )
    return "".join(b.text for b in response.content if b.type == "text")


def main() -> None:
    client = anthropic.Anthropic()

    print("=== システムプロンプトなし ===")
    print(ask(client, None))
    print()
    print("=== システムプロンプトあり ===")
    print(ask(client, SYSTEM_PROMPT))


if __name__ == "__main__":
    main()
