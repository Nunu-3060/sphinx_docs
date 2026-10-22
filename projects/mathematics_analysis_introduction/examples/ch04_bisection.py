"""第 4 章「関数の極限と連続性」の数値実験：二分法。

方程式 x^3 - 2 = 0 の解（2 の立方根）を二分法で求め、
各反復での区間幅・実際の誤差・誤差の上界を表示する。

実行方法::

    python ch04_bisection.py
"""

from collections.abc import Callable


def bisection(
    f: Callable[[float], float], a: float, b: float, num_iterations: int
) -> list[tuple[float, float]]:
    """二分法で f(x) = 0 の解を含む区間を num_iterations 回だけ半分にする。

    f は区間 [a, b] で連続で、f(a) と f(b) の符号が異なるものとする。
    各反復の後の区間 (a_k, b_k) をリストで返す（先頭は初期区間）。
    """
    fa = f(a)
    if fa * f(b) > 0:
        raise ValueError("f(a) と f(b) の符号が同じである")
    intervals = [(a, b)]
    for _ in range(num_iterations):
        c = (a + b) / 2.0
        fc = f(c)
        if fc == 0.0:
            # 解がちょうど見つかった場合は幅 0 の区間にする
            a, b = c, c
        elif fa * fc < 0:
            # 解は左半分 [a, c] にある
            b = c
        else:
            # 解は右半分 [c, b] にある
            a, fa = c, fc
        intervals.append((a, b))
    return intervals


def iterations_needed(a: float, b: float, tolerance: float) -> int:
    """誤差を tolerance 以下にするのに必要な反復回数 k を返す。

    k 回反復後の中点の誤差は (b - a) / 2^(k+1) 以下なので、
    これが tolerance 以下となる最小の k を求める。
    """
    k = 0
    while (b - a) / 2.0 ** (k + 1) > tolerance:
        k += 1
    return k


def main() -> None:
    """2 の立方根を二分法で求め、誤差の推移を表示する。"""

    def f(x: float) -> float:
        return x**3 - 2.0

    true_root = 2.0 ** (1.0 / 3.0)
    a0, b0 = 1.0, 2.0
    intervals = bisection(f, a0, b0, 30)

    print("方程式 x^3 - 2 = 0 を区間 [1, 2] で二分法により解く")
    print("c_k: 区間の中点、error: |c_k - 2^(1/3)|、bound: 誤差の上界 (b - a) / 2^(k+1)")
    print(f"{'k':>3} {'a_k':>14} {'b_k':>14} {'c_k':>14} {'error':>12} {'bound':>12}")
    for k, (a, b) in enumerate(intervals):
        if k % 3 != 0:
            continue
        c = (a + b) / 2.0
        error = abs(c - true_root)
        bound = (b0 - a0) / 2.0 ** (k + 1)
        print(f"{k:>3} {a:>14.10f} {b:>14.10f} {c:>14.10f} {error:>12.3e} {bound:>12.3e}")
    print()
    print(f"真の値 2^(1/3) = {true_root:.10f}")
    print(f"誤差 1e-10 以下に必要な反復回数: {iterations_needed(a0, b0, 1e-10)}")


if __name__ == "__main__":
    main()
