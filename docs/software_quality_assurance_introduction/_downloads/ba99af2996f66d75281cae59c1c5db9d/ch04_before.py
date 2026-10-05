# 第 4 章のサンプル: 規約違反と型エラーを含む「悪い例」です。
# flake8 と mypy の検出例を示すため、意図的に問題を残しています。
import os, sys
def calc(items, rate = 0.1):
    total=0
    for i in items:
        total += i["price"]*i["qty"]
    if rate == None:
        return total
    return total*(1+rate)

def label(total: float) -> str:
    return total
