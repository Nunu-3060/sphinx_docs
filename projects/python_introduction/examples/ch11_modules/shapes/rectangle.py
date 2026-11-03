"""長方形に関する計算を行うモジュール。"""


def calculate_area(width: float, height: float) -> float:
    """長方形の面積を計算して返す。"""
    return width * height


def calculate_perimeter(width: float, height: float) -> float:
    """長方形の周囲の長さを計算して返す。"""
    return (width + height) * 2
