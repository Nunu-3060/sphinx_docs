"""SIMT の分岐ダイバージェンスのシミュレーター。

ワープ（32 スレッド）が次のようなカーネルを実行するときのサイクル数を数えます。

    共通の処理（COMMON 命令）
    if (条件) { THEN 命令 } else { ELSE 命令 }
    共通の処理（COMMON 命令）

モデル: ワープは 1 サイクルに 1 命令を 32 レーンに同時に発行します。
分岐の両側に実行すべきスレッドがいれば、両方の経路を順に実行し、
条件を満たさないレーンはマスク（アクティブマスク）で止めておきます。
条件の異なる 4 種類の分岐について、4 ワープ（128 スレッド）分の
サイクル数とレーンの利用率を比べます。

実行方法: python gpu_simt_sim.py
"""

from collections.abc import Callable

WARP_SIZE = 32
NUM_WARPS = 4
COMMON = 10  # 分岐の前後の共通部分の命令数（前後それぞれ）
THEN = 20  # if 側の命令数
ELSE = 20  # else 側の命令数


def run_warp(warp: int, cond: Callable[[int], bool],
             verbose: bool = False) -> tuple[int, int]:
    """1 ワープを実行し、（サイクル数、有効なレーン×サイクル）を返す。"""
    tids = range(warp * WARP_SIZE, (warp + 1) * WARP_SIZE)
    # 条件を満たすレーンのビットを立てたマスク（ビット i がレーン i）
    mask = 0
    for lane, tid in enumerate(tids):
        if cond(tid):
            mask |= 1 << lane
    full = (1 << WARP_SIZE) - 1
    # （区間名、命令数、アクティブマスク）の列。空のマスクの経路は飛ばす
    phases = [("共通", COMMON, full)]
    if mask:
        phases.append(("then", THEN, mask))
    if mask != full:
        phases.append(("else", ELSE, full & ~mask))
    phases.append(("共通", COMMON, full))
    cycles = 0
    useful = 0
    for name, n, active in phases:
        if verbose:
            print(f"  マスク 0x{active:08X}  {n:>2} サイクル  {name}")
        cycles += n
        useful += n * bin(active).count("1")
    return cycles, useful


def main() -> None:
    cases: list[tuple[str, Callable[[int], bool]]] = [
        ("分岐なし（全員 then）", lambda t: True),
        ("半分ずつ（レーン < 16）", lambda t: t % WARP_SIZE < 16),
        ("偶奇（tid % 2 == 0）", lambda t: t % 2 == 0),
        ("ワープ単位（warp % 2 == 0）", lambda t: (t // WARP_SIZE) % 2 == 0),
    ]
    print("ワープ 0 の実行の様子（偶奇で分岐する場合）")
    run_warp(0, cases[2][1], verbose=True)
    print()
    print(f"{NUM_WARPS} ワープ（{NUM_WARPS * WARP_SIZE} スレッド）の合計")
    for label, cond in cases:
        total = 0
        useful = 0
        for w in range(NUM_WARPS):
            c, u = run_warp(w, cond)
            total += c
            useful += u
        util = useful / (total * WARP_SIZE)
        print(f"  {total:>4} サイクル  レーン利用率 {util:6.1%}  {label}")


if __name__ == "__main__":
    main()
