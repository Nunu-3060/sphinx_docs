"""COSMO RUSH のリソースファイル (cosmo_rush.pyxres) を生成するスクリプト。

本書の題材ゲームで使うドット絵・タイルマップ・効果音・BGM をコードで定義し、
リソースファイルとして保存する。生成したファイルは Pyxel Editor で開いて編集できる。

使い方:
    python make_assets.py

保存先:
    examples/assets/cosmo_rush.pyxres
    examples/cosmo_rush/cosmo_rush.pyxres (完成版ゲーム用のコピー)
"""

import random
from pathlib import Path

import pyxel

HERE = Path(__file__).resolve().parent
OUTPUT_FILES = [
    HERE / "cosmo_rush.pyxres",
    HERE.parent / "cosmo_rush" / "cosmo_rush.pyxres",
]

# ---------------------------------------------------------------------------
# ドット絵の定義
#
# 1 文字が 1 ピクセルで、0-9 と a-f がパレットのカラー番号を表す。
# "." は 0 (黒 = 透明色) と同じ意味で、読みやすさのために使っている。
# 左右対称の絵は左半分だけを書き、mirror() で右半分を補う。
# ---------------------------------------------------------------------------

PLAYER_BODY = [
    ".......7",
    ".......7",
    "......7c",
    "......7c",
    ".....76c",
    ".....766",
    "..d..766",
    "..d.7665",
    "..d76655",
    ".d766655",
    ".d766666",
    "d7766666",
    "d776dd66",
    "d.7..d66",
]
PLAYER_FLAMES = [
    [".....a9.", "......8."],
    [".....9a.", ".....8.."],
]

ENEMY_A_BODY = [
    "...28899",
    "..88999a",
    ".889997a",
    ".889999a",
    "..88999a",
    "...28899",
]
ENEMY_A_LEGS = [
    ([".2......", ".22.....", "..22.888"], ["..22.888", ".22.....", ".2......"]),
    (["2.......", ".22.....", "...2.888"], ["...2.888", ".22.....", "2......."]),
]

ENEMY_B_FRAMES = [
    [
        "........",
        "........",
        "........",
        "......55",
        ".....5c7",
        ".....ccc",
        "...33333",
        "..3bbbbb",
        ".3bbbbbb",
        "33333333",
        ".3.a..3.",
        "...33333",
        "........",
        "........",
        "........",
        "........",
    ],
    [
        "........",
        "........",
        "........",
        "......55",
        ".....5c7",
        ".....ccc",
        "...33333",
        "..3bbbbb",
        ".3bbbbbb",
        "33333333",
        ".3...a3.",
        "...33333",
        "........",
        "........",
        "........",
        "........",
    ],
]

ENEMY_C_FRAMES = [
    [
        "........",
        ".2......",
        ".2e.....",
        ".2ee....",
        ".2eee222",
        ".2ee2eee",
        ".22e2eee",
        "..2e2e88",
        "..2e2e87",
        "..22ee88",
        "...22eee",
        "....2222",
        ".....2.2",
        ".....8.8",
        "........",
        "........",
    ],
    [
        "........",
        ".2......",
        ".2e.....",
        ".2ee....",
        ".2eee222",
        ".2ee2eee",
        ".22e2eee",
        "..2e2e88",
        "..2e2e8a",
        "..22ee88",
        "...22eee",
        "....2222",
        ".....2.2",
        "......9.",
        "........",
        "........",
    ],
]

BOSS_FRAMES = [
    [
        "................",
        "................",
        "..........dddddd",
        "........dd666666",
        "......dd66555555",
        ".....d6655222222",
        "....d66522eeeeee",
        "...d6652eeee2222",
        "..d6652eee222222",
        "..d652eee2255555",
        ".d6652ee25588888",
        ".d652ee255899999",
        "d6652ee258899aaa",
        "d652ee2258999a77",
        "d652ee2258999a77",
        "d652ee2258899aaa",
        "d6652ee255899999",
        ".d652eee25588888",
        ".d6652eee2255555",
        "..d6652eee222222",
        "..d66d52eeee2222",
        "...dd.d652eeeeee",
        "......d6652eee22",
        ".....d66.d6522e2",
        "....d66...d652e2",
        "...d66.....d652e",
        "...d6.......d652",
        "...d6........d6d",
        "...88.........d.",
        "...9...........8",
        "...............9",
        "................",
    ],
]


def mirror(rows: list[str]) -> list[str]:
    """左半分のドット絵を左右反転して連結し、左右対称の絵にする。"""
    return [row + row[::-1] for row in rows]


def to_hex(rows: list[str]) -> list[str]:
    """"." を "0" に置き換えて Image.set() に渡せる形式にする。"""
    return [row.replace(".", "0") for row in rows]


def boss_blink_frame(rows: list[str]) -> list[str]:
    """ボスのコア (中心の白と黄色) の色を入れ替えて点滅用のコマを作る。"""
    table = str.maketrans({"7": "8", "a": "9", "9": "a"})
    return [row.translate(table) for row in rows]


