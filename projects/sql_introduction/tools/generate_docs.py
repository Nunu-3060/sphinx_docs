"""テンプレートから本文の rst ファイルと SQL の例のファイルを生成するスクリプト.

tools/templates/ の rst ファイル（テンプレート）を読み込み、次の独自の
ディレクティブを展開して source/ に書き出します。

``.. sqlfile:: 名前 タイトル``
    以降の sqlrun の SQL を examples/sql/名前.sql に書き出すことを指定します。
    SQL を実行するデータベースは、名前ごとに初期状態から用意されます。
    同じ名前の sqlrun は、前の sqlrun を実行した後のデータに対して実行されます。

``.. sqlrun::``
    中に書いた SQL を実行し、SQL のコードブロックと実行結果の表に展開します。
    次のオプションを指定できます。

    ``:error:``        エラーになることを期待します（エラーメッセージを表示）。
    ``:hide-code:``    SQL のコードブロックを出力しません。
    ``:hide-result:``  実行結果を出力しません。
    ``:no-export:``    examples/sql/ の SQL ファイルに書き出しません。

``.. pyoutput:: スクリプト名 [引数 ...]``
    examples/ の Python スクリプトを実行し、その出力に展開します。

このほか、日本語の文字に隣接するインライン記法（````SELECT````（ など）が
rst として正しく解釈されるよう、必要な位置にエスケープした空白（``\\ ``）を
補います。

使い方（プロジェクトのルートで実行します）::

    python tools/generate_docs.py
"""

import os
import re
import shlex
import sqlite3
import subprocess
import sys
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "tools" / "templates"
SOURCE_DIR = ROOT / "source"
EXAMPLES_DIR = ROOT / "examples"
SQL_DIR = EXAMPLES_DIR / "sql"
SAMPLES_PAGE = "appendix_e_samples.rst"

# SQL 文の分割には、examples/run_query.py と同じ関数を使います。
# examples/ に __pycache__ ができないよう、バイトコードの書き出しを止めます。
sys.dont_write_bytecode = True
sys.path.insert(0, str(EXAMPLES_DIR))
from run_query import split_statements  # noqa: E402

INDENT = "   "
SQLRUN_OPTIONS = {"error", "hide-code", "hide-result", "no-export"}
INLINE_MARKUP = re.compile(r"(:[\w-]+:`[^`]+`|``[^`]+``|`[^`]+`_{1,2})")
CODE_DIRECTIVE = re.compile(r"^\s*\.\. (code-block|literalinclude|math)::")


class GenerationError(Exception):
    """テンプレートの展開に失敗したことを表す例外です."""


@dataclass
class SqlFile:
    """1 つの SQL ファイルに書き出す内容と、実行用のデータベースです."""

    title: str
    conn: sqlite3.Connection
    statements: list[str] = field(default_factory=list)


def create_database() -> sqlite3.Connection:
    """サンプルデータベースを初期状態でメモリ上に作成します."""
    conn = sqlite3.connect(":memory:", autocommit=True)
    conn.execute("PRAGMA foreign_keys = ON")
    for name in ("schema.sql", "data.sql"):
        conn.executescript((EXAMPLES_DIR / name).read_text(encoding="utf-8"))
    return conn


def escape_cell(value: Any) -> str:
    """実行結果の値を、list-table のセルに書ける rst の文字列に変換します."""
    if value is None:
        return "NULL"
    text = str(value)
    if text == "":
        return "``''``"
    text = re.sub(r"([\\*_`|<>\[\]@])", r"\\\1", text)
    # 箇条書きや番号付きリストの記号と解釈される書き出しを避けます。
    if re.match(r"^([-+*]\s|#\.|\d+[.)]\s|\d+[.)]$)", text):
        text = "\\" + text
    return text


