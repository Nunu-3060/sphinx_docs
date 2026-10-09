"""送信前にトークン数を数え、料金を概算するサンプル.

count_tokens エンドポイントは料金がかからず、メッセージを生成しません。
ここでは入力トークン数と、出力トークン数の想定値から料金を概算します。

実行例:
    python ex06_count_tokens.py
"""

import os

import anthropic

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")

# 100 万トークンあたりの料金 (米ドル)。2026 年 10 月時点の公表値。
# 最新の料金は公式の料金ページで確認すること。
PRICES_PER_MTOK: dict[str, tuple[float, float]] = {
    "claude-fable-5-1": (10.00, 50.00),
    "claude-opus-5-5": (4.00, 20.00),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-haiku-4-5": (1.00, 5.00),
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """入出力トークン数から料金 (米ドル) を計算する."""
    input_price, output_price = PRICES_PER_MTOK[model]
    return (
        input_tokens * input_price + output_tokens * output_price
    ) / 1_000_000


def main() -> None:
    client = anthropic.Anthropic()

    system = "あなたは技術文書の翻訳者です。"
    document = "Claude is a family of large language models. " * 200

    count = client.messages.count_tokens(
        model=MODEL,
        system=system,
        messages=[
            {"role": "user", "content": f"次の文章を和訳してください。\n\n{document}"},
        ],
    )

    expected_output_tokens = 3000  # 想定する出力トークン数
    cost = estimate_cost(MODEL, count.input_tokens, expected_output_tokens)

    print(f"モデル              : {MODEL}")
    print(f"入力トークン数      : {count.input_tokens:,}")
    print(f"想定出力トークン数  : {expected_output_tokens:,}")
    print(f"概算料金            : ${cost:.4f}")


if __name__ == "__main__":
    main()
