"""引越しの前後で行うことを時期ごとに示す横棒グラフを描く."""

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic",
                               "sans-serif"]

# (項目, 開始日, 終了日)  引越し日を 0 とした日数
items: list[tuple[str, int, int]] = [
    ("新居探し・旧居の解約連絡", -60, -30),
    ("引越し業者の見積もり・予約", -50, -30),
    ("不用品の処分・荷造り", -30, -1),
    ("転出届などの役所手続き", -14, 0),
    ("郵便の転送・ライフラインの申込み", -14, -3),
    ("搬出・搬入・明け渡し", 0, 1),
    ("転入届・マイナンバーカード", 0, 14),
    ("運転免許証・自動車・各種住所変更", 0, 30),
]

fig, ax = plt.subplots(figsize=(8, 4))
for row, (label, start, end) in enumerate(reversed(items)):
    color = "#4C78A8" if end <= 0 else "#F58518"
    ax.barh(row, end - start, left=start, color=color, height=0.6)
ax.set_yticks(range(len(items)))
ax.set_yticklabels([label for label, _, _ in reversed(items)])
ax.axvline(0, color="#D62728", linestyle="--", linewidth=1.5)
ax.text(1, len(items) - 1, "← 引越し日", color="#D62728", fontsize=10,
        va="center")
ax.set_xlim(-62, 32)
ax.set_xticks(range(-60, 31, 10))
ax.set_xlabel("引越し日からの日数（マイナスは引越し前）")
ax.grid(axis="x", linestyle=":", alpha=0.6)
fig.tight_layout()