def list_table(
    columns: Sequence[str], rows: Sequence[Sequence[Any]]
) -> list[str]:
    """実行結果を list-table の行のリストに変換します."""
    lines = [
        ".. list-table::", "   :header-rows: 1", "   :class: sql-result", "",
    ]
    for row in [list(columns), *[list(r) for r in rows]]:
        for index, value in enumerate(row):
            prefix = "   * - " if index == 0 else "     - "
            lines.append(prefix + escape_cell(value))
    lines.append("")
    return lines


def plan_text(rows: Sequence[Sequence[Any]]) -> list[str]:
    """EXPLAIN QUERY PLAN の結果を、sqlite3 コマンドと同様の木の形式にします."""
    children: dict[int, list[tuple[int, str]]] = {}
    for node_id, parent, _, detail in rows:
        children.setdefault(parent, []).append((node_id, detail))
    lines = ["QUERY PLAN"]

    def walk(parent: int, prefix: str) -> None:
        nodes = children.get(parent, [])
        for index, (node_id, detail) in enumerate(nodes):
            last = index == len(nodes) - 1
            lines.append(prefix + ("`--" if last else "|--") + detail)
            walk(node_id, prefix + ("   " if last else "|  "))

    walk(0, "")
    return lines


def is_query_plan(statement: str) -> bool:
    """コメント行を除いた SQL 文が EXPLAIN QUERY PLAN で始まるかを返します."""
    code = " ".join(
        line for line in statement.splitlines()
        if not line.strip().startswith("--")
    )
    return code.strip().upper().startswith("EXPLAIN QUERY PLAN")


def code_block(language: str, text: str, linenos: bool) -> list[str]:
    """コードブロックの rst の行のリストを作ります."""
    lines = [f".. code-block:: {language}"]
    if linenos:
        lines.append("   :linenos:")
    lines.append("")
    lines += [INDENT + line if line else "" for line in text.splitlines()]
    lines.append("")
    return lines


def ok_before(ch: str) -> bool:
    """インライン記法の開始の直前に置ける文字かどうかを返します."""
    return (
        ch.isspace() or ch in "-:/'\"<([{"
        or unicodedata.category(ch) in ("Pd", "Po", "Pi", "Pf", "Ps")
    )


def ok_after(ch: str) -> bool:
    """インライン記法の終了の直後に置ける文字かどうかを返します."""
    return (
        ch.isspace() or ch in "-.,:;!?\\/'\")]}>"
        or unicodedata.category(ch) in ("Pd", "Po", "Pi", "Pf", "Pe")
    )


def fix_inline(line: str) -> str:
    """インライン記法の前後に、必要に応じてエスケープした空白を補います."""
    parts: list[str] = []
    pos = 0
    for match in INLINE_MARKUP.finditer(line):
        start, end = match.span()
        parts.append(line[pos:start])
        prev = line[start - 1] if start > 0 else " "
        # 直前のインライン記法の後に補った空白がある場合は、重ねて補いません。
        if not ok_before(prev) and not "".join(parts).endswith("\\ "):
            parts.append("\\ ")
        parts.append(match.group(0))
        nxt = line[end] if end < len(line) else " "
        if not ok_after(nxt):
            parts.append("\\ ")
        pos = end
    parts.append(line[pos:])
    return "".join(parts)


def starts_code_block(line: str) -> bool:
    """コードブロック（ディレクティブまたはリテラルブロック）の開始行かを返します."""
    if CODE_DIRECTIVE.match(line):
        return True
    stripped = line.strip()
    return stripped.endswith("::") and not stripped.startswith("..")


def fix_markup(lines: list[str]) -> list[str]:
    """コードブロック以外の行について、インライン記法の前後を補正します."""
    result = []
    code_indent: int | None = None
    for line in lines:
        indent = len(line) - len(line.lstrip())
        if code_indent is not None:
            if not line.strip() or indent > code_indent:
                result.append(line)
                continue
            code_indent = None
        if starts_code_block(line):
            code_indent = indent
            result.append(line)
            continue
        result.append(fix_inline(line))
    return result


