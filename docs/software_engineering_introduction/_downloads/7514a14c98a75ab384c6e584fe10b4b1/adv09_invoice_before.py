"""発展課題 9-A の対象となるレガシーコード（第 9 章）.

請求書の文字列を作る関数。テストがなく、名前やマジックナンバーから
仕様を読み取りにくい。この関数をリファクタリングすることが課題である。
"""


def inv(d: list[tuple[str, int, int]], m: bool) -> str:
    s = ""
    t = 0
    for x in d:
        s = s + x[0] + " x" + str(x[2]) + " = " + str(x[1] * x[2]) + "\n"
        t = t + x[1] * x[2]
    if m:
        if t >= 3000:
            t = t * 95 // 100
    else:
        if t < 5000:
            t = t + 500
    s = s + "合計 " + str(t)
    return s


if __name__ == "__main__":
    print(inv([("ノート", 300, 4), ("ペン", 150, 10)], True))
