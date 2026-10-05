"""第 10 章のサンプル: 品質検査の手順を定義する nox の設定ファイルです。

手元でも CI でも nox コマンド 1 つで同じ検査を実行できます。
"""

import nox

nox.options.sessions = ["lint", "typecheck", "tests"]
REQUIREMENTS = "requirements-dev.txt"


@nox.session
def lint(session: nox.Session) -> None:
    """flake8 で規約違反と複雑すぎる関数を検出します。"""
    session.install("-r", REQUIREMENTS)
    session.run("flake8", ".")


@nox.session
def typecheck(session: nox.Session) -> None:
    """mypy で型の誤りを検出します。"""
    session.install("-r", REQUIREMENTS)
    session.run("mypy", ".")


@nox.session
def tests(session: nox.Session) -> None:
    """pytest でテストを実行し、カバレッジが 80 % 未満なら失敗させます。"""
    session.install("-r", REQUIREMENTS)
    session.run(
        "pytest",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-fail-under=80",
        "--junitxml=reports/junit.xml",
    )
