"""旅行の前後で行うことを時期ごとに示す横棒グラフを描く."""

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"]

# (項目, 開始日, 終了日)  出発日を 0 とした日数
items: list[tuple[str, int, int]] = [
    ("目的・行き先・時期・予算を決める", -90, -60),
    ("移動手段を予約する", -60, -14),
    ("宿泊施設を予約する", -60, -14),
    ("観光施設などを予約する", -30, -7),
    ("持ち物・留守宅を準備する", -7, -1),
    ("天気・運行情報を確認する", -3, 0),
    ("旅行（1 泊 2 日〜6 泊 7 日）", 0, 7),
    ("精算・振り返り", 7, 14),
]

fig, ax = plt.subplots(figsize=(8, 4))
for row, (label, start, end) in enumerate(reversed(items)):
    if end <= 0:
        color = "#4C78A8"
    elif start == 0:
        color = "#F58518"
    else:
        color = "#54A24B"
    ax.barh(row, end - start, left=start, color=color, height=0.6)
ax.set_yticks(range(len(items)))
ax.set_yticklabels([label for label, _, _ in reversed(items)])
ax.axvline(0, color="#D62728", linestyle="--", linewidth=1.5)
ax.text(-1, len(items) - 1, "出発日 →", color="#D62728", fontsize=10, ha="right", va="center")
ax.set_xlim(-92, 16)
ax.set_xticks(range(-90, 15, 15))
ax.set_xlabel("出発日からの日数（マイナスは出発前）")
ax.grid(axis="x", linestyle=":", alpha=0.6)
fig.tight_layout()
