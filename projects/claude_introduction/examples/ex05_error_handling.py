"""API 呼び出しのエラー処理と stop_reason の確認を行うサンプル.

SDK は 408、409、429、5xx と接続エラーを自動で再試行します (既定 2 回)。
それでも失敗した場合に備え、例外を具体的な型から順に捕捉します。

実行例:
    python ex05_error_handling.py
"""

import os
import sys

import anthropic
from anthropic.types import Message

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")


def create_message(client: anthropic.Anthropic, prompt: str) -> Message | None:
    """メッセージを送信する。失敗した場合は原因を表示して None を返す."""
    try:
        return client.messages.create(
            model=MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.AuthenticationError:
        print("API キーが無効です。ANTHROPIC_API_KEY を確認してください。")
    except anthropic.NotFoundError:
        print(f"モデル '{MODEL}' が見つかりません。モデル ID を確認してください。")
    except anthropic.BadRequestError as e:
        print(f"リクエストの内容に誤りがあります: {e.message}")
    except anthropic.RateLimitError as e:
        retry_after = e.response.headers.get("retry-after", "不明")
        print(f"レート制限に達しました。{retry_after} 秒後に再試行してください。")
    except anthropic.APIStatusError as e:
        print(f"API エラー (HTTP {e.status_code}): {e.message}")
    except anthropic.APIConnectionError:
        print("API に接続できません。ネットワーク設定を確認してください。")
    return None


def print_result(message: Message) -> None:
    """stop_reason に応じて結果を表示する."""
    # 問い合わせ時に役立つリクエスト ID
    print(f"request_id: {message._request_id}")

    if message.stop_reason == "refusal":
        # 安全上の理由で応答が拒否された場合、content を読む前に判定する
        details = message.stop_details
        category = details.category if details else None
        print(f"応答が拒否されました (category={category})")
        return

    text = "".join(b.text for b in message.content if b.type == "text")
    print(text)

    if message.stop_reason == "max_tokens":
        print("[警告] max_tokens に達したため、応答が途中で切れています。")


def main() -> None:
    # 再試行回数とタイムアウト (秒) はクライアント生成時に変更できる
    client = anthropic.Anthropic(max_retries=3, timeout=60.0)

    message = create_message(client, "1 から 10 までの素数を列挙してください。")
    if message is None:
        sys.exit(1)
    print_result(message)


if __name__ == "__main__":
    main()
