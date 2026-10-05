"""テスト対象の関数（第 7 章、境界値分析の例）.

年齢から入場料金を求める。料金の区分は次のとおりである。

* 0 歳から 5 歳: 無料（0 円）
* 6 歳から 12 歳: 500 円
* 13 歳から 64 歳: 1000 円
* 65 歳以上: 700 円
* 負の年齢: 不正な入力として ValueError を送出する
"""


def admission_fee(age: int) -> int:
    """年齢 ``age`` に対応する入場料金（円）を返す."""
    if age < 0:
        raise ValueError("年齢は 0 以上を指定すること")
    if age <= 5:
        return 0
    if age <= 12:
        return 500
    if age <= 64:
        return 1000
    return 700


if __name__ == "__main__":
    for age in (3, 10, 30, 70):
        print(f"{age} 歳: {admission_fee(age)} 円")
