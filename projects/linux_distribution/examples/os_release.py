"""/etc/os-release を読み取り、ディストリビューションの名称・バージョン・系統を表示する。

使い方::

    python os_release.py                 # /etc/os-release（なければ /usr/lib/os-release）を読む
    python os_release.py path/to/file    # 指定したファイルを読む
"""

from __future__ import annotations

import shlex
import sys
from pathlib import Path

# os-release の標準の配置場所（先頭から順に探す）
DEFAULT_PATHS = (Path("/etc/os-release"), Path("/usr/lib/os-release"))

# ID / ID_LIKE の値と系統の対応
FAMILIES = {
    "debian": "Debian 系",
    "ubuntu": "Debian 系",
    "rhel": "Red Hat 系",
    "fedora": "Red Hat 系",
    "centos": "Red Hat 系",
    "suse": "SUSE 系",
    "opensuse": "SUSE 系",
    "arch": "Arch Linux 系",
    "gentoo": "Gentoo 系",
    "slackware": "Slackware 系",
    "alpine": "Alpine Linux 系",
}


def parse_os_release(text: str) -> dict[str, str]:
    """os-release 形式の文字列を解析し、キーと値の辞書を返す。

    各行は ``KEY=VALUE`` の形式で、値はシェルと同じ規則で引用符に囲まれることがある。
    空行と ``#`` で始まる行は無視する。
    """
    result: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        # 引用符とエスケープはシェルの規則で解釈する
        words = shlex.split(value)
        result[key] = words[0] if words else ""
    return result


def detect_family(info: dict[str, str]) -> str:
    """ID と ID_LIKE から系統を判定する。判定できなければ「不明」を返す。"""
    candidates = [info.get("ID", "")] + info.get("ID_LIKE", "").split()
    for candidate in candidates:
        if candidate in FAMILIES:
            return FAMILIES[candidate]
    return "不明"


def find_os_release() -> Path | None:
    """os-release ファイルを標準の配置場所から探す。"""
    for path in DEFAULT_PATHS:
        if path.is_file():
            return path
    return None


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else find_os_release()
    if path is None or not path.is_file():
        print("os-release ファイルが見つかりません。", file=sys.stderr)
        return 1

    info = parse_os_release(path.read_text(encoding="utf-8"))
    print(f"名称      : {info.get('NAME', '不明')}")
    print(f"バージョン: {info.get('VERSION', info.get('VERSION_ID', '不明'))}")
    print(f"ID        : {info.get('ID', '不明')}")
    print(f"ID_LIKE   : {info.get('ID_LIKE', '（なし）')}")
    print(f"系統      : {detect_family(info)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
