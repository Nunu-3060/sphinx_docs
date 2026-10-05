"""安全でないデシリアライズ（pickle）の危険性を確認するサンプル.

pickle はデータの復元時に任意の関数を呼び出せる仕組みを持つため、
信頼できないデータを pickle.loads() に渡すと任意のコードが実行されます。
このサンプルでは、無害な print() が呼び出されることで危険性を示します。

実行方法:
    python unsafe_deserialization.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import json
import pickle
from typing import Any


class Malicious:
    """復元時に関数を呼び出させるオブジェクト（攻撃者が用意する）."""

    def __reduce__(self) -> tuple[Any, tuple[str]]:
        # 実際の攻撃では os.system などが指定される
        return (print, ("  !!! 復元しただけで関数が実行されました !!!",))


def main() -> None:
    # 攻撃者が送ってきたデータ（中身はただのバイト列に見える）
    payload = pickle.dumps(Malicious())
    print(f"受信したデータ（{len(payload)} バイト）: {payload[:32]!r}...")

    print("[pickle.loads()（悪い例）]")
    pickle.loads(payload)

    print("[json.loads()（良い例）]")
    data = json.loads('{"name": "alice", "roles": ["user"]}')
    print(f"  復元されるのは辞書・リスト・文字列・数値などのデータだけ: {data}")


if __name__ == "__main__":
    main()