def put(x: int, y: int, rows: list[str]) -> None:
    """イメージバンク 0 の (x, y) にドット絵を書き込む。"""
    pyxel.images[0].set(x, y, to_hex(rows))


def make_sprites() -> None:
    """キャラクターのスプライトをイメージバンク 0 に書き込む。"""
    img = pyxel.images[0]
    img.cls(0)

    # (0, 0) から 16x16 は空けておく (タイルマップの初期タイル (0, 0) を空白にするため)

    # 自機 (16x16, 2 コマ): (16, 0), (32, 0)
    for i, flame in enumerate(PLAYER_FLAMES):
        put(16 + i * 16, 0, mirror(PLAYER_BODY + flame))

    # 自機の弾 (8x8): (48, 0)
    put(48, 0, ["...cc...", "..c77c..", "..c77c..", "..c77c..", "...cc...", "...66...", "...55...", "........"])

    # 敵の弾 (8x8): (56, 0)
    img.circ(59, 3, 2, 8)
    img.circ(59, 3, 1, 14)
    img.pset(59, 3, 7)

    # 敵 A (16x16, 2 コマ): (0, 16), (16, 16)
    for i, (top, bottom) in enumerate(ENEMY_A_LEGS):
        rows = ["........"] * 2 + top + ENEMY_A_BODY + bottom + ["........"] * 2
        put(i * 16, 16, mirror(rows[:16]))

    # 敵 B (16x16, 2 コマ): (32, 16), (48, 16)
    for i, rows in enumerate(ENEMY_B_FRAMES):
        put(32 + i * 16, 16, mirror(rows))

    # 敵 C (16x16, 2 コマ): (64, 16), (80, 16)
    for i, rows in enumerate(ENEMY_C_FRAMES):
        put(64 + i * 16, 16, mirror(rows))

    # ボス (32x32, 2 コマ): (0, 32), (32, 32)
    put(0, 32, mirror(BOSS_FRAMES[0]))
    put(32, 32, mirror(boss_blink_frame(BOSS_FRAMES[0])))

    # 爆発 (16x16, 4 コマ): (0, 64), (16, 64), (32, 64), (48, 64)
    explosion = [
        [(5, 7), (3, 10), (1, 7)],
        [(7, 9), (5, 10), (3, 7)],
        [(7, 8), (6, 9), (4, 13)],
        [(7, 13), (6, 5), (5, 0)],
    ]
    for i, circles in enumerate(explosion):
        cx = i * 16 + 8
        for r, col in circles:
            img.circ(cx, 72, r, col)


def make_tiles() -> None:
    """背景用のタイル (8x8) をイメージバンク 0 の y = 128 以降に書き込む。"""
    img = pyxel.images[0]
    # (0, 0) 何もない宇宙 (イメージバンクの左上 8x8 は空けてある)
    # (1, 16) 暗い星、(2, 16) 星、(3, 16) 明るい星
    img.pset(8 + 3, 132, 5)
    img.pset(16 + 5, 130, 6)
    img.pset(24 + 3, 131, 6)
    img.pset(24 + 3, 133, 6)
    img.pset(24 + 2, 132, 6)
    img.pset(24 + 4, 132, 6)
    img.pset(24 + 3, 132, 7)
    # (4, 16) 薄い星雲、(5, 16) 濃い星雲
    for y in range(8):
        for x in range(8):
            if (x + y) % 2 == 0 and y % 2 == 0:
                img.pset(32 + x, 128 + y, 1)
            if (x + y) % 2 == 0:
                img.pset(40 + x, 128 + y, 1)

    # (0, 17) から 4x4 タイル (32x32): 惑星
    img.circ(16, 152, 13, 2)
    img.circ(13, 149, 10, 14)
    img.circ(15, 151, 10, 2)
    img.circ(20, 158, 2, 1)
    img.circ(9, 156, 1, 1)
    img.circ(19, 146, 1, 1)
    # (4, 17) から 2x2 タイル (16x16): 小惑星
    img.elli(34, 139, 12, 10, 4)
    img.elli(35, 140, 7, 5, 9)
    img.pset(41, 145, 13)
    img.pset(38, 146, 13)


def make_tilemap() -> None:
    """タイルマップ 0 (16x64 タイル = 128x512 ピクセル) に背景を並べる。"""
    tm = pyxel.tilemaps[0]
    tm.imgsrc = 0
    tm.cls((0, 0))
    rng = random.Random(3060)
    for ty in range(64):
        for tx in range(16):
            r = rng.random()
            if r < 0.04:
                tm.pset(tx, ty, (3, 16))
            elif r < 0.12:
                tm.pset(tx, ty, (2, 16))
            elif r < 0.25:
                tm.pset(tx, ty, (1, 16))
    # 星雲の帯
    for ty in range(20, 30):
        width = 6 - abs(ty - 25)
        for tx in range(max(0, 9 - width), min(16, 9 + width)):
            tm.pset(tx, ty, (5, 16) if abs(tx - 9) < width - 2 else (4, 16))
    # 惑星 (4x4 タイル) と小惑星 (2x2 タイル)
    for tx, ty in [(1, 4)]:
        for dy in range(4):
            for dx in range(4):
                tm.pset(tx + dx, ty + dy, (dx, 17 + dy))
    for tx, ty in [(12, 14), (3, 40), (10, 52)]:
        for dy in range(2):
            for dx in range(2):
                tm.pset(tx + dx, ty + dy, (4 + dx, 17 + dy))


