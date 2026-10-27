"""Claude Code の Stop フックとして使い、テストが成功するまで作業を続けさせるスクリプト。

Claude が応答を終えようとしたときに pytest を実行する。失敗したテストがあれば
``{"decision": "block", "reason": ...}`` を出力し、Claude に作業を続けさせる。

``stop_hook_active`` が真のときは、すでにこのフックによって作業を続けている。
この場合は終了を止めない。テストがいつまでも成功しない場合に、ループが
終わらなくなるのを防ぐためである。
"""

from __future__ import annotations

import json
import subprocess
import sys


def main() -> int:
    hook_input = json.load(sys.stdin)
    if hook_input.get("stop_hook_active"):
        return 0

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header"],
        cwd=hook_input.get("cwd"),
        capture_output=True,
        text=True,
        timeout=600,
    )
    if result.returncode == 0:
        return 0

    tail = "\n".join(result.stdout.splitlines()[-20:])
    decision = {
        "decision": "block",
        "reason": f"テストが失敗している。原因を調べて修正し、再度 pytest を実行すること。\n{tail}",
    }
    print(json.dumps(decision, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
