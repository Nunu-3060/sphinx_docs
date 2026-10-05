"""第 14 章: フォールトツリーから頂上事象の発生確率を計算する。

電気ポットの「空だき」による過熱を頂上事象とする、簡単な
フォールトツリーを考えます。

* 頂上事象: 過熱 = 空だき状態 AND 保護機能がすべて失敗
* 空だき状態 = 水位センサーの故障 OR 利用者が水を入れ忘れる
* 保護機能の失敗 = 温度ヒューズの故障 AND 制御ソフトウェアの
  温度監視の失敗

各基本事象は互いに独立と仮定し、AND ゲートは確率の積、
OR ゲートは 1 - (1 - p1)(1 - p2)… で計算します。

実行例::

    python ch14_fault_tree.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class Event:
    """フォールトツリーの事象。

    基本事象は probability を持ち、中間事象・頂上事象は gate ("AND" または
    "OR") と下位の事象 children を持ちます。
    """

    name: str
    probability: float | None = None
    gate: str | None = None
    children: list[Event] = field(default_factory=list)

    def evaluate(self) -> float:
        """この事象の発生確率を計算する。"""
        if self.probability is not None:
            return self.probability
        values = [child.evaluate() for child in self.children]
        if self.gate == "AND":
            return math.prod(values)
        if self.gate == "OR":
            return 1 - math.prod(1 - p for p in values)
        raise ValueError(f"未知のゲートです: {self.gate}")

    def show(self, indent: int = 0) -> None:
        """木構造と各事象の確率を表示する。"""
        label = f"[{self.gate}] " if self.gate else ""
        print(f"{'  ' * indent}{label}{self.name}: {self.evaluate():.2e}")
        for child in self.children:
            child.show(indent + 1)


def build_tree(software_failure: float) -> Event:
    """フォールトツリーを組み立てる。確率は 1 回の使用あたりの値。"""
    dry = Event("空だき状態", gate="OR", children=[
        Event("水位センサーの故障", probability=1e-4),
        Event("水の入れ忘れ", probability=1e-2),
    ])
    protection = Event("保護機能の失敗", gate="AND", children=[
        Event("温度ヒューズの故障", probability=1e-4),
        Event("温度監視ソフトウェアの失敗", probability=software_failure),
    ])
    return Event("過熱", gate="AND", children=[dry, protection])


def main() -> None:
    top = build_tree(software_failure=1e-3)
    top.show()

    print("\n温度監視ソフトウェアの失敗確率を変えたときの頂上事象の確率")
    for p in (1e-1, 1e-2, 1e-3, 1e-4):
        print(f"  {p:.0e} -> {build_tree(p).evaluate():.2e}")
    print("\n保護機能をソフトウェアだけにした場合 (温度ヒューズなし)")
    dry = top.children[0].evaluate()
    print(f"  空だき状態 {dry:.2e} × ソフトウェアの失敗 1e-03 "
          f"= {dry * 1e-3:.2e}")


if __name__ == "__main__":
    main()
