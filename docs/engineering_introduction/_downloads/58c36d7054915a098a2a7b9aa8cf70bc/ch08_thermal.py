"""第 8 章: 熱抵抗を使って半導体の温度を見積もり、放熱器を選ぶ。

12 V から 5 V を作り、0.5 A を流すリニアレギュレーター (TO-220
パッケージ) を例に、次のことを確かめます。

1. 定常状態のジャンクション温度を、熱抵抗の直列回路で計算する
2. 温度の上限を守るために必要な放熱器の熱抵抗を求める
3. スイッチングレギュレーターに替えた場合の損失と比べる
4. 電源を入れてから温度が上がっていく様子 (過渡応答) を図にする
   (ch08_thermal.png)

熱抵抗や熱容量の値は、説明のための代表的な値です。実際の設計では
部品のデータシートの値を使ってください。

実行例::

    python ch08_thermal.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

V_IN = 12.0  # 入力電圧 [V]
V_OUT = 5.0  # 出力電圧 [V]
CURRENT = 0.5  # 出力電流 [A]
T_AMBIENT = 50.0  # 想定する最高の周囲温度 [℃]
T_J_MAX = 125.0  # ジャンクション温度の絶対最大定格 [℃]
T_J_TARGET = 110.0  # 設計の目標 (定格に余裕を持たせた上限) [℃]
R_JA = 50.0  # 放熱器なしのジャンクション-周囲間の熱抵抗 [K/W]
R_JC = 5.0  # ジャンクション-ケース間の熱抵抗 [K/W]
R_CS = 0.5  # ケース-放熱器間 (放熱グリース) の熱抵抗 [K/W]
R_SA = 10.0  # 選んだ放熱器の熱抵抗 [K/W]
HEAT_CAPACITY = 30.0  # 部品と放熱器の熱容量 [J/K]
EFFICIENCY = 0.90  # スイッチングレギュレーターの効率


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def junction_temperature(power: float, resistance: float) -> float:
    """定常状態のジャンクション温度 Tj = Ta + P × Rθ を返す。"""
    return T_AMBIENT + power * resistance


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    # 1. リニアレギュレーターの損失は (入力電圧 - 出力電圧) × 電流
    power = (V_IN - V_OUT) * CURRENT
    efficiency = V_OUT / V_IN
    print(f"1. リニアレギュレーターの損失: {power:.2f} W "
          f"(効率 {efficiency:.0%})")
    t_bare = junction_temperature(power, R_JA)
    print(f"   放熱器なし: Tj = {t_bare:.0f} ℃ "
          f"(定格 {T_J_MAX:.0f} ℃ を超える)")

    # 2. 必要な放熱器の熱抵抗
    r_total_max = (T_J_TARGET - T_AMBIENT) / power
    r_sa_max = r_total_max - R_JC - R_CS
    print(f"2. Tj を {T_J_TARGET:.0f} ℃ 以下にするには、熱抵抗の合計を "
          f"{r_total_max:.1f} K/W 以下にする必要があります。")
    print(f"   放熱器の熱抵抗: {r_sa_max:.1f} K/W 以下")
    r_total = R_JC + R_CS + R_SA
    t_sink = junction_temperature(power, r_total)
    print(f"   {R_SA:.0f} K/W の放熱器を使うと: Tj = {t_sink:.1f} ℃")

    # 3. スイッチングレギュレーターの損失
    p_out = V_OUT * CURRENT
    p_loss = p_out / EFFICIENCY - p_out
    t_switching = junction_temperature(p_loss, R_JA)
    print(f"3. 効率 {EFFICIENCY:.0%} のスイッチングレギュレーター: "
          f"損失 {p_loss:.2f} W、放熱器なしで Tj = {t_switching:.0f} ℃")

    # 4. 過渡応答 (1 次遅れ系として近似)
    tau = r_total * HEAT_CAPACITY
    print(f"4. 熱時定数: {tau:.0f} s (約 {tau / 60:.1f} 分)")
    t = np.linspace(0.0, 2500.0, 500)
    temperature = T_AMBIENT + power * r_total * (1 - np.exp(-t / tau))

    setup_font()
    fig = Figure(figsize=(7, 4), layout="constrained")
    ax = fig.add_subplot()
    ax.plot(t / 60, temperature, label="ジャンクション温度")
    ax.axhline(T_J_MAX, color="tab:red", linestyle="--",
               label=f"絶対最大定格 {T_J_MAX:.0f} ℃")
    ax.axhline(T_J_TARGET, color="tab:orange", linestyle=":",
               label=f"設計の目標 {T_J_TARGET:.0f} ℃")
    ax.axvline(tau / 60, color="gray", linestyle=":")
    ax.annotate("熱時定数", xy=(tau / 60, T_AMBIENT + 5),
                xytext=(tau / 60 + 2, T_AMBIENT + 5))
    ax.set_xlabel("電源を入れてからの時間 [分]")
    ax.set_ylabel("温度 [℃]")
    ax.set_ylim(40, 135)
    ax.set_title(f"放熱器 ({R_SA:.0f} K/W) 付きの温度上昇 "
                 f"(周囲温度 {T_AMBIENT:.0f} ℃)")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right")
    fig.savefig(outdir / "ch08_thermal.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
