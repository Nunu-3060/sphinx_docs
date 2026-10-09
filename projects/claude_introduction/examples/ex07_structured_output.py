"""構造化出力で、自由記述の文章から決まった形式のデータを取り出すサンプル.

Pydantic のモデルを output_format に渡すと、応答がそのスキーマに従うことが
保証され、検証済みのオブジェクトとして受け取れます。

実行例:
    python ex07_structured_output.py
"""

import os
from typing import Literal

import anthropic
from pydantic import BaseModel

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")

INQUIRY = """\
お世話になっております。株式会社サンプルの山田です。
先週導入した会計システムで、月次レポートの PDF 出力が 3 回に 1 回ほど
失敗します。締め日が 10 月 31 日なので、それまでに解決したいです。
連絡先は yamada@example.com です。
"""


class Ticket(BaseModel):
    """問い合わせから抽出するチケット情報."""

    customer_name: str
    company: str
    email: str
    summary: str
    priority: Literal["high", "medium", "low"]
    deadline: str | None


def main() -> None:
    client = anthropic.Anthropic()

    response = client.messages.parse(
        model=MODEL,
        max_tokens=4096,
        system=(
            "問い合わせ文からチケット情報を抽出してください。"
            "priority は high / medium / low のいずれかで判定してください。"
        ),
        messages=[{"role": "user", "content": INQUIRY}],
        output_format=Ticket,
    )

    ticket = response.parsed_output
    if ticket is None:
        print(f"抽出に失敗しました (stop_reason={response.stop_reason})")
        return

    # 検証済みの Ticket オブジェクトとして扱える
    print(ticket.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
