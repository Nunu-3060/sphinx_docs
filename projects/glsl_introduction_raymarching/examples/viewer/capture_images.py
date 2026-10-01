"""シェーダーの実行結果の画像を、headless ブラウザーで撮影する。

``shader_viewer.py`` で生成した HTML を Chrome または Edge の headless モードで
開き、スクリーンショットを PNG ファイルとして保存する。WebGL は CPU で動作する
SwiftShader で実行するため、GPU の無い環境でも撮影できる。

既定では、画像が存在しないか、シェーダー (またはこのスクリプトとビューアー)
より古い画像だけを撮影し直す。Sphinx の conf.py からも同じ処理を呼び出す。

使い方::

    python capture_images.py            # 古い画像だけを撮影する
    python capture_images.py --force    # すべての画像を撮影する
    python capture_images.py 05_lighting 06_shadow   # 指定したものだけ

ブラウザーは次の順に探す。

1. 環境変数 ``SHADER_BROWSER`` に指定された実行ファイル
2. Chrome と Edge の標準のインストール先
3. PATH 上の ``chrome``、``google-chrome``、``chromium``、``msedge`` など
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from shader_viewer import write_html

VIEWER_DIR = Path(__file__).resolve().parent
DEFAULT_SHADER_DIR = VIEWER_DIR.parent / "shaders"
DEFAULT_OUTPUT_DIR = VIEWER_DIR.parent.parent / "source" / "_static" / "images"

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 360
DEFAULT_TIME = 1.0   # 撮影時の iTime [s]
DEFAULT_FRAMES = 1   # 撮影前に描画するフレーム数 (iFrame は 0 から始まる)
TIMEOUT = 900        # ブラウザー 1 回の実行の制限時間 [s]


@dataclass(frozen=True)
class CaptureSetting:
    """撮影の条件。"""

    time: float = DEFAULT_TIME
    frames: int = DEFAULT_FRAMES


# 既定以外の条件で撮影するシェーダー
CAPTURE_SETTINGS: dict[str, CaptureSetting] = {
    "04_smooth_union": CaptureSetting(time=2.7),   # 2 つの球が重なる時刻
    "17_progressive": CaptureSetting(frames=64),   # 64 フレーム分を蓄積する
    "16_atmosphere": CaptureSetting(time=7.0),     # 夕日の時刻
    "10_curl": CaptureSetting(time=6.2832),        # 流す時間が最大の時刻
    "20_still_life": CaptureSetting(frames=40),    # 40 フレーム分を蓄積する
    "20_still_life_debug": CaptureSetting(frames=8),
}

BROWSER_ENV = "SHADER_BROWSER"
BROWSER_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]
BROWSER_NAMES = ["chrome", "google-chrome", "google-chrome-stable",
                 "chromium", "chromium-browser", "msedge", "microsoft-edge"]

# 撮影結果に影響するファイル。これらより古い画像は撮影し直す
DEPENDENCIES = [VIEWER_DIR / "shader_viewer.py", Path(__file__).resolve()]


@dataclass(frozen=True)
class CaptureResult:
    """1 つのシェーダーの撮影結果。"""

    shader: Path
    image: Path
    error: str | None = None


def find_browser() -> Path | None:
    """撮影に使うブラウザーの実行ファイルを探す。見つからなければ None。"""
    candidates: list[str] = []
    env = os.environ.get(BROWSER_ENV)
    if env:
        candidates.append(env)
    candidates.extend(BROWSER_PATHS)
    for name in BROWSER_NAMES:
        found = shutil.which(name)
        if found:
            candidates.append(found)
    for candidate in candidates:
        path = Path(candidate)
        if path.is_file():
            return path
    return None


def image_path(shader: Path, output_dir: Path) -> Path:
    """シェーダーに対応する画像ファイルのパスを返す。"""
    return output_dir / f"{shader.stem}.png"


def is_outdated(shader: Path, image: Path) -> bool:
    """画像が存在しないか、シェーダーや依存ファイルより古ければ True。"""
    if not image.is_file():
        return True
    newest = max(p.stat().st_mtime for p in [shader, *DEPENDENCIES])
    return image.stat().st_mtime < newest


def _run_browser(browser: Path, profile: Path, options: list[str],
                 url: str) -> str:
    """ヘッドレスモードでブラウザーを実行し、標準出力を返す。"""
    command = [
        str(browser),
        "--headless=new",
        "--use-angle=swiftshader",
        "--enable-unsafe-swiftshader",
        "--ignore-gpu-blocklist",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--virtual-time-budget=3000",
        f"--window-size={IMAGE_WIDTH},{IMAGE_HEIGHT}",
        f"--user-data-dir={profile}",
        *options,
        url,
    ]
    completed = subprocess.run(command, capture_output=True, text=True,
                               encoding="utf-8", errors="replace",
                               timeout=TIMEOUT)
    return completed.stdout


def _compile_error(dom: str) -> str | None:
    """ビューアーの DOM からシェーダーのエラーメッセージを取り出す。"""
    title = re.search(r"<title>(.*?)</title>", dom, re.S)
    if title is None:
        return "ページを読み込めなかった"
    if not title.group(1).startswith("ERROR"):
        return None
    message = re.search(r'<pre id="error"[^>]*>(.*?)</pre>', dom, re.S)
    return html.unescape(message.group(1)) if message else title.group(1)


def capture(browser: Path, shader: Path, image: Path) -> CaptureResult:
    """1 つのシェーダーを実行して撮影する。"""
    with tempfile.TemporaryDirectory() as work:
        work_dir = Path(work)
        page = write_html(shader, work_dir / f"{shader.stem}.html")
        setting = CAPTURE_SETTINGS.get(shader.stem, CaptureSetting())
        url = f"{page.as_uri()}#t={setting.time}&frames={setting.frames}"
        profile = work_dir / "profile"
        try:
            # 1 回目: シェーダーのコンパイルエラーの有無を調べる。
            # コンパイルは読み込み時に行われるので、描画はしない (frames=0)
            dom = _run_browser(browser, profile, ["--dump-dom"],
                               f"{page.as_uri()}#frames=0")
            error = _compile_error(dom)
            if error is not None:
                return CaptureResult(shader, image, error)
            # 2 回目: 撮影する
            image.parent.mkdir(parents=True, exist_ok=True)
            _run_browser(browser, profile,
                         [f"--screenshot={image.resolve()}"], url)
        except subprocess.TimeoutExpired:
            return CaptureResult(shader, image, "ブラウザーが時間内に終了しない")
    if not image.is_file():
        return CaptureResult(shader, image, "画像が作成されなかった")
    return CaptureResult(shader, image)


def capture_all(shaders: list[Path], output_dir: Path, browser: Path,
                jobs: int = 4) -> list[CaptureResult]:
    """複数のシェーダーを並列に撮影する。"""
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as executor:
        futures = [executor.submit(capture, browser, shader,
                                   image_path(shader, output_dir))
                   for shader in shaders]
        return [future.result() for future in futures]


def select_shaders(shader_dir: Path, output_dir: Path, names: list[str],
                   force: bool) -> list[Path]:
    """撮影するシェーダーを選ぶ。

    Args:
        shader_dir: シェーダーのフォルダー。
        output_dir: 画像の出力先のフォルダー。
        names: 撮影するシェーダーの名前 (拡張子なし)。空ならすべて。
        force: True なら、画像が新しくても撮影する。

    Returns:
        撮影するシェーダーのパスのリスト。
    """
    shaders = sorted(shader_dir.glob("*.frag"))
    if names:
        wanted = {name.removesuffix(".frag") for name in names}
        shaders = [s for s in shaders if s.stem in wanted]
    if not force:
        shaders = [s for s in shaders
                   if is_outdated(s, image_path(s, output_dir))]
    return shaders


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(
        description="シェーダーの実行結果の画像を撮影する。")
    parser.add_argument("names", nargs="*",
                        help="撮影するシェーダーの名前 (省略時はすべて)")
    parser.add_argument("--force", action="store_true",
                        help="画像が新しくても撮影し直す")
    parser.add_argument("--jobs", type=int, default=4,
                        help="同時に実行するブラウザーの数 (既定: 4)")
    parser.add_argument("--shader-dir", type=Path, default=DEFAULT_SHADER_DIR,
                        help="シェーダーのフォルダー")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
                        help="画像の出力先のフォルダー")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """エントリーポイント。"""
    args = parse_args(argv)
    shaders = select_shaders(args.shader_dir, args.output_dir, args.names,
                             args.force)
    if not shaders:
        print("撮影し直す画像は無い。")
        return 0

    browser = find_browser()
    if browser is None:
        print("Chrome または Edge が見つからない。"
              f"環境変数 {BROWSER_ENV} で実行ファイルを指定できる。",
              file=sys.stderr)
        return 1

    print(f"{len(shaders)} 個のシェーダーを撮影する ({browser.name})")
    results = capture_all(shaders, args.output_dir, browser, args.jobs)
    failed = 0
    for result in results:
        if result.error is None:
            print(f"  OK     {result.image.name}")
        else:
            failed += 1
            print(f"  FAILED {result.shader.name}: {result.error}",
                  file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
