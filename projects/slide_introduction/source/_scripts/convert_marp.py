"""examples/marp のサンプルスライドを marp-cli で HTML / PDF / PNG に変換する.

conf.py からビルドの開始時に呼び出す。単独でも実行できる。

    py convert_marp.py

marp-cli は環境変数 MARP_CLI があればその値を、なければ PATH 上の marp を使う。
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = SCRIPT_DIR.parent
PROJECT_DIR = SOURCE_DIR.parent
MARP_DIR = PROJECT_DIR / 'examples' / 'marp'
THEME_DIR = MARP_DIR / 'themes'
STATIC_OUT = SOURCE_DIR / '_static' / 'marp'
IMAGE_OUT = SOURCE_DIR / 'images' / 'marp'

# marp-cli の 1 回の実行にかける時間の上限（秒）
TIMEOUT = 180


class MarpError(Exception):
    """marp-cli が見つからない、または変換に失敗したことを表す."""


def find_marp() -> str:
    """marp-cli の実行ファイルのパスを返す."""
    env = os.environ.get('MARP_CLI')
    if env:
        return env
    found = shutil.which('marp')
    if found is None:
        raise MarpError('marp-cli が見つからない（npm install -g @marp-team/marp-cli で導入できる）')
    return found


def run_marp(marp: str, args: list[str]) -> None:
    """marp-cli を実行し、失敗したら MarpError を送出する."""
    # --theme-set は複数の値を取るので、入力ファイルを吸い込まないよう最後に置く。
    # marp-cli は標準入力からも Markdown を読もうとするため、--no-stdin で止める
    command = [marp, '--no-stdin', *args, '--theme-set', str(THEME_DIR)]
    try:
        result = subprocess.run(command, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=TIMEOUT, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise MarpError(f'marp-cli を実行できなかった: {exc}') from exc
    if result.returncode != 0:
        raise MarpError(f'marp-cli が失敗した（終了コード {result.returncode}）: {result.stderr.strip()}')


def convert(markdown: Path, marp: str) -> list[Path]:
    """1 つの Markdown を HTML、PDF、スライドごとの PNG に変換し、出力したファイルを返す."""
    stem = markdown.stem
    html = STATIC_OUT / f'{stem}.html'
    pdf = STATIC_OUT / f'{stem}.pdf'
    run_marp(marp, [str(markdown), '-o', str(html)])
    run_marp(marp, [str(markdown), '--pdf', '-o', str(pdf)])
    # --images を指定すると、tech_talk.001.png のようにスライドごとに番号が付く
    for old in IMAGE_OUT.glob(f'{stem}.*.png'):
        old.unlink()
    run_marp(marp, [str(markdown), '--images', 'png', '-o', str(IMAGE_OUT / f'{stem}.png')])
    outputs = [html, pdf, *sorted(IMAGE_OUT.glob(f'{stem}.*.png'))]
    missing = [path.name for path in (html, pdf) if not path.exists()]
    if missing or len(outputs) == 2:
        raise MarpError(f'{markdown.name} の変換結果が見つからない: {missing or "PNG"}')
    return outputs


def convert_all() -> list[Path]:
    """examples/marp 直下のすべての Markdown を変換し、出力したファイルを返す."""
    marp = find_marp()
    STATIC_OUT.mkdir(parents=True, exist_ok=True)
    IMAGE_OUT.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for markdown in sorted(MARP_DIR.glob('*.md')):
        outputs.extend(convert(markdown, marp))
    return outputs


def main() -> int:
    try:
        outputs = convert_all()
    except MarpError as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1
    print(f'converted: {len(outputs)} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
