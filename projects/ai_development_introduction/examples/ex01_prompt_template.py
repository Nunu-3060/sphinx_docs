"""プロンプトの構成要素を組み立てるテンプレートの例。

役割・制約・出力形式をシステムプロンプトに、タスク・例・入力を
ユーザーメッセージに配置する。構成要素を分けて管理すると、
どの要素を変えたときに出力がどう変わるかを比較しやすくなる。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Example:
    """入力と期待する出力の組（few-shot の例）。"""

    input: str
    output: str


@dataclass(frozen=True)
class PromptSpec:
    """プロンプトの構成要素。"""

    role: str
    task: str
    constraints: tuple[str, ...] = ()
    examples: tuple[Example, ...] = ()
    output_format: str = ""


def build_system_prompt(spec: PromptSpec) -> str:
    """役割・制約・出力形式からシステムプロンプトを組み立てる。"""
    lines = [spec.role]
    if spec.constraints:
        lines.append("")
        lines.append("# 制約")
        lines.extend(f"- {c}" for c in spec.constraints)
    if spec.output_format:
        lines.append("")
        lines.append("# 出力形式")
        lines.append(spec.output_format)
    return "\n".join(lines)


def build_user_prompt(spec: PromptSpec, input_text: str) -> str:
    """タスク・例・入力からユーザーメッセージを組み立てる。

    入力や例は XML 風のタグで囲み、指示と区別できるようにする。
    """
    parts = [spec.task]
    if spec.examples:
        parts.append("<examples>")
        for ex in spec.examples:
            parts.append(f"<example>\n<input>{ex.input}</input>\n<output>{ex.output}</output>\n</example>")
        parts.append("</examples>")
    parts.append(f"<input>\n{input_text}\n</input>")
    return "\n".join(parts)


def main() -> None:
    spec = PromptSpec(
        role="あなたは Python のコードレビューを担当するシニアエンジニアである。",
        task="次の関数をレビューし、不具合の可能性がある箇所を指摘せよ。",
        constraints=(
            "指摘は不具合に限定し、命名やスタイルには触れない",
            "根拠となる入力例を必ず添える",
            "問題がなければ「指摘なし」とだけ答える",
        ),
        examples=(
            Example(
                input="def head(xs: list[int]) -> int:\n    return xs[0]",
                output='[{"line": 2, "issue": "空リストで IndexError", "input": "[]"}]',
            ),
        ),
        output_format='JSON 配列で返す。各要素は "line"、"issue"、"input" の 3 つのキーを持つ。',
    )
    code = "def average(xs: list[float]) -> float:\n    return sum(xs) / len(xs)"

    print("===== システムプロンプト =====")
    print(build_system_prompt(spec))
    print()
    print("===== ユーザーメッセージ =====")
    print(build_user_prompt(spec, code))


if __name__ == "__main__":
    main()
