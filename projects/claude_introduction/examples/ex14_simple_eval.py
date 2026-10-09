"""プロンプトの品質を評価 (eval) する簡単なサンプル.

正解付きのテストケースに対してプロンプトを実行し、正解率を測ります。
プロンプトやモデルを変更したときに、品質が上がったか下がったかを
数値で比較できるようにするのが目的です。

実行例:
    python ex14_simple_eval.py
"""

import os
from dataclasses import dataclass

import anthropic

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")

LABELS = ("bug", "feature", "question")

SYSTEM_PROMPT = (
    "あなたは課題管理システムの分類担当です。"
    "利用者の投稿を bug / feature / question のいずれかに分類し、"
    "ラベルの英単語 1 語だけを出力してください。"
)


@dataclass(frozen=True)
class Case:
    """評価用のテストケース."""

    text: str
    expected: str


CASES = [
    Case("ログインボタンを押すと 500 エラーになります。", "bug"),
    Case("CSV 形式でもエクスポートできるようにしてほしい。", "feature"),
    Case("パスワードの有効期限は何日ですか。", "question"),
    Case("ダークモードに対応してもらえると助かります。", "feature"),
    Case("保存した設定が再起動すると消えてしまう。", "bug"),
]


def classify(client: anthropic.Anthropic, text: str) -> str:
    """投稿を分類し、ラベルを返す."""
    # 思考のトークンも max_tokens に含まれるため、出力が短くても余裕を持たせる
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
    )
    if response.stop_reason != "end_turn":
        return f"<{response.stop_reason}>"  # 打ち切りや拒否は不正解として扱う
    answer = "".join(b.text for b in response.content if b.type == "text")
    return answer.strip().lower()


def main() -> None:
    client = anthropic.Anthropic()

    correct = 0
    for case in CASES:
        actual = classify(client, case.text)
        ok = actual == case.expected
        correct += ok
        mark = "OK" if ok else "NG"
        print(f"[{mark}] 期待={case.expected:<8} 実際={actual:<8} {case.text}")

    print(f"\n正解率: {correct}/{len(CASES)} ({correct / len(CASES):.0%})")


if __name__ == "__main__":
    main()
