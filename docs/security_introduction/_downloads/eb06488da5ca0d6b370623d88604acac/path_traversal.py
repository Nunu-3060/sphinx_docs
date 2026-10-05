"""パストラバーサルとその対策のサンプル.

利用者が指定したファイル名をそのままパスに連結すると、「../」を使って
公開用ディレクトリの外にあるファイルを読まれてしまいます。

実行方法:
    python path_traversal.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import tempfile
from pathlib import Path


def resolve_unsafe(base_dir: Path, filename: str) -> Path:
    """ファイル名をそのまま連結する（悪い例）."""
    return base_dir / filename


def resolve_safe(base_dir: Path, filename: str) -> Path:
    """正規化した結果が base_dir の配下にあることを確認する（良い例）."""
    base = base_dir.resolve()
    target = (base / filename).resolve()
    if not target.is_relative_to(base):
        raise PermissionError(f"公開ディレクトリの外は参照できません: {filename}")
    return target


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        public = root / "public"
        public.mkdir()
        (public / "hello.txt").write_text("公開ファイル", encoding="utf-8")
        (root / "secret.txt").write_text("秘密の情報", encoding="utf-8")

        attack = "../secret.txt"

        print("[悪い例]")
        path = resolve_unsafe(public, attack)
        print(f"  {attack} -> {path.read_text(encoding='utf-8')}")

        print("[良い例]")
        path = resolve_safe(public, "hello.txt")
        print(f"  hello.txt -> {path.read_text(encoding='utf-8')}")
        try:
            resolve_safe(public, attack)
        except PermissionError as error:
            print(f"  {attack} -> 拒否（{error}）")


if __name__ == "__main__":
    main()
