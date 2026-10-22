"""第 11 章「道具に頼る」のテストの例。

pytest がある場合は ``python -m pytest ch11_tools_test.py`` で、
無い場合は ``python ch11_tools_test.py`` でテストを実行できる。
"""


def average(values: list[float]) -> float:
    """数値の一覧の平均を返す。空の一覧を渡すと ValueError を送出する。"""
    if not values:
        raise ValueError("values が空である")
    return sum(values) / len(values)


def test_average_of_several_values() -> None:
    assert average([1.0, 2.0, 3.0]) == 2.0


def test_average_of_single_value() -> None:
    assert average([5.0]) == 5.0


def test_average_of_empty_list_raises_error() -> None:
    try:
        average([])
    except ValueError:
        return
    raise AssertionError("ValueError が送出されなかった")


if __name__ == "__main__":
    test_average_of_several_values()
    test_average_of_single_value()
    test_average_of_empty_list_raises_error()
    print("すべてのテストに合格した")
