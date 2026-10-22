"""rst の表記を機械的に検査する。

* 敬体 (です・ます) が混じっていないか
* 日本語と半角英数字の間に空白があるか
* 日本語どうしの間に不自然な空白がないか
* 表記ゆれの候補がないか

コードブロックやディレクティブの中身、URL は検査しない。

使い方:
    python check_style.py
"""

import re
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent
JA = r"[぀-ヿ一-鿿]"
CHECKS = [
    ("敬体", re.compile(r"(です|ます|でした|ません|ください)[。、）]")),
    ("日本語の直後に英数字", re.compile(rf"{JA}[A-Za-z0-9]")),
    ("英数字の直後に日本語", re.compile(rf"[A-Za-z0-9]{JA}")),
    ("日本語どうしの間の空白", re.compile(rf"{JA} +{JA}")),
    ("全角英数字", re.compile(r"[Ａ-Ｚａ-ｚ０-９]")),
]
VARIANTS = ["フォルダ", "メソッド", "ひとつ", "ふたつ", "出来る", "様に", "事が", "ゲームパット", "エディター", "サンプルプログラム"]


def strip_inline(line: str) -> str:
    """インラインのリテラル、ロール、URL を取り除く。"""
    line = re.sub(r"``.*?``", " X ", line)
    line = re.sub(r":[a-z]+:`[^`]*`", " X ", line)
    line = re.sub(r"`[^`]*`__?", " X ", line)
    line = re.sub(r"https?://\S+", " X ", line)
    return line.replace("\\ ", "")


def main() -> None:
    count = 0
    for path in sorted(SOURCE.glob("*.rst")):
        in_block = False
        block_indent = 0
        for no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            stripped = raw.strip()
            indent = len(raw) - len(raw.lstrip())
            if in_block:
                if stripped and indent <= block_indent:
                    in_block = False
                else:
                    continue
            if re.match(r"\.\. (code-block|literalinclude|graphviz|math)::", stripped):
                in_block = True
                block_indent = indent
                continue
            if stripped.startswith(".. ") or stripped.startswith(":"):
                continue
            line = strip_inline(raw)
            for name, pattern in CHECKS:
                for m in pattern.finditer(line):
                    print(f"{path.name}:{no}: [{name}] ...{line[max(0, m.start() - 10):m.end() + 10].strip()}...")
                    count += 1
            for word in VARIANTS:
                if word in line:
                    print(f"{path.name}:{no}: [表記ゆれの候補] {word}")
                    count += 1
    print(f"{count} 件")


if __name__ == "__main__":
    main()