class Generator:
    """テンプレートを展開して rst ファイルと SQL ファイルを生成します."""

    def __init__(self) -> None:
        self.sql_files: dict[str, SqlFile] = {}

    def run_sqlrun(self, name: str, options: set[str], body: str) -> list[str]:
        """sqlrun ディレクティブの SQL を実行し、展開後の rst の行を返します."""
        sql_file = self.sql_files[name]
        error: str | None = None
        result: tuple[list[str], list[Any], str] | None = None
        for statement in split_statements(body):
            try:
                cursor = sql_file.conn.execute(statement)
                rows = cursor.fetchall()
            except sqlite3.Error as exc:
                error = f"sqlite3.{type(exc).__name__}: {exc}"
                break
            if cursor.description is not None:
                columns = [d[0] for d in cursor.description]
                result = (columns, rows, statement)

        if "error" in options and error is None:
            raise GenerationError(f"エラーになるはずの SQL が成功しました:\n{body}")
        if "error" not in options and error is not None:
            raise GenerationError(f"SQL がエラーになりました: {error}\n{body}")

        lines: list[str] = []
        if "hide-code" not in options:
            lines += code_block("sql", body, linenos=True)
        if "hide-result" not in options:
            if error is not None:
                lines += code_block("text", error, linenos=False)
            elif result is not None:
                columns, rows, statement = result
                if is_query_plan(statement):
                    plan = "\n".join(plan_text(rows))
                    lines += code_block("text", plan, linenos=False)
                elif rows:
                    lines += list_table(columns, rows)
                else:
                    lines += ["結果は 0 行です。", ""]
        if "no-export" not in options:
            if error is not None:
                sql_file.statements.append("-- 次の文はエラーになります。")
            sql_file.statements += [body.strip(), ""]
        return lines

    def run_pyoutput(self, command: str) -> list[str]:
        """pyoutput ディレクティブのスクリプトを実行し、出力のコードブロックを返します.

        スクリプトは shop.db を初期状態に戻してから実行します。
        実行後にも shop.db を初期状態に戻します。そのため、examples/shop.db に
        加えた変更は失われます。
        """
        script, *args = shlex.split(command)
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        reset = [sys.executable, str(EXAMPLES_DIR / "create_shop_db.py")]
        subprocess.run(reset, check=True, capture_output=True, env=env)
        proc = subprocess.run(
            [sys.executable, str(EXAMPLES_DIR / script), *args],
            cwd=EXAMPLES_DIR, capture_output=True, text=True,
            encoding="utf-8", env=env,
        )
        subprocess.run(reset, check=True, capture_output=True, env=env)
        if proc.returncode != 0:
            raise GenerationError(f"{script} の実行に失敗しました:\n{proc.stderr}")
        return code_block("text", proc.stdout.rstrip(), linenos=False)

    def process(self, template: Path) -> None:
        """1 つのテンプレートを展開し、source/ に同じ名前で書き出します."""
        lines = template.read_text(encoding="utf-8").splitlines()
        out: list[str] = []
        current: str | None = None
        i = 0
        while i < len(lines):
            line = lines[i]
            if match := re.match(r"^\.\. sqlfile:: (\S+) (.+)$", line):
                current = match.group(1)
                self.sql_files[current] = SqlFile(
                    match.group(2), create_database()
                )
                i += 1
            elif match := re.match(r"^\.\. pyoutput:: (.+)$", line):
                out += self.run_pyoutput(match.group(1))
                i += 1
            elif match := re.match(r"^( *)\.\. sqlrun::\s*$", line):
                if current is None:
                    raise GenerationError(
                        f"{template.name}:{i + 1}: sqlrun より前に sqlfile がありません"
                    )
                indent = match.group(1)
                options, body, i = self.read_sqlrun(
                    lines, i + 1, indent + INDENT
                )
                expanded = self.run_sqlrun(current, options, body)
                out += [indent + x if x else "" for x in expanded]
            else:
                out.append(line)
                i += 1
        text = "\n".join(fix_markup(out)).rstrip() + "\n"
        text = re.sub(r"\n{3,}", "\n\n", text)
        (SOURCE_DIR / template.name).write_text(text, encoding="utf-8")

    @staticmethod
    def read_sqlrun(
        lines: list[str], start: int, body_indent: str
    ) -> tuple[set[str], str, int]:
        """sqlrun のオプションと本文を読み、次に読む行の位置とともに返します."""
        i = start
        options: set[str] = set()
        option_line = re.compile("^" + body_indent + r":[\w-]+:")
        while i < len(lines) and option_line.match(lines[i]):
            option = lines[i].strip().strip(":")
            if option not in SQLRUN_OPTIONS:
                raise GenerationError(f"sqlrun の不明なオプション: {option}")
            options.add(option)
            i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        body: list[str] = []
        while i < len(lines) and (
            lines[i].startswith(body_indent) or not lines[i].strip()
        ):
            body.append(lines[i][len(body_indent):])
            i += 1
        while body and not body[-1]:
            body.pop()
        return options, "\n".join(body), i

    def write_sql_files(self) -> None:
        """sqlrun の SQL を、sqlfile ごとに examples/sql/ に書き出します."""
        SQL_DIR.mkdir(exist_ok=True)
        for old in SQL_DIR.glob("*.sql"):
            old.unlink()
        for name, sql_file in self.sql_files.items():
            if not sql_file.statements:
                continue
            header = [
                f"-- {sql_file.title}",
                "--",
                "-- 使い方（examples フォルダーで実行します）:",
                f"--   python run_query.py sql/{name}.sql",
                "",
            ]
            text = "\n".join(header + sql_file.statements).rstrip() + "\n"
            (SQL_DIR / f"{name}.sql").write_text(text, encoding="utf-8")

    def fill_samples_page(self) -> None:
        """付録 E の SQL ファイルの一覧と内容の部分を埋めます."""
        names = sorted(
            (n for n, f in self.sql_files.items() if f.statements),
            key=lambda n: (n.startswith("answers"), n),
        )
        rows: list[str] = []
        includes: list[str] = []
        for name in names:
            rows += [
                f"   * - :download:`{name}.sql <../examples/sql/{name}.sql>`",
                f"     - {self.sql_files[name].title}",
            ]
            includes += [
                f"{name}.sql",
                "^" * (len(name) + 4),
                "",
                f".. literalinclude:: ../examples/sql/{name}.sql",
                "   :language: sql",
                "   :linenos:",
                "",
            ]
        page = SOURCE_DIR / SAMPLES_PAGE
        text = page.read_text(encoding="utf-8")
        text = text.replace("SQLFILE_ROWS", "\n".join(rows))
        text = text.replace("SQLFILE_INCLUDES", "\n".join(includes).rstrip())
        page.write_text(text, encoding="utf-8")

    def close(self) -> None:
        """実行用のデータベースを閉じます."""
        for sql_file in self.sql_files.values():
            sql_file.conn.close()


def main() -> int:
    """すべてのテンプレートを展開します."""
    templates = sorted(TEMPLATE_DIR.glob("*.rst"))
    shop_db = EXAMPLES_DIR / "shop.db"
    shop_db_existed = shop_db.exists()
    generator = Generator()
    try:
        for template in templates:
            generator.process(template)
        generator.write_sql_files()
        generator.fill_samples_page()
    except GenerationError as error:
        print(f"エラー: {error}", file=sys.stderr)
        return 1
    finally:
        generator.close()
        # pyoutput の実行のために作成した shop.db は、元になかった場合は削除します。
        if not shop_db_existed:
            shop_db.unlink(missing_ok=True)
    count = sum(1 for f in generator.sql_files.values() if f.statements)
    print(f"rst ファイル {len(templates)} 件、SQL ファイル {count} 件を生成しました。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
