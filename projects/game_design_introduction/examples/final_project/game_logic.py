"""『宝石と見張り』のルール（画面表示を含まない部分）。

ルール:
    * プレイヤーは 1 ターンに上下左右へ 1 マス動くか、その場で待つ。壁へは動けない（ターンも進まない）。
    * 宝石をすべて集めてから出口に入るとクリアである。宝石が残っているあいだ、出口はただの床として扱う。
    * プレイヤーが動いた後、見張りが全員 1 マス進む。進む先が壁なら向きを反転して 1 マス進む。
    * 見張りのいるマスに入るか、見張りが自分のいるマスに来ると捕まる。

レベルは次の文字で表したテキストファイルで定義する。

    #  壁          .  床          @  プレイヤーのスタート位置
    *  宝石        E  出口        > < ^ v  見張り（文字が最初に進む向きを表す）

先頭が ';' の行は「; キー: 値」の形の設定行で、name（レベル名）と hint（ヒント）を書ける。
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, auto
from pathlib import Path

Pos = tuple[int, int]  # (x, y)。x は右向き、y は下向きが正

UP: Pos = (0, -1)
DOWN: Pos = (0, 1)
LEFT: Pos = (-1, 0)
RIGHT: Pos = (1, 0)
WAIT: Pos = (0, 0)
MOVES: tuple[Pos, ...] = (UP, DOWN, LEFT, RIGHT, WAIT)

GUARD_CHARS: dict[str, Pos] = {">": RIGHT, "<": LEFT, "^": UP, "v": DOWN}


class Status(Enum):
    PLAYING = auto()
    CLEARED = auto()
    CAUGHT = auto()


@dataclass(frozen=True)
class Guard:
    pos: Pos
    direction: Pos


@dataclass(frozen=True)
class State:
    """あるターンの盤面。変更できない値として扱い、1 手ごとに新しい State を作る。"""

    player: Pos
    gems: frozenset[Pos]  # まだ拾っていない宝石
    guards: tuple[Guard, ...]
    turn: int = 0
    status: Status = Status.PLAYING


def add(a: Pos, b: Pos) -> Pos:
    return a[0] + b[0], a[1] + b[1]


@dataclass(frozen=True)
class Level:
    name: str
    width: int
    height: int
    walls: frozenset[Pos]
    exit: Pos
    initial: State
    hint: str = ""

    @classmethod
    def from_text(cls, text: str, default_name: str = "") -> Level:
        metadata: dict[str, str] = {}
        rows: list[str] = []
        for line in text.splitlines():
            if line.startswith(";"):
                key, _, value = line[1:].partition(":")
                metadata[key.strip()] = value.strip()
            elif line.strip():
                rows.append(line.rstrip())

        walls: set[Pos] = set()
        gems: set[Pos] = set()
        guards: list[Guard] = []
        player: Pos | None = None
        exit_pos: Pos | None = None
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                pos = (x, y)
                if char == "#":
                    walls.add(pos)
                elif char == "@":
                    player = pos
                elif char == "*":
                    gems.add(pos)
                elif char == "E":
                    exit_pos = pos
                elif char in GUARD_CHARS:
                    guards.append(Guard(pos, GUARD_CHARS[char]))
                elif char != ".":
                    raise ValueError(f"未知の文字 {char!r}（{x}, {y}）")
        if player is None or exit_pos is None:
            raise ValueError("プレイヤー（@）と出口（E）が必要です")

        return cls(
            name=metadata.get("name", default_name),
            width=max(len(row) for row in rows),
            height=len(rows),
            walls=frozenset(walls),
            exit=exit_pos,
            initial=State(player, frozenset(gems), tuple(guards)),
            hint=metadata.get("hint", ""),
        )

    @classmethod
    def load(cls, path: Path) -> Level:
        return cls.from_text(path.read_text(encoding="utf-8"), default_name=path.stem)

    def is_wall(self, pos: Pos) -> bool:
        x, y = pos
        return pos in self.walls or not (0 <= x < self.width and 0 <= y < self.height)

    def move_guard(self, guard: Guard) -> Guard:
        """見張りを 1 マス進める。前が壁なら反転し、反転した先も壁なら動かない。"""
        ahead = add(guard.pos, guard.direction)
        if not self.is_wall(ahead):
            return Guard(ahead, guard.direction)
        back = (-guard.direction[0], -guard.direction[1])
        behind = add(guard.pos, back)
        return Guard(guard.pos if self.is_wall(behind) else behind, back)

    def step(self, state: State, move: Pos) -> State | None:
        """1 手進めた盤面を返す。壁に向かって動こうとした場合は None を返す。"""
        if state.status is not Status.PLAYING:
            return None
        target = add(state.player, move)
        if self.is_wall(target):
            return None

        gems = state.gems - {target}
        turn = state.turn + 1
        if any(g.pos == target for g in state.guards):
            return replace(state, player=target, turn=turn, status=Status.CAUGHT)
        if target == self.exit and not gems:
            return replace(state, player=target, gems=gems, turn=turn, status=Status.CLEARED)

        guards = tuple(self.move_guard(g) for g in state.guards)
        caught = any(g.pos == target for g in guards)
        return State(target, gems, guards, turn, Status.CAUGHT if caught else Status.PLAYING)


def load_levels(directory: Path) -> list[Level]:
    """directory にある *.txt をファイル名の順に読み込む。"""
    return [Level.load(path) for path in sorted(directory.glob("*.txt"))]
