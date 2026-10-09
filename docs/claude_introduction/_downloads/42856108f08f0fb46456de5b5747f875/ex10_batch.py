"""Message Batches API で大量のリクエストを非同期にまとめて処理するサンプル.

バッチ処理は即時性が不要な処理向けで、通常の半額で利用できます。
結果の順序は送信順と一致しないため、custom_id で対応付けます。

実行例:
    python ex10_batch.py
"""

import os
import time

import anthropic
from anthropic.types.message_create_params import (
    MessageCreateParamsNonStreaming,
)
from anthropic.types.messages.batch_create_params import Request

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")

REVIEWS = {
    "review-1": "配送が早く、梱包も丁寧でした。",
    "review-2": "説明書が分かりにくく、設定に 2 時間かかりました。",
    "review-3": "値段相応だと思います。",
}

POLL_INTERVAL_SEC = 30


def build_requests() -> list[Request]:
    """レビューごとに感情分類のリクエストを作る."""
    return [
        Request(
            custom_id=review_id,
            params=MessageCreateParamsNonStreaming(
                model=MODEL,
                max_tokens=1024,
                system="レビューの感情を positive / negative / neutral の"
                "いずれか 1 語で答えてください。",
                messages=[{"role": "user", "content": text}],
            ),
        )
        for review_id, text in REVIEWS.items()
    ]


def main() -> None:
    client = anthropic.Anthropic()

    batch = client.messages.batches.create(requests=build_requests())
    print(f"バッチを作成しました: {batch.id}")

    # 処理が終わるまで定期的に状態を確認する (多くは 1 時間以内、最長 24 時間)
    while batch.processing_status != "ended":
        time.sleep(POLL_INTERVAL_SEC)
        batch = client.messages.batches.retrieve(batch.id)
        print(f"  状態: {batch.processing_status}")

    for result in client.messages.batches.results(batch.id):
        if result.result.type == "succeeded":
            message = result.result.message
            text = "".join(
                b.text for b in message.content if b.type == "text"
            )
            print(f"{result.custom_id}: {text.strip()}")
        else:
            print(f"{result.custom_id}: 失敗 ({result.result.type})")


if __name__ == "__main__":
    main()
