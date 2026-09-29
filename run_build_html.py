"""各 Sphinx プロジェクトの build_html.bat を一括で実行する。

カレントディレクトリの ``projects/*/build_html.bat`` を順番に実行し、
最後に成功・失敗の一覧を表示する。各プロジェクトの出力は
``<プロジェクト>/build/build_html.log`` に保存する。

使い方::

    python run_build_html.py              # 全件をビルドする（ブラウザは開かない）
    python run_build_html.py --open       # ビルド後にブラウザで index.html を開く
    python run_build_html.py python_introduction unity_introduction
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from sphinx_projects import (
    BAT_NAME,
    BUILD_DIR_NAME,
    HTML_RELATIVE_DIR,
    INDEX_NAME,
    add_projects_argument,
    find_projects,
)

LOG_NAME = "build_html.log"
# build_html.bat はこの環境変数が定義されているとブラウザを開かない。
NO_OPEN_ENV = "SPHINX_NO_OPEN"


@dataclass
class BuildResult:
    """1 プロジェクト分のビルド結果。"""

    project: Path
    returncode: int
    seconds: float

    @property
    def succeeded(self) -> bool:
        index = self.project / HTML_RELATIVE_DIR / INDEX_NAME
        return self.returncode == 0 and index.exists()


def run_build(project: Path, open_browser: bool) -> BuildResult:
    """build_html.bat を実行し、出力をログファイルに保存する。"""
    env = os.environ.copy()
    if open_browser:
        env.pop(NO_OPEN_ENV, None)
    else:
        env[NO_OPEN_ENV] = "1"

    start = time.perf_counter()
    completed = subprocess.run(
        ["cmd", "/c", str(project / BAT_NAME)],
        cwd=project,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    seconds = time.perf_counter() - start

    # build_html.bat が build を削除してから作り直すので、実行後に書き込む。
    log_dir = project / BUILD_DIR_NAME
    log_dir.mkdir(exist_ok=True)
    (log_dir / LOG_NAME).write_bytes(completed.stdout)
    return BuildResult(project, completed.returncode, seconds)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    add_projects_argument(parser)
    parser.add_argument(
        "--open",
        action="store_true",
        help="ビルド後に既定のブラウザで index.html を開く",
    )
    args = parser.parse_args()

    # build_html.bat を持つプロジェクトを対象にする
    projects = find_projects(Path.cwd(), args.projects, marker=BAT_NAME)
    results: list[BuildResult] = []
    for number, project in enumerate(projects, start=1):
        print(f"[{number}/{len(projects)}] {project.name} ...", flush=True)
        result = run_build(project, args.open)
        results.append(result)
        status = "成功" if result.succeeded else "失敗"
        print(f"    {status} ({result.seconds:.1f} 秒)", flush=True)

    failed = [result for result in results if not result.succeeded]
    print()
    print(f"成功: {len(results) - len(failed)} 件, 失敗: {len(failed)} 件")
    for result in failed:
        log_path = result.project / BUILD_DIR_NAME / LOG_NAME
        print(f"  失敗: {result.project.name} (ログ: {log_path})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
