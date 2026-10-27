"""プレイログからヒートマップを描き、プレイヤーがつまずく場所を見つける。

ログは次の列を持つ CSV ファイルとする（1 行が 1 つの出来事）。

    session,level,x,y,event
    1,demo,41.8,2.3,death

* session : テストプレイの回（プレイヤー）の番号
* level   : レベルの名前
* x, y    : 出来事が起きた位置
* event   : 出来事の種類（death, clear, quit など）

--input を省略すると、横スクロールのアクションゲームを想定した架空のログを生成して使う。
架空のレベルには x = 40（穴）、x = 90（敵）、x = 150（難しいジャンプ）の 3 か所の難所がある。

実行例:
    python playtest_heatmap.py                                   # 架空のログで描画する
    python playtest_heatmap.py --save-demo-log demo_log.csv      # 架空のログを CSV に保存する
    python playtest_heatmap.py --input final_project/playlog.csv --event move --level 二つの通り道 --grid
"""

from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass

import matplotlib.pyplot as plt

FIELDS = ["session", "level", "x", "y", "event"]


@dataclass(frozen=True)
class Record:
    session: int
    level: str
    x: float
    y: float
    event: str


@dataclass(frozen=True)
class Hazard:
    """架空のレベルの難所。success は 1 回の挑戦で突破できる確率。"""

    x: float
    y: float
    success: float


DEMO_HAZARDS = [Hazard(40, 2, 0.85), Hazard(90, 6, 0.7), Hazard(150, 9, 0.35)]
GIVE_UP_DEATHS = 6  # 同じ難所でこの回数ミスすると、プレイをやめてしまう


def play_hazard(session: int, hazard: Hazard, skill: float, rng: random.Random) -> tuple[list[Record], bool]:
    """1 つの難所を突破するか諦めるまで挑戦する。出来事の一覧と、突破できたかを返す。"""
    records: list[Record] = []
    while rng.random() >= hazard.success + skill:
        x, y = round(rng.gauss(hazard.x, 3), 1), round(max(0.0, rng.gauss(hazard.y, 1)), 1)
        records.append(Record(session, "demo", x, y, "death"))
        if len(records) >= GIVE_UP_DEATHS:
            records.append(Record(session, "demo", x, y, "quit"))
            return records, False
    return records, True


def make_demo_log(sessions: int, rng: random.Random) -> list[Record]:
    """難所ごとに突破できるまで挑戦を繰り返す、架空のプレイヤーのログを作る。"""
    records: list[Record] = []
    for session in range(1, sessions + 1):
        skill = rng.uniform(-0.1, 0.1)  # プレイヤーごとの腕前の差
        for hazard in DEMO_HAZARDS:
            events, passed = play_hazard(session, hazard, skill, rng)
            records += events
            if not passed:
                break  # 諦めたプレイヤーは次の難所に進まない
        else:
            records.append(Record(session, "demo", 195.0, 3.0, "clear"))
    return records


def load_log(path: str) -> list[Record]:
    with open(path, newline="", encoding="utf-8") as f:
        return [
            Record(int(row["session"]), row["level"], float(row["x"]), float(row["y"]), row["event"])
            for row in csv.DictReader(f)
        ]


def save_log(path: str, records: list[Record]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDS)
        for r in records:
            writer.writerow([r.session, r.level, r.x, r.y, r.event])


def summarize(records: list[Record]) -> None:
    sessions = {r.session for r in records}
    counts: dict[str, int] = {}
    for r in records:
        counts[r.event] = counts.get(r.event, 0) + 1
    print(f"セッション数: {len(sessions)}")
    for event, count in sorted(counts.items()):
        print(f"  {event}: {count} 件")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", help="読み込むログ（CSV）。省略時は架空のログを生成する")
    parser.add_argument("--save-demo-log", metavar="PATH", help="生成した架空のログを保存する")
    parser.add_argument("--event", default="death", help="ヒートマップにする出来事の種類")
    parser.add_argument("--level", help="対象のレベル（省略時はすべて）")
    parser.add_argument("--bins", type=int, default=40, help="横方向の区画数")
    parser.add_argument("--y-bins", type=int, help="縦方向の区画数（省略時は区画がほぼ正方形になるように決める）")
    parser.add_argument("--grid", action="store_true",
                        help="座標をタイルの番号とみなし、1 マスを 1 区画にして y 軸を下向きにする")
    parser.add_argument("--output", help="グラフを保存するファイル名（省略時は画面に表示する）")
    parser.add_argument("--seed", type=int, default=3, help="架空のログを作るときの乱数のシード")
    args = parser.parse_args()

    if args.input:
        records = load_log(args.input)
    else:
        records = make_demo_log(sessions=30, rng=random.Random(args.seed))
        args.y_bins = args.y_bins or 6
        if args.save_demo_log:
            save_log(args.save_demo_log, records)
    summarize(records)

    points = [r for r in records if r.event == args.event and (args.level is None or r.level == args.level)]
    if not points:
        print(f"event = {args.event} の記録がありません。")
        return
    xs, ys = [p.x for p in points], [p.y for p in points]
    if args.grid:
        # 整数の座標を中心に、1 マスが 1 区画になるように範囲を決める。
        x_range = (min(xs) - 0.5, max(xs) + 0.5)
        y_range = (min(ys) - 0.5, max(ys) + 0.5)
        x_bins, y_bins = round(x_range[1] - x_range[0]), round(y_range[1] - y_range[0])
    else:
        x_range = (min(xs) - 1, max(xs) + 1) if args.input else (0, 200)
        y_range = (min(ys) - 1, max(ys) + 1) if args.input else (0, 12)
        x_bins = args.bins
        y_bins = args.y_bins or max(1, round(x_bins * (y_range[1] - y_range[0]) / (x_range[1] - x_range[0])))

    plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "sans-serif"]
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(8, 5), sharex=True, layout="constrained",
                                      gridspec_kw={"height_ratios": [2, 1]})
    *_, mesh = top.hist2d(xs, ys, bins=[x_bins, y_bins], range=[x_range, y_range], cmap="inferno")
    fig.colorbar(mesh, ax=[top, bottom], label="件数")
    top.set_ylabel("y")
    top.set_title(f"「{args.event}」の位置のヒートマップ（{len(points)} 件）")
    if args.grid:
        top.invert_yaxis()
    bottom.hist(xs, bins=x_bins, range=x_range, color="tab:red")
    bottom.set_xlabel("x")
    bottom.set_ylabel("件数")
    bottom.grid(alpha=0.3)

    if args.output:
        fig.savefig(args.output, dpi=110)
    else:
        plt.show()


if __name__ == "__main__":
    main()
