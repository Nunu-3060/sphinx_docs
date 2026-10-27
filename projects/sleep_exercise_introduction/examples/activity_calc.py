"""1 週間の活動記録 CSV から身体活動量 (メッツ・時) を計算し、推奨量と比べる。

CSV には活動ごとに次の 3 列を記録する。

* day: 曜日 (月, 火, ...)
* activity: 活動の種類 (ACTIVITIES のキー。walk, brisk_walk など)
* minutes: 活動した時間 (分)

使い方::

    python activity_calc.py activity_sample.csv --weight 65
"""

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

# 「健康づくりのための身体活動・運動ガイド2023」の成人向けの推奨値
TARGET_ACTIVITY = 23.0  # 3 メッツ以上の身体活動 (メッツ・時/週)
TARGET_EXERCISE = 4.0  # 3 メッツ以上の運動 (メッツ・時/週)
TARGET_STRENGTH_DAYS = 2  # 筋力トレーニングを行う日数 (日/週)
MODERATE_METS = 3.0  # 中強度とみなす強さの下限 (メッツ)

DAYS = "月火水木金土日"


@dataclass(frozen=True)
class Activity:
    """活動の種類。"""

    label: str
    mets: float
    is_exercise: bool  # 運動 (体力の維持・向上を目的に計画的に行うもの) なら True
    is_strength: bool = False  # 筋力トレーニングなら True


# 主な活動のメッツ値 (改訂第 2 版『身体活動のメッツ (METs) 表』成人版による)
ACTIVITIES: dict[str, Activity] = {
    "desk_work": Activity("座ってデスクワーク", 1.3, False),
    "standing_work": Activity("立ってパソコン作業", 1.3, False),
    "walk": Activity("歩く (時速 4 km 程度)", 3.0, False),
    "walk_moderate": Activity("歩く (時速 4.5〜5.5 km)", 3.8, False),
    "stairs": Activity("階段をゆっくり上る", 4.5, False),
    "cycle": Activity("自転車に乗る (時速 16 km 未満)", 4.0, False),
    "stretch": Activity("ストレッチ (ゆったり)", 2.3, True),
    "bodyweight": Activity("自重の筋力トレーニング", 3.0, True, is_strength=True),
    "brisk_walk": Activity("速歩 (時速 5.7〜6.3 km)", 4.8, True),
    "jogging": Activity("ジョギング", 7.5, True),
}


@dataclass(frozen=True)
class Entry:
    """活動記録の 1 行。"""

    day: str
    activity: Activity
    minutes: float

    @property
    def mets_hours(self) -> float:
        """身体活動量 (メッツ・時)。"""
        return self.activity.mets * self.minutes / 60


@dataclass(frozen=True)
class WeeklySummary:
    """1 週間の集計結果。"""

    activity_mets_hours: float  # 3 メッツ以上の身体活動の合計
    exercise_mets_hours: float  # そのうち運動の合計
    strength_days: int
    energy_kcal: float  # 記録したすべての活動の消費エネルギー (安静時の分を含む)


def load_entries(path: Path) -> list[Entry]:
    """CSV ファイルから活動記録を読み込む。"""
    entries = []
    with path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            day = row["day"].strip()
            if day not in DAYS:
                raise ValueError(f"曜日が正しくない: {day}")
            key = row["activity"].strip()
            if key not in ACTIVITIES:
                raise ValueError(f"未知の活動: {key} (使える活動: {', '.join(ACTIVITIES)})")
            entries.append(Entry(day, ACTIVITIES[key], float(row["minutes"])))
    return entries


def summarize(entries: list[Entry], weight_kg: float) -> WeeklySummary:
    """1 週間分の活動記録を集計する。"""
    moderate = [e for e in entries if e.activity.mets >= MODERATE_METS]
    return WeeklySummary(
        activity_mets_hours=sum(e.mets_hours for e in moderate),
        exercise_mets_hours=sum(e.mets_hours for e in moderate if e.activity.is_exercise),
        strength_days=len({e.day for e in entries if e.activity.is_strength}),
        # 消費エネルギー (kcal) ≒ 1.05 × メッツ・時 × 体重 (kg)
        energy_kcal=sum(1.05 * e.mets_hours * weight_kg for e in entries),
    )


def daily_mets_hours(entries: list[Entry]) -> dict[str, float]:
    """曜日ごとの 3 メッツ以上の身体活動量 (メッツ・時) を求める。"""
    totals = {day: 0.0 for day in DAYS}
    for entry in entries:
        if entry.activity.mets >= MODERATE_METS:
            totals[entry.day] += entry.mets_hours
    return totals


def judge(value: float, target: float) -> str:
    """推奨値を満たしているかどうかを「達成」か「未達」で返す。"""
    return "達成" if value >= target else "未達"


def format_report(entries: list[Entry], summary: WeeklySummary) -> str:
    """集計結果を、人が読みやすい文章にする。"""
    lines = ["曜日ごとの身体活動量 (3 メッツ以上)"]
    for day, value in daily_mets_hours(entries).items():
        lines.append(f"  {day}: {value:4.1f} メッツ・時")
    lines += [
        "",
        f"身体活動 : {summary.activity_mets_hours:4.1f} メッツ・時/週 "
        f"(目安 {TARGET_ACTIVITY:.0f} 以上) {judge(summary.activity_mets_hours, TARGET_ACTIVITY)}",
        f"運動     : {summary.exercise_mets_hours:4.1f} メッツ・時/週 "
        f"(目安 {TARGET_EXERCISE:.0f} 以上) {judge(summary.exercise_mets_hours, TARGET_EXERCISE)}",
        f"筋トレ   : {summary.strength_days} 日/週 "
        f"(目安 {TARGET_STRENGTH_DAYS}〜3 日) {judge(summary.strength_days, TARGET_STRENGTH_DAYS)}",
        f"消費エネルギー (記録した活動の合計) : 約 {summary.energy_kcal:,.0f} kcal",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="1 週間の身体活動量を計算する。")
    parser.add_argument("csv_file", type=Path, help="活動記録の CSV ファイル")
    parser.add_argument("--weight", type=float, default=60.0, help="体重 (kg)。既定値は 60")
    args = parser.parse_args()

    entries = load_entries(args.csv_file)
    print(format_report(entries, summarize(entries, args.weight)))


if __name__ == "__main__":
    main()
