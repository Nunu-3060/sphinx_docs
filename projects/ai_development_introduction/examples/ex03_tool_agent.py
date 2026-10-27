"""ツールを使う最小のエージェントの例。

モデルの応答にツール呼び出しが含まれていればツールを実行し、結果を会話履歴に
追加して再びモデルを呼ぶ。ツール呼び出しがなくなったら、その応答を最終回答とする。
ツールの失敗は例外にせず、モデルが読んで次の行動を選べる文章として返す。
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from llm_stub import LLMClient, Message, Response, RuleBasedLLM, ToolCall


@dataclass(frozen=True)
class Tool:
    """モデルに提供するツール。parameters は引数名と説明の対応。"""

    name: str
    description: str
    parameters: dict[str, str]
    func: Callable[[dict[str, str]], str]


class ToolRegistry:
    """ツールの登録・説明文の生成・実行を受け持つ。"""

    def __init__(self, tools: Sequence[Tool]) -> None:
        self._tools = {t.name: t for t in tools}

    def describe(self) -> str:
        """システムプロンプトに含めるツールの説明を返す。"""
        lines = ["# 使えるツール"]
        for t in self._tools.values():
            params = ", ".join(f"{k}: {v}" for k, v in t.parameters.items())
            lines.append(f"- {t.name}({params}): {t.description}")
        return "\n".join(lines)

    def execute(self, call: ToolCall) -> str:
        tool = self._tools.get(call.name)
        if tool is None:
            return f"エラー: ツール {call.name} は存在しない。使えるツール: {', '.join(self._tools)}"
        missing = [p for p in tool.parameters if p not in call.arguments]
        if missing:
            return f"エラー: 引数 {', '.join(missing)} が不足している"
        return tool.func(call.arguments)


def run_agent(llm: LLMClient, system: str, task: str, registry: ToolRegistry, max_turns: int = 8) -> str:
    """エージェントループ。max_turns 回モデルを呼んでも終わらなければ打ち切る。"""
    messages: list[Message] = [Message("user", task)]
    full_system = f"{system}\n\n{registry.describe()}"
    for turn in range(1, max_turns + 1):
        response = llm.complete(full_system, messages)
        messages.append(Message("assistant", response.text, response.tool_calls))
        if not response.tool_calls:
            return response.text
        for call in response.tool_calls:
            result = registry.execute(call)
            print(f"[{turn}] {call.name}({call.arguments}) -> {result[:60]}")
            messages.append(Message("tool", result, tool_call_id=call.call_id))
    return f"{max_turns} 回で完了しなかったため打ち切った"


# ---- ツールの実装（ファイルシステムの代わりに辞書を使う） ----

FILES = {
    "README.md": "サンプルアプリ。設定は config/ 配下にある。",
    "config/app.toml": "[server]\nport = 8080\ntimeout = 30\n",
    "src/main.py": "print('hello')\n",
}


def list_files(args: dict[str, str]) -> str:
    prefix = args["prefix"]
    names = [n for n in FILES if n.startswith(prefix)]
    return "\n".join(names) if names else f"{prefix} で始まるファイルはない"


def read_file(args: dict[str, str]) -> str:
    path = args["path"]
    if path not in FILES:
        return f"エラー: {path} は存在しない。list_files でファイル名を確認すること"
    return FILES[path]


# ---- モデルの代わり：直前のツール結果を読んで次の行動を決める ----

def agent_rule(system: str, messages: Sequence[Message]) -> Response:
    last = messages[-1]
    if last.role == "user":
        # 推測したパスを読みに行く（ここでは誤ったパスを推測する）
        return Response("設定ファイルを読む", (ToolCall("c1", "read_file", {"path": "config.toml"}),))
    if last.content.startswith("エラー"):
        return Response("ファイル一覧を確認する", (ToolCall("c2", "list_files", {"prefix": "config/"}),))
    if last.content.startswith("config/"):
        path = last.content.splitlines()[0]
        return Response("見つかったファイルを読む", (ToolCall("c3", "read_file", {"path": path}),))
    match = re.search(r"timeout = (\d+)", last.content)
    if match:
        return Response(f"timeout の設定値は {match.group(1)} 秒である（config/app.toml）。")
    return Response("timeout の設定は見つからなかった。")


def main() -> None:
    registry = ToolRegistry([
        Tool("list_files", "指定した接頭辞で始まるファイルの一覧を返す", {"prefix": "パスの接頭辞"}, list_files),
        Tool("read_file", "ファイルの内容を返す", {"path": "ファイルのパス"}, read_file),
    ])
    answer = run_agent(
        RuleBasedLLM(agent_rule),
        system="あなたはリポジトリを調査するエージェントである。",
        task="サーバーの timeout の設定値を調べて",
        registry=registry,
    )
    print(f"最終回答: {answer}")


if __name__ == "__main__":
    main()
