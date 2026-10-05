"""第 12 章: 同値分割と境界値分析に基づいて単体試験を書く。

リチウムイオン電池の電圧 [mV] から、残量の状態を判定する関数を
試験します。仕様は次のとおりです。

* 0 mV 未満または 5000 mV を超える値は、センサーの異常として
  ValueError を送出する
* 3300 mV 未満は「要充電」
* 3300 mV 以上 4000 mV 未満は「通常」
* 4000 mV 以上は「満充電」

実行例::

    python ch12_boundary_test.py -v
"""

from __future__ import annotations

import unittest

LOW_THRESHOLD_MV = 3300
FULL_THRESHOLD_MV = 4000
SENSOR_MIN_MV = 0
SENSOR_MAX_MV = 5000


def battery_state(voltage_mv: int) -> str:
    """電池の電圧 [mV] から残量の状態を返す。"""
    if not SENSOR_MIN_MV <= voltage_mv <= SENSOR_MAX_MV:
        raise ValueError(f"電圧が測定範囲外です: {voltage_mv} mV")
    if voltage_mv < LOW_THRESHOLD_MV:
        return "要充電"
    if voltage_mv < FULL_THRESHOLD_MV:
        return "通常"
    return "満充電"


class BatteryStateTest(unittest.TestCase):
    """battery_state() の単体試験。"""

    def test_representative_values(self) -> None:
        """同値分割: 各区間の代表値で 1 回ずつ確かめる。"""
        cases = [(2000, "要充電"), (3700, "通常"), (4500, "満充電")]
        for voltage, expected in cases:
            with self.subTest(voltage=voltage):
                self.assertEqual(battery_state(voltage), expected)

    def test_boundaries(self) -> None:
        """境界値分析: 区間の境目の両側を確かめる。"""
        cases = [
            (0, "要充電"),
            (3299, "要充電"),
            (3300, "通常"),
            (3999, "通常"),
            (4000, "満充電"),
            (5000, "満充電"),
        ]
        for voltage, expected in cases:
            with self.subTest(voltage=voltage):
                self.assertEqual(battery_state(voltage), expected)

    def test_out_of_range(self) -> None:
        """異常値: 測定範囲のすぐ外側では例外を送出する。"""
        for voltage in (-1, 5001):
            with self.subTest(voltage=voltage):
                with self.assertRaises(ValueError):
                    battery_state(voltage)


if __name__ == "__main__":
    unittest.main()
