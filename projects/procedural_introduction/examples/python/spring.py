"""ばねと減衰による追従（第 12 章）。

目標値 target を、固有振動数 frequency [Hz] と減衰比 damping で決まる 2 次系として追う。
どの関数も配列を受け取り、要素ごとに独立に計算する（複数の値や 2 次元の位置をまとめて扱える）。
"""

from __future__ import annotations

import math

import numpy as np

from common import FloatArray


def spring_step(
    x: FloatArray, v: FloatArray, target: FloatArray, frequency: float, damping: float, dt: float
) -> tuple[FloatArray, FloatArray]:
    """位置 x・速度 v を時間 dt だけ進める（半陰的オイラー法）。

    加速度は a = ω²(target - x) - 2ζω v（ω = 2π frequency、ζ = damping）。
    先に速度を更新し、新しい速度で位置を進める。
    """
    omega = 2.0 * math.pi * frequency
    a = omega * omega * (target - x) - 2.0 * damping * omega * v
    v = v + a * dt
    x = x + v * dt
    return x, v


def spring_substeps(
    x: FloatArray, v: FloatArray, target: FloatArray, frequency: float, damping: float, dt: float,
    max_step: float = 1.0 / 120.0,
) -> tuple[FloatArray, FloatArray]:
    """dt が max_step より長いときは、等分した小さな刻みに分けて進める（硬いばねでも安定させる）。"""
    count = max(1, math.ceil(dt / max_step))
    for _ in range(count):
        x, v = spring_step(x, v, target, frequency, damping, dt / count)
    return x, v


def smooth_toward(x: FloatArray, target: FloatArray, rate: float, dt: float) -> FloatArray:
    """指数関数的に目標値へ近づける。rate [1/s] が大きいほど速い。フレームレートに依存しない。"""
    result: FloatArray = x + (target - x) * (1.0 - np.exp(-rate * dt))
    return result
