"""本文で使用する図（PNG）を Pillow で生成するスクリプト.

Graphviz で描きにくい図（V 字モデル、テストピラミッド、ガントチャート、
不確実性のコーン）を生成する。このスクリプトと同じフォルダーに PNG を出力する。

実行方法: ``python make_figures.py``
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent
FONT_PATH = "C:/Windows/Fonts/meiryo.ttc"
FONT_BOLD_PATH = "C:/Windows/Fonts/meiryob.ttc"

# 配色（本文の Graphviz の図と共通）
WHITE = "#ffffff"
TEXT = "#0b0b0b"
TEXT_SUB = "#52514e"
GRID = "#dddcd8"
BLUE = "#2a78d6"
BLUE_LIGHT = "#e3eefb"
ORANGE = "#eb6834"
ORANGE_LIGHT = "#fde8df"
AQUA = "#1baf7a"
YELLOW = "#eda100"
MAGENTA = "#e87ba4"

Point = tuple[float, float]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """日本語を表示できるフォントを返す."""
    return ImageFont.truetype(FONT_BOLD_PATH if bold else FONT_PATH, size)


def center_text(
    draw: ImageDraw.ImageDraw,
    xy: Point,
    text: str,
    size: int,
    fill: str = TEXT,
    bold: bool = False,
) -> None:
    """``xy`` を中心として文字列を描く."""
    draw.text(xy, text, font=font(size, bold), fill=fill, anchor="mm")


def box(
    draw: ImageDraw.ImageDraw,
    center: Point,
    size: Point,
    text: str,
    fill: str = BLUE_LIGHT,
    outline: str = BLUE,
) -> None:
    """角の丸い四角形の中に文字列を描く."""
    cx, cy = center
    w, h = size
    draw.rounded_rectangle(
        (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
        radius=14,
        fill=fill,
        outline=outline,
        width=3,
    )
    center_text(draw, center, text, 30)


def arrow(
    draw: ImageDraw.ImageDraw,
    start: Point,
    end: Point,
    color: str = TEXT_SUB,
    width: int = 3,
    dashed: bool = False,
    head: float = 16,
) -> None:
    """``start`` から ``end`` への矢印を描く."""
    (x1, y1), (x2, y2) = start, end
    angle = math.atan2(y2 - y1, x2 - x1)
    # 矢じりの分だけ線を短くする
    lx, ly = x2 - head * math.cos(angle), y2 - head * math.sin(angle)
    if dashed:
        length = math.hypot(lx - x1, ly - y1)
        step = 14.0
        n = int(length // step)
        for i in range(0, n, 2):
            t1, t2 = i * step / length, min((i + 1) * step / length, 1.0)
            draw.line(
                (x1 + (lx - x1) * t1, y1 + (ly - y1) * t1,
                 x1 + (lx - x1) * t2, y1 + (ly - y1) * t2),
                fill=color,
                width=width,
            )
    else:
        draw.line((x1, y1, lx, ly), fill=color, width=width)
    spread = math.radians(25)
    points = [
        (x2, y2),
        (x2 - head * math.cos(angle - spread),
         y2 - head * math.sin(angle - spread)),
        (x2 - head * math.cos(angle + spread),
         y2 - head * math.sin(angle + spread)),
    ]
    draw.polygon(points, fill=color)


def v_model() -> Image.Image:
    """V 字モデルの図を描く."""
    image = Image.new("RGB", (1560, 680), WHITE)
    draw = ImageDraw.Draw(image)
    size = (230, 76)
    rows = [100, 240, 380, 520]
    left = [("要求定義", 180), ("基本設計", 310), ("詳細設計", 440),
            ("実装", 570)]
    right = [("受け入れテスト", 1380), ("システムテスト", 1250),
             ("結合テスト", 1120), ("単体テスト", 990)]

    # 開発工程とテストの対応（破線）
    # 最下段は工程の流れの矢印と重ならないよう、破線を上にずらす
    for (_, lx), (_, rx), y in zip(left, right, rows):
        dy = -18 if y == rows[-1] else 0
        arrow(draw, (rx - size[0] / 2 - 6, y + dy),
              (lx + size[0] / 2 + 6, y + dy), color=ORANGE, dashed=True)
        center_text(draw, ((lx + rx) / 2, y + dy - 22), "確認", 24, ORANGE)

    # 工程の流れ（実線）
    for (_, x1), (_, x2), y1, y2 in zip(left, left[1:], rows, rows[1:]):
        arrow(draw, (x1, y1 + size[1] / 2), (x2 - 40, y2 - size[1] / 2))
    arrow(draw, (left[-1][1] + size[0] / 2, rows[-1] + 18),
          (right[-1][1] - size[0] / 2, rows[-1] + 18))
    rev_rows = rows[::-1]
    rev_right = right[::-1]
    for (_, x1), (_, x2), y1, y2 in zip(rev_right, rev_right[1:], rev_rows,
                                        rev_rows[1:]):
        arrow(draw, (x1 + 40, y1 - size[1] / 2), (x2, y2 + size[1] / 2))

    for (name, x), y in zip(left, rows):
        box(draw, (x, y), size, name)
    for (name, x), y in zip(right, rows):
        box(draw, (x, y), size, name)

    center_text(draw, (300, 640), "開発工程（詳細化）", 28, TEXT_SUB)
    center_text(draw, (1260, 640), "テスト工程（統合）", 28, TEXT_SUB)
    return image


def test_pyramid() -> Image.Image:
    """テストピラミッドの図を描く."""
    image = Image.new("RGB", (1300, 700), WHITE)
    draw = ImageDraw.Draw(image)
    top: Point = (450, 40)
    base_y = 640
    half_width = 400
    levels = [
        ("システムテスト・受け入れテスト", "#bcd6f5"),
        ("結合テスト", "#7fb0ea"),
        ("単体テスト", BLUE),
    ]
    height = base_y - top[1]
    bands = [0.0, 0.36, 0.66, 1.0]

    def x_at(ratio: float) -> float:
        return half_width * ratio

    for (name, color), r1, r2 in zip(levels, bands, bands[1:]):
        y1 = top[1] + height * r1
        y2 = top[1] + height * r2
        polygon = [
            (top[0] - x_at(r1), y1),
            (top[0] + x_at(r1), y1),
            (top[0] + x_at(r2), y2),
            (top[0] - x_at(r2), y2),
        ]
        draw.polygon(polygon, fill=color, outline=WHITE, width=4)
        text_color = WHITE if color == BLUE else TEXT
        label_y = (y1 + y2) / 2 + (40 if r1 == 0.0 else 0)
        size = 26 if r1 == 0.0 else 32
        center_text(draw, (top[0], label_y), name, size, text_color, True)

    # 右側の説明
    ax = 960
    arrow(draw, (ax, 560), (ax, 90), color=TEXT_SUB)
    draw.text((ax + 24, 70), "実行に時間がかかる", font=font(28),
              fill=TEXT, anchor="lm")
    draw.text((ax + 24, 112), "原因の特定が難しい", font=font(28),
              fill=TEXT, anchor="lm")
    draw.text((ax + 24, 154), "→ 数を絞る", font=font(28, True),
              fill=TEXT, anchor="lm")
    draw.text((ax + 24, 540), "実行が速い", font=font(28),
              fill=TEXT, anchor="lm")
    draw.text((ax + 24, 582), "原因を特定しやすい", font=font(28),
              fill=TEXT, anchor="lm")
    draw.text((ax + 24, 624), "→ 数を多く用意する", font=font(28, True),
              fill=TEXT, anchor="lm")
    return image


def gantt_chart() -> Image.Image:
    """第 11 章の作業例のガントチャートを描く."""
    tasks = [
        ("A 要求定義", 0, 5, True),
        ("B 画面の設計と実装", 5, 15, True),
        ("C データベースの設計と構築", 5, 11, False),
        ("D 結合テスト", 15, 19, True),
    ]
    image = Image.new("RGB", (1400, 610), WHITE)
    draw = ImageDraw.Draw(image)
    x0, x1 = 460, 1340
    y0 = 70
    row_h = 90
    days = 20

    def x_of(day: float) -> float:
        return x0 + (x1 - x0) * day / days

    # 目盛り
    for day in range(0, days + 1):
        x = x_of(day)
        if day % 5 == 0:
            draw.line((x, y0 - 10, x, y0 + row_h * len(tasks)), fill=GRID,
                      width=2)
            center_text(draw, (x, y0 - 34), f"{day}", 24, TEXT_SUB)
    center_text(draw, ((x0 + x1) / 2, y0 + row_h * len(tasks) + 40),
                "経過日数", 26, TEXT_SUB)

    for i, (name, start, end, critical) in enumerate(tasks):
        cy = y0 + row_h * i + row_h / 2
        draw.text((x0 - 24, cy), name, font=font(28), fill=TEXT,
                  anchor="rm")
        color = ORANGE if critical else BLUE
        draw.rounded_rectangle(
            (x_of(start) + 2, cy - 22, x_of(end) - 2, cy + 22),
            radius=6,
            fill=color,
        )
        if not critical:
            # 余裕（フロート）を破線の枠で示す
            fx1, fx2 = x_of(end) + 2, x_of(15) - 2
            for x in range(int(fx1), int(fx2), 16):
                draw.line((x, cy - 22, min(x + 8, fx2), cy - 22),
                          fill=BLUE, width=2)
                draw.line((x, cy + 22, min(x + 8, fx2), cy + 22),
                          fill=BLUE, width=2)
            draw.line((fx2, cy - 22, fx2, cy + 22), fill=BLUE, width=2)
            center_text(draw, ((fx1 + fx2) / 2, cy), "余裕 4 日", 24,
                        TEXT_SUB)

    # 凡例
    ly = 560
    draw.rounded_rectangle((x0, ly - 14, x0 + 40, ly + 14), radius=4,
                           fill=ORANGE)
    draw.text((x0 + 52, ly), "クリティカルパス上の作業", font=font(24),
              fill=TEXT, anchor="lm")
    draw.rounded_rectangle((x0 + 420, ly - 14, x0 + 460, ly + 14),
                           radius=4, fill=BLUE)
    draw.text((x0 + 472, ly), "それ以外の作業", font=font(24), fill=TEXT,
              anchor="lm")
    return image


def cone_of_uncertainty() -> Image.Image:
    """不確実性のコーンを描く（縦軸は対数目盛り）."""
    phases = [
        "初期の構想",
        "製品定義の承認",
        "要求定義の完了",
        "UI 設計の完了",
        "詳細設計の完了",
        "完了",
    ]
    upper = [4.0, 2.0, 1.5, 1.25, 1.1, 1.0]
    lower = [0.25, 0.5, 0.67, 0.8, 0.9, 1.0]
    image = Image.new("RGB", (1400, 760), WHITE)
    draw = ImageDraw.Draw(image)
    x0, x1 = 200, 1300
    y_top, y_bottom = 50, 610

    def x_of(i: int) -> float:
        return x0 + (x1 - x0) * i / (len(phases) - 1)

    def y_of(value: float) -> float:
        ratio = (math.log2(value) + 2) / 4  # 0.25 → 0, 4 → 1
        return y_bottom - (y_bottom - y_top) * ratio

    ticks = [0.25, 0.5, 0.67, 0.8, 1.0, 1.25, 1.5, 2.0, 4.0]
    for value in ticks:
        y = y_of(value)
        draw.line((x0, y, x1, y), fill=GRID, width=2)
        draw.text((x0 - 16, y), f"{value:g} 倍", font=font(24),
                  fill=TEXT_SUB, anchor="rm")

    polygon = [(x_of(i), y_of(v)) for i, v in enumerate(upper)]
    polygon += [(x_of(i), y_of(v)) for i, v in reversed(list(
        enumerate(lower)))]
    draw.polygon(polygon, fill=BLUE_LIGHT)
    for values in (upper, lower):
        points = [(x_of(i), y_of(v)) for i, v in enumerate(values)]
        draw.line(points, fill=BLUE, width=4, joint="curve")
        for x, y in points:
            draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=BLUE,
                         outline=WHITE, width=2)
    draw.line((x0, y_of(1.0), x1, y_of(1.0)), fill=TEXT_SUB, width=2)

    for i, name in enumerate(phases):
        center_text(draw, (x_of(i), y_bottom + 40), name, 24, TEXT)
    center_text(draw, ((x0 + x1) / 2, y_bottom + 100),
                "プロジェクトの進行", 26, TEXT_SUB)
    draw.text((x0 + 30, y_of(1.6)), "見積もりの誤差の範囲",
              font=font(26), fill=TEXT, anchor="lm")
    return image


def stick_figure(draw: ImageDraw.ImageDraw, x: float, y: float,
                 name: str) -> None:
    """UML のアクター（人の形）を描く。``(x, y)`` は胴体の中心."""
    draw.ellipse((x - 22, y - 92, x + 22, y - 48), outline=TEXT, width=3)
    draw.line((x, y - 48, x, y + 10), fill=TEXT, width=3)
    draw.line((x - 38, y - 28, x + 38, y - 28), fill=TEXT, width=3)
    draw.line((x, y + 10, x - 30, y + 62), fill=TEXT, width=3)
    draw.line((x, y + 10, x + 30, y + 62), fill=TEXT, width=3)
    center_text(draw, (x, y + 92), name, 28)


def ellipse_edge(center: Point, size: Point, toward: Point) -> Point:
    """楕円の中心から ``toward`` へ向かう直線と、楕円の周の交点を返す."""
    (cx, cy), (w, h), (tx, ty) = center, size, toward
    dx, dy = tx - cx, ty - cy
    t = 1 / math.sqrt((dx / (w / 2)) ** 2 + (dy / (h / 2)) ** 2)
    return cx + dx * t, cy + dy * t


def use_case_diagram() -> Image.Image:
    """ネットショップのユースケース図を描く."""
    image = Image.new("RGB", (1400, 760), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rectangle((390, 30, 1010, 730), outline=TEXT_SUB, width=3)
    center_text(draw, (700, 70), "ネットショップ", 30, TEXT, True)

    size = (400, 88)
    cases = {
        "search": ("商品を検索する", (700.0, 160.0)),
        "order": ("商品を注文する", (700.0, 280.0)),
        "history": ("注文履歴を見る", (700.0, 400.0)),
        "register": ("商品を登録する", (700.0, 530.0)),
        "report": ("売上レポートを出力する", (700.0, 650.0)),
    }
    actors = {
        "member": ("会員", (170.0, 290.0)),
        "admin": ("管理者", (170.0, 590.0)),
        "payment": ("決済システム", (1230.0, 290.0)),
    }
    links = [
        ("member", "search"),
        ("member", "order"),
        ("member", "history"),
        ("admin", "register"),
        ("admin", "report"),
        ("payment", "order"),
    ]
    for actor, case in links:
        ax, ay = actors[actor][1]
        start = (ax + (48 if ax < 700 else -48), ay - 28)
        end = ellipse_edge(cases[case][1], size, start)
        draw.line((start, end), fill=TEXT_SUB, width=3)
    for name, (cx, cy) in cases.values():
        draw.ellipse((cx - size[0] / 2, cy - size[1] / 2,
                      cx + size[0] / 2, cy + size[1] / 2),
                     fill=BLUE_LIGHT, outline=BLUE, width=3)
        center_text(draw, (cx, cy), name, 28)
    for name, (x, y) in actors.values():
        stick_figure(draw, x, y, name)
    return image


Commit = tuple[str, float]  # (レーン名, x 座標)


def branch_diagram(
    width: int,
    lanes: list[tuple[str, str]],
    commits: dict[str, Commit],
    edges: list[tuple[str, str]],
    notes: list[tuple[str, str, int]],
) -> Image.Image:
    """ブランチとコミットの図を描く.

    ``lanes`` は (レーン名, 色) の一覧で、上から順に並べる。
    ``notes`` は (コミット名, 文字列, 上下のずれ) の一覧で、コミットの
    近くに注記を描く。
    """
    lane_gap = 100
    height = lane_gap * len(lanes) + 60
    image = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    lane_y = {name: 70 + lane_gap * i for i, (name, _) in enumerate(lanes)}
    lane_color = dict(lanes)

    for name, _ in lanes:
        draw.text((24, lane_y[name]), name, font=font(28, True),
                  fill=TEXT, anchor="lm")
        draw.line((210, lane_y[name], width - 30, lane_y[name]), fill=GRID,
                  width=2)

    def position(commit: str) -> Point:
        lane, x = commits[commit]
        return x, lane_y[lane]

    def rank(lane: str) -> int:
        """main < develop < その他のブランチの順に大きい値を返す."""
        return {"main": 0, "develop": 1}.get(lane, 2)

    # 分岐・マージの線は、より短命な側のブランチの色で描く
    for start, end in edges:
        (x1, y1), (x2, y2) = position(start), position(end)
        lane = max(commits[start][0], commits[end][0], key=rank)
        color = lane_color[lane]
        draw.line((x1, y1, x2, y2), fill=color, width=6)
    for commit in commits:
        x, y = position(commit)
        color = lane_color[commits[commit][0]]
        draw.ellipse((x - 15, y - 15, x + 15, y + 15), fill=color,
                     outline=WHITE, width=4)
    for commit, text, dy in notes:
        x, y = position(commit)
        center_text(draw, (x, y + dy), text, 22, TEXT_SUB)
    return image


def github_flow() -> Image.Image:
    """GitHub Flow の図を描く."""
    lanes = [("feature-a", ORANGE), ("main", BLUE), ("feature-b", AQUA)]
    commits: dict[str, Commit] = {
        "m0": ("main", 260),
        "m1": ("main", 720),
        "m2": ("main", 1080),
        "m3": ("main", 1240),
        "a1": ("feature-a", 380),
        "a2": ("feature-a", 500),
        "a3": ("feature-a", 600),
        "b1": ("feature-b", 420),
        "b2": ("feature-b", 640),
        "b3": ("feature-b", 900),
    }
    edges = [
        ("m0", "m1"), ("m1", "m2"), ("m2", "m3"),
        ("m0", "a1"), ("a1", "a2"), ("a2", "a3"), ("a3", "m1"),
        ("m0", "b1"), ("b1", "b2"), ("b2", "b3"), ("b3", "m2"),
    ]
    notes = [
        ("a3", "プルリクエスト・レビュー", -42),
        ("b3", "プルリクエスト・レビュー", 42),
        ("m1", "マージしてデプロイ", 42),
        ("m2", "マージしてデプロイ", -42),
    ]
    return branch_diagram(1320, lanes, commits, edges, notes)


def git_flow() -> Image.Image:
    """Git Flow の図を描く."""
    lanes = [
        ("main", BLUE),
        ("hotfix", MAGENTA),
        ("release", YELLOW),
        ("develop", ORANGE),
        ("feature", AQUA),
    ]
    commits: dict[str, Commit] = {
        "m0": ("main", 250),
        "m1": ("main", 640),
        "m2": ("main", 1180),
        "h1": ("hotfix", 520),
        "d0": ("develop", 300),
        "d1": ("develop", 460),
        "d2": ("develop", 700),
        "d3": ("develop", 900),
        "d4": ("develop", 1240),
        "f1": ("feature", 350),
        "f2": ("feature", 410),
        "f3": ("feature", 760),
        "f4": ("feature", 840),
        "r1": ("release", 980),
        "r2": ("release", 1100),
    }
    edges = [
        ("m0", "m1"), ("m1", "m2"),
        ("m0", "h1"), ("h1", "m1"), ("h1", "d2"),
        ("m0", "d0"), ("d0", "d1"), ("d1", "d2"), ("d2", "d3"),
        ("d3", "d4"),
        ("d0", "f1"), ("f1", "f2"), ("f2", "d1"),
        ("d2", "f3"), ("f3", "f4"), ("f4", "d3"),
        ("d3", "r1"), ("r1", "r2"), ("r2", "m2"), ("r2", "d4"),
    ]
    notes = [
        ("m0", "v1.0", -36),
        ("m1", "v1.0.1", -36),
        ("m2", "v1.1", -36),
        ("h1", "緊急修正", -36),
        ("r1", "リリース準備", -36),
    ]
    return branch_diagram(1320, lanes, commits, edges, notes)


def main() -> None:
    """すべての図を生成して保存する."""
    figures = {
        "v_model.png": v_model(),
        "test_pyramid.png": test_pyramid(),
        "gantt_chart.png": gantt_chart(),
        "cone_of_uncertainty.png": cone_of_uncertainty(),
        "use_case_diagram.png": use_case_diagram(),
        "github_flow.png": github_flow(),
        "git_flow.png": git_flow(),
    }
    for name, image in figures.items():
        image.save(OUT_DIR / name)
        print(f"{name} を出力した")


if __name__ == "__main__":
    main()
