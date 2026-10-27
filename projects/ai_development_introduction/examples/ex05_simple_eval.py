"""プロンプトの 2 つの版を、同じ評価データで採点して比較する例。

題材は不具合報告の重大度（high / medium / low）の分類である。
模擬モデルは、システムプロンプトに書かれた判定基準だけを手がかりに分類する。
そのため、判定基準を充実させた版のほうが正解率が上がる。
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from math import comb

from llm_stub import LLMClient, Message, Response, RuleBasedLLM


@dataclass(frozen=True)
class EvalCase:
    input: str
    expected: str


CASES = [
    EvalCase("保存ボタンを押すと入力したデータが消失する", "high"),
    EvalCase("ログインできない利用者がいる", "high"),
    EvalCase("決済時に二重に課金される", "high"),
    EvalCase("一覧画面の表示に 10 秒かかる", "medium"),
    EvalCase("CSV 出力で日付の形式が仕様と異なる", "medium"),
    EvalCase("ヘルプのリンクが切れている", "low"),
    EvalCase("ボタンの文言に誤字がある", "low"),
]

PROMPT_A = """不具合報告の重大度を high / medium / low のいずれかで答えよ。
- high: 消失
- low: 誤字
"""

PROMPT_B = """不具合報告の重大度を high / medium / low のいずれかで答えよ。
- high: 消失, ログイン, 課金
- medium: 秒, 形式
- low: 誤字, リンク
"""


def classifier_rule(system: str, messages: Sequence[Message]) -> Response:
    """システムプロンプトの「- 重大度: キーワード」の行を判定基準として使う。"""
    report = messages[-1].content
    for label, keywords in re.findall(r"^- (high|medium|low): (.+)$", system, flags=re.MULTILINE):
        if any(k.strip() in report for k in keywords.split(",")):
            return Response(label)
    return Response("medium")  # 判断できないときの既定値


def exact_match(output: str, expected: str) -> bool:
    return output.strip().lower() == expected


def evaluate(llm: LLMClient, system: str, cases: Sequence[EvalCase],
             grader: Callable[[str, str], bool]) -> tuple[float, list[str]]:
    """正解率と、失敗したケースの説明を返す。"""
    failures = []
    for case in cases:
        output = llm.complete(system, [Message("user", case.input)]).text
        if not grader(output, case.expected):
            failures.append(f"{case.input!r}: 期待 {case.expected}, 出力 {output}")
    return 1 - len(failures) / len(cases), failures


def pass_at_k(n: int, c: int, k: int) -> float:
    """n 回の試行のうち c 回成功したとき、k 回試して 1 回以上成功する確率の不偏推定量。"""
    if n - c < k:
        return 1.0
    return 1 - comb(n - c, k) / comb(n, k)


def main() -> None:
    llm = RuleBasedLLM(classifier_rule)
    for name, prompt in [("プロンプト A", PROMPT_A), ("プロンプト B", PROMPT_B)]:
        accuracy, failures = evaluate(llm, prompt, CASES, exact_match)
        print(f"{name}: 正解率 {accuracy:.0%}")
        for f in failures:
            print(f"    失敗 {f}")
    print(f"pass@1 = {pass_at_k(10, 3, 1):.2f}, pass@5 = {pass_at_k(10, 3, 5):.2f}（10 回中 3 回成功）")


if __name__ == "__main__":
    main()
