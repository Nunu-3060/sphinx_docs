"""本文で使う図を source/images に生成する。

matplotlib によるグラフ、Pillow によるスプライトシート、pygame-ce によるサンプルゲームの画面を出力する。
build_html.bat から呼び出す。
"""

import math
import os
import random
import sys
from pathlib import Path

import matplotlib
from matplotlib import font_manager

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

SOURCE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = SOURCE_DIR / "images"
EXAMPLES_DIR = SOURCE_DIR.parent / "examples"


def select_font(candidates: list[str]) -> str:
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    return candidates[-1]


# Noto Sans JP は細字しか無い環境があるため、游ゴシックを優先する
plt.rcParams["font.family"] = select_font(["Yu Gothic", "Meiryo", "Noto Sans JP"])
plt.rcParams["axes.unicode_minus"] = False


def make_dt_comparison() -> None:
    """フレーム数基準の移動とデルタタイム基準の移動を、フレームレートが落ちた場合で比較する。"""
    speed = 480.0  # ピクセル毎秒
    step_per_frame = speed / 60  # 60 FPS を前提にした 1 フレームあたりの移動量
    times = [0.0]
    by_frame = [0.0]
    by_dt = [0.0]
    t = 0.0
    while t < 2.0:
        dt = 1 / 60 if t < 1.0 else 1 / 30  # 1 秒後から処理が重くなり 30 FPS に落ちる
        t += dt
        times.append(t)
        by_frame.append(by_frame[-1] + step_per_frame)
        by_dt.append(by_dt[-1] + speed * dt)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axvspan(1.0, 2.0, color="0.9")
    ax.text(1.5, 60, "処理が重くなり 30 FPS に低下", ha="center")
    ax.plot(times, by_dt, label="デルタタイム基準（速度 × dt）", linewidth=2)
    ax.plot(times, by_frame, label="フレーム数基準（1 フレームに 8 ピクセル）", linewidth=2, linestyle="--")
    ax.set_xlabel("経過時間（秒）")
    ax.set_ylabel("移動距離（ピクセル）")
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1000)
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(IMAGE_DIR / "dt_comparison.png", dpi=110)
    plt.close(fig)


def make_bounce_angle() -> None:
    """パドルに当たった位置と、反射後の向きの関係を矢印で示す。"""
    max_angle = math.radians(60)
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.add_patch(plt.Rectangle((-1, -0.12), 2, 0.12, color="#8090c0"))
    for offset in (-1.0, -0.5, 0.0, 0.5, 1.0):
        angle = offset * max_angle
        dx, dy = 0.9 * math.sin(angle), 0.9 * math.cos(angle)
        ax.annotate("", xy=(offset + dx, dy), xytext=(offset, 0),
                    arrowprops={"arrowstyle": "-|>", "linewidth": 2, "color": "#d04040"})
        ax.text(offset, -0.28, f"offset = {offset:+.1f}\n{math.degrees(angle):+.0f}°", ha="center", va="top")
    ax.text(0, -0.06, "パドル", ha="center", va="center", color="white", fontsize=9)
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-0.7, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(IMAGE_DIR / "bounce_angle.png", dpi=110)
    plt.close(fig)


def make_sprites() -> None:
    """examples/make_sprites.py でスプライトシートを作り、確認しやすいよう 6 倍に拡大して保存する。"""
    from PIL import Image

    import make_sprites as sprites

    sheet, _ = sprites.make_sheet()
    background = Image.new("RGBA", sheet.size, (40, 44, 60, 255))
    background.alpha_composite(sheet)
    scale = 6
    background.resize((sheet.width * scale, sheet.height * scale), Image.Resampling.NEAREST).save(
        IMAGE_DIR / "sprites.png")


def make_screenshots() -> None:
    """examples/step07_polish.py の各シーンを、ウィンドウを開かずに描画して保存する。"""
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    import pygame

    import step07_polish as game

    pygame.init()
    screen = pygame.display.set_mode((game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
    random.seed(3)
    sounds = game.SoundBank()

    game.TitleScene(sounds).draw(screen)
    pygame.image.save(screen, IMAGE_DIR / "screen_title.png")

    # プレイ画面: 実際に少し遊ばせてから、ブロックを壊した直後の様子を撮る
    play = game.PlayScene(sounds)
    game.read_direction = lambda: 0.0  # type: ignore[assignment]
    play.ball.launch()
    frames = 0
    while frames < 60 * 30:
        play.paddle.rect.centerx = play.ball.rect.centerx + random.uniform(-30, 30)
        play.update(1 / 60)
        frames += 1
        if frames > 60 * 8 and len(play.particles) >= game.PARTICLE_COUNT and 0.36 < play.particles[-1].life < 0.4:
            break
    play.draw(screen)
    pygame.image.save(screen, IMAGE_DIR / "screen_play.png")

    game.ResultScene(sounds, 1500, cleared=True).draw(screen)
    pygame.image.save(screen, IMAGE_DIR / "screen_result.png")
    pygame.quit()


def main() -> None:
    IMAGE_DIR.mkdir(exist_ok=True)
    sys.path.insert(0, str(EXAMPLES_DIR))
    make_dt_comparison()
    make_bounce_angle()
    make_sprites()
    make_screenshots()


if __name__ == "__main__":
    main()
