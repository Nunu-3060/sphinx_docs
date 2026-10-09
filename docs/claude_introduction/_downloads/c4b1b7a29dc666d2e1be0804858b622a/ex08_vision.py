"""画像を入力して内容を説明してもらうサンプル.

画像ファイルを Base64 で符号化し、テキストと一緒に送信します。
対応形式は JPEG、PNG、GIF、WebP です。

実行例:
    python ex08_vision.py screenshot.png
"""

import base64
import os
import sys
from pathlib import Path
from typing import Literal

import anthropic

MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")

MediaType = Literal["image/jpeg", "image/png", "image/gif", "image/webp"]

MEDIA_TYPES: dict[str, MediaType] = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def describe_image(client: anthropic.Anthropic, path: Path) -> str:
    """画像の内容を説明する文章を返す."""
    media_type = MEDIA_TYPES.get(path.suffix.lower())
    if media_type is None:
        raise ValueError(f"対応していない形式です: {path.suffix}")

    data = base64.standard_b64encode(path.read_bytes()).decode("ascii")

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    # 画像はテキストより前に置くと精度が上がりやすい
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "この画像に何が写っているか説明してください。",
                    },
                ],
            },
        ],
    )
    return "".join(b.text for b in response.content if b.type == "text")


def main() -> None:
    if len(sys.argv) != 2:
        print("使い方: python ex08_vision.py <画像ファイル>")
        sys.exit(1)

    client = anthropic.Anthropic()
    print(describe_image(client, Path(sys.argv[1])))


if __name__ == "__main__":
    main()
