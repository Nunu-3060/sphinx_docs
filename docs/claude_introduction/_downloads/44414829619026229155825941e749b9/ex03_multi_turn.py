"""会話履歴を保持して複数ターンの対話を行うサンプル.

Messages API はステートレスです。過去のやり取りを覚えてもらうには、
毎回の呼び出しで会話履歴全体を messages に渡します。

実行例:
    python ex03_multi_turn.py
    (空行を入力すると終了します)
"""

import os

import anthropic
from anthropic.types import MessageParam

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")


class Conversation:
    """会話履歴を保持し、Claude との対話を管理するクラス."""

    def __init__(self, client: anthropic.Anthropic, system: str) -> None:
        self._client = client
        self._system = system
        self._history: list[MessageParam] = []

    def send(self, user_text: str) -> str:
        """利用者の発言を送信し、Claude の応答テキストを返す."""
        self._history.append({"role": "user", "content": user_text})

        response = self._client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=self._system,
            messages=self._history,
        )

        # 応答のコンテンツブロックをそのまま履歴に追加する。
        # テキストだけを取り出して追加すると、思考ブロックなどが失われる。
        self._history.append(
            {"role": "assistant", "content": response.content}
        )

        return "".join(b.text for b in response.content if b.type == "text")


def main() -> None:
    conversation = Conversation(
        anthropic.Anthropic(),
        system="あなたは簡潔に答えるアシスタントです。",
    )

    while True:
        user_text = input("あなた> ").strip()
        if not user_text:
            break
        print(f"Claude> {conversation.send(user_text)}\n")


if __name__ == "__main__":
    main()
