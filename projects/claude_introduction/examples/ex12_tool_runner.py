"""SDK のツールランナーでツール利用のループを自動化するサンプル.

@beta_tool を付けた関数は、型ヒントと docstring からツール定義が
自動生成されます。ループの制御は SDK が行います (ベータ機能)。

実行例:
    python ex12_tool_runner.py
"""

import os
from datetime import date

import anthropic
from anthropic import beta_tool

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")


@beta_tool
def days_until(target: str) -> str:
    """今日から指定日までの日数を返す.

    Args:
        target: 日付。YYYY-MM-DD 形式。
    """
    try:
        delta = date.fromisoformat(target) - date.today()
    except ValueError:
        return f"日付の形式が正しくありません: {target}"
    return f"{target} まで {delta.days} 日です。"


@beta_tool
def weekday_of(target: str) -> str:
    """指定日の曜日を返す.

    Args:
        target: 日付。YYYY-MM-DD 形式。
    """
    names = ["月", "火", "水", "木", "金", "土", "日"]
    try:
        day = date.fromisoformat(target)
    except ValueError:
        return f"日付の形式が正しくありません: {target}"
    return f"{target} は {names[day.weekday()]} 曜日です。"


def main() -> None:
    client = anthropic.Anthropic()

    runner = client.beta.messages.tool_runner(
        model=MODEL,
        max_tokens=4096,
        tools=[days_until, weekday_of],
        messages=[
            {
                "role": "user",
                "content": "2026-12-25 は何曜日で、今日から何日後ですか。",
            },
        ],
    )

    # ツール呼び出しが無くなるまで、各ターンの応答が順に返される
    for message in runner:
        for block in message.content:
            if block.type == "tool_use":
                print(f"[tool] {block.name}({block.input})")
            elif block.type == "text":
                print(block.text)


if __name__ == "__main__":
    main()
