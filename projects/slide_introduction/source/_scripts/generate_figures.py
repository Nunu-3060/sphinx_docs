"""本文で使う図を source/images に生成する.

conf.py からビルドの開始時に呼び出す。単独でも実行できる。

    py generate_figures.py

スライドの見本は Pillow で描く。960 x 540 px のキャンバスを 16:9 のスライド（13.33 x 7.5 インチ）とみなすので、
1 px がちょうど 1 pt に相当する。グラフは matplotlib で描く。スライドの文章と数値はすべて架空のものである。
"""

import io
from collections.abc import Callable, Sequence
from pathlib import Path

import matplotlib
import numpy as np
import numpy.typing as npt
from PIL import Image, ImageDraw, ImageFont

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / 'images'

# スライドの大きさ（px）。1 px = 1 pt として扱う
SLIDE_W = 960
SLIDE_H = 540

# 配色（Marp のサンプルテーマ simple.css と同じ）
MAIN = (31, 78, 121)
ACCENT = (217, 72, 15)
TEXT = (31, 41, 51)
MUTED = (107, 119, 133)
LIGHT = (238, 243, 248)
LINE = (200, 209, 220)
WHITE = (255, 255, 255)
BAD = (192, 57, 43)
GOOD = (47, 133, 90)

Color = tuple[int, int, int]
FloatImage = npt.NDArray[np.float64]

FONT_CANDIDATES = [
    Path(r'C:\Windows\Fonts\NotoSansJP-VF.ttf'),
    Path(r'C:\Windows\Fonts\meiryo.ttc'),
]
MONO_FONT = Path(r'C:\Windows\Fonts\consola.ttf')
MATPLOTLIB_FONTS = ['Meiryo', 'Yu Gothic', 'sans-serif']


# ---------------------------------------------------------------------------
# 共通の部品
# ---------------------------------------------------------------------------


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """日本語を表示できるフォントを返す."""
    for path in FONT_CANDIDATES:
        if not path.exists():
            continue
        if path.name.startswith('NotoSansJP-VF'):
            loaded = ImageFont.truetype(str(path), size)
            loaded.set_variation_by_name('Bold' if bold else 'Regular')
            return loaded
        index = 2 if bold else 0  # meiryo.ttc の 0 番は標準、2 番は太字
        return ImageFont.truetype(str(path), size, index=index)
    raise FileNotFoundError('日本語フォントが見つからない')


def mono_font(size: int) -> ImageFont.FreeTypeFont:
    """コード用の等幅フォントを返す（なければ日本語フォントで代用する）."""
    if MONO_FONT.exists():
        return ImageFont.truetype(str(MONO_FONT), size)
    return font(size)


def new_slide(background: Color = WHITE) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """空のスライドを作る."""
    image = Image.new('RGB', (SLIDE_W, SLIDE_H), background)
    return image, ImageDraw.Draw(image)


def text_width(draw: ImageDraw.ImageDraw, text: str, size: int, bold: bool = False) -> float:
    return draw.textlength(text, font=font(size, bold))


def draw_title(draw: ImageDraw.ImageDraw, text: str, size: int = 30, color: Color = MAIN,
               underline: bool = True) -> None:
    """スライドのタイトルを左上に描く."""
    draw.text((48, 36), text, font=font(size, True), fill=color)
    if underline:
        y = 36 + size + 16
        draw.line((48, y, SLIDE_W - 48, y), fill=color, width=3)


def draw_bullets(draw: ImageDraw.ImageDraw, items: Sequence[str], x: int, y: int, size: int,
                 gap: float = 1.6, color: Color = TEXT) -> int:
    """箇条書きを描き、最後の行の下端の y 座標を返す."""
    for item in items:
        indent = 0
        text = item
        while text.startswith('  '):
            indent += 1
            text = text[2:]
        bx = x + indent * size * 1.5
        r = max(2, size // 7)
        cy = y + size * 0.62
        draw.ellipse((bx, cy - r, bx + 2 * r, cy + r), fill=color)
        draw.text((bx + size * 0.9, y), text, font=font(size), fill=color)
        y += int(size * gap)
    return y


def frame(image: Image.Image) -> Image.Image:
    """スライドの周りに薄い枠線を付ける（白い背景と本文の境目を見せるため）."""
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, image.width - 1, image.height - 1), outline=LINE, width=2)
    return image


