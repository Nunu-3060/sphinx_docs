"""オーケストレーター・ワーカー型のマルチエージェントの例。

オーケストレーターが作業を分割し、ワーカーを並列に動かす。各ワーカーは
独立したコンテキスト（会話履歴）で作業し、短い報告だけを返す。オーケストレーターは
ファイルの中身を読まずに報告だけを統合するため、自身のコンテキストを節約できる。
"""

from __future__ import annotations

from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from llm_stub import Message, Response, RuleBasedLLM, estimate_tokens

SOURCES = {
    "auth.py": "def login(user, password):\n    # TODO: 試行回数の制限\n    return check(user, password)\n",
    "order.py": "def total(items):\n    return sum(i.price * i.qty for i in items)\n",
    "report.py": "def export(rows):\n    # TODO: 文字コードの指定\n    # TODO: 大量データ時の分割\n    pass\n",
    "util.py": "def clamp(x, lo, hi):\n    return max(lo, min(x, hi))\n",
}


@dataclass(frozen=True)
class WorkerReport:
    target: str
    summary: str
    context_tokens: int


def worker_rule(system: str, messages: Sequence[Message]) -> Response:
    """模擬ワーカー：渡されたソースの TODO を数えて報告する。"""
    source = messages[-1].content
    todos = [line.split("TODO:")[1].strip() for line in source.splitlines() if "TODO:" in line]
    if not todos:
        return Response("未完了の作業なし")
    return Response(f"未完了 {len(todos)} 件: " + "、".join(todos))


def run_worker(target: str) -> WorkerReport:
    """1 つのファイルを担当するワーカー。独自のコンテキストを持つ。"""
    llm = RuleBasedLLM(worker_rule)
    system = "あなたはコード調査の担当者である。未完了の作業を短く報告せよ。"
    messages = [Message("user", SOURCES[target])]
    response = llm.complete(system, messages)
    used = estimate_tokens(system) + sum(estimate_tokens(m.content) for m in messages)
    return WorkerReport(target, response.text, used)


def orchestrate(targets: Sequence[str]) -> str:
    with ThreadPoolExecutor(max_workers=4) as pool:
        reports = list(pool.map(run_worker, targets))
    for r in reports:
        print(f"ワーカー {r.target:<10} コンテキスト {r.context_tokens:>3} トークン -> {r.summary}")
    summary = "\n".join(f"- {r.target}: {r.summary}" for r in reports)
    print(f"オーケストレーターが受け取った報告: {estimate_tokens(summary)} トークン")
    return summary


def main() -> None:
    print(orchestrate(sorted(SOURCES)))


if __name__ == "__main__":
    main()
