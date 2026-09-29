"""本資料で使うサンプルデータ（架空の生徒の成績）を作成する。

実行すると、このファイルと同じフォルダーにある data/scores.csv を
作成（上書き）する。乱数のシードを固定しているため、何度実行しても
同じデータになる。
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 2024
STUDENTS_PER_CLASS = 50
OUTPUT_PATH = Path(__file__).parent / "data" / "scores.csv"


def make_scores(rng: np.random.Generator) -> pd.DataFrame:
    """2 クラス分の架空の成績データを作成する。

    Args:
        rng: 乱数生成器

    Returns:
        列 student_id, class, club, study_hours, math, english を持つ表
    """
    n = STUDENTS_PER_CLASS * 2
    classes = np.repeat(["A", "B"], STUDENTS_PER_CLASS)
    clubs = rng.choice(["sports", "culture", "none"], size=n,
                       p=[0.4, 0.3, 0.3])
    # 1 日あたりの平均学習時間（0.0 ～ 6.0 時間、0.1 時間刻み）
    study_hours = np.round(rng.uniform(0.0, 6.0, size=n), 1)

    # 学習時間が長いほど点数が高くなるようにし、クラスと部活動の影響も
    # 少し加える。最後に 0 ～ 100 点の整数に丸める。
    class_effect = np.where(classes == "B", 5.0, 0.0)
    club_effect = np.where(clubs == "culture", 4.0, 0.0)
    math = (35.0 + 6.0 * study_hours + class_effect + club_effect
            + rng.normal(0.0, 10.0, size=n))
    english = 40.0 + 4.0 * study_hours + rng.normal(0.0, 12.0, size=n)

    return pd.DataFrame({
        "student_id": np.arange(1, n + 1),
        "class": classes,
        "club": clubs,
        "study_hours": study_hours,
        "math": np.clip(np.round(math), 0, 100).astype(int),
        "english": np.clip(np.round(english), 0, 100).astype(int),
    })


def main() -> None:
    """サンプルデータを作成して CSV ファイルに保存する。"""
    rng = np.random.default_rng(SEED)
    scores = make_scores(rng)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    scores.to_csv(OUTPUT_PATH, index=False)
    print(f"{OUTPUT_PATH} を作成しました（{len(scores)} 行）。")


if __name__ == "__main__":
    main()
