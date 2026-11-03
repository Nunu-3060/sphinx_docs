"""各 Sphinx プロジェクトの build_html.bat を一括で実行する。

カレントディレクトリの ``projects/*/build_html.bat`` を順番に実行し、
最後に成功・失敗・省略の一覧を表示する。各プロジェクトの出力は
``<プロジェクト>/build/build_html.log`` に保存する。

前回のビルドが成功していて、その後に入力が変わっていないプロジェクトは
ビルドを省略する。入力は次のものとする。

* プロジェクトのフォルダー内の全ファイル（build と __pycache__ は除く）の
  相対パス・サイズ・更新日時。ファイルの追加・削除も変更として扱う。
* このスクリプトを実行している Python のバージョンと、
  インストールされているパッケージのバージョン（Sphinx やテーマの更新を検出する）。

ビルドに成功すると、入力の要約（ハッシュ値）を
``<プロジェクト>/build/build_html.stamp`` に保存する。build_html.bat は
最初に build を削除するので、失敗したプロジェクトには stamp が残らず、
次回は必ずビルドされる。

使い方::

    python run_build_html.py              # 変更のあったものだけビルドする
    python run_build_html.py --force      # 変更の有無にかかわらず全件をビルドする
    python run_build_html.py --open       # ビルド後にブラウザで index.html を開く
    python run_build_html.py python_introduction unity_introduction
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
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
STAMP_NAME = "build_html.stamp"
# build_html.bat はこの環境変数が定義されているとブラウザを開かない。
NO_OPEN_ENV = "SPHINX_NO_OPEN"
# 入力の要約に含めないフォルダー（build はビルド結果、__pycache__ は
# ビルド中に作られる .py のキャッシュで、元の .py の変更は別に検出できる）
IGNORED_DIR_NAMES = {BUILD_DIR_NAME, "__pycache__"}


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


def environment_lines() -> list[str]:
    """Python とインストール済みパッケージのバージョンを、並び順を固定して返す。"""
    packages = sorted(
        f"{dist.metadata['Name']}=={dist.version}"
        for dist in importlib.metadata.distributions()
    )
    return [f"python {sys.version}", *packages]


def input_digest(project: Path, environment: list[str]) -> str:
    """プロジェクトの入力（ファイルの一覧・サイズ・更新日時と環境）のハッシュ値を返す。"""
    digest = hashlib.sha256()
    for line in environment:
        digest.update(line.encode("utf-8") + b"\n")
    for root, dirs, files in os.walk(project):
        # os.walk の巡回順を固定し、除外するフォルダーには入らない
        dirs[:] = sorted(name for name in dirs if name not in IGNORED_DIR_NAMES)
        for name in sorted(files):
            path = Path(root) / name
            stat = path.stat()
            relative = path.relative_to(project).as_posix()
            digest.update(
                f"{relative}\t{stat.st_size}\t{stat.st_mtime_ns}\n".encode("utf-8")
            )
    return digest.hexdigest()


def stamp_path_of(project: Path) -> Path:
    """前回のビルド成功時の入力の要約を保存するファイルを返す。"""
    return project / BUILD_DIR_NAME / STAMP_NAME


def is_up_to_date(project: Path, environment: list[str]) -> bool:
    """前回のビルドが成功していて、その後に入力が変わっていなければ True を返す。"""
    stamp_path = stamp_path_of(project)
    index = project / HTML_RELATIVE_DIR / INDEX_NAME
    if not stamp_path.is_file() or not index.is_file():
        return False
    stamp = stamp_path.read_text(encoding="ascii").strip()
    return stamp == input_digest(project, environment)


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
    parser.add_argument(
        "--force",
        action="store_true",
        help="入力が変わっていないプロジェクトも省略せずにビルドする",
    )
    args = parser.parse_args()

    # build_html.bat を持つプロジェクトを対象にする
    projects = find_projects(Path.cwd(), args.projects, marker=BAT_NAME)
    environment = environment_lines()
    results: list[BuildResult] = []
    skipped: list[Path] = []
    for number, project in enumerate(projects, start=1):
        print(f"[{number}/{len(projects)}] {project.name} ...", flush=True)
        if not args.force and is_up_to_date(project, environment):
            skipped.append(project)
            print("    省略（前回のビルドから変更なし）", flush=True)
            continue
        result = run_build(project, args.open)
        results.append(result)
        if result.succeeded:
            # ビルド中に source などへ書き出されるファイルも含めるため、
            # 要約はビルドの後に作る。
            stamp_path_of(project).write_text(
                input_digest(project, environment) + "\n", encoding="ascii"
            )
        status = "成功" if result.succeeded else "失敗"
        print(f"    {status} ({result.seconds:.1f} 秒)", flush=True)

    failed = [result for result in results if not result.succeeded]
    print()
    print(f"成功: {len(results) - len(failed)} 件, 失敗: {len(failed)} 件, "
          f"省略: {len(skipped)} 件")
    for result in failed:
        log_path = result.project / BUILD_DIR_NAME / LOG_NAME
        print(f"  失敗: {result.project.name} (ログ: {log_path})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
