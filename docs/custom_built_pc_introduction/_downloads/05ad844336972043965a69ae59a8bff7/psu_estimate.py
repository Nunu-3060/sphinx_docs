"""電源ユニットの推奨容量を見積もるスクリプト.

CPU、GPU、その他のパーツの最大消費電力を合計し、余裕係数を掛けた値を求める。
その値以上となる最小の一般的な電源容量を推奨容量として表示する。

使い方::

    python psu_estimate.py --cpu 120 --gpu 250 --other 75
    python psu_estimate.py --cpu 120 --gpu 250 --other 75 --margin 1.6
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

# 市販の電源ユニットでよく見られる定格容量 [W]
COMMON_CAPACITIES: tuple[int, ...] = (450, 550, 650, 750, 850, 1000, 1200, 1300, 1600)

# 既定の余裕係数 (合計消費電力が定格容量の約 3 分の 2 に収まる)
DEFAULT_MARGIN = 1.5


@dataclass(frozen=True)
class PowerEstimate:
    """見積もり結果."""

    total_watts: float
    """各パーツの最大消費電力の合計 [W]."""

    required_watts: float
    """合計に余裕係数を掛けた必要容量 [W]."""

    recommended_watts: int | None
    """推奨する定格容量 [W]。該当する容量が無い場合は None."""


def estimate(cpu: float, gpu: float, other: float, margin: float = DEFAULT_MARGIN) -> PowerEstimate:
    """最大消費電力から推奨する電源容量を求める.

    Args:
        cpu: CPU の最大消費電力 [W]。TDP ではなく最大値 (PL2 や PPT) を指定する。
        gpu: GPU の最大消費電力 [W]。内蔵 GPU のみの場合は 0 を指定する。
        other: マザーボード、メモリ、ストレージ、ファンなどの合計 [W]。
        margin: 余裕係数。1.0 以上を指定する。

    Returns:
        見積もり結果。

    Raises:
        ValueError: 消費電力が負の値、または余裕係数が 1.0 未満の場合。
    """
    if min(cpu, gpu, other) < 0:
        raise ValueError("消費電力には 0 以上の値を指定してください。")
    if margin < 1.0:
        raise ValueError("余裕係数には 1.0 以上の値を指定してください。")

    total = cpu + gpu + other
    required = total * margin
    recommended = next((c for c in COMMON_CAPACITIES if c >= required), None)
    return PowerEstimate(total_watts=total, required_watts=required, recommended_watts=recommended)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """コマンドライン引数を解析する."""
    parser = argparse.ArgumentParser(description="電源ユニットの推奨容量を見積もる。")
    parser.add_argument("--cpu", type=float, required=True, help="CPU の最大消費電力 [W]")
    parser.add_argument("--gpu", type=float, default=0.0, help="GPU の最大消費電力 [W] (既定値: 0)")
    parser.add_argument("--other", type=float, default=60.0, help="その他のパーツの合計 [W] (既定値: 60)")
    parser.add_argument("--margin", type=float, default=DEFAULT_MARGIN,
                        help=f"余裕係数 (既定値: {DEFAULT_MARGIN})")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """エントリーポイント."""
    args = parse_args(argv)
    try:
        result = estimate(args.cpu, args.gpu, args.other, args.margin)
    except ValueError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1

    print(f"合計消費電力 : {result.total_watts:.0f} W")
    print(f"必要容量     : {result.required_watts:.0f} W (余裕係数 {args.margin})")
    if result.recommended_watts is None:
        print(f"推奨容量     : {COMMON_CAPACITIES[-1]} W を超えるため、構成を見直してください。")
    else:
        print(f"推奨容量     : {result.recommended_watts} W")
    return 0


if __name__ == "__main__":
    sys.exit(main())
