"""ツール利用のループを自分で書くサンプル.

Claude が「どのツールをどの引数で呼ぶか」を決め、プログラム側が実際に
ツールを実行して結果を返します。stop_reason が tool_use の間はこれを
繰り返し、end_turn になったら終了します。

実行例:
    python ex11_tool_use_manual.py
"""

import json
import os
from typing import Any

import anthropic
from anthropic.types import MessageParam, ToolParam, ToolResultBlockParam

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")
MAX_TURNS = 10  # 無限ループを防ぐための上限

# 在庫データの代わりに使う辞書 (実際にはデータベースなどを参照する)
STOCK = {"A-100": 12, "B-200": 0, "C-300": 5}
PRICE = {"A-100": 1500, "B-200": 3200, "C-300": 800}

TOOLS: list[ToolParam] = [
    {
        "name": "get_stock",
        "description": "商品コードを指定して在庫数を取得する。",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "item_code": {
                    "type": "string",
                    "description": "商品コード。例: A-100",
                },
            },
            "required": ["item_code"],
            "additionalProperties": False,
        },
    },
    {
        "name": "get_price",
        "description": "商品コードを指定して税抜単価 (円) を取得する。",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {
                "item_code": {"type": "string"},
            },
            "required": ["item_code"],
            "additionalProperties": False,
        },
    },
]


def run_tool(name: str, tool_input: dict[str, Any]) -> tuple[str, bool]:
    """ツールを実行し、(結果の文字列, エラーかどうか) を返す."""
    code = str(tool_input.get("item_code", ""))
    table = {"get_stock": STOCK, "get_price": PRICE}.get(name)
    if table is None:
        return f"不明なツールです: {name}", True
    if code not in table:
        return f"商品コード {code} は存在しません。", True
    return json.dumps({"item_code": code, "value": table[code]}), False


def main() -> None:
    client = anthropic.Anthropic()
    messages: list[MessageParam] = [
        {
            "role": "user",
            "content": "A-100 と B-200 の在庫と単価を調べて、"
            "在庫がある商品の在庫金額の合計を教えてください。",
        },
    ]

    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
        )
        # Claude の応答 (tool_use ブロックを含む) を履歴に追加する
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            break

        # 要求されたツールをすべて実行し、結果を 1 つの user メッセージで返す
        results: list[ToolResultBlockParam] = []
        for block in response.content:
            if block.type == "tool_use":
                content, is_error = run_tool(block.name, block.input)
                print(f"[tool] {block.name}({block.input}) -> {content}")
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": content,
                        "is_error": is_error,
                    }
                )
        messages.append({"role": "user", "content": results})
    else:
        # break せずにループが終わった = 上限までツール呼び出しが続いた
        print(f"[警告] {MAX_TURNS} ターン以内に作業が終わりませんでした。")
        return

    if response.stop_reason != "end_turn":
        print(f"[警告] 応答が完了していません (stop_reason={response.stop_reason})")
    print("".join(b.text for b in response.content if b.type == "text"))


if __name__ == "__main__":
    main()
