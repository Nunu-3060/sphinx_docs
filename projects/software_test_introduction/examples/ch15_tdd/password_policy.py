"""パスワードの規則を検査する（TDD で作った最終版）."""

from collections.abc import Callable

MIN_LENGTH = 8
"""パスワードの最小の長さ."""

# (規則を満たすかを判定する関数, 満たさないときのメッセージ)
_RULES: list[tuple[Callable[[str], bool], str]] = [
    (lambda pw: len(pw) >= MIN_LENGTH, f"{MIN_LENGTH} 文字以上にしてください"),
    (lambda pw: any(c.isdigit() for c in pw), "数字を含めてください"),
    (lambda pw: any(c.isupper() for c in pw), "英大文字を含めてください"),
    (lambda pw: any(c.islower() for c in pw), "英小文字を含めてください"),
]


def validate_password(password: str) -> list[str]:
    """規則に違反している項目のメッセージを返す（違反がなければ空のリスト）."""
    return [message for rule, message in _RULES if not rule(password)]
