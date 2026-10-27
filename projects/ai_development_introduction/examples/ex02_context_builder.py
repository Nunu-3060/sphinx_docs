"""トークン予算の範囲内でコンテキストを組み立てる例。

1. 検索（キーワードの一致数による簡易的な RAG）で関連文書を選ぶ。
2. 古い会話履歴を要約して圧縮する（コンパクション）。
3. 優先度の高い順に、予算に収まるだけコンテキストに入れる。
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal

from llm_stub import estimate_tokens

Kind = Literal["instruction", "memory", "retrieved", "history"]


@dataclass(frozen=True)
class ContextItem:
    """コンテキストに入れる候補の情報。priority は小さいほど優先する。"""

    kind: Kind
    text: str
    priority: int

    @property
    def tokens(self) -> int:
        return estimate_tokens(self.text)


def tokenize(text: str) -> set[str]:
    """英数字の単語と、2 文字以上の漢字・カタカナの並びを検索語として取り出す。"""
    return set(re.findall(r"[A-Za-z0-9_]+|[一-鿿゠-ヿ]{2,}", text.lower()))


def retrieve(query: str, documents: dict[str, str], top_k: int) -> list[tuple[str, str]]:
    """クエリと共通する語が多い順に、文書を top_k 件返す。共通する語がない文書は返さない。"""
    query_terms = tokenize(query)
    scored = []
    for name, body in documents.items():
        score = len(query_terms & tokenize(body))
        if score > 0:
            scored.append((score, name, body))
    scored.sort(key=lambda t: t[0], reverse=True)
    return [(name, body) for _, name, body in scored[:top_k]]


def compact_history(history: Sequence[str], keep_last: int,
                    summarize: Callable[[Sequence[str]], str]) -> tuple[str | None, list[str]]:
    """直近 keep_last 件を残し、それより古い履歴を 1 件の要約に置き換える。

    要約（古い履歴がなければ None）と、直近の履歴を返す。
    """
    if len(history) <= keep_last:
        return None, list(history)
    old, recent = history[:-keep_last], history[-keep_last:]
    return summarize(old), list(recent)


def naive_summarize(lines: Sequence[str]) -> str:
    """要約の代わりに各行の先頭だけを残す。実際には LLM に要約させる。"""
    heads = " / ".join(line[:16] for line in lines)
    return f"（これまでの {len(lines)} 件の要約）{heads}"


def build_context(items: Sequence[ContextItem], budget: int) -> tuple[list[ContextItem], list[ContextItem]]:
    """優先度の高い順に、予算に収まる項目を選ぶ。選ばれた項目と、外れた項目を返す。"""
    selected: list[ContextItem] = []
    dropped: list[ContextItem] = []
    used = 0
    for item in sorted(items, key=lambda i: i.priority):
        if used + item.tokens <= budget:
            selected.append(item)
            used += item.tokens
        else:
            dropped.append(item)
    return selected, dropped


def main() -> None:
    documents = {
        "docs/deploy.md": "デプロイ手順: main ブランチにマージすると CI が staging に自動デプロイする。",
        "docs/testing.md": "テスト: pytest を使う。DB を使うテストは docker compose で PostgreSQL を起動してから実行する。",
        "docs/style.md": "コーディング規約: 型ヒント必須。flake8 と mypy を通すこと。",
        "docs/history.md": "2019 年の移行作業の記録。旧システムは Perl で書かれていた。",
    }
    query = "DB を使うテストを pytest で実行したい"
    history = [
        "利用者: ログイン画面の不具合を調べて",
        "AI: auth.py の 42 行目でセッションの期限切れを判定していないのが原因だった",
        "利用者: 修正して",
        "AI: auth.py を修正し、既存テストがすべて成功することを確認した",
        "利用者: 次は注文 API のテストを追加したい",
    ]

    items: list[ContextItem] = [
        ContextItem("instruction", "あなたはこのリポジトリの開発を支援するエージェントである。", 0),
        ContextItem("memory", "プロジェクト規約: 型ヒント必須。テストは tests/ に置く。", 1),
    ]
    summary, recent = compact_history(history, keep_last=2, summarize=naive_summarize)
    for line in recent:
        items.append(ContextItem("history", line, 2))
    for name, body in retrieve(query, documents, top_k=2):
        items.append(ContextItem("retrieved", f"[{name}] {body}", 3))
    if summary is not None:
        items.append(ContextItem("history", summary, 4))

    selected, dropped = build_context(items, budget=160)

    print(f"{'種類':<10}{'トークン':>8}  内容")
    for item in selected:
        print(f"{item.kind:<12}{item.tokens:>8}  {item.text[:40]}")
    print(f"合計 {sum(i.tokens for i in selected)} トークン（予算 160）")
    for item in dropped:
        print(f"予算超過で除外: {item.kind} {item.text[:40]}")


if __name__ == "__main__":
    main()
