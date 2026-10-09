"""シーケンス図: 時間の流れに沿ったやり取りを描く.

ログイン処理での、ブラウザーと 3 つのサーバーの間のメッセージの
やり取りを描く。縦方向が時間の流れ（上から下）を表す。

使い方: python ch12_sequence.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont

PARTICIPANTS = ["ブラウザー", "Web サーバー", "認証サーバー", "データベース"]
# (送信元, 送信先, メッセージ, 応答か)。応答は破線の矢印で描く
MESSAGES = [
    (0, 1, "POST /login", False),
    (1, 2, "認証の要求", False),
    (2, 3, "ユーザーの検索", False),
    (3, 2, "ユーザー情報", True),
    (2, 2, "パスワードの照合", False),
    (2, 1, "トークン", True),
    (1, 0, "302 リダイレクト", True),
]
STEP = 1.0  # メッセージ 1 つ分の縦の間隔


def create_figure() -> Figure:
    """ログイン処理のシーケンス図を描く."""
    fig, ax = plt.subplots(figsize=(8, 4.8))
    bottom = -(len(MESSAGES) + 0.5) * STEP
    # 参加者の箱と、そこから下に伸びる生存線（ライフライン）
    for x, name in enumerate(PARTICIPANTS):
        ax.text(x, 0.6, name, ha="center", va="center",
                bbox={"boxstyle": "round", "facecolor": "#dbe9f6"})
        ax.plot([x, x], [0.3, bottom], color="gray", linestyle="--",
                linewidth=1)
    for row, (source, target, text, is_reply) in enumerate(MESSAGES):
        y = -(row + 0.5) * STEP
        style = "--" if is_reply else "-"
        if source == target:
            # 自分自身へのメッセージは、右に出て戻る矢印で描く
            right = source + 0.15
            ax.plot([source, right, right], [y, y, y - 0.3], color="black",
                    linewidth=1)
            ax.annotate("", xy=(source, y - 0.3), xytext=(right, y - 0.3),
                        arrowprops={"arrowstyle": "->"})
            ax.text(right + 0.05, y - 0.15, text, va="center", fontsize=9)
            continue
        ax.annotate("", xy=(target, y), xytext=(source, y),
                    arrowprops={"arrowstyle": "->", "linestyle": style})
        ax.text((source + target) / 2, y + 0.08, text, ha="center",
                va="bottom", fontsize=9)
    ax.annotate("時間", xy=(-0.45, bottom), xytext=(-0.45, -0.2),
                arrowprops={"arrowstyle": "->"}, ha="center")
    ax.set_xlim(-0.6, len(PARTICIPANTS) - 0.4)
    ax.set_ylim(bottom - 0.2, 1.0)
    ax.set_axis_off()
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
