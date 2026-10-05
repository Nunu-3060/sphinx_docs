"""クラウドの IAM ポリシーから過剰な権限を検出するサンプル.

AWS の IAM ポリシーと同じ形式の JSON を読み込み、ワイルドカード（*）による
過剰な権限など、最小権限の原則に反する記述を指摘します。
実際のクラウドには接続しません。

実行方法:
    python iam_policy_check.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import json
from typing import Any

POLICY_JSON = """
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadReports",
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::example-reports/*"
    },
    {
      "Sid": "DeveloperShortcut",
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    },
    {
      "Sid": "ManageQueues",
      "Effect": "Allow",
      "Action": "sqs:*",
      "Resource": "*"
    },
    {
      "Sid": "EverythingExceptIam",
      "Effect": "Allow",
      "NotAction": "iam:*",
      "Resource": "*"
    }
  ]
}
"""


def as_list(value: Any) -> list[str]:
    """文字列または文字列のリストを、リストにそろえる."""
    if isinstance(value, str):
        return [value]
    return [str(item) for item in value]


def check_statement(statement: dict[str, Any]) -> list[str]:
    """1 つのステートメントを検査し、指摘事項の一覧を返す."""
    if statement.get("Effect") != "Allow":
        return []
    findings: list[str] = []
    actions = as_list(statement.get("Action", []))
    resources = as_list(statement.get("Resource", []))

    if "*" in actions:
        findings.append("すべての操作（Action: *）を許可しています")
    for action in actions:
        if action != "*" and action.endswith(":*"):
            findings.append(f"サービスの全操作（{action}）を許可しています")
    if "NotAction" in statement:
        findings.append("NotAction と Allow の組み合わせは、"
                        "列挙した操作以外のすべてを許可します")
    if "*" in resources:
        findings.append("すべてのリソース（Resource: *）が対象です")
    return findings


def main() -> None:
    policy = json.loads(POLICY_JSON)
    for statement in policy["Statement"]:
        sid = statement.get("Sid", "（Sid なし）")
        findings = check_statement(statement)
        if not findings:
            print(f"[OK]   {sid}")
            continue
        print(f"[警告] {sid}")
        for finding in findings:
            print(f"         - {finding}")


if __name__ == "__main__":
    main()
