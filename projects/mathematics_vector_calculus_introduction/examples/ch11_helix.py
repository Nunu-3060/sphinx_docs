"""らせん状の針金の質量（スカラー場の線積分）と、重力がする仕事（ベクトル場の線積分）を計算する.

使い方: python ch11_helix.py
"""

import math

import numpy as np
from numpy.typing import NDArray
from scipy import integrate

Vec = NDArray[np.float64]


def helix(t: float) -> Vec:
    """らせん r(t) = (cos t, sin t, t)."""
    return np.array([math.cos(t), math.sin(t), t])


def helix_velocity(t: float) -> Vec:
    """らせんの速度 r'(t) = (-sin t, cos t, 1)."""
    return np.array([-math.sin(t), math.cos(t), 1.0])


def wire_mass() -> float:
    """線密度 μ = z の針金の質量 ∫_C μ ds = ∫ μ(r(t)) |r'(t)| dt."""
    value, _ = integrate.quad(lambda t: helix(t)[2] * float(np.linalg.norm(helix_velocity(t))),
                              0.0, 2.0 * math.pi)
    return float(value)


def gravity_work_helix(m: float, g: float) -> float:
    """重力 F = (0, 0, -mg) が、らせんを t = 2π から t = 0 まで下る物体にする仕事."""
    force = np.array([0.0, 0.0, -m * g])
    # t を 2π から 0 へ逆向きにたどるので、積分の上端と下端を入れ替える
    value, _ = integrate.quad(lambda t: float(force @ helix_velocity(t)), 2.0 * math.pi, 0.0)
    return float(value)


def gravity_work_straight(m: float, g: float) -> float:
    """同じ 2 点を結ぶ線分 r(s) = (1, 0, 2π(1 - s)) に沿って、重力がする仕事."""
    force = np.array([0.0, 0.0, -m * g])
    velocity = np.array([0.0, 0.0, -2.0 * math.pi])
    value, _ = integrate.quad(lambda s: float(force @ velocity), 0.0, 1.0)
    return float(value)


def report() -> None:
    """計算結果を、手計算の値と並べて表示する."""
    print(f"針金の質量: {wire_mass():.6f}  (厳密な値 2*sqrt(2)*pi^2 = {2.0 * math.sqrt(2.0) * math.pi**2:.6f})")
    m, g = 1.0, 9.8
    print(f"重力の仕事（らせんに沿って下る）: {gravity_work_helix(m, g):.6f} J")
    print(f"重力の仕事（まっすぐ下る）      : {gravity_work_straight(m, g):.6f} J")
    print(f"位置エネルギーの減少 m g h      : {m * g * 2.0 * math.pi:.6f} J")


def main() -> None:
    report()


if __name__ == "__main__":
    main()
