"""第 11 章の図「入力の長さと処理時間」を作成するスクリプト。

パターン (a+)+$ と、それを改善したパターンについて、
"a" を n 個並べた後に "b" を付けた文字列 (一致に失敗する文字列) の
検索にかかる時間を計測し、グラフを PNG 形式で保存する。

実行方法 (matplotlib が必要)::

    python ch11_redos_benchmark.py [出力ファイル名]

出力ファイル名を省略すると、カレントディレクトリに redos_time.png を作成する。
n が大きいほど時間がかかるため、実行には数十秒程度かかる。
"""
import re
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画面を使わずにファイルへ出力する
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

PATTERNS = {
    "(a+)+$": re.compile(r"(a+)+$"),
    "(?>a+)+$": re.compile(r"(?>a+)+$"),
    "a+$": re.compile(r"a+$"),
}
LENGTHS = list(range(10, 25))
REPEAT = 3

# 日本語を表示できるフォントのうち、インストールされているものを使う
JAPANESE_FONTS = ("Meiryo", "Yu Gothic", "Noto Sans CJK JP", "Noto Sans JP", "IPAexGothic", "Hiragino Sans")
INSTALLED_FONTS = {font.name for font in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = [name for name in JAPANESE_FONTS if name in INSTALLED_FONTS] + ["sans-serif"]


def measure(pattern: re.Pattern[str], n: int) -> float:
    """長さ n の失敗する入力に対する検索時間 (秒) を REPEAT 回計測し、最小値を返す。"""
    text = "a" * n + "b"
    times = []
    for _ in range(REPEAT):
        start = time.perf_counter()
        pattern.search(text)
        times.append(time.perf_counter() - start)
    return min(times)


def main() -> None:
    """計測してグラフを保存する。"""
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("redos_time.png")
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=120)
    for (label, pattern), marker in zip(PATTERNS.items(), ("o", "s", "^")):
        seconds = [measure(pattern, n) for n in LENGTHS]
        print(label, " ".join(f"{s:.2e}" for s in seconds))
        ax.plot(LENGTHS, seconds, marker=marker, label=label)
    ax.set_yscale("log")
    ax.set_xlabel("入力の長さ n (\"a\" × n + \"b\")")
    ax.set_ylabel("検索時間 [秒] (対数目盛)")
    ax.set_title("一致に失敗するときの検索時間")
    ax.grid(True, which="major", linestyle=":")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output)
    print(f"saved: {output}")


if __name__ == "__main__":
    main()
