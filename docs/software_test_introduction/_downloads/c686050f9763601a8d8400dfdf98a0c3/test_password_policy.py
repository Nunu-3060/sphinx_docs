"""TDD の過程で書いたテスト（最終版）."""

from password_policy import validate_password


def test_valid_password_has_no_error() -> None:
    assert validate_password("Secret123") == []


def test_too_short() -> None:
    assert validate_password("Sec123") == ["8 文字以上にしてください"]


def test_exactly_min_length_is_valid() -> None:
    assert validate_password("Secret12") == []


def test_without_digit() -> None:
    assert validate_password("SecretPass") == ["数字を含めてください"]


def test_without_uppercase() -> None:
    assert validate_password("secret123") == ["英大文字を含めてください"]


def test_without_lowercase() -> None:
    assert validate_password("SECRET123") == ["英小文字を含めてください"]


def test_multiple_errors() -> None:
    assert validate_password("abc") == [
        "8 文字以上にしてください",
        "数字を含めてください",
        "英大文字を含めてください",
    ]
