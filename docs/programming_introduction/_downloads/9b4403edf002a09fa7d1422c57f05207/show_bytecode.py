"""Python の関数がどのようなバイトコードに変換されるかを表示する。"""

import dis


def add(a: int, b: int) -> int:
    """2 つの整数の和を返す。"""
    return a + b


def main() -> None:
    """add 関数のバイトコードを逆アセンブルして表示する。"""
    dis.dis(add)


if __name__ == "__main__":
    main()
