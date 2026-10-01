"""pytest の組み込み fixture を使う."""

import os
from pathlib import Path

import pytest


def save_greeting(path: Path, name: str) -> None:
    """あいさつ文をファイルに書き込む."""
    path.write_text(f"こんにちは、{name}さん\n", encoding="utf-8")


def print_total(prices: list[int]) -> None:
    """合計金額を表示する."""
    print(f"合計: {sum(prices)} 円")


def get_shop_name() -> str:
    """環境変数 SHOP_NAME の値を返す（未設定なら既定の名前を返す）."""
    return os.environ.get("SHOP_NAME", "テスト商店")


def test_tmp_path(tmp_path: Path) -> None:
    # tmp_path はテストごとに作られる一時フォルダー
    path = tmp_path / "greeting.txt"
    save_greeting(path, "佐藤")
    assert path.read_text(encoding="utf-8") == "こんにちは、佐藤さん\n"


def test_capsys(capsys: pytest.CaptureFixture[str]) -> None:
    print_total([100, 250])
    captured = capsys.readouterr()
    assert captured.out == "合計: 350 円\n"


def test_monkeypatch_setenv(monkeypatch: pytest.MonkeyPatch) -> None:
    # テストが終わると、環境変数は元に戻る
    monkeypatch.setenv("SHOP_NAME", "サンプル堂")
    assert get_shop_name() == "サンプル堂"


def test_monkeypatch_delenv(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SHOP_NAME", raising=False)
    assert get_shop_name() == "テスト商店"
