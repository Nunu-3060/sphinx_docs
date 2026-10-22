"""第 10 章「実践パターン集」のサンプルコード。

各 demo_* 関数は本文から引用している。
行末の「# ->」コメントは、その行で表示される内容を示す。

実行方法 (sample.log を同じフォルダに置くこと)::

    python ch10_practical.py
"""
import re
from collections import Counter
from pathlib import Path

LOG_FILE = Path(__file__).with_name("sample.log")

LOG_PATTERN = re.compile(
    r"""
    (?P<date>\d{4}-\d{2}-\d{2})     # 日付
    \s+
    (?P<time>\d{2}:\d{2}:\d{2})     # 時刻
    \s+
    (?P<level>[A-Z]+)               # ログレベル
    \s+
    \[(?P<component>\w+)\]          # コンポーネント名
    \s+
    (?P<message>.*)                 # 残りはすべてメッセージ
    """,
    flags=re.VERBOSE,
)


def parse_log_line(line: str) -> dict[str, str] | None:
    """ログ 1 行を解析して辞書を返す。形式に合わない行は None を返す。"""
    m = LOG_PATTERN.fullmatch(line.rstrip("\n"))
    return m.groupdict() if m else None


def demo_parse_log() -> None:
    """ログファイルを解析してログレベルごとに件数を数える。"""
    levels: Counter[str] = Counter()
    with LOG_FILE.open(encoding="utf-8") as f:
        for line in f:
            entry = parse_log_line(line)
            if entry is None:
                print("skip:", line.strip())
                continue
            levels[entry["level"]] += 1
            if entry["level"] == "ERROR":
                print(entry["time"], entry["component"], entry["message"])
    print(dict(levels))
    # -> 09:01:10 db connection timeout after 30s
    # -> 09:02:30 web GET /api/users 500 120ms
    # -> skip: this line is broken
    # -> {'INFO': 3, 'WARN': 1, 'ERROR': 2}


def demo_http_status() -> None:
    """HTTP のステータスコードと応答時間を取り出す。"""
    pattern = re.compile(r"(?P<method>GET|POST) (?P<path>\S+) (?P<status>\d{3}) (?P<ms>\d+)ms")
    text = LOG_FILE.read_text(encoding="utf-8")
    for m in pattern.finditer(text):
        if int(m["status"]) >= 300:
            print(m["status"], m["path"], m["ms"])
    # -> 301 /old-page 3
    # -> 500 /api/users 120


def demo_normalize_date() -> None:
    """表記がばらばらな日付を YYYY-MM-DD 形式にそろえる。"""
    pattern = re.compile(r"(\d{4})[/年-](\d{1,2})[/月-](\d{1,2})日?")

    def to_iso(m: re.Match[str]) -> str:
        year, month, day = (int(g) for g in m.groups())
        return f"{year:04d}-{month:02d}-{day:02d}"

    text = "開始 2026/4/1、中間 2026年7月15日、終了 2027-3-31"
    print(pattern.sub(to_iso, text))  # -> 開始 2026-04-01、中間 2026-07-15、終了 2027-03-31


def demo_key_value() -> None:
    """key=value 形式の文字列を辞書に変換する。値は引用符で囲まれている場合がある。"""
    text = 'host=example.com port=8080 user="John Smith" debug=true'
    pairs = re.findall(r'(\w+)=("[^"]*"|\S+)', text)
    config = {key: value.strip('"') for key, value in pairs}
    print(config)  # -> {'host': 'example.com', 'port': '8080', 'user': 'John Smith', 'debug': 'true'}


def demo_normalize_space() -> None:
    """連続する空白 (改行やタブを含む) を 1 つの半角空白にまとめる。"""
    text = "  Hello,\t\tregular   \n expression!  "
    print(repr(re.sub(r"\s+", " ", text).strip()))  # -> 'Hello, regular expression!'


def demo_validate() -> None:
    """入力値の形式を検証する。検証では fullmatch() と re.ASCII を使う。"""
    postal_code = re.compile(r"\d{3}-\d{4}", flags=re.ASCII)
    for value in ("100-0001", "1000001", "１００-０００１", "100-00012"):
        print(value, bool(postal_code.fullmatch(value)))
    # -> 100-0001 True
    # -> 1000001 False
    # -> １００-０００１ False
    # -> 100-00012 False


def demo_email_rough_check() -> None:
    """メールアドレスは「明らかにおかしいものを弾く」程度の検査にとどめる。"""
    rough = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
    for value in ("user@example.com", "user.name+tag@example.co.jp", "user@localhost", "a b@example.com"):
        print(value, bool(rough.fullmatch(value)))
    # -> user@example.com True
    # -> user.name+tag@example.co.jp True
    # -> user@localhost False
    # -> a b@example.com False


def main() -> None:
    """すべてのデモを順に実行する。"""
    demos = (
        demo_parse_log,
        demo_http_status,
        demo_normalize_date,
        demo_key_value,
        demo_normalize_space,
        demo_validate,
        demo_email_rough_check,
    )
    for demo in demos:
        print(f"=== {demo.__name__} ===")
        demo()


if __name__ == "__main__":
    main()
