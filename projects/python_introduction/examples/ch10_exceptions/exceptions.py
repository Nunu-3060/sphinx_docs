"""例外処理の基本的な書き方を示すサンプルです。"""


class InvalidScoreError(Exception):
    """点数が正しい範囲外である場合に送出される例外です。"""


def validate_score(score: int) -> int:
    """点数を検証し、0 から 100 の範囲外であれば例外を送出します。"""
    if score < 0 or score > 100:
        raise InvalidScoreError(f"点数は 0 から 100 の範囲で指定してください: {score}")
    return score


def divide(a: int, b: int) -> float:
    """2 つの整数を受け取り、除算した結果を返します。"""
    try:
        result: float = a / b
    except ZeroDivisionError:
        print("エラー: 0 で割ることはできません。")
        return 0.0
    else:
        return result
    finally:
        print(f"{a} を {b} で割る処理を実行しました。")


def main() -> None:
    """例外処理の使用例を表示します。"""
    print("10 ÷ 2 =", divide(10, 2))
    print("10 ÷ 0 =", divide(10, 0))

    try:
        validate_score(150)
    except InvalidScoreError as error:
        print("エラー:", error)


if __name__ == "__main__":
    main()
