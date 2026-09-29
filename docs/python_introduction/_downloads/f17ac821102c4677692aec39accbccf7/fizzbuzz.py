"""条件分岐と繰り返しの基本を示す FizzBuzz のサンプルです。"""


def fizzbuzz(number: int) -> str:
    """数値を受け取り、FizzBuzz のルールに従った文字列を返します。"""
    if number % 15 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    else:
        return str(number)


def main() -> None:
    """1 から 20 までの数値に対して FizzBuzz の結果を表示します。"""
    number: int = 1
    while number <= 20:
        print(fizzbuzz(number))
        number += 1


if __name__ == "__main__":
    main()
