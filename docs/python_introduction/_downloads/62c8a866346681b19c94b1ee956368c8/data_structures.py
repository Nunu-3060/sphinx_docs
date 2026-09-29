"""リスト、タプル、辞書、集合の基本的な操作を示すサンプルです。"""


def summarize_scores(scores: list[int]) -> float:
    """点数のリストを受け取り、平均点を返します。"""
    return sum(scores) / len(scores)


def squares_of(numbers: list[int]) -> list[int]:
    """整数のリストを受け取り、各要素を 2 乗したリストをリスト内包表記で返します。"""
    return [number ** 2 for number in numbers]


def squares_dict_of(numbers: list[int]) -> dict[int, int]:
    """整数のリストを受け取り、各要素とその 2 乗を対応させた辞書を辞書内包表記で返します。"""
    return {number: number ** 2 for number in numbers}


def unique_squares_of(numbers: list[int]) -> set[int]:
    """整数のリストを受け取り、各要素を 2 乗した値の集合を集合内包表記で返します。"""
    return {number ** 2 for number in numbers}


def main() -> None:
    """代表的なデータ構造の使い方を表示します。"""
    fruits: list[str] = ["りんご", "みかん", "ぶどう"]
    print("先頭の要素:", fruits[0])
    print("末尾の要素:", fruits[-1])

    fruits.append("バナナ")
    fruits[1] = "メロン"
    print("果物のリスト:", fruits)

    point: tuple[int, int] = (3, 5)
    print("座標:", point)

    scores: list[int] = [80, 90, 70, 100]
    print("平均点:", summarize_scores(scores))

    person: dict[str, str | int] = {"name": "佐藤", "job": "エンジニア"}
    print("名前:", person["name"])
    print("職業:", person["job"])

    person["age"] = 30
    print("辞書全体:", person)

    numbers: list[int] = [1, 2, 2, 3, 3, 3]
    unique_numbers: set[int] = set(numbers)
    print("重複を除いた集合:", unique_numbers)

    print("点数を 2 乗したリスト:", squares_of(scores))
    print("点数と 2 乗の対応表:", squares_dict_of(scores))
    print("2 乗した値の集合:", unique_squares_of(numbers))


if __name__ == "__main__":
    main()
