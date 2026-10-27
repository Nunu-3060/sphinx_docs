"""暗号で使う剰余演算の基本アルゴリズム。

- ユークリッドの互除法と拡張ユークリッド法
- モジュラ逆元
- 繰り返し二乗法による高速べき乗剰余
- 中国剰余定理

実行方法::

    python modular_arith.py
"""


def gcd(a: int, b: int) -> int:
    """ユークリッドの互除法で最大公約数を求める。"""
    while b:
        a, b = b, a % b
    return abs(a)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """a x + b y = g = gcd(a, b) を満たす (g, x, y) を返す。"""
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    return old_r, old_x, old_y


def mod_inverse(a: int, n: int) -> int:
    """a x ≡ 1 (mod n) を満たす x を返す。逆元が無ければ ValueError を送出する。"""
    g, x, _ = extended_gcd(a % n, n)
    if g != 1:
        raise ValueError(f"{a} は法 {n} で逆元を持たない")
    return x % n


def pow_mod(base: int, exponent: int, modulus: int) -> int:
    """繰り返し二乗法（左から右へのバイナリ法）で base^exponent mod modulus を求める。"""
    result = 1
    base %= modulus
    for bit in bin(exponent)[2:]:
        result = result * result % modulus
        if bit == "1":
            result = result * base % modulus
    return result


def crt(remainders: list[int], moduli: list[int]) -> int:
    """x ≡ r_i (mod m_i) を全て満たす 0 <= x < m_1 m_2 ... を返す（m_i は互いに素）。"""
    total_modulus = 1
    for m in moduli:
        total_modulus *= m
    x = 0
    for r, m in zip(remainders, moduli):
        partial = total_modulus // m
        x += r * partial * mod_inverse(partial, m)
    return x % total_modulus


def main() -> None:
    print(f"gcd(240, 46) = {gcd(240, 46)}")
    g, x, y = extended_gcd(240, 46)
    print(f"240 * ({x}) + 46 * ({y}) = {g}")
    print(f"7 の法 40 における逆元 = {mod_inverse(7, 40)}")
    print(f"3^200 mod 101 = {pow_mod(3, 200, 101)}（組み込み pow: {pow(3, 200, 101)}）")
    print(f"x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7) の解 = {crt([2, 3, 2], [3, 5, 7])}")


if __name__ == "__main__":
    main()
