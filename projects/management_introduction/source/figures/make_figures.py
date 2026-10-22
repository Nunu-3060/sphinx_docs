"""本文で使用する matplotlib の図を生成する。

build_html.bat から呼び出され、このスクリプトと同じフォルダに PNG ファイルを出力する。
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

OUTPUT_DIR = Path(__file__).resolve().parent
FONT_CANDIDATES = ["Noto Sans JP", "Yu Gothic", "Meiryo"]
DPI = 150

# 図全体で使う配色
BLUE = "#2b6cb0"
ORANGE = "#dd6b20"
GREEN = "#2f855a"
RED = "#c53030"
GRAY = "#718096"


def setup_font() -> None:
    """日本語フォントを候補の先頭から順に探して設定する。

    matplotlib は可変フォントの太さを選べないため、標準の太さ（400）の書体を持つフォントだけを候補とする。
    """
    available = {font.name for font in font_manager.fontManager.ttflist if font.weight in (400, "normal", "regular")}
    for name in FONT_CANDIDATES:
        if name in available:
            plt.rcParams["font.family"] = name
            return
    raise RuntimeError("日本語フォントが見つからない: " + ", ".join(FONT_CANDIDATES))


def save(fig: Figure, name: str) -> None:
    """図を PNG ファイルとして保存して閉じる。"""
    fig.savefig(OUTPUT_DIR / name, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def draw_first_90_days() -> None:
    """着任後 90 日のタイムラインを描く。"""
    phases = [
        ("知る\n（現状把握）", 0, 30, BLUE),
        ("つなぐ\n（関係構築・課題の絞り込み）", 30, 60, GREEN),
        ("動かす\n（小さな改善の実行）", 60, 90, ORANGE),
    ]
    tasks = [
        ("上司と期待値をすり合わせる", 0, 10),
        ("メンバー全員と初回面談", 0, 20),
        ("業務・プロジェクトの棚卸し", 5, 30),
        ("関係者へのあいさつ回り", 10, 40),
        ("定例の 1on1 を開始", 20, 90),
        ("課題の優先順位を決める", 35, 55),
        ("チームの目標を言語化", 45, 65),
        ("小さな改善を 1 つ実行", 60, 85),
        ("90 日の振り返り", 85, 90),
    ]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for label, start, end, color in phases:
        ax.axvspan(start, end, color=color, alpha=0.10)
        ax.text((start + end) / 2, len(tasks) + 0.15, label, ha="center", va="bottom", fontsize=10, color=color)
    for i, (label, start, end) in enumerate(reversed(tasks)):
        ax.barh(i, end - start, left=start, height=0.55, color=GRAY)
        ax.text(start - 1, i, label, ha="right", va="center", fontsize=9)
    ax.set_xlim(0, 90)
    ax.set_ylim(-0.7, len(tasks) + 1.2)
    ax.set_xticks([0, 30, 60, 90])
    ax.set_xticklabels(["着任", "30 日", "60 日", "90 日"])
    ax.set_yticks([])
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    save(fig, "first_90_days.png")


def draw_priority_matrix() -> None:
    """緊急度と重要度のマトリクスを描く。"""
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    cells = [
        (0, 1, "第 2 領域\n重要だが緊急でない", "目標設定、育成、仕組みの改善、\n関係づくり、技術的負債の返済", GREEN),
        (1, 1, "第 1 領域\n重要かつ緊急", "障害対応、締め切り直前の作業、\nクレーム対応", RED),
        (0, 0, "第 4 領域\n重要でも緊急でもない", "目的のない会議、惰性の作業", GRAY),
        (1, 0, "第 3 領域\n緊急だが重要でない", "多くの割り込み、一部の会議や\n問い合わせ", ORANGE),
    ]
    for x, y, title, body, color in cells:
        ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color, alpha=0.15, edgecolor="white", linewidth=3))
        ax.text(x + 0.5, y + 0.68, title, ha="center", va="center", fontsize=11, color=color, fontweight="bold")
        ax.text(x + 0.5, y + 0.32, body, ha="center", va="center", fontsize=9)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xticks([0.5, 1.5])
    ax.set_xticklabels(["緊急でない", "緊急"])
    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels(["重要でない", "重要"])
    ax.set_xlabel("緊急度 →")
    ax.set_ylabel("重要度 →")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    save(fig, "priority_matrix.png")


def draw_three_point_estimate() -> None:
    """三点見積りの考え方（ベータ分布による近似）を描く。"""
    optimistic, most_likely, pessimistic = 3.0, 5.0, 13.0
    expected = (optimistic + 4 * most_likely + pessimistic) / 6
    sigma = (pessimistic - optimistic) / 6

    # PERT で用いられるベータ分布のパラメータ
    alpha = 1 + 4 * (most_likely - optimistic) / (pessimistic - optimistic)
    beta = 1 + 4 * (pessimistic - most_likely) / (pessimistic - optimistic)
    x = np.linspace(optimistic, pessimistic, 400)
    t = (x - optimistic) / (pessimistic - optimistic)
    density = t ** (alpha - 1) * (1 - t) ** (beta - 1)
    density = density / density.max()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(x, density, color=BLUE, alpha=0.15)
    ax.plot(x, density, color=BLUE)
    marks = [
        (optimistic, "楽観値 O = 3", GREEN, 1.08),
        (most_likely, "最可能値 M = 5", BLUE, 1.20),
        (expected, f"期待値 E = {expected:.1f}", ORANGE, 1.08),
        (pessimistic, "悲観値 P = 13", RED, 1.08),
    ]
    for value, label, color, height in marks:
        ax.axvline(value, color=color, linestyle="--", linewidth=1.2)
        ax.text(
            value, height, label, ha="center", va="bottom", fontsize=9, color=color,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5}, zorder=3,
        )
    ax.annotate(
        "",
        xy=(expected + sigma, 0.15),
        xytext=(expected - sigma, 0.15),
        arrowprops={"arrowstyle": "<->", "color": GRAY},
    )
    ax.text(
        expected, 0.18, f"E ± σ（σ ≒ {sigma:.2f}）", ha="center", va="bottom", fontsize=9, color=GRAY,
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5, "alpha": 0.8}, zorder=3,
    )
    ax.set_xlim(2, 14)
    ax.set_ylim(0, 1.35)
    ax.set_xlabel("所要日数")
    ax.set_yticks([])
    ax.set_ylabel("起こりやすさ")
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    save(fig, "three_point_estimate.png")


def draw_delegation_styles() -> None:
    """メンバーの状態と関わり方（状況対応型リーダーシップ）の関係を描く。"""
    fig, ax = plt.subplots(figsize=(7.5, 5.6))
    styles = [
        (1.5, 0.5, "S1 指示型", "やり方を具体的に示し、\nこまめに確認する", RED),
        (1.5, 1.5, "S2 コーチ型", "理由を説明し、意見を聞きつつ\n方向付けも行う", ORANGE),
        (0.5, 1.5, "S3 支援型", "やり方は任せ、\n相談と励ましで支える", GREEN),
        (0.5, 0.5, "S4 委任型", "目的と期限を決めて任せ、\n報告を受ける", BLUE),
    ]
    for x, y, title, body, color in styles:
        ax.add_patch(
            Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor=color, alpha=0.13, edgecolor="white", linewidth=3)
        )
        ax.text(x, y + 0.18, title, ha="center", va="center", fontsize=12, color=color, fontweight="bold")
        ax.text(x, y - 0.17, body, ha="center", va="center", fontsize=9)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xticks([0.5, 1.5])
    ax.set_xticklabels(["少ない", "多い"])
    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels(["少ない", "多い"])
    ax.set_xlabel("指示的な関わり（やり方を示す量） →")
    ax.set_ylabel("支援的な関わり（話を聞き、励ます量） →")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    # S1 → S2 → S3 → S4 の移行を矢印で示す
    for start, end in [((1.88, 0.75), (1.88, 1.25)), ((1.25, 1.88), (0.75, 1.88)), ((0.12, 1.25), (0.12, 0.75))]:
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "-|>", "color": GRAY, "linewidth": 1.5})
    save(fig, "delegation_styles.png")


def draw_tuckman() -> None:
    """タックマンモデルの各段階とチームの生産性のイメージを描く。"""
    stages = ["形成期", "混乱期", "統一期", "機能期", "散会期"]
    x = np.linspace(0, 5, 500)
    performance = np.interp(
        x,
        [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
        [0.45, 0.42, 0.35, 0.22, 0.30, 0.52, 0.72, 0.88, 0.92, 0.80, 0.55],
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = [BLUE, RED, ORANGE, GREEN, GRAY]
    for i, (stage, color) in enumerate(zip(stages, colors)):
        ax.axvspan(i, i + 1, color=color, alpha=0.08)
        ax.text(i + 0.5, 1.03, stage, ha="center", va="bottom", fontsize=10, color=color)
    ax.plot(x, performance, color=BLUE, linewidth=2)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1.15)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("時間 →")
    ax.set_ylabel("チームの生産性（イメージ） →")
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    save(fig, "tuckman.png")


def draw_time_allocation() -> None:
    """プレイヤーからマネージャーへの時間配分の変化のイメージを描く。"""
    roles = ["プレイヤー", "リーダー\n（数名）", "マネージャー\n（10 名程度）"]
    categories = [
        ("自分の実務", np.array([80, 50, 20]), BLUE),
        ("メンバー支援・育成", np.array([5, 20, 35]), GREEN),
        ("計画・調整・会議", np.array([10, 20, 30]), ORANGE),
        ("組織・採用・評価", np.array([5, 10, 15]), GRAY),
    ]
    fig, ax = plt.subplots(figsize=(7.5, 4))
    left = np.zeros(len(roles))
    for label, values, color in categories:
        ax.barh(roles, values, left=left, color=color, alpha=0.85, label=label)
        for y, (value, start) in enumerate(zip(values, left)):
            ax.text(start + value / 2, y, f"{value}%", ha="center", va="center", fontsize=8, color="white")
        left = left + values
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("勤務時間に占める割合（イメージ）")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=4, fontsize=8, frameon=False)
    for side in ("right", "top"):
        ax.spines[side].set_visible(False)
    save(fig, "time_allocation.png")


def main() -> None:
    """すべての図を生成する。"""
    setup_font()
    draw_first_90_days()
    draw_priority_matrix()
    draw_three_point_estimate()
    draw_delegation_styles()
    draw_tuckman()
    draw_time_allocation()


if __name__ == "__main__":
    main()
