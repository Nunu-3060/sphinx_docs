"""OS コマンドインジェクションとその対策のサンプル.

shell=True で利用者の入力を含むコマンド文字列を実行すると、入力に含まれる
「&」や「;」などの記号がシェルに解釈され、別のコマンドが実行されます。
このサンプルでは無害な echo コマンドだけを使います。

実行方法:
    python command_injection.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import subprocess
import sys


def greet_unsafe(name: str) -> str:
    """入力をコマンド文字列に連結し、シェル経由で実行する（悪い例）."""
    command = f"echo Hello, {name}"
    print(f"  シェルに渡す文字列: {command}")
    result = subprocess.run(command, shell=True, capture_output=True,
                            text=True, check=False)
    return result.stdout.strip()


def greet_safe(name: str) -> str:
    """コマンドと引数をリストで渡し、シェルを経由しない（良い例）.

    入力は 1 つの引数としてそのまま渡されるため、記号は解釈されない。
    """
    script = "import sys; print('Hello,', sys.argv[1])"
    command = [sys.executable, "-c", script, name]
    result = subprocess.run(command, capture_output=True, text=True,
                            check=True)
    return result.stdout.strip()


def main() -> None:
    attack = "alice & echo INJECTED"

    print("[shell=True（悪い例）]")
    print(f"  出力: {greet_unsafe(attack)!r}")

    print("[引数のリスト（良い例）]")
    print(f"  出力: {greet_safe(attack)!r}")


if __name__ == "__main__":
    main()
