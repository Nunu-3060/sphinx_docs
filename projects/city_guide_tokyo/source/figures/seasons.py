"""都内の主な花と紅葉の見ごろの目安を月単位の帯グラフで示す."""

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"]


def to_month(month: int, day: int) -> float:
    """月と日を、1 月 1 日を 1.0 とする月単位の値に変換する."""
    return month + (day - 1) / 30


# (項目, (開始月, 開始日), (終了月, 終了日), 色)
items: list[tuple[str, tuple[int, int], tuple[int, int], str]] = [
    ("椿（伊豆大島）", (1, 20), (3, 20), "#C0392B"),
    ("梅", (2, 1), (3, 10), "#E68FAC"),
    ("桜（ソメイヨシノ）", (3, 22), (4, 8), "#F4A7B9"),
    ("つつじ", (4, 10), (5, 5), "#D35D8F"),
    ("ばら（春）", (5, 10), (6, 10), "#C2185B"),
    ("花菖蒲", (6, 1), (6, 25), "#7E57C2"),
    ("あじさい", (6, 5), (7, 5), "#5C6BC0"),
    ("ハス", (7, 5), (8, 15), "#EC8FA3"),
    ("ひまわり", (7, 20), (8, 20), "#F1C40F"),
    ("コスモス", (9, 20), (10, 31), "#E091C9"),
    ("ばら（秋）", (10, 10), (11, 10), "#C2185B"),
    ("いちょうの黄葉", (11, 15), (12, 8), "#E6B800"),
    ("紅葉", (11, 10), (12, 10), "#D35400"),
]

fig, ax = plt.subplots(figsize=(9, 5))
for row, (label, (sm, sd), (em, ed), color) in enumerate(reversed(items)):
    start = to_month(sm, sd)
    end = to_month(em, ed)
    ax.barh(row, end - start, left=start, color=color, height=0.6)
ax.set_yticks(range(len(items)))
ax.set_yticklabels([label for label, _, _, _ in reversed(items)])
ax.set_xlim(1, 13)
ax.set_xticks([m + 0.5 for m in range(1, 13)])
ax.set_xticklabels([f"{m} 月" for m in range(1, 13)])
ax.set_xticks(range(1, 14), minor=True)
ax.tick_params(axis="x", which="major", length=0)
ax.grid(axis="x", which="minor", linestyle=":", alpha=0.7)
ax.set_xlabel("見ごろの目安（年や場所によって前後する）")
fig.tight_layout()
