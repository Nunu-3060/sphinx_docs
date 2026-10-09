"""最小構成の MCP サーバーのサンプル (MCP Python SDK 2.x).

メモの一覧取得と追加を行うツールを公開します。標準入出力 (stdio) で
通信するため、Claude Code や Claude のデスクトップアプリから子プロセスとして
起動して使います。

Claude Code への登録例:
    claude mcp add memo -- python /path/to/ex13_mcp_server.py
"""

from mcp.server.mcpserver import MCPServer

server = MCPServer("memo")

# プロセスが動いている間だけ保持する簡易的なメモ帳
_memos: list[str] = []


@server.tool()
def add_memo(text: str) -> str:
    """メモを 1 件追加する.

    Args:
        text: メモの本文。
    """
    _memos.append(text)
    return f"メモを追加しました (全 {len(_memos)} 件)。"


@server.tool()
def list_memos() -> list[str]:
    """保存されているメモを古い順にすべて返す."""
    return list(_memos)


@server.resource("memo://count")
def memo_count() -> str:
    """保存されているメモの件数."""
    return str(len(_memos))


if __name__ == "__main__":
    server.run(transport="stdio")
