"""テストの結果をモデルに返して修正させる、自己修正ループの例。

ループは次のいずれかで終了する。

* すべてのテストが成功した（成功）
* 前回と同じテストが同じ理由で失敗した（行き詰まり）
* 最大反復回数に達した（打ち切り）

注意: 生成されたコードを exec で実行している。実際のシステムでは、
コンテナなどの隔離された環境で実行すること。
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from llm_stub import LLMClient, Message, Response, RuleBasedLLM

Outcome = Literal["success", "stalled", "max_iterations"]

TEST_CASES: list[tuple[int, bool]] = [(2024, True), (2023, False), (1900, False), (2000, True)]


@dataclass(frozen=True)
class LoopResult:
    outcome: Outcome
    iterations: int
    code: str


def run_tests(code: str) -> list[str]:
    """コードを実行し、失敗したテストの説明の一覧を返す。空なら全件成功。"""
    namespace: dict[str, object] = {}
    try:
        exec(code, namespace)
    except Exception as e:  # 生成コードはどんな例外でも起こしうる
        return [f"コードを実行できない: {e!r}"]
    func = namespace.get("is_leap_year")
    if not callable(func):
        return ["関数 is_leap_year が定義されていない"]
    failures = []
    for year, expected in TEST_CASES:
        actual = func(year)
        if actual != expected:
            failures.append(f"is_leap_year({year}) は {expected} であるべきだが {actual} を返した")
    return failures


def fix_loop(llm: LLMClient, task: str, max_iterations: int = 5) -> LoopResult:
    messages: list[Message] = [Message("user", task)]
    previous_failures: list[str] | None = None
    code = ""
    for i in range(1, max_iterations + 1):
        code = llm.complete("Python のコードだけを出力せよ。", messages).text
        messages.append(Message("assistant", code))
        failures = run_tests(code)
        print(f"--- 反復 {i}: 失敗 {len(failures)} 件")
        for f in failures:
            print(f"    {f}")
        if not failures:
            return LoopResult("success", i, code)
        if failures == previous_failures:
            return LoopResult("stalled", i, code)
        previous_failures = failures
        feedback = "テストが失敗した。原因を考えて修正したコード全体を出力せよ。\n" + "\n".join(failures)
        messages.append(Message("user", feedback))
    return LoopResult("max_iterations", max_iterations, code)


# ---- モデルの代わり：フィードバックの内容に応じて、段階的に正しいコードへ近づく ----

ATTEMPTS = [
    "def is_leap_year(year):\n    return year % 4 == 0\n",
    "def is_leap_year(year):\n    return year % 4 == 0 and year % 100 != 0\n",
    "def is_leap_year(year):\n    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)\n",
]


def fixer_rule(system: str, messages: Sequence[Message]) -> Response:
    feedback_count = sum(1 for m in messages if m.role == "user") - 1
    return Response(ATTEMPTS[min(feedback_count, len(ATTEMPTS) - 1)])


def main() -> None:
    result = fix_loop(RuleBasedLLM(fixer_rule), "西暦 year がうるう年かを返す関数 is_leap_year を書け。")
    print(f"結果: {result.outcome}（{result.iterations} 回）")
    print(result.code)


if __name__ == "__main__":
    main()
