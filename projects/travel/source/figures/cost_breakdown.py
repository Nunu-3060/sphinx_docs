"""2 人で 2 泊 3 日の旅行をする場合の費用の内訳の例を描く."""

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"]

# (費目, 2 人分の金額（円）)
costs: list[tuple[str, int]] = [
    ("交通費（往復）", 56000),
    ("宿泊費（2 泊）", 50000),
    ("食費（3 日）", 30000),
    ("観光・現地交通費（3 日）", 18000),
    ("予備費（10 %）", 15400),
]

labels = [label for label, _ in reversed(costs)]
values = [value for _, value in reversed(costs)]

fig, ax = plt.subplots(figsize=(8, 3.2))
bars = ax.barh(labels, values, color="#4C78A8", height=0.6)
for bar, value in zip(bars, values):
    ax.text(bar.get_width() + 800, bar.get_y() + bar.get_height() / 2, f"{value:,} 円", va="center", fontsize=10)
ax.set_xlim(0, 70000)
ax.set_xlabel("金額（円、2 人分）")
ax.xaxis.set_major_formatter(lambda x, _: f"{int(x):,}")
ax.grid(axis="x", linestyle=":", alpha=0.6)
fig.tight_layout()
