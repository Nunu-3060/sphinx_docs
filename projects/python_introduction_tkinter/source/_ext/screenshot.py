"""サンプルコードの実行結果のスクリーンショットを作成する Sphinx 拡張です。

HTML のビルドを開始するとき (builder-inited イベント) に、サンプルコードを
1 本ずつ別のプロセスで起動し、メインウィンドウを撮影して PNG で保存します。

conf.py で次の設定値を指定できます。

* screenshot_mode
    * "auto": 画像がない場合と、サンプルコードが画像より新しい場合に撮影します。
    * "always": すべてのサンプルコードを撮影し直します。
    * "never": 撮影しません。
    * 環境変数 SCREENSHOT_MODE を設定すると、conf.py の値より優先されます。
* screenshot_examples_dir: サンプルコードのフォルダー (conf.py からの相対パス)
* screenshot_output_dir: 画像の保存先 (conf.py からの相対パス)
* screenshot_delay_ms: 起動してから撮影するまでの待ち時間 (ミリ秒)
* screenshot_timeout: 1 本のサンプルコードに許す最大の実行時間 (秒)

撮影は画面の一部をそのまま取り込むため、Windows のデスクトップ環境が必要です。
撮影中は、サンプルコードのウィンドウが一時的に最前面に表示されます。
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

MODES = ("auto", "always", "never")


# ----------------------------------------------------------------------
# Sphinx 拡張としての処理 (ビルドするプロセスで実行されます)
# ----------------------------------------------------------------------
def setup(app: Any) -> dict[str, Any]:
    """拡張を登録します。Sphinx から呼び出されます。"""
    app.add_config_value("screenshot_mode", "auto", "env")
    app.add_config_value("screenshot_examples_dir", "../examples", "env")
    app.add_config_value("screenshot_output_dir", "images", "env")
    app.add_config_value("screenshot_delay_ms", 900, "env")
    app.add_config_value("screenshot_timeout", 20, "env")
    app.connect("builder-inited", generate_screenshots)
    return {"version": "1.0", "parallel_read_safe": True}


def generate_screenshots(app: Any) -> None:
    """必要なサンプルコードを撮影します。"""
    from sphinx.util import logging

    logger = logging.getLogger(__name__)
    config = app.config
    mode = os.environ.get("SCREENSHOT_MODE", config.screenshot_mode)
    if mode not in MODES:
        logger.warning(f"screenshot_mode の値が不正です: {mode!r}")
        return
    if mode == "never":
        return

    confdir = Path(app.confdir)
    examples_dir = (confdir / config.screenshot_examples_dir).resolve()
    output_dir = (confdir / config.screenshot_output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    targets = []
    for example in sorted(examples_dir.glob("*.py")):
        image = output_dir / f"{example.stem}.png"
        if mode == "always" or _is_outdated(example, image):
            targets.append((example, image))
    if not targets:
        return

    if sys.platform != "win32":
        logger.warning(
            "スクリーンショットの撮影は Windows だけに対応しています。"
            f"撮影していない画像が {len(targets)} 件あります。"
        )
        return

    logger.info(f"スクリーンショットを撮影します ({len(targets)} 件)")
    for example, image in targets:
        logger.info(f"  {example.name} -> {image.name}")
        command = [
            sys.executable,
            __file__,
            str(example),
            str(image),
            str(config.screenshot_delay_ms),
        ]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                timeout=config.screenshot_timeout,
                cwd=example.parent,
            )
        except subprocess.TimeoutExpired:
            logger.warning(f"{example.name} の撮影がタイムアウトしました")
            continue
        if result.returncode != 0:
            message = result.stderr.decode(errors="replace").strip()
            logger.warning(f"{example.name} の撮影に失敗しました\n{message}")


def _is_outdated(example: Path, image: Path) -> bool:
    """画像がないか、サンプルコードより古い場合に True を返します。"""
    if not image.exists():
        return True
    return image.stat().st_mtime < example.stat().st_mtime


# ----------------------------------------------------------------------
# 撮影処理 (サンプルコードごとに別のプロセスで実行されます)
# ----------------------------------------------------------------------
def _prepare_memo_app(root: Any) -> None:
    """簡易メモ帳に文字列を入力し、使用中の状態にします。"""
    import tkinter as tk

    text = next(w for w in _descendants(root) if isinstance(w, tk.Text))
    text.insert("1.0", "買い物メモ\n\n・牛乳\n・パン\n・卵\n")
    text.mark_set("insert", "5.2")
    text.event_generate("<KeyRelease>")


# 撮影の前に画面の状態を整える関数 (サンプルコードのファイル名ごと)
PREPARE_HOOKS = {
    "ch12_memo_app.py": _prepare_memo_app,
}


def _descendants(widget: Any) -> list[Any]:
    """ウィジェットの子孫をすべて返します。"""
    result = []
    for child in widget.winfo_children():
        result.append(child)
        result.extend(_descendants(child))
    return result


def _window_bounds(root: Any) -> tuple[int, int, int, int]:
    """影を除いたウィンドウの外枠の座標 (左, 上, 右, 下) を返します。"""
    import ctypes
    from ctypes import wintypes

    dwmwa_extended_frame_bounds = 9
    rect = wintypes.RECT()
    hwnd = wintypes.HWND(int(root.wm_frame(), 16))
    ctypes.windll.dwmapi.DwmGetWindowAttribute(  # type: ignore[attr-defined]
        hwnd,
        dwmwa_extended_frame_bounds,
        ctypes.byref(rect),
        ctypes.sizeof(rect),
    )
    return rect.left, rect.top, rect.right, rect.bottom


def capture(example: Path, image: Path, delay_ms: int) -> None:
    """サンプルコードを実行し、メインウィンドウを撮影して終了します。"""
    import ctypes
    import runpy
    import tkinter as tk

    from PIL import ImageGrab

    # 高 DPI 環境でも、ぼやけずに実際の画素で撮影します
    windll = ctypes.windll  # type: ignore[attr-defined]
    windll.shcore.SetProcessDpiAwareness(2)

    original_mainloop = tk.Misc.mainloop
    temporary = image.with_suffix(".tmp.png")

    def patched_mainloop(self: tk.Misc, n: int = 0) -> None:
        """撮影と終了を予約してから、本来の mainloop を実行します。"""
        root = self.winfo_toplevel()
        hook = PREPARE_HOOKS.get(example.name)
        if hook is not None:
            root.after(delay_ms // 3, hook, root)

        def bring_to_front() -> None:
            root.attributes("-topmost", True)
            root.lift()
            root.focus_force()  # タイトルバーをアクティブな表示にします
            root.update()
            root.after(400, grab)

        def grab() -> None:
            root.update()
            ImageGrab.grab(_window_bounds(root), all_screens=True).save(
                temporary
            )
            root.destroy()

        root.after(delay_ms, bring_to_front)
        original_mainloop(self, n)

    tk.Misc.mainloop = patched_mainloop  # type: ignore[method-assign]
    sys.path.insert(0, str(example.parent))
    runpy.run_path(str(example), run_name="__main__")
    if not temporary.exists():
        raise RuntimeError("ウィンドウを撮影できませんでした")
    # 撮影に成功した場合だけ、既存の画像を置き換えます
    temporary.replace(image)


if __name__ == "__main__":
    capture(Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]))
