"""ffmpeg を使った動画の書き出し。

Python で作ったフレーム（NumPy 配列）を、生の画素列として ffmpeg の標準入力に
渡し、連番画像のファイルを作らずに動画にする。

ffmpeg は次の順で探す。

1. 環境変数 FFMPEG に書かれた実行ファイル
2. 環境変数 PATH の通った ffmpeg
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from types import TracebackType

import numpy as np

from common import ByteArray, FloatArray, to_bytes


class FFmpegNotFoundError(RuntimeError):
    """ffmpeg が見つからないときの例外。"""


def find_ffmpeg() -> str | None:
    """ffmpeg の実行ファイルのパスを返す。見つからなければ None を返す。"""
    configured = os.environ.get("FFMPEG")
    if configured and Path(configured).is_file():
        return configured
    return shutil.which("ffmpeg")


def require_ffmpeg() -> str:
    """ffmpeg の実行ファイルのパスを返す。見つからなければ例外を送出する。"""
    path = find_ffmpeg()
    if path is None:
        raise FFmpegNotFoundError("ffmpeg が見つからない。PATH を通すか、環境変数 FFMPEG を設定すること。")
    return path


def run_ffmpeg(arguments: list[str]) -> None:
    """ffmpeg を引数 arguments で実行する。進行状況の表示は抑え、エラーだけを表示する。"""
    subprocess.run([require_ffmpeg(), "-y", "-hide_banner", "-loglevel", "error", *arguments], check=True)


class VideoWriter:
    """フレームを 1 枚ずつ受け取り、H.264 の MP4 を書き出す。

    使用例::

        with VideoWriter(path, 640, 360, fps=30) as writer:
            for frame in frames:
                writer.write(frame)  # (360, 640, 3) の配列
    """

    def __init__(self, path: Path, width: int, height: int, fps: int = 30, crf: int = 28) -> None:
        if width % 2 or height % 2:
            raise ValueError("yuv420p で書き出すため、幅と高さは偶数にする")
        self.width = width
        self.height = height
        arguments = [
            require_ffmpeg(), "-y", "-hide_banner", "-loglevel", "error",
            # 入力: 標準入力から 8 bit RGB の生の画素列を読む
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{width}x{height}", "-r", str(fps), "-i", "-",
            # 出力: 多くのブラウザーで再生できる H.264 + yuv420p。faststart で先頭から再生できるようにする
            "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-an", str(path),
        ]
        self._process = subprocess.Popen(arguments, stdin=subprocess.PIPE)

    def write(self, frame: FloatArray | ByteArray) -> None:
        """1 フレームを書き込む。実数の配列は 0〜1 の範囲とみなす。グレースケールも受け付ける。"""
        data = frame if frame.dtype == np.uint8 else to_bytes(frame.astype(np.float64))
        if data.ndim == 2:
            data = np.asarray(np.repeat(data[:, :, None], 3, axis=2), dtype=np.uint8)
        if data.shape != (self.height, self.width, 3):
            raise ValueError(f"フレームの形が {data.shape} で、({self.height}, {self.width}, 3) と異なる")
        assert self._process.stdin is not None
        self._process.stdin.write(np.ascontiguousarray(data).tobytes())

    def close(self) -> None:
        """入力を閉じ、ffmpeg の終了を待つ。"""
        assert self._process.stdin is not None
        self._process.stdin.close()
        if self._process.wait() != 0:
            raise RuntimeError("ffmpeg が異常終了した")

    def __enter__(self) -> VideoWriter:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None
    ) -> None:
        self.close()


def to_webm(source: Path, target: Path, crf: int = 40) -> None:
    """動画を VP9 の WebM に変換する（-b:v 0 と -crf で画質を固定する）。"""
    run_ffmpeg(["-i", str(source), "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", str(crf), "-an", str(target)])


def to_gif(source: Path, target: Path, fps: int = 15, width: int = 320, colors: int = 64) -> None:
    """動画を GIF に変換する。動画から最適な 256 色以下のパレットを作り、それを使って減色する。"""
    graph = (
        f"fps={fps},scale={width}:-1:flags=lanczos,split[a][b];"
        f"[a]palettegen=max_colors={colors}[palette];[b][palette]paletteuse=dither=bayer"
    )
    run_ffmpeg(["-i", str(source), "-vf", graph, str(target)])
