"""本書のサンプルで共通に使う、LLM を模擬するクライアント。

実際の LLM API を呼ばずに動作を確認できるよう、応答をあらかじめ決めておく
``ScriptedLLM`` と、入力に応じて応答を決める ``RuleBasedLLM`` を用意する。
どちらも ``LLMClient`` プロトコルを満たすため、同じインターフェースを持つ
実 API のクライアントに差し替えられる。
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Literal, Protocol

Role = Literal["user", "assistant", "tool"]


@dataclass(frozen=True)
class ToolCall:
    """モデルが要求したツール呼び出し。"""

    call_id: str
    name: str
    arguments: dict[str, str]


@dataclass(frozen=True)
class Message:
    """会話履歴の 1 件分のメッセージ。"""

    role: Role
    content: str
    tool_calls: tuple[ToolCall, ...] = ()
    tool_call_id: str | None = None


@dataclass(frozen=True)
class Response:
    """モデルの応答。ツール呼び出しを含む場合がある。"""

    text: str
    tool_calls: tuple[ToolCall, ...] = ()


class LLMClient(Protocol):
    """サンプルが前提とする LLM クライアントのインターフェース。"""

    def complete(self, system: str, messages: Sequence[Message]) -> Response:
        """システムプロンプトと会話履歴を受け取り、応答を返す。"""
        ...


class ScriptedLLM:
    """あらかじめ用意した応答を順番に返すクライアント。"""

    def __init__(self, responses: Iterable[Response]) -> None:
        self._responses = list(responses)
        self.call_count = 0

    def complete(self, system: str, messages: Sequence[Message]) -> Response:
        if self.call_count >= len(self._responses):
            raise RuntimeError("用意した応答をすべて使い切った")
        response = self._responses[self.call_count]
        self.call_count += 1
        return response


Rule = Callable[[str, Sequence[Message]], Response]


class RuleBasedLLM:
    """入力（システムプロンプトと会話履歴）から応答を決める関数を使うクライアント。"""

    def __init__(self, rule: Rule) -> None:
        self._rule = rule
        self.call_count = 0

    def complete(self, system: str, messages: Sequence[Message]) -> Response:
        self.call_count += 1
        return self._rule(system, messages)


def estimate_tokens(text: str) -> int:
    """トークン数を概算する。

    実際のトークン数はモデルのトークナイザーによって異なる。ここでは
    ASCII 文字は 4 文字で 1 トークン、それ以外の文字は 1 文字で 1 トークンとみなす。
    """
    ascii_chars = sum(1 for ch in text if ch.isascii())
    other_chars = len(text) - ascii_chars
    return (ascii_chars + 3) // 4 + other_chars
