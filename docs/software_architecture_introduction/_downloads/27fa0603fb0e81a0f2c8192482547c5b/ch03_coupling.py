"""結合度の高いコードと低いコードの比較.

ポイント還元の計算を例に、次の 2 つの実装を比べます。

* 悪い例: グローバル変数と、受け取ったデータ構造の全体に依存している
* 良い例: 必要な値だけを引数で受け取る

実行方法::

    python ch03_coupling.py
"""

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# 悪い例: 共通結合（グローバル変数）とスタンプ結合（データ構造全体への依存）
# ---------------------------------------------------------------------------

# どこからでも書き換えられるグローバルな設定
config: dict[str, float] = {"point_rate": 0.01}


@dataclass
class Member:
    """会員を表します."""

    name: str
    rank: str
    history: list[int] = field(default_factory=list)


def bad_calc_points(member: Member) -> int:
    """最後の購入金額に対するポイントを返します（悪い例）.

    グローバル変数 config を読み、会員のデータ全体を受け取って、その
    内部の構造（購入履歴のリストの末尾が最新であること）に依存しています。
    config や Member の実装を変更すると、この関数も壊れます。
    """
    rate = config["point_rate"]
    if member.rank == "gold":
        rate = rate * 2
    return int(member.history[-1] * rate)


# ---------------------------------------------------------------------------
# 良い例: データ結合（必要な値だけを引数で受け取る）
# ---------------------------------------------------------------------------

RANK_MULTIPLIER: dict[str, int] = {"regular": 1, "gold": 2}


def calc_points(amount: int, rank: str, base_rate: float = 0.01) -> int:
    """購入金額と会員ランクから、付与するポイントを返します（良い例）.

    計算に必要な値だけを引数で受け取るので、呼び出し側のデータ構造や
    グローバルな状態に依存しません。
    """
    return int(amount * base_rate * RANK_MULTIPLIER[rank])


def main() -> None:
    """2 つの実装が同じ結果を返すことを確認します."""
    member = Member("佐藤", "gold", [1000, 2500])
    print("悪い例:", bad_calc_points(member))
    print("良い例:", calc_points(member.history[-1], member.rank))

    # グローバル変数を別の場所で書き換えると、悪い例の結果が変わってしまう
    config["point_rate"] = 0.05
    print("config の変更後の悪い例:", bad_calc_points(member))
    print("config の変更後の良い例:",
          calc_points(member.history[-1], member.rank))


if __name__ == "__main__":
    main()
