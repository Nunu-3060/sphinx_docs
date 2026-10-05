"""第 6 章: PID 制御のシミュレーションを行う。

制御対象として、2 つの 1 次遅れ要素を直列につないだ系
(時定数 1.0 s と 0.5 s、ゲイン 1) を考えます。モーターの回転速度や
ヒーターの温度など、多くの機器がこれに近い振る舞いをします。

この対象を、P 制御、PI 制御、PID 制御で目標値 1.0 に追従させ、
応答を比較します。コントローラーは 10 ms ごとに計算する
離散時間の制御とし、実際のマイコンやソフトウェアでの実装に
近い形にしています。

図は ch06_pid.png として保存します。

実行例::

    python ch06_pid.py --outdir output
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure
from numpy.typing import NDArray

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

TAU1 = 1.0  # 1 つ目の 1 次遅れ要素の時定数 [s]
TAU2 = 0.5  # 2 つ目の 1 次遅れ要素の時定数 [s]
CONTROL_PERIOD = 0.01  # コントローラーの計算周期 [s]
PLANT_SUBSTEPS = 10  # 制御周期 1 回あたりの制御対象の積分回数
SETPOINT = 1.0  # 目標値
T_END = 10.0  # シミュレーションの終了時刻 [s]

Array = NDArray[np.float64]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


@dataclass
class PidController:
    """離散時間の PID コントローラー。"""

    kp: float  # 比例ゲイン
    ki: float  # 積分ゲイン
    kd: float  # 微分ゲイン
    dt: float  # 計算周期 [s]
    integral: float = 0.0
    previous_measurement: float | None = None

    def update(self, setpoint: float, measurement: float) -> float:
        """目標値と測定値から操作量を計算する。"""
        error = setpoint - measurement
        self.integral += error * self.dt

        # 微分は偏差ではなく測定値に対して行う。目標値が急に変わった
        # ときに操作量が跳ね上がる現象 (微分キック) を避けるため。
        if self.previous_measurement is None:
            derivative = 0.0
        else:
            derivative = -(measurement - self.previous_measurement) / self.dt
        self.previous_measurement = measurement

        return self.kp * error + self.ki * self.integral + self.kd * derivative


def simulate(controller: PidController) -> tuple[Array, Array]:
    """閉ループ系をシミュレーションし、時刻と出力を返す。"""
    steps = int(round(T_END / CONTROL_PERIOD))
    times = np.arange(steps + 1, dtype=np.float64) * CONTROL_PERIOD
    outputs = np.empty(steps + 1)
    x1 = x2 = 0.0  # 1 つ目と 2 つ目の要素の出力
    h = CONTROL_PERIOD / PLANT_SUBSTEPS
    for i in range(steps + 1):
        outputs[i] = x2
        u = controller.update(SETPOINT, x2)
        # 次の計算周期まで操作量 u を一定に保ち、制御対象を進める
        for _ in range(PLANT_SUBSTEPS):
            x1 += h * (u - x1) / TAU1
            x2 += h * (x1 - x2) / TAU2
    return times, outputs


def describe(times: Array, outputs: Array) -> str:
    """最大行き過ぎ量、整定時間、定常偏差を文字列にまとめる。"""
    final = float(np.mean(outputs[-100:]))
    overshoot = max(0.0, (float(np.max(outputs)) - final) / final * 100)
    # 最終値の ±2 % の範囲に入ったまま出なくなる時刻を整定時間とする
    outside = np.nonzero(np.abs(outputs - final) > 0.02 * abs(final))[0]
    settling = float(times[outside[-1] + 1]) if outside.size else 0.0
    error = SETPOINT - final
    return (f"行き過ぎ量 {overshoot:5.1f} %, 整定時間 {settling:5.2f} s, "
            f"定常偏差 {error:6.3f}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    cases = {
        "P 制御 (Kp = 2)": (2.0, 0.0, 0.0),
        "P 制御 (Kp = 10)": (10.0, 0.0, 0.0),
        "PI 制御 (Kp = 2, Ki = 2)": (2.0, 2.0, 0.0),
        "PID 制御 (Kp = 6, Ki = 4, Kd = 1.5)": (6.0, 4.0, 1.5),
    }

    setup_font()
    fig = Figure(figsize=(8, 4.5), layout="constrained")
    ax = fig.add_subplot()
    for label, (kp, ki, kd) in cases.items():
        controller = PidController(kp, ki, kd, CONTROL_PERIOD)
        times, outputs = simulate(controller)
        print(f"{label:36s}: {describe(times, outputs)}")
        ax.plot(times, outputs, label=label)
    ax.axhline(SETPOINT, color="gray", linestyle=":", label="目標値")
    ax.set_xlabel("時刻 [s]")
    ax.set_ylabel("出力")
    ax.set_title("制御方式とゲインによる応答の違い")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right")
    fig.savefig(outdir / "ch06_pid.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
