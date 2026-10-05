"""ログに機密情報を出力しないためのサンプル.

logging のフィルターで、パスワードやトークンなどをログに書き込む前に
伏せ字に置き換えます。シークレットはソースコードに書かず、
環境変数などから読み込みます。

実行方法:
    python log_masking.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import logging
import os
import re

# 伏せ字にする項目のパターン（キー名=値、キー名: 値 の形式）
SENSITIVE = re.compile(
    r"(?P<key>password|passwd|token|api_key|secret)"
    r"(?P<sep>\s*[=:]\s*)(?P<value>[^\s,&]+)",
    re.IGNORECASE,
)
CARD_NUMBER = re.compile(r"\b(?:\d[ -]?){12}(?P<last>\d{4})\b")


class MaskingFilter(logging.Filter):
    """ログメッセージに含まれる機密情報を伏せ字にするフィルター."""

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        message = SENSITIVE.sub(r"\g<key>\g<sep>****", message)
        message = CARD_NUMBER.sub(r"****-****-****-\g<last>", message)
        record.msg = message
        record.args = None
        return True


def load_api_key() -> str:
    """API キーを環境変数から読み込む（ソースコードに書かない）."""
    api_key = os.environ.get("DEMO_API_KEY")
    if api_key is None:
        # 説明用の値。実際のアプリケーションではエラーとして扱う
        api_key = "sk-demo-1234567890"
    return api_key


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logger = logging.getLogger("demo")
    logger.addFilter(MaskingFilter())

    api_key = load_api_key()
    logger.info("login request: user=alice password=P@ssw0rd")
    logger.info("calling API with api_key=%s", api_key)
    logger.info("payment: card=4111 1111 1111 1111 amount=1200")


if __name__ == "__main__":
    main()
