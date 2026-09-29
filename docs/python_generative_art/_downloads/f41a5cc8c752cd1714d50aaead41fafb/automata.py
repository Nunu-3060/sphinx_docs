"""セルオートマトン: 格子と近傍ルールの反復による図形生成。

各セルが「状態」を持ち、次の世代の状態が自身と近傍セルの現在の状態
だけから決まる、というごく単純な規則を繰り返し適用するだけで、
1次元では複雑な模様が、2次元では生き物のように動き回るパターンが
生まれる。NumPyでは、格子全体をずらして重ね合わせる ``np.roll`` を
使うことで、セルごとのPythonループなしに1世代分の更新を一括計算
できる。
"""

import numpy as np
from PIL import Image


def elementary_ca(rule: int, width: int, steps: int) -> np.ndarray:
    """Wolframの初等セルオートマトンを width幅×steps世代分計算する。

    各セルの次の状態は、自身と両隣の3セル(左・中央・右、8通りの
    近傍パターン)から、``rule`` 番号(0-255)のビットで決まる。戻り値は
    形状 ``(steps, width)`` のブール配列で、行が世代、列が空間位置を
    表す。初期状態は中央の1セルだけを1にしたものを使う。
    """
    rule_bits: np.ndarray = np.array(
        [(rule >> i) & 1 for i in range(8)], dtype=np.uint8
    )
    grid: np.ndarray = np.zeros((steps, width), dtype=np.uint8)
    grid[0, width // 2] = 1

    for t in range(steps - 1):
        left: np.ndarray = np.roll(grid[t], 1)
        center: np.ndarray = grid[t]
        right: np.ndarray = np.roll(grid[t], -1)
        neighborhood: np.ndarray = (left << 2) | (center << 1) | right
        grid[t + 1] = rule_bits[neighborhood]

    return grid.astype(bool)


def render_grid(
    grid: np.ndarray,
    on_color: tuple[int, int, int] = (30, 30, 30),
    off_color: tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    """ブール配列を、状態に応じて2色に塗り分けた画像として描画する。"""
    pixels: np.ndarray = np.where(
        grid[..., np.newaxis], on_color, off_color
    )
    return Image.fromarray(pixels.astype(np.uint8))


def life_step(grid: np.ndarray) -> np.ndarray:
    """Conwayのライフゲームを1世代分進める(周期境界)。

    生存条件は「周囲8マスの生存数がちょうど3なら誕生」
    「2または3なら生存を維持」で、それ以外は死滅する。周囲8方向への
    ずらし・加算は固定回数のPythonループだが、その中身は格子全体への
    NumPy演算なので、セル数が増えてもループ回数自体は変わらない。
    """
    neighbor_count: np.ndarray = np.zeros(grid.shape, dtype=np.int64)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            neighbor_count += np.roll(
                np.roll(grid, dy, axis=0), dx, axis=1
            )

    born: np.ndarray = (neighbor_count == 3) & ~grid
    survive: np.ndarray = (
        (neighbor_count == 2) | (neighbor_count == 3)
    ) & grid
    return born | survive


def simulate_life(grid: np.ndarray, num_steps: int) -> np.ndarray:
    """初期状態 ``grid`` から num_steps 世代分の履歴を返す。

    戻り値は形状 ``(num_steps,) + grid.shape`` のブール配列。
    """
    history: np.ndarray = np.empty(
        (num_steps,) + grid.shape, dtype=bool
    )
    current: np.ndarray = grid
    for step in range(num_steps):
        history[step] = current
        current = life_step(current)
    return history


def render_life_trail(
    history: np.ndarray,
    color: tuple[int, int, int] = (40, 90, 60),
    fade: float = 0.90,
) -> Image.Image:
    """各世代を指数的に減衰させながら重ね合わせ、セルが動き回った
    軌跡を1枚の静止画として可視化する。

    直近の世代ほど濃く、古い世代ほど薄く残るため、静止画のまま
    「どこがよく動いていたか」という時間的な情報を表現できる。
    """
    height: int
    width: int
    _, height, width = history.shape
    accumulator: np.ndarray = np.zeros((height, width), dtype=float)
    for state in history:
        accumulator = accumulator * fade + state.astype(float)

    max_value: float = float(accumulator.max())
    normalized: np.ndarray = (
        accumulator / max_value if max_value > 0 else accumulator
    )

    background: np.ndarray = np.full((height, width, 3), 255.0)
    fg: np.ndarray = np.array(color, dtype=float)
    pixels: np.ndarray = (
        background + (fg - background) * normalized[..., np.newaxis]
    )
    return Image.fromarray(pixels.round().astype(np.uint8))


def brians_brain_step(grid: np.ndarray) -> np.ndarray:
    """Brian's Brainを1世代分進める(周期境界)。

    各セルは 死(0)・発火(1)・消えかけ(2) の3状態を持つ。死んでいる
    セルは、周囲8マスにちょうど2つ発火セルがあれば新たに発火する。
    発火セルは近傍によらず必ず消えかけに移り、消えかけのセルは
    近傍によらず必ず死に戻る。ライフゲームと違って「生存」という
    状態がなく、発火したセルは1世代後には必ず消えるため、模様は
    決して静止せず走り続ける。
    """
    firing: np.ndarray = grid == 1
    firing_neighbors: np.ndarray = np.zeros(grid.shape, dtype=np.int64)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            shifted: np.ndarray = np.roll(
                np.roll(firing, dy, axis=0), dx, axis=1
            )
            firing_neighbors += shifted

    next_grid: np.ndarray = np.zeros_like(grid)
    next_grid[(grid == 0) & (firing_neighbors == 2)] = 1
    next_grid[grid == 1] = 2
    return next_grid


def simulate_brain(grid: np.ndarray, num_steps: int) -> np.ndarray:
    """初期状態 ``grid`` から num_steps 世代分のBrian's Brain履歴を返す。"""
    history: np.ndarray = np.empty(
        (num_steps,) + grid.shape, dtype=grid.dtype
    )
    current: np.ndarray = grid
    for step in range(num_steps):
        history[step] = current
        current = brians_brain_step(current)
    return history


def render_brain(
    grid: np.ndarray,
    firing_color: tuple[int, int, int] = (255, 210, 70),
    dying_color: tuple[int, int, int] = (90, 60, 120),
    off_color: tuple[int, int, int] = (20, 20, 30),
) -> Image.Image:
    """Brian's Brainの3状態(死・発火・消えかけ)を3色で塗り分けて描画する。"""
    pixels: np.ndarray = np.full(
        grid.shape + (3,), off_color, dtype=np.uint8
    )
    pixels[grid == 1] = firing_color
    pixels[grid == 2] = dying_color
    return Image.fromarray(pixels)


def langtons_ant(grid_size: int, steps: int) -> np.ndarray:
    """ラングトンの蟻を steps 歩シミュレートし、最終的な盤面を返す。

    盤面は 白(0)/黒(1) の2状態。蟻は現在いるマスの色に応じて
    「白マスなら右に90度回頭し、マスを黒く塗ってから前進」
    「黒マスなら左に90度回頭し、マスを白く塗ってから前進」を繰り返す。
    各ステップの結果が直前の盤面と蟻の位置・向きの両方に依存する
    逐次処理のため、ライフゲームのように盤面全体をNumPy演算だけで
    一括更新することはできない。約1万歩を過ぎたあたりから、それまでの
    無秩序な軌跡が一転して斜めに伸び続ける規則的な「ハイウェイ」模様に
    落ち着くことが知られている。
    """
    grid: np.ndarray = np.zeros((grid_size, grid_size), dtype=np.uint8)
    y, x = grid_size // 2, grid_size // 2

    # heading 0-3 が、上・右・下・左の順に90度ずつ回頭した向きに対応する。
    directions: np.ndarray = np.array([(-1, 0), (0, 1), (1, 0), (0, -1)])
    heading: int = 0

    for _ in range(steps):
        if grid[y, x] == 0:
            heading = (heading + 1) % 4
            grid[y, x] = 1
        else:
            heading = (heading - 1) % 4
            grid[y, x] = 0
        dy, dx = directions[heading]
        y = (y + dy) % grid_size
        x = (x + dx) % grid_size

    return grid


def bml_traffic_step(grid: np.ndarray, horizontal: bool) -> np.ndarray:
    """BML交通モデルを1半ステップ分進める(周期境界)。

    盤面は 空(0)・右に進む赤い車(1)・下に進む青い車(2) の3状態。
    ``horizontal=True`` の半ステップでは赤い車だけが、``False`` の
    半ステップでは青い車だけが、進行方向のマスが空いていれば1マス
    前進する。同じ半ステップで動く車は全員が同じ方向へ1マスだけ
    ずれるので行き先が重なることはなく、「1マス先が空いているか」を
    ``np.roll`` で判定するだけで全車を同時に動かせる。
    """
    axis: int = 1 if horizontal else 0
    color: int = 1 if horizontal else 2

    ahead_is_empty: np.ndarray = np.roll(grid, -1, axis=axis) == 0
    can_move: np.ndarray = (grid == color) & ahead_is_empty

    next_grid: np.ndarray = grid.copy()
    next_grid[can_move] = 0
    next_grid[np.roll(can_move, 1, axis=axis)] = color
    return next_grid


def simulate_bml_traffic(
    grid_size: int, density: float, half_steps: int, seed: int = 0
) -> np.ndarray:
    """BML交通モデルを half_steps 半ステップ分進めた最終盤面を返す。

    赤(右向き)・青(下向き)の車を、それぞれ全体密度 ``density`` の
    半分ずつランダムな位置に配置してから、赤の半ステップと青の
    半ステップを交互に繰り返す。密度が低いうちは車どうしがほとんど
    ぶつからず流れ続けるが、ある密度を境に、どこかで生じた渋滞が
    解消できずに盤面全体が完全に停止する(**ジャム相転移**)。
    """
    rng: np.random.Generator = np.random.default_rng(seed)
    is_car: np.ndarray = rng.random((grid_size, grid_size)) < density
    is_red: np.ndarray = rng.random((grid_size, grid_size)) < 0.5

    grid: np.ndarray = np.zeros((grid_size, grid_size), dtype=np.uint8)
    grid[is_car & is_red] = 1
    grid[is_car & ~is_red] = 2

    for step in range(half_steps):
        grid = bml_traffic_step(grid, horizontal=(step % 2 == 0))

    return grid


def render_traffic(
    grid: np.ndarray,
    red_color: tuple[int, int, int] = (210, 60, 60),
    blue_color: tuple[int, int, int] = (60, 90, 200),
    empty_color: tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    """BML交通モデルの3状態(空・赤い車・青い車)を3色で塗り分けて描画する。"""
    pixels: np.ndarray = np.full(
        grid.shape + (3,), empty_color, dtype=np.uint8
    )
    pixels[grid == 1] = red_color
    pixels[grid == 2] = blue_color
    return Image.fromarray(pixels)


def main() -> None:
    width: int = 400
    steps: int = 200

    render_grid(elementary_ca(rule=30, width=width, steps=steps)).save(
        "ca_rule30.png"
    )
    render_grid(elementary_ca(rule=90, width=width, steps=steps)).save(
        "ca_rule90.png"
    )

    rng: np.random.Generator = np.random.default_rng(seed=2)
    initial: np.ndarray = rng.random((120, 120)) < 0.25
    history: np.ndarray = simulate_life(initial, num_steps=150)
    trail_image: Image.Image = render_life_trail(history)
    upscaled: Image.Image = trail_image.resize(
        (trail_image.width * 4, trail_image.height * 4),
        resample=Image.Resampling.NEAREST,
    )
    upscaled.save("life_trail.png")

    brain_rng: np.random.Generator = np.random.default_rng(seed=1)
    brain_initial: np.ndarray = np.where(
        brain_rng.random((150, 200)) < 0.2, 1, 0
    ).astype(np.uint8)
    brain_history: np.ndarray = simulate_brain(brain_initial, num_steps=40)
    render_brain(brain_history[-1]).resize(
        (800, 600), resample=Image.Resampling.NEAREST
    ).save("brians_brain.png")

    ant_grid: np.ndarray = langtons_ant(grid_size=120, steps=11000)
    render_grid(
        ant_grid.astype(bool),
        on_color=(30, 30, 30),
        off_color=(255, 255, 255),
    ).resize((600, 600), resample=Image.Resampling.NEAREST).save(
        "langtons_ant.png"
    )

    render_traffic(
        simulate_bml_traffic(
            grid_size=150, density=0.3, half_steps=400, seed=3
        )
    ).resize((600, 600), resample=Image.Resampling.NEAREST).save(
        "bml_traffic_free.png"
    )
    render_traffic(
        simulate_bml_traffic(
            grid_size=150, density=0.5, half_steps=400, seed=3
        )
    ).resize((600, 600), resample=Image.Resampling.NEAREST).save(
        "bml_traffic_jam.png"
    )


if __name__ == "__main__":
    main()
