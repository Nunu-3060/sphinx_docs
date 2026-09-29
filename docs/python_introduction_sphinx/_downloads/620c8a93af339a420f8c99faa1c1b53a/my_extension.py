"""GitHub のリポジトリへのリンクを作るロールを追加する Sphinx 拡張機能の例。

conf.py の ``extensions`` に ``"my_extension"`` を追加すると、
reST の中で次のように書けるようになります。

    :github:`sphinx-doc/sphinx`

このロールは https://github.com/sphinx-doc/sphinx へのリンクに変換されます。
"""

from __future__ import annotations

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxRole
from sphinx.util.typing import ExtensionMetadata

GITHUB_URL = "https://github.com/"


class GitHubRole(SphinxRole):
    """``:github:`owner/repo``` を GitHub へのリンクに変換するロール。"""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        """ロールの処理本体です。

        Returns:
            生成したノードのリストと、エラーメッセージのリスト。
        """
        repository = self.text.strip()
        if repository.count("/") != 1:
            message = self.inliner.reporter.error(
                f"'owner/repo' の形式で指定してください: {repository}",
                line=self.lineno,
            )
            problem = self.inliner.problematic(
                self.rawtext, self.rawtext, message
            )
            return [problem], [message]

        node = nodes.reference(
            self.rawtext, repository, refuri=GITHUB_URL + repository
        )
        return [node], []


def setup(app: Sphinx) -> ExtensionMetadata:
    """Sphinx が拡張機能を読み込むときに呼び出す関数です。

    Args:
        app: Sphinx のアプリケーションオブジェクト。

    Returns:
        拡張機能のメタデータ。
    """
    app.add_role("github", GitHubRole())
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
