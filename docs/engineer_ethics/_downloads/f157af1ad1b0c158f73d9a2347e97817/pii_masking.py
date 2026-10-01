"""ログに出力する文字列から個人情報をマスキングするサンプルです。

ログは障害調査のために多くの人が閲覧し、長期間保存されます。
メールアドレスや電話番号をそのまま記録すると、ログ経由で個人情報が
漏えいするおそれがあります。このサンプルでは、logging モジュールの
フィルターを使い、ログに書き込む前に個人情報を伏せ字にします。

実行方法::

    python pii_masking.py
"""

import logging
import re

# メールアドレス（例: taro.yamada@example.com）
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")

# ハイフン区切りの国内電話番号（例: 090-1234-5678, 03-1234-5678）
PHONE_PATTERN = re.compile(r"\b0\d{1,4}-\d{1,4}-\d{3,4}\b")


def mask_email(match: re.Match[str]) -> str:
    """メールアドレスのローカル部を先頭 1 文字だけ残して伏せます。"""
    local, domain = match.group(0).split("@", 1)
    return f"{local[0]}***@{domain}"


def mask_phone(match: re.Match[str]) -> str:
    """電話番号の末尾 4 桁だけを残し、それ以外の数字を伏せます。"""
    phone = match.group(0)
    head, tail = phone[:-4], phone[-4:]
    return re.sub(r"\d", "*", head) + tail


def mask_pii(text: str) -> str:
    """文字列に含まれるメールアドレスと電話番号をマスキングします。"""
    text = EMAIL_PATTERN.sub(mask_email, text)
    return PHONE_PATTERN.sub(mask_phone, text)


class PiiMaskingFilter(logging.Filter):
    """ログレコードのメッセージから個人情報を取り除くフィルターです。"""

    def filter(self, record: logging.LogRecord) -> bool:
        # 引数を埋め込んだ後のメッセージをマスキングし、引数は破棄します。
        record.msg = mask_pii(record.getMessage())
        record.args = None
        return True


def create_logger() -> logging.Logger:
    """マスキング用フィルターを組み込んだロガーを作成します。"""
    logger = logging.getLogger("pii_masking_demo")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    handler.addFilter(PiiMaskingFilter())
    logger.addHandler(handler)
    return logger


def main() -> None:
    """マスキングの前後でログの内容を比較します。"""
    message = "問い合わせ受付: %s / %s"
    email = "taro.yamada@example.com"
    phone = "090-1234-5678"

    print("マスキングなし:", message % (email, phone))

    logger = create_logger()
    logger.info(message, email, phone)


if __name__ == "__main__":
    main()
