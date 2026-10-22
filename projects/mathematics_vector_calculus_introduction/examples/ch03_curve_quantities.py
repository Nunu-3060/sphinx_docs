"""らせんの弧長と曲率を、公式（SymPy）と数値計算（SciPy、NumPy）で求めて比べる.

使い方: python ch03_curve_quantities.py
"""

import numpy as np
import sympy as sp
from numpy.typing import NDArray
from scipy import integrate

import vc_plot

A = 1.0  # らせんの半径 a
B = 0.25  # 1 ラジアンあたりに z 方向へ進む量 b


def velocity(t: float) -> NDArray[np.float64]:
    """らせん r(t) = (a cos t, a sin t, b t) の速度 r'(t) を返す."""
    return np.array([-A * np.sin(t), A * np.cos(t), B])


def acceleration(t: float) -> NDArray[np.float64]:
    """らせんの加速度 r''(t) を返す."""
    return np.array([-A * np.cos(t), -A * np.sin(t), 0.0])


def arc_length(t0: float, t1: float) -> float:
    """t0 から t1 までの弧長（|r'(t)| の積分）を数値積分で求める."""
    value, _ = integrate.quad(lambda t: float(np.linalg.norm(velocity(t))), t0, t1)
    return float(value)


def curvature(t: float) -> float:
    """曲率 κ = |r' × r''| / |r'|^3 を返す."""
    v = velocity(t)
    a = acceleration(t)
    return float(np.linalg.norm(np.cross(v, a)) / np.linalg.norm(v) ** 3)


def report() -> None:
    """弧長と曲率の式を SymPy で導き、数値計算の結果と比べる."""
    t = sp.symbols("t", real=True)
    a, b = sp.symbols("a b", positive=True)
    r = sp.Matrix([a * sp.cos(t), a * sp.sin(t), b * t])
    v = r.diff(t)
    acc = v.diff(t)
    speed = sp.simplify(sp.sqrt(v.dot(v)))
    cross = v.cross(acc)
    kappa = sp.simplify(sp.sqrt(sp.simplify(cross.dot(cross))) / speed**3)
    print(f"|r'(t)| = {speed}")
    print(f"κ       = {kappa}")

    exact_length = 2.0 * np.pi * np.sqrt(A**2 + B**2)
    exact_kappa = A / (A**2 + B**2)
    print(f"a = {A}, b = {B} のとき")
    print(f"1 周分の弧長：式 {exact_length:.6f}、数値積分 {arc_length(0.0, 2.0 * np.pi):.6f}")
    for ti in (0.0, 1.0, 2.0):
        print(f"t = {ti:.1f} の曲率：式 {exact_kappa:.6f}、数値計算 {curvature(ti):.6f}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