def pair(before: Image.Image, after: Image.Image, labels: tuple[str, str] = ('改善前', '改善後'),
         scale: float = 0.5, colors: tuple[Color, Color] = (BAD, GOOD)) -> Image.Image:
    """2 枚のスライドを左右に並べ、上にラベルを付ける."""
    w = int(SLIDE_W * scale)
    h = int(SLIDE_H * scale)
    gap = 32
    label_h = 44
    canvas = Image.new('RGB', (w * 2 + gap * 3, h + label_h + gap), WHITE)
    draw = ImageDraw.Draw(canvas)
    for i, (slide, label) in enumerate(zip((before, after), labels)):
        x = gap + i * (w + gap)
        draw_label(draw, x, label, colors[i])
        canvas.paste(frame(slide.resize((w, h), Image.Resampling.LANCZOS)), (x, label_h))
    return canvas


def draw_label(draw: ImageDraw.ImageDraw, x: float, label: str, color: Color, y: float = 8) -> None:
    """図の上に付ける色付きのラベルを、文字の幅に合わせて描く."""
    w = text_width(draw, label, 18, True) + 32
    draw.rounded_rectangle((x, y, x + w, y + 30), radius=6, fill=color)
    draw.text((x + w / 2, y + 15), label, font=font(18, True), fill=WHITE, anchor='mm')


