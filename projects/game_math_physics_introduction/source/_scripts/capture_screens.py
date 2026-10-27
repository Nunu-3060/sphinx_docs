"""本文に載せるデモの画面写真（source/images/screen_*.png）を作り直す。

画面を出さないダミーのドライバーでデモを起動し、決まった入力を与えて、指定したフレームの画面を保存する。
ビルドのたびに作る必要は無いので、conf.py からは呼び出さない。デモを変更したときに手動で実行する。

実行方法（プロジェクトのフォルダーで実行する）:
    py source/_scripts/capture_screens.py
"""

from __future__ import annotations

import importlib
import math
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / 'examples'
OUT = ROOT / 'source' / 'images'
sys.path.insert(0, str(EXAMPLES))

import pygame  # noqa: E402

Script = Callable[[int], tuple[list[pygame.event.Event], set[int], tuple[int, int]]]


def key(k: int) -> list[pygame.event.Event]:
    return [pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode='', scancode=0)]


def click(pos: tuple[int, int]) -> list[pygame.event.Event]:
    return [pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos),
            pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=pos)]


def platformer_input(f: int) -> tuple[list[pygame.event.Event], set[int], tuple[int, int]]:
    """右へ走りながら、一定の間隔でジャンプする。"""
    held = {pygame.K_RIGHT}
    if f % 45 < 30:
        held.add(pygame.K_SPACE)
    return (key(pygame.K_SPACE) if f % 45 == 10 else []), held, (0, 0)


def circle_mouse(f: int) -> tuple[int, int]:
    return int(320 + 150 * math.cos(f * 0.03)), int(240 + 150 * math.sin(f * 0.03))


# モジュール名: (保存するフレーム, 入力を返す関数)
SHOTS: dict[str, tuple[int, Script]] = {
    'vectors_demo': (190, lambda f: ([], {pygame.K_d, pygame.K_w} if f < 80 else {pygame.K_d}, (0, 0))),
    'homing': (140, lambda f: ([], set(), (420, 160))),
    'camera_demo': (110, lambda f: ((click((400, 300)) if f == 30 else []) + (key(pygame.K_SPACE) if f == 100 else []),
                                    {pygame.K_RIGHT, pygame.K_v} if f < 50 else {pygame.K_x}, (300, 200))),
    'cube_demo': (100, lambda f: ([], {pygame.K_UP, pygame.K_LEFT} if f < 60 else set(), (0, 0))),
    'jump': (70, lambda f: (key(pygame.K_SPACE) if f == 20 else [],
                            {pygame.K_SPACE, pygame.K_RIGHT} if f < 60 else {pygame.K_RIGHT}, (0, 0))),
    'collision_demo': (0, lambda f: ([], set(), (330, 250))),
    'response': (230, lambda f: (click((300, 100)) if f % 40 == 0 else [], set(), (0, 0))),
    'rope': (190, lambda f: ((key(pygame.K_c) if f == 100 else []) + (click((320, 200)) if f == 150 else []),
                             set(), circle_mouse(f))),
    'pymunk_demo': (200, lambda f: (click((450, 380)) if f == 100 else [], set(), (0, 0))),
    'platformer': (400, platformer_input),
}


class FakeKeys:
    def __init__(self, held: set[int]) -> None:
        self.held = held

    def __getitem__(self, k: int) -> bool:
        return k in self.held


def capture(name: str, shot: int, script: Script) -> None:
    module: Any = importlib.import_module(name)
    state: dict[str, Any] = {'frame': 0, 'held': set(), 'mouse': (0, 0)}
    real_get, real_flip = pygame.event.get, pygame.display.flip
    real_pressed, real_mouse = pygame.key.get_pressed, pygame.mouse.get_pos

    def fake_get(*args: Any, **kwargs: Any) -> list[pygame.event.Event]:
        real_get()
        if state['frame'] > shot:
            return [pygame.event.Event(pygame.QUIT)]
        events, state['held'], state['mouse'] = script(state['frame'])
        return events

    def fake_flip() -> None:
        real_flip()
        if state['frame'] == shot:
            pygame.image.save(pygame.display.get_surface(), str(OUT / f'screen_{name}.png'))
        state['frame'] += 1

    pygame.event.get = fake_get  # type: ignore[assignment]
    pygame.display.flip = fake_flip  # type: ignore[assignment]
    pygame.key.get_pressed = lambda: FakeKeys(state['held'])  # type: ignore[assignment, return-value]
    pygame.mouse.get_pos = lambda: state['mouse']  # type: ignore[assignment]
    try:
        module.main()
    finally:
        pygame.event.get, pygame.display.flip = real_get, real_flip  # type: ignore[assignment]
        pygame.key.get_pressed, pygame.mouse.get_pos = real_pressed, real_mouse  # type: ignore[assignment]


def main() -> None:
    os.chdir(EXAMPLES)
    for name, (shot, script) in SHOTS.items():
        capture(name, shot, script)
        print('saved', f'screen_{name}.png')


if __name__ == '__main__':
    main()
