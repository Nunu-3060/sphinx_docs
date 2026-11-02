"""すごろくのルールを変えて、勝敗がどう決まるかを測る（2 章、8 章）。

基本ルール:
    * 2 人が交互に 1 個のダイスを振り、出た目だけ進む。先にゴールに着いた（越えた）方が勝ち。
    * 1 回の手番で 1 回だけ振り直してよい。振り直したら 2 回目の目に従う。

振り直しの判断が、このゲームで唯一の「プレイヤーの選択」である。
判断の仕方（戦略）として、次の 3 つを用意する。
    * skilled: 3 以下が出たら振り直す（期待値 3.5 より小さい目を捨てる）
    * random:  2 回に 1 回、でたらめに振り直す
    * never:   振り直さない

ルールの変更（関数 run の引数 rule）:
    * basic:    基本ルール
    * catch_up: 後ろにいるプレイヤーは出た目に 2 を足す（追いつきルール、負のフィードバック）
    * run_away: 前にいるプレイヤーは出た目に 2 を足す（独走ルール、正のフィードバック）

実行方法:
    py sugoroku.py                   演習 3 と演習 4 の表をすべて表示する
    py sugoroku.py --play            基本ルールで遊ぶ（相手は skilled）
"""

import random
import statistics
import sys
from dataclasses import dataclass
from typing import Literal

Strategy = Literal["skilled", "random", "never"]
Rule = Literal["basic", "catch_up", "run_away"]
RULES: list[Rule] = ["basic", "catch_up", "run_away"]
BONUS = 2


@dataclass
class GameResult:
    winner: int        # 勝ったプレイヤーの番号（0 が先手）
    turns: int         # 両者の手番の合計
    lead_changes: int  # 先頭が入れ替わった回数
    gap: int           # ゲーム終了時に負けた側がゴールまで残していたマス数


def wants_reroll(strategy: Strategy, face: int, rng: random.Random) -> bool:
    if strategy == "skilled":
        return face <= 3
    if strategy == "random":
        return rng.random() < 0.5
    return False


def bonus(rule: Rule, me: int, other: int) -> int:
    """ルールの変更による出目への加算を返す。"""
    if rule == "catch_up" and me < other:
        return BONUS
    if rule == "run_away" and me > other:
        return BONUS
    return 0


def play_game(rule: Rule, length: int, strategies: tuple[Strategy, Strategy], rng: random.Random) -> GameResult:
    """1 ゲームを最後まで進め、結果を返す。"""
    pos = [0, 0]
    leader: int | None = None
    lead_changes = 0
    turns = 0
    player = 0
    while True:
        face = rng.randint(1, 6)
        if wants_reroll(strategies[player], face, rng):
            face = rng.randint(1, 6)
        pos[player] += face + bonus(rule, pos[player], pos[1 - player])
        turns += 1
        if pos[player] >= length:
            return GameResult(player, turns, lead_changes, length - pos[1 - player])
        if pos[0] != pos[1]:
            new_leader = 0 if pos[0] > pos[1] else 1
            if leader is not None and new_leader != leader:
                lead_changes += 1
            leader = new_leader
        player = 1 - player


def run(rule: Rule, length: int, strategies: tuple[Strategy, Strategy], games: int,
        seed: int = 1, swap: bool = False) -> list[GameResult]:
    """games 回対戦する。swap が真なら先手と後手を 1 回ごとに入れ替え、結果の番号は strategies の順にそろえる。"""
    rng = random.Random(seed)
    results = []
    for g in range(games):
        if swap and g % 2 == 1:
            r = play_game(rule, length, (strategies[1], strategies[0]), rng)
            r.winner = 1 - r.winner
        else:
            r = play_game(rule, length, strategies, rng)
        results.append(r)
    return results


def win_rate(results: list[GameResult], player: int = 0) -> float:
    return sum(r.winner == player for r in results) / len(results)


def exercise3(games: int) -> None:
    print("演習 3-1 同じ戦略どうし（random 対 random）での先手の勝率")
    for length in (10, 30, 100):
        print(f"  ゴールまで {length:3d} マス: {win_rate(run('basic', length, ('random', 'random'), games)):.3f}")
    print("演習 3-2 skilled 対 random での skilled の勝率（先手と後手を交互に入れ替える）")
    for length in (10, 30, 100, 300):
        results = run("basic", length, ("skilled", "random"), games, swap=True)
        print(f"  ゴールまで {length:3d} マス: {win_rate(results):.3f}")


def exercise4(games: int, length: int = 30) -> None:
    print(f"演習 4 ルールによる違い（ゴールまで {length} マス、skilled 対 random、先手と後手を交互に入れ替える）")
    print("  ルール      skilled の勝率  負けた側の残りマス  先頭の入れ替わり")
    for rule in RULES:
        results = run(rule, length, ("skilled", "random"), games, swap=True)
        gap = statistics.mean(r.gap for r in results)
        changes = statistics.mean(r.lead_changes for r in results)
        print(f"  {rule:10s}  {win_rate(results):14.3f}  {gap:18.1f}  {changes:16.2f}")


def play_interactive(length: int = 30) -> None:
    rng = random.Random()
    pos = [0, 0]
    player = 0
    while True:
        if player == 0:
            face = rng.randint(1, 6)
            answer = input(f"あなた {pos[0]} / 相手 {pos[1]} / ゴール {length}  出目 {face}。振り直す？ (y/n) > ")
            if answer.strip().lower() == "y":
                face = rng.randint(1, 6)
                print(f"  振り直しの出目 {face}")
        else:
            face = rng.randint(1, 6)
            if wants_reroll("skilled", face, rng):
                face = rng.randint(1, 6)
            print(f"  相手の出目 {face}")
        pos[player] += face
        if pos[player] >= length:
            print("あなたの勝ち" if player == 0 else "相手の勝ち")
            return
        player = 1 - player


def main() -> None:
    if "--play" in sys.argv:
        play_interactive()
        return
    games = 20_000
    exercise3(games)
    exercise4(games)


if __name__ == "__main__":
    main()
