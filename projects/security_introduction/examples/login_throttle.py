"""ログイン試行の制限（スロットリング）のサンプル.

同じアカウントへのログイン失敗が続いた場合に、次に試行できるまでの
待ち時間を指数関数的に延ばします。総当たり攻撃の速度を大きく落とせます。

実行方法:
    python login_throttle.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

from dataclasses import dataclass, field

FREE_ATTEMPTS = 3  # 待ち時間なしで許す連続失敗回数
BASE_DELAY = 1.0  # 待ち時間の基準値（秒）
MAX_DELAY = 900.0  # 待ち時間の上限（秒）


@dataclass
class AccountState:
    """アカウントごとの失敗回数と、次に試行できる時刻."""

    failures: int = 0
    locked_until: float = 0.0


@dataclass
class LoginThrottle:
    """アカウント単位でログイン試行を制限する."""

    states: dict[str, AccountState] = field(default_factory=dict)

    def is_allowed(self, account: str, now: float) -> bool:
        """現在時刻 now にログインを試行してよいか判定する."""
        state = self.states.get(account)
        return state is None or now >= state.locked_until

    def record_failure(self, account: str, now: float) -> float:
        """失敗を記録し、次に試行できるまでの待ち時間（秒）を返す."""
        state = self.states.setdefault(account, AccountState())
        state.failures += 1
        over = state.failures - FREE_ATTEMPTS
        delay = 0.0 if over <= 0 else min(BASE_DELAY * 2 ** over, MAX_DELAY)
        state.locked_until = now + delay
        return delay

    def record_success(self, account: str) -> None:
        """成功したら失敗回数をリセットする."""
        self.states.pop(account, None)


def main() -> None:
    throttle = LoginThrottle()
    duration = 3600  # 攻撃者が 1 秒に 1 回、1 時間試行し続けたとする
    accepted = 0

    # 説明のため、時刻は実時間ではなく数値で進める
    for now in range(duration):
        if not throttle.is_allowed("alice", now):
            continue  # ロック中の試行はパスワードを照合せずに拒否する
        accepted += 1
        delay = throttle.record_failure("alice", now)
        print(f"{now:5d} 秒: 照合して失敗。次の試行まで {delay:4.0f} 秒待つ")

    print(f"制限なしの場合に照合される回数: {duration} 回")
    print(f"制限ありの場合に照合された回数: {accepted} 回")


if __name__ == "__main__":
    main()
