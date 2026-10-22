"""pygame-ce で BGM と効果音をゲームのように鳴らす.

先に make_all.py を実行して output フォルダに WAV ファイルを作っておくこと。

* BGM はループ再生する
* スペースキー、C キー、X キーで効果音を鳴らす
* 上下キーで BGM の音量を変える
"""

import sys
from pathlib import Path

import pygame

AUDIO_DIR = Path(__file__).resolve().parent / "output"

SOUND_KEYS = {
    pygame.K_SPACE: "se_jump.wav",
    pygame.K_c: "se_coin.wav",
    pygame.K_x: "se_explosion.wav",
}


def main() -> None:
    # バッファを小さくすると、キーを押してから音が鳴るまでの遅れが短くなる
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    pygame.mixer.set_num_channels(8)  # 効果音を同時に鳴らせる数
    screen = pygame.display.set_mode((480, 200))
    pygame.display.set_caption("8 bit sound demo")
    font = pygame.font.Font(None, 28)

    effects = {key: pygame.mixer.Sound(AUDIO_DIR / name) for key, name in SOUND_KEYS.items()}
    for effect in effects.values():
        effect.set_volume(0.8)

    pygame.mixer.music.load(AUDIO_DIR / "bgm_loop.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)  # -1 は無限ループ

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in effects:
                    effects[event.key].play()
                elif event.key == pygame.K_UP:
                    pygame.mixer.music.set_volume(min(pygame.mixer.music.get_volume() + 0.1, 1.0))
                elif event.key == pygame.K_DOWN:
                    pygame.mixer.music.set_volume(max(pygame.mixer.music.get_volume() - 0.1, 0.0))
                elif event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((20, 20, 40))
        lines = [
            "SPACE: jump   C: coin   X: explosion",
            f"UP / DOWN: BGM volume ({pygame.mixer.music.get_volume():.1f})",
            "ESC: quit",
        ]
        for i, line in enumerate(lines):
            screen.blit(font.render(line, True, (230, 230, 230)), (20, 40 + 40 * i))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
