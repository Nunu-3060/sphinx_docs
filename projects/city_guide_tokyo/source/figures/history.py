"""東京の歴史の主な出来事と、関連する名所を時代順に示す図を描く."""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"]

# (年, 出来事, 関連する名所)
events: list[tuple[int, str, str]] = [
    (1457, "太田道灌が江戸城を築く", "皇居東御苑"),
    (1590, "徳川家康が江戸に入る", "皇居東御苑・増上寺"),
    (1603, "江戸幕府が開かれ、日本橋が架けられる", "日本橋"),
    (1657, "明暦の大火で江戸城の天守が焼失する", "皇居東御苑（天守台）・回向院"),
    (1702, "柳沢吉保が六義園を完成させる", "六義園"),
    (1868, "江戸が東京と改められる", "上野恩賜公園（上野戦争の地）"),
    (1872, "新橋〜横浜間に鉄道が開業する", "東京国立博物館（同年創立）"),
    (1914, "東京駅が開業する", "東京駅丸の内駅舎"),
    (1920, "明治神宮が創建される", "明治神宮・表参道"),
    (1923, "関東大震災が起こる", "隅田川の橋（震災復興橋梁）"),
    (1943, "東京府と東京市が東京都になる", "─"),
    (1945, "東京大空襲で市街地の多くが焼失する", "谷中（戦災を免れた街並み）"),
    (1958, "東京タワーが完成する", "東京タワー"),
    (1964, "東京オリンピックが開かれる", "国立代々木競技場（原宿）"),
    (1991, "都庁が丸の内から新宿に移転する", "東京都庁展望室"),
    (2012, "東京スカイツリーが開業する", "東京スカイツリー"),
    (2018, "中央卸売市場が築地から豊洲に移転する", "豊洲市場・築地場外市場"),
]

# (時代の名前, 開始年, 終了年, 色)
eras: list[tuple[str, int, int, str]] = [
    ("室町・\n戦国", 1400, 1602, "#D9D9D9"),
    ("江戸", 1603, 1867, "#F2CF8C"),
    ("明治〜\n戦前", 1868, 1944, "#A9CCE3"),
    ("戦後〜\n現在", 1945, 2100, "#B5DDA4"),
]

fig, ax = plt.subplots(figsize=(9.5, 7.2))
n = len(events)
for row, (year, text, place) in enumerate(events):
    y = n - 1 - row
    era_color = next(color for _, start, end, color in eras if start <= year <= end)
    ax.add_patch(Rectangle((0.0, y - 0.5), 0.9, 1.0, facecolor=era_color, edgecolor="white"))
    ax.text(1.05, y, f"{year} 年", va="center", ha="left", fontsize=10, fontweight="bold")
    ax.text(2.15, y, text, va="center", ha="left", fontsize=10)
    ax.text(7.0, y, place, va="center", ha="left", fontsize=10, color="#1F4E79")
    if row % 2 == 0:
        ax.add_patch(Rectangle((1.0, y - 0.5), 9.6, 1.0, facecolor="#F5F5F5", edgecolor="none", zorder=0))

# 時代の帯に名前を書き入れる
for name, start, end, _ in eras:
    rows = [n - 1 - i for i, (year, _, _) in enumerate(events) if start <= year <= end]
    if rows:
        ax.text(0.45, (min(rows) + max(rows)) / 2, name, va="center", ha="center", fontsize=9)

ax.text(2.15, n - 0.1, "主な出来事", ha="left", va="bottom", fontsize=10, color="#555555")
ax.text(7.0, n - 0.1, "関連する名所", ha="left", va="bottom", fontsize=10, color="#555555")
ax.set_xlim(0, 10.6)
ax.set_ylim(-0.6, n + 0.4)
ax.axis("off")
fig.tight_layout()
