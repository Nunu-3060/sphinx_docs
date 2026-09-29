"""在庫管理 CLI の入口です（コンポジションルート）.

オブジェクトの組み立てだけを行います。どのリポジトリを使うかを決めて
いるのは、アプリケーション全体でこのファイルだけです。
"""

import sys
from pathlib import Path

from .cli import build_parser, execute
from .repository import JsonFileItemRepository
from .service import InventoryService


def main(argv: list[str]) -> int:
    """引数を解析し、オブジェクトを組み立てて、コマンドを実行します."""
    args = build_parser().parse_args(argv)
    repository = JsonFileItemRepository(Path(args.file))
    service = InventoryService(repository)
    return execute(args, service, sys.stdout)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
