"""Claude Agent SDK でコードベースを調査するエージェントを動かすサンプル.

Claude Agent SDK は、Claude Code のエージェント機能をライブラリとして
使えるようにしたものです。ファイルの読み取りや検索などの組み込みツールと、
エージェントのループがあらかじめ用意されています。

事前に次のパッケージをインストールしてください。
    pip install claude-agent-sdk

実行例:
    python ex15_agent_sdk.py /path/to/repository
"""

import asyncio
import sys

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    query,
)

PROMPT = """\
このリポジトリの構成を調査し、次の 3 点を日本語で簡潔に報告してください。
1. 主な機能
2. ディレクトリ構成と各ディレクトリの役割
3. テストの実行方法
"""


async def investigate(repository: str) -> None:
    """リポジトリを読み取り専用で調査し、経過と結果を表示する."""
    options = ClaudeAgentOptions(
        cwd=repository,
        # 読み取り系のツールだけを許可し、ファイルの変更やコマンド実行はさせない
        allowed_tools=["Read", "Grep", "Glob"],
        permission_mode="dontAsk",
        max_turns=30,
        max_budget_usd=1.0,
    )

    async for message in query(prompt=PROMPT, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, ToolUseBlock):
                    print(f"[tool] {block.name} {block.input}")
                elif isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            cost = message.total_cost_usd or 0.0
            print(f"\n--- ターン数: {message.num_turns}, 料金: ${cost:.4f}")


def main() -> None:
    if len(sys.argv) != 2:
        print("使い方: python ex15_agent_sdk.py <リポジトリのパス>")
        sys.exit(1)
    asyncio.run(investigate(sys.argv[1]))


if __name__ == "__main__":
    main()