def box(draw: ImageDraw.ImageDraw, xy: tuple[float, float, float, float], text: str, size: int,
        fill: Color = LIGHT, outline: Color = MAIN, color: Color = TEXT, bold: bool = False,
        radius: int = 10) -> None:
    """角の丸い四角形の中央に文字を描く（改行を含んでもよい）."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=2)
    cx = (xy[0] + xy[2]) / 2
    cy = (xy[1] + xy[3]) / 2
    draw.multiline_text((cx, cy), text, font=font(size, bold), fill=color, anchor='mm', align='center',
                        spacing=6)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[float, float], end: tuple[float, float],
          color: Color = MUTED, width: int = 3) -> None:
    """矢印を描く."""
    draw.line((start, end), fill=color, width=width)
    v = np.array(end, dtype=float) - np.array(start, dtype=float)
    length = float(np.hypot(v[0], v[1]))
    if length == 0:
        return
    u = v / length
    n = np.array([-u[1], u[0]])
    tip = np.array(end, dtype=float)
    p1 = tip - u * 14 + n * 7
    p2 = tip - u * 14 - n * 7
    draw.polygon([tuple(tip), tuple(p1), tuple(p2)], fill=color)


def figure_to_image(fig: Figure, dpi: int = 100) -> Image.Image:
    """matplotlib の図を Pillow の画像に変換する."""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=dpi, facecolor='white')
    plt.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert('RGB')


def hex_color(color: Color) -> str:
    return '#{:02x}{:02x}{:02x}'.format(*color)


def setup_matplotlib() -> None:
    available = {f.name for f in font_manager.fontManager.ttflist}
    families = [name for name in MATPLOTLIB_FONTS if name in available or name == 'sans-serif']
    plt.rcParams['font.family'] = families
    plt.rcParams['axes.unicode_minus'] = False


def save(image: Image.Image, name: str) -> Path:
    path = OUT_DIR / name
    image.save(path, optimize=True)
    return path


# ---------------------------------------------------------------------------
# 2 章: 読むスライドと見るスライド
# ---------------------------------------------------------------------------


def fig_read_vs_listen() -> Image.Image:
    before, d = new_slide()
    draw_title(d, '検索性能の改善について', size=26)
    lines = [
        '現在、ログ検索の平均応答時間は約 30 秒であり、障害調査の際に',
        '多数回の検索を行う必要があることから、調査全体の所要時間の',
        '大きな部分を検索の待ち時間が占めている状況である。調査の結果、',
        '原因は検索時に日付による絞り込みを行わず、保存期間である 90 日分',
        'のデータをすべて読み込んでいることにあると判明した。そこで、日付',
        'によるパーティション分割と、利用頻度の高い検索条件（サービス名',
        'およびログレベル）に対する複合インデックスの作成を実施した。その',
        '結果、平均応答時間は約 3 秒となり、調査 1 件あたりの検索待ち時間',
        'は約 20 分から約 2 分に短縮された。なお、インデックスの追加により',
        'ストレージ使用量は 4.0 TB から 4.2 TB に増加している。',
    ]
    y = 104
    for line in lines:
        d.text((48, y), line, font=font(17), fill=TEXT)
        y += 36

    after, d = new_slide()
    draw_title(d, '検索の待ち時間は 30 秒から 3 秒になった', size=30)
    base = 470
    for i, (label, value, color) in enumerate((('対策前', 30, MUTED), ('対策後', 3, ACCENT))):
        x = 200 + i * 330
        top = base - value * 10
        d.rectangle((x, top, x + 200, base), fill=color)
        d.text((x + 100, top - 12), f'{value} 秒', font=font(34, True), fill=color, anchor='md')
        d.text((x + 100, base + 10), label, font=font(24), fill=TEXT, anchor='ma')
    d.line((150, base, 810, base), fill=MUTED, width=2)
    return pair(before, after, ('読むスライド', '見るスライド'))


# ---------------------------------------------------------------------------
# 4 章: 時間配分
# ---------------------------------------------------------------------------


def fig_time_allocation() -> Image.Image:
    talks = ['5 分の LT', '10 分の報告', '20 分の技術発表', '40 分の勉強会']
    parts = ['導入', '本論', 'まとめ', '質疑応答']
    minutes = np.array([
        [0.5, 4.0, 0.5, 0.0],
        [1.0, 5.0, 1.0, 3.0],
        [2.0, 12.0, 1.0, 5.0],
        [3.0, 24.0, 3.0, 10.0],
    ])
    colors = [hex_color(MUTED), hex_color(MAIN), hex_color(ACCENT), '#9fb3c8']
    fig, ax = plt.subplots(figsize=(8.0, 3.4))
    ratio = minutes / minutes.sum(axis=1, keepdims=True) * 100
    left = np.zeros(len(talks))
    for j, part in enumerate(parts):
        ax.barh(talks, ratio[:, j], left=left, color=colors[j], label=part, height=0.6)
        for i in range(len(talks)):
            if minutes[i, j] > 0 and ratio[i, j] >= 7:
                value = f'{minutes[i, j]:g} 分'
                ax.text(left[i] + ratio[i, j] / 2, i, value, ha='center', va='center', color='white', fontsize=10)
        left += ratio[:, j]
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel('持ち時間に占める割合（%）')
    ax.legend(ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.2), frameon=False)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    return figure_to_image(fig, dpi=110)


# ---------------------------------------------------------------------------
# 5 章: デザインの 4 原則
# ---------------------------------------------------------------------------


def fig_proximity() -> Image.Image:
    items = [('ログ基盤', '検索を 10 倍速くした'), ('CI', 'ビルドを 8 分短縮した'), ('監視', '誤報を 6 割減らした')]
    before, d = new_slide()
    draw_title(d, '今期の改善', underline=False)
    y = 110
    for name, desc in items:
        d.text((60, y), name, font=font(26, True), fill=MAIN)
        y += 56
        d.text((60, y), desc, font=font(22), fill=TEXT)
        y += 56
    after, d = new_slide()
    draw_title(d, '今期の改善', underline=False)
    y = 110
    for name, desc in items:
        d.text((60, y), name, font=font(26, True), fill=MAIN)
        d.text((60, y + 38), desc, font=font(22), fill=TEXT)
        y += 130
    return pair(before, after)


def fig_alignment() -> Image.Image:
    before, d = new_slide()
    d.text((150, 40), '移行の手順', font=font(30, True), fill=MAIN)
    for i, (x, text) in enumerate(((90, '1. 新しい API を用意する'), (210, '2. 両方に書き込む'),
                                   (130, '3. 読み込みを切り替える'), (260, '4. 古い API を止める'))):
        d.text((x, 130 + i * 80), text, font=font(24), fill=TEXT)
    d.rectangle((640, 150, 880, 380), outline=MAIN, width=2)
    d.text((700, 250), '図', font=font(24), fill=MUTED)
    after, d = new_slide()
    d.text((60, 40), '移行の手順', font=font(30, True), fill=MAIN)
    for i, text in enumerate(('1. 新しい API を用意する', '2. 両方に書き込む', '3. 読み込みを切り替える', '4. 古い API を止める')):
        d.text((60, 130 + i * 80), text, font=font(24), fill=TEXT)
    d.rectangle((600, 130, 900, 410), outline=MAIN, width=2)
    d.text((750, 270), '図', font=font(24), fill=MUTED, anchor='mm')
    return pair(before, after)


def fig_repetition() -> Image.Image:
    def slide(title: str, title_color: Color, size: int, x: int, bold: bool, underline: bool) -> Image.Image:
        image, d = new_slide()
        d.text((x, 40), title, font=font(size, bold), fill=title_color)
        if underline:
            d.line((x, 40 + size + 20, SLIDE_W - 60, 40 + size + 20), fill=title_color, width=5)
        draw_bullets(d, ['本文の 1 行目', '本文の 2 行目'], x + 10, 170, 40)
        return image

    rows = [
        ('改善前: タイトルの位置・大きさ・色がばらばら', [
            slide('背景', MAIN, 60, 60, True, True), slide('原因', BAD, 44, 260, False, False),
            slide('対策', GOOD, 72, 140, True, False)]),
        ('改善後: 同じ型をくり返す', [slide(t, MAIN, 60, 60, True, True) for t in ('背景', '原因', '対策')]),
    ]
    w, h = SLIDE_W // 3, SLIDE_H // 3
    gap = 20
    label_h = 46
    canvas = Image.new('RGB', (w * 3 + gap * 4, (h + label_h + gap) * 2), WHITE)
    d = ImageDraw.Draw(canvas)
    for r, (label, slides) in enumerate(rows):
        y = r * (h + label_h + gap)
        draw_label(d, gap, label, BAD if r == 0 else GOOD, y=y + 8)
        for c, s in enumerate(slides):
            canvas.paste(frame(s.resize((w, h), Image.Resampling.LANCZOS)), (gap + c * (w + gap), y + label_h))
    return canvas


def fig_contrast() -> Image.Image:
    before, d = new_slide()
    d.text((60, 40), '結果', font=font(30), fill=(120, 130, 140))
    d.text((60, 130), '平均応答時間は 30 秒から 3 秒になった', font=font(26), fill=(150, 160, 170))
    d.text((60, 190), 'ストレージ使用量は 4.0 TB から 4.2 TB に増えた', font=font(26), fill=(150, 160, 170))
    d.text((60, 250), '調査 1 件の検索待ちは 20 分から 2 分になった', font=font(26), fill=(150, 160, 170))
    after, d = new_slide()
    d.text((60, 40), '結果', font=font(30, True), fill=MAIN)
    d.text((60, 130), '平均応答時間は 30 秒から 3 秒になった', font=font(30, True), fill=ACCENT)
    d.text((60, 210), 'ストレージ使用量は 4.0 TB から 4.2 TB に増えた', font=font(22), fill=TEXT)
    d.text((60, 260), '調査 1 件の検索待ちは 20 分から 2 分になった', font=font(22), fill=TEXT)
    return pair(before, after)


def fig_eye_flow() -> Image.Image:
    z, d = new_slide()
    d.text((60, 40), 'タイトル', font=font(30, True), fill=MAIN)
    d.rectangle((60, 120, 440, 470), outline=LINE, width=2)
    d.text((250, 295), '図・グラフ', font=font(24), fill=MUTED, anchor='mm')
    draw_bullets(d, ['要点 1', '要点 2', '要点 3'], 520, 150, 24, gap=2.2)
    points = [(80, 95), (880, 95), (120, 480), (880, 480)]
    for a, b in zip(points, points[1:]):
        arrow(d, a, b, color=ACCENT, width=5)
    f, d = new_slide()
    d.text((60, 40), 'タイトル', font=font(30, True), fill=MAIN)
    y = 130
    for _ in range(5):
        d.text((60, y), '見出し', font=font(22, True), fill=TEXT)
        d.line((170, y + 14, 860, y + 14), fill=LINE, width=8)
        y += 72
    arrow(d, (60, 100), (880, 100), color=ACCENT, width=5)
    arrow(d, (60, 188), (600, 188), color=ACCENT, width=5)
    arrow(d, (40, 100), (40, 490), color=ACCENT, width=5)
    return pair(z, f, ('Z 型', 'F 型'), colors=(MAIN, MAIN))


def fig_font_size() -> Image.Image:
    slide, d = new_slide()
    d.text((48, 24), '文字の大きさと見え方', font=font(32, True), fill=MAIN)
    y = 92
    for size in (12, 16, 18, 24, 32, 40):
        d.text((48, y), f'{size} pt: 検索は 3 秒で終わる', font=font(size), fill=TEXT)
        y += int(size * 1.55) + 12
    full = frame(slide.copy())
    far = frame(slide.resize((SLIDE_W // 5, SLIDE_H // 5), Image.Resampling.LANCZOS))
    far = far.resize((SLIDE_W // 2, SLIDE_H // 2), Image.Resampling.BILINEAR)
    near = full.resize((SLIDE_W // 2, SLIDE_H // 2), Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', (SLIDE_W + 96, SLIDE_H // 2 + 60), WHITE)
    draw = ImageDraw.Draw(canvas)
    canvas.paste(near, (32, 50))
    canvas.paste(far, (SLIDE_W // 2 + 64, 50))
    draw.text((32, 12), '手元の画面で見たとき', font=font(18, True), fill=TEXT)
    draw.text((SLIDE_W // 2 + 64, 12), '会場の後方から見たとき（解像度を落として再現）', font=font(18, True), fill=TEXT)
    return canvas


# ---------------------------------------------------------------------------
# 5 章: 色
# ---------------------------------------------------------------------------


def relative_luminance(color: Color) -> float:
    """WCAG 2 の相対輝度."""
    channels = np.array(color, dtype=float) / 255
    linear = np.where(channels <= 0.04045, channels / 12.92, ((channels + 0.055) / 1.055) ** 2.4)
    return float(0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2])


def contrast_ratio(a: Color, b: Color) -> float:
    la, lb = sorted((relative_luminance(a), relative_luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def fig_color_palette() -> Image.Image:
    canvas = Image.new('RGB', (980, 470), WHITE)
    d = ImageDraw.Draw(canvas)
    d.text((24, 16), '配色の例（面積の比率）', font=font(22, True), fill=TEXT)
    x = 24
    for name, color, share, fg in (('ベースカラー', (246, 248, 250), 70, TEXT), ('メインカラー', MAIN, 25, WHITE),
                                   ('アクセントカラー', ACCENT, 5, WHITE)):
        w = int(9.3 * share)
        d.rectangle((x, 60, x + w, 160), fill=color, outline=LINE)
        if share >= 25:
            d.text((x + 12, 72), name, font=font(18, True), fill=fg)
            d.text((x + 12, 104), f'{share} %  {hex_color(color)}', font=font(16), fill=fg)
        else:
            d.text((x + w + 4, 168), f'{name}\n{share} %  {hex_color(color)}', font=font(16), fill=TEXT, anchor='ra')
        x += w
    d.text((24, 230), '文字と背景のコントラスト比', font=font(22, True), fill=TEXT)
    samples = [((150, 160, 170), WHITE), (MUTED, WHITE), (TEXT, WHITE), (WHITE, MAIN), (WHITE, ACCENT), (MAIN, LIGHT)]
    for i, (fg, bg) in enumerate(samples):
        col = i % 3
        row = i // 3
        x0 = 24 + col * 318
        y0 = 274 + row * 96
        d.rectangle((x0, y0, x0 + 300, y0 + 80), fill=bg, outline=LINE)
        d.text((x0 + 16, y0 + 10), '本文の文字', font=font(24, True), fill=fg)
        ratio = contrast_ratio(fg, bg)
        mark = '○' if ratio >= 4.5 else '×'
        d.text((x0 + 16, y0 + 48), f'{ratio:.1f} : 1  {mark}', font=font(16), fill=fg)
    return canvas


# Machado ら（2009）の色覚シミュレーション行列（重さ 1.0）。線形 RGB に掛ける
CVD_MATRICES = {
    '1 型色覚（P 型）のシミュレーション': np.array([
        [0.152286, 1.052583, -0.204868],
        [0.114503, 0.786281, 0.099216],
        [-0.003882, -0.048116, 1.051998],
    ]),
    '2 型色覚（D 型）のシミュレーション': np.array([
        [0.367322, 0.860646, -0.227968],
        [0.280085, 0.672501, 0.047413],
        [-0.011820, 0.042940, 0.968881],
    ]),
}


def simulate_cvd(image: Image.Image, matrix: FloatImage) -> Image.Image:
    srgb = np.asarray(image, dtype=float) / 255
    linear = np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)
    converted = np.clip(linear @ matrix.T, 0, 1)
    back = np.where(converted <= 0.0031308, converted * 12.92, 1.055 * converted ** (1 / 2.4) - 0.055)
    return Image.fromarray((back * 255).round().astype(np.uint8))


def cvd_chart(improved: bool) -> Image.Image:
    months = np.arange(1, 13)
    rng = np.random.default_rng(3)
    plan = 40 + months * 5.0
    actual = plan + rng.normal(0, 4, len(months)) - np.where(months > 7, (months - 7) * 6.0, 0)
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    if improved:
        ax.plot(months, plan, color='#0072b2', linewidth=2.5, linestyle='--')
        ax.plot(months, actual, color='#e69f00', linewidth=3, marker='o')
        ax.text(12.2, plan[-1], '計画', color='#0072b2', va='center', fontsize=12, fontweight='bold')
        ax.text(12.2, actual[-1], '実績', color='#b07800', va='center', fontsize=12, fontweight='bold')
        ax.set_xlim(0.5, 13.6)
    else:
        ax.plot(months, plan, color='#2ca02c', linewidth=2)
        ax.plot(months, actual, color='#d62728', linewidth=2)
        ax.legend(['計画', '実績'], loc='upper left', fontsize=10)
        ax.set_xlim(0.5, 12.5)
    ax.set_title('月別の処理件数（千件）', fontsize=12)
    ax.set_xticks([1, 4, 7, 10])
    ax.set_xticklabels(['1 月', '4 月', '7 月', '10 月'])
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    return figure_to_image(fig, dpi=100)


def fig_color_vision() -> Image.Image:
    rows = [('改善前: 赤と緑で区別', cvd_chart(False)), ('改善後: 青と橙、線種、直接ラベル', cvd_chart(True))]
    columns = ['一般色覚', *CVD_MATRICES]
    w, h = rows[0][1].size
    label_w = 0
    head_h = 40
    row_label_h = 34
    canvas = Image.new('RGB', (w * 3 + 40 + label_w, (h + row_label_h) * 2 + head_h + 10), WHITE)
    d = ImageDraw.Draw(canvas)
    for c, name in enumerate(columns):
        d.text((label_w + c * (w + 20) + w // 2, 12), name, font=font(16, True), fill=TEXT, anchor='ma')
    for r, (label, chart) in enumerate(rows):
        y = head_h + r * (h + row_label_h)
        d.text((8, y + 4), label, font=font(17, True), fill=BAD if r == 0 else GOOD)
        for c, name in enumerate(columns):
            image = chart if c == 0 else simulate_cvd(chart, CVD_MATRICES[name])
            canvas.paste(image, (label_w + c * (w + 20), y + row_label_h))
    return canvas


# ---------------------------------------------------------------------------
# 6 章: 図表
# ---------------------------------------------------------------------------


def fig_bullets_to_diagram() -> Image.Image:
    before, d = new_slide()
    draw_title(d, 'リリースの流れ')
    draw_bullets(d, [
        '開発者がプルリクエストを作る',
        'CI が自動テストを実行する',
        '  テストに失敗したら開発者が修正する',
        'レビュアーが承認する',
        'main にマージするとステージングに配備される',
        '受け入れ確認のあと本番に配備する',
    ], 60, 120, 22, gap=1.75)
    after, d = new_slide()
    draw_title(d, 'テストに通らない変更は本番に届かない')
    steps = ['PR 作成', '自動テスト', 'レビュー', 'ステージング', '本番']
    xs = [40 + i * 180 for i in range(5)]
    for i, (x, name) in enumerate(zip(xs, steps)):
        fill = ACCENT if name == '自動テスト' else LIGHT
        color = WHITE if name == '自動テスト' else TEXT
        box(d, (x, 230, x + 150, 310), name, 22, fill=fill, color=color, bold=True)
        if i < 4:
            arrow(d, (x + 150, 270), (x + 180, 270))
    arrow(d, (295, 310), (295, 400), color=BAD)
    arrow(d, (295, 400), (115, 400), color=BAD)
    arrow(d, (115, 400), (115, 312), color=BAD)
    d.text((205, 410), '失敗したら修正', font=font(20), fill=BAD, anchor='ma')
    return pair(before, after)


def fig_diagram_patterns() -> Image.Image:
    cell_w, cell_h = 300, 230
    canvas = Image.new('RGB', (cell_w * 3, cell_h * 2), WHITE)
    d = ImageDraw.Draw(canvas)

    def title(col: int, row: int, text: str, note: str) -> tuple[int, int]:
        x0, y0 = col * cell_w, row * cell_h
        d.text((x0 + 16, y0 + 8), text, font=font(20, True), fill=MAIN)
        d.text((x0 + 16, y0 + 36), note, font=font(14), fill=MUTED)
        return x0, y0

    x, y = title(0, 0, 'フロー', '順序・手順・処理の流れ')
    for i in range(3):
        box(d, (x + 16 + i * 92, y + 110, x + 86 + i * 92, y + 160), f'手順 {i + 1}', 15)
        if i < 2:
            arrow(d, (x + 86 + i * 92, y + 135), (x + 108 + i * 92, y + 135), width=2)

    x, y = title(1, 0, '比較', '2 つ以上の選択肢を並べる')
    box(d, (x + 20, y + 70, x + 140, y + 210), 'A 案\n\n速い\n高い', 16)
    box(d, (x + 160, y + 70, x + 280, y + 210), 'B 案\n\n遅い\n安い', 16)

    x, y = title(2, 0, '階層', '全体と部分・ツリー構造')
    box(d, (x + 110, y + 70, x + 190, y + 110), '全体', 15)
    for i in range(3):
        bx = x + 20 + i * 95
        box(d, (bx, y + 160, bx + 75, y + 200), f'部分 {i + 1}', 14)
        d.line((x + 150, y + 110, bx + 37, y + 160), fill=MUTED, width=2)

    x, y = title(0, 1, 'マトリクス', '2 つの軸で分類する')
    gx, gy = x + 70, y + 70
    for i in range(2):
        for j in range(2):
            fill = ACCENT if (i, j) == (1, 1) else LIGHT  # 費用が低く効果が高い
            d.rectangle((gx + i * 90, gy + j * 65, gx + i * 90 + 86, gy + j * 65 + 61), fill=fill, outline=MAIN)
    d.text((gx + 90, gy + 136), '効果 →', font=font(13), fill=MUTED, anchor='ma')
    d.text((gx - 8, gy + 65), '↑\n費\n用', font=font(13), fill=MUTED, anchor='rm')

    x, y = title(1, 1, 'サイクル', '繰り返す流れ')
    cx, cy, r = x + 150, y + 140, 58
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=MUTED, width=2)
    for k, name in enumerate(('計画', '実行', '評価', '改善')):
        angle = -np.pi / 2 + k * np.pi / 2
        px, py = cx + r * np.cos(angle), cy + r * np.sin(angle)
        box(d, (px - 32, py - 18, px + 32, py + 18), name, 14)

    x, y = title(2, 1, '構成要素', '要素の関係・システム構成')
    box(d, (x + 20, y + 120, x + 100, y + 165), '利用者', 14)
    box(d, (x + 120, y + 120, x + 190, y + 165), 'API', 14)
    box(d, (x + 210, y + 80, x + 285, y + 120), 'DB', 14)
    box(d, (x + 210, y + 165, x + 285, y + 205), 'キュー', 14)
    arrow(d, (x + 100, y + 142), (x + 120, y + 142), width=2)
    arrow(d, (x + 190, y + 135), (x + 210, y + 105), width=2)
    arrow(d, (x + 190, y + 150), (x + 210, y + 180), width=2)
    for i in range(1, 3):
        d.line((i * cell_w, 0, i * cell_w, cell_h * 2), fill=LINE, width=1)
    d.line((0, cell_h, cell_w * 3, cell_h), fill=LINE, width=1)
    return canvas


def fig_chart_before_after() -> Image.Image:
    teams = ['A', 'B', 'C', 'D', 'E', 'F']
    values = np.array([12, 15, 11, 31, 14, 13])
    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    colors = plt.get_cmap('tab10')(np.arange(len(teams)))
    ax.bar(teams, values, color=colors)
    ax.grid(True, linestyle='-', color='#999999')
    ax.set_title('チーム別の障害件数')
    ax.legend(handles=[Rectangle((0, 0), 1, 1, color=c) for c in colors], labels=teams, fontsize=7, ncol=2)
    ax.set_ylabel('件数')
    before = figure_to_image(fig)

    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    colors_after = [hex_color(ACCENT) if t == 'D' else '#c8d1dc' for t in teams]
    bars = ax.bar(teams, values, color=colors_after)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.6, str(value), ha='center', fontsize=10,
                color=hex_color(ACCENT) if value == values.max() else '#6b7785')
    ax.set_title('D チームの障害は他チームの約 2 倍', loc='left', fontsize=12, fontweight='bold', color=hex_color(MAIN))
    ax.set_yticks([])
    for side in ('top', 'right', 'left'):
        ax.spines[side].set_visible(False)
    ax.set_xticks(range(len(teams)))
    ax.set_xticklabels([f'{t} チーム' for t in teams], fontsize=9)
    fig.tight_layout()
    after = figure_to_image(fig)
    return side_by_side(before, after)


def side_by_side(before: Image.Image, after: Image.Image, labels: tuple[str, str] = ('改善前', '改善後')
                 ) -> Image.Image:
    """matplotlib の図 2 枚を左右に並べる."""
    gap = 24
    label_h = 44
    w = before.width + after.width + gap * 3
    h = max(before.height, after.height) + label_h
    canvas = Image.new('RGB', (w, h), WHITE)
    d = ImageDraw.Draw(canvas)
    x = gap
    for i, (image, label) in enumerate(zip((before, after), labels)):
        draw_label(d, x, label, BAD if i == 0 else GOOD)
        canvas.paste(image, (x, label_h))
        x += image.width + gap
    return canvas


def fig_pie_vs_bar() -> Image.Image:
    labels = ['Web', 'iOS', 'Android', 'API', 'バッチ', 'その他']
    values = np.array([24, 19, 18, 17, 14, 8])
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    ax.pie(values, labels=labels, startangle=90, counterclock=False, textprops={'fontsize': 9})
    ax.set_title('問い合わせの内訳', fontsize=11)
    before = figure_to_image(fig)
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    order = np.argsort(values)
    ax.barh(np.array(labels)[order], values[order], color=hex_color(MAIN))
    for i, value in enumerate(values[order]):
        ax.text(value + 0.4, i, f'{value} %', va='center', fontsize=9)
    ax.set_title('問い合わせの内訳（%）', fontsize=11, loc='left')
    ax.set_xticks([])
    for side in ('top', 'right', 'bottom'):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    after = figure_to_image(fig)
    return side_by_side(before, after, ('円グラフ', '棒グラフ'))


def fig_code_slide() -> Image.Image:
    code_before = [
        'import json', 'import logging', 'from pathlib import Path', '', 'logger = logging.getLogger(__name__)', '',
        '', 'def load_config(path: Path) -> dict:', '    if not path.exists():',
        '        logger.warning("config not found: %s", path)', '        return {}',
        '    with path.open(encoding="utf-8") as f:', '        data = json.load(f)',
        '    for key in ("host", "port", "user"):', '        if key not in data:',
        '            raise KeyError(key)', '    data["port"] = int(data["port"])', '    return data',
    ]
    before, d = new_slide()
    draw_title(d, 'コード', size=24, underline=False)
    d.rectangle((40, 80, 920, 520), fill=(246, 248, 250))
    mono = mono_font(15)
    for i, line in enumerate(code_before):
        d.text((56, 90 + i * 23), line, font=mono, fill=TEXT)

    after, d = new_slide()
    draw_title(d, '必須の項目がなければ、起動時に止める', size=28)
    code_after = [
        'for key in ("host", "port", "user"):',
        '    if key not in data:',
        '        raise KeyError(key)',
    ]
    mono_big = mono_font(30)
    d.rectangle((48, 150, 912, 360), fill=(246, 248, 250))
    d.rectangle((48, 262, 912, 312), fill=(255, 236, 222))
    for i, line in enumerate(code_after):
        d.text((72, 170 + i * 48), line, font=mono_big, fill=TEXT)
    d.text((48, 400), '設定ミスに、本番で初めて気付くことを防ぐ', font=font(24), fill=TEXT)
    return pair(before, after)


# ---------------------------------------------------------------------------
# 12 章: アンチパターン
# ---------------------------------------------------------------------------


def fig_antipattern() -> Image.Image:
    before, d = new_slide((255, 252, 230))
    d.rectangle((0, 0, SLIDE_W, 70), fill=(0, 102, 51))
    d.text((24, 14), '★☆ 第 3 四半期 システム運用状況のご報告 ☆★', font=font(28, True), fill=(255, 255, 0))
    draw_bullets(d, [
        '稼働率は 99.95 % で目標（99.9 %）を達成',
        '障害は 4 件発生（うち重大 1 件）',
        '  重大障害は 8 月 12 日、DB のディスク逼迫',
        '問い合わせ件数は前期比 12 % 減少',
        '来期は監視項目の見直しとログ基盤の刷新を予定',
        '予算の追加（約 300 万円）について承認をお願いしたい',
    ], 30, 100, 21, gap=1.7, color=(60, 60, 160))
    for i, (cx, cy, color) in enumerate(((820, 420, (255, 0, 0)), (880, 470, (0, 0, 255)), (760, 470, (255, 165, 0)))):
        d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=color)
    d.text((600, 300), '重要！', font=font(36, True), fill=(255, 0, 0))

    after, d = new_slide()
    draw_title(d, '監視を見直すため、300 万円の追加予算を承認してほしい', size=26)
    box(d, (48, 130, 450, 300), '稼働率 99.95 %\n目標を達成', 26, bold=True)
    box(d, (510, 130, 912, 300), '重大障害 1 件\nディスク逼迫を\n検知できなかった', 24, fill=(255, 236, 222),
        outline=ACCENT, bold=True)
    d.text((48, 340), '来期の対応', font=font(24, True), fill=MAIN)
    draw_bullets(d, ['ディスク使用量などの監視項目を追加する', 'ログ基盤を刷新し、調査の時間を短くする'], 60, 385, 22)
    return pair(before, after)


# ---------------------------------------------------------------------------


FIGURES: dict[str, Callable[[], Image.Image]] = {
    'ch02_read_vs_listen.png': fig_read_vs_listen,
    'ch04_time_allocation.png': fig_time_allocation,
    'ch05_proximity.png': fig_proximity,
    'ch05_alignment.png': fig_alignment,
    'ch05_repetition.png': fig_repetition,
    'ch05_contrast.png': fig_contrast,
    'ch05_eye_flow.png': fig_eye_flow,
    'ch05_font_size.png': fig_font_size,
    'ch05_color_palette.png': fig_color_palette,
    'ch05_color_vision.png': fig_color_vision,
    'ch06_bullets_to_diagram.png': fig_bullets_to_diagram,
    'ch06_diagram_patterns.png': fig_diagram_patterns,
    'ch06_chart_before_after.png': fig_chart_before_after,
    'ch06_pie_vs_bar.png': fig_pie_vs_bar,
    'ch06_code_slide.png': fig_code_slide,
    'ch12_antipattern.png': fig_antipattern,
}


def main() -> list[Path]:
    """すべての図を生成し、出力したファイルのパスを返す."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    setup_matplotlib()
    paths = [save(make(), name) for name, make in FIGURES.items()]
    print(f'generated: {len(paths)} figures')
    return paths


if __name__ == '__main__':
    main()