def make_logo() -> None:
    """タイトルロゴをイメージバンク 1 の (0, 0) に書き込む。

    標準フォントで書いた文字を 3 倍に拡大し、縁取りとグラデーションを付ける。
    """
    title = "COSMO RUSH"
    src = pyxel.Image(len(title) * 4, 6)
    src.cls(0)
    src.text(0, 0, title, 7)
    scale = 3
    dst = pyxel.images[1]
    dst.cls(0)
    gradient = [10, 10, 9, 9, 8, 8]
    for pass_no in range(2):
        for y in range(src.height):
            for x in range(src.width):
                if src.pget(x, y) == 0:
                    continue
                px = 2 + x * scale
                py = 2 + y * scale
                if pass_no == 0:
                    dst.rect(px - 2, py - 2, scale + 4, scale + 4, 1)
                else:
                    dst.rect(px, py, scale, scale, gradient[y])


def make_sounds() -> None:
    """効果音と BGM の素材となるサウンドを定義する。"""
    snd = pyxel.sounds
    # 効果音 (チャンネル 3 で鳴らす)
    snd[0].set("a3d3", "p", "54", "nf", 3)  # 自機の弾
    snd[1].set("c2a1f1d1c1", "n", "76543", "nnnnf", 6)  # 敵の爆発
    snd[2].set("c3g2c2g1c1g0c0", "n", "7776543", "nnnnnnf", 9)  # 自機の被弾
    snd[3].set("c3e3g3c4", "s", "6", "nnnf", 5)  # 決定
    snd[4].set("a2ra2ra2r", "s", "6", "n", 12)  # ボス出現の警告
    snd[5].set("e2d2c2b1a1rrr", "t", "7", "nnnnf", 18)  # ゲームオーバー
    snd[6].set("g1c1", "n", "4", "f", 3)  # 敵に命中 (倒せなかったとき)

    # タイトル画面の BGM (ミュージック 0)
    snd[10].set(
        "c2e2g2c3 b2g2e2g2 a2c3e3a3 g3rrr f2a2c3f3 e3c3a2c3 d3b2g2b2 c3rrr",
        "s",
        "5",
        "nnnnnnnnnnnnnnnf nnnnnnnnnnnnnnnf",
        24,
    )
    snd[11].set(
        "c1rg0r e1rg0r f1rc1r c1rg0r f1ra0r c1ra0r g0rb0r c1rrr",
        "t",
        "7",
        "n",
        24,
    )

    # プレイ中の BGM (ミュージック 1)
    snd[20].set(
        "a2re3ra3g3e3r f3rc3rf3e3c3r g3rd3rg3f3d3b2 c3re3ra2rrr",
        "p",
        "5",
        "nnnnnnnf",
        20,
    )
    snd[21].set(
        "e3e3re3d3c3d3e3 f3rf3re3d3c3r d3d3rd3c3b2c3d3 e3rg#2rb2re3r",
        "p",
        "5",
        "nnnnnnnf",
        20,
    )
    snd[22].set(
        "a0a1a0a1a0a1a0a1 f0f1f0f1f0f1f0f1 g0g1g0g1g0g1g0g1 a0a1a0a1a0a1a0a1",
        "t",
        "7",
        "n",
        20,
    )
    snd[23].set(
        "a0a1a0a1a0a1a0a1 f0f1f0f1f0f1f0f1 g0g1g0g1g0g1g0g1 e0e1e0e1e0e1e0e1",
        "t",
        "7",
        "n",
        20,
    )
    snd[24].set(
        "c1ra3rc1c1a3r c1ra3rc1c1a3r c1ra3rc1c1a3r c1ra3rc1a3a3a3",
        "n",
        "60406640",
        "f",
        20,
    )


def make_musics() -> None:
    """サウンドを組み合わせて BGM (ミュージック) を定義する。"""
    pyxel.musics[0].set([10], [11])
    pyxel.musics[1].set([20, 21], [22, 23], [24, 24])


def main() -> None:
    pyxel.init(128, 160, headless=True)
    make_sprites()
    make_tiles()
    make_tilemap()
    make_logo()
    make_sounds()
    make_musics()
    for path in OUTPUT_FILES:
        path.parent.mkdir(parents=True, exist_ok=True)
        pyxel.save(str(path))
        print(f"saved: {path}")


if __name__ == "__main__":
    main()
