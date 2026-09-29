"""自作パッケージ shapes をインポートして利用するサンプルです。"""

from shapes import calculate_area, calculate_perimeter


def main() -> None:
    """長方形の面積と周囲の長さを計算して表示します。"""
    width: float = 4.0
    height: float = 3.0

    print("面積:", calculate_area(width, height))
    print("周囲の長さ:", calculate_perimeter(width, height))


if __name__ == "__main__":
    main()
