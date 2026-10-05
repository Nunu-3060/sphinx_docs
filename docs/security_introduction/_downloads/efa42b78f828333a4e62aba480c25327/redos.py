"""正規表現によるサービス拒否（ReDoS）のサンプル.

量指定子を入れ子にした正規表現は、一致しない入力に対して
バックトラックの回数が入力の長さに対して指数関数的に増えます。

実行方法:
    python redos.py
    （入力が長くなるにつれて、数秒かかることがあります）

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import re
import time

VULNERABLE = re.compile(r"^(a+)+$")  # 量指定子が入れ子になっている
SAFE = re.compile(r"^a+$")  # 同じ文字列に一致し、入れ子がない
MAX_INPUT_LENGTH = 64  # 対策: 入力の長さもあわせて制限する


def measure(pattern: re.Pattern[str], text: str) -> float:
    """パターンの照合にかかった時間（秒）を返す."""
    start = time.perf_counter()
    pattern.match(text)
    return time.perf_counter() - start


def is_valid(text: str) -> bool:
    """長さを制限したうえで、入れ子のないパターンで検証する（良い例）."""
    return len(text) <= MAX_INPUT_LENGTH and SAFE.match(text) is not None


def main() -> None:
    print("長さ  入れ子あり（秒）  入れ子なし（秒）")
    for length in range(14, 25, 2):
        # 最後に一致しない文字を置き、すべての組み合わせを試させる
        text = "a" * length + "!"
        slow = measure(VULNERABLE, text)
        fast = measure(SAFE, text)
        print(f"{length:4d}  {slow:16.4f}  {fast:16.6f}")
    print("入れ子ありは、長さが 2 増えるたびに時間が約 4 倍になります。")
    print(f"is_valid('aaaa') = {is_valid('aaaa')}")
    print(f"is_valid('a' * 100) = {is_valid('a' * 100)}")


if __name__ == "__main__":
    main()
