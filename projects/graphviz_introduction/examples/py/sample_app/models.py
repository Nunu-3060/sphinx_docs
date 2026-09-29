"""アプリケーションで扱うデータの型を定義する."""

from dataclasses import dataclass


@dataclass
class Task:
    """1 件のタスクを表す."""

    title: str
    done: bool = False
