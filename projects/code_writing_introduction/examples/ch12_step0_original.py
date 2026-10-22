"""第 12 章「実践：悪いコードを直してみる」の元のコード。"""


def main(d: list[tuple[str, int, int, int]]) -> None:
    t2 = 0
    for s in d:
        t = s[1] + s[2] + s[3]
        a = t / 3
        if a >= 80:
            g = "A"
        else:
            if a >= 60:
                g = "B"
            else:
                g = "C"
        print(s[0] + ": 合計 " + str(t) + " 点, 平均 " + str(round(a, 1)) + " 点, 評価 " + g)
    for s in d:
        t2 += s[1] + s[2] + s[3]
    print("全体の平均: " + str(round(t2 / (len(d) * 3), 1)) + " 点")


if __name__ == "__main__":
    main([("佐藤", 85, 90, 78), ("鈴木", 60, 55, 70), ("高橋", 40, 52, 38)])
