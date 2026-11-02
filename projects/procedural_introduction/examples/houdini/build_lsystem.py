r"""第 16 章: L-System SOP で植物を作るネットワーク（/obj/lsystem）を組む。

第 8 章の L-system を、Houdini の L-System SOP で書いた例である。3 種類を並べる。

* plant: 括弧付き L-system の草（平面内で枝分かれする）
* bush: 確率付きの規則による茂み。乱数のシードを変えた 3 本
* tree: 3 次元で枝分かれする木（第 16 章の散布の例でも使う）

hython での実行例（examples/houdini で）:

    hython build_lsystem.py
"""

from __future__ import annotations

import hou

from hou_common import check_errors, describe, finish, out_path, recreate_geo, save_hip


def add_lsystem(geo: hou.Node, name: str, premise: str, rules: list[str], generations: int,
                angle: float, step: float) -> hou.Node:
    """L-System SOP を作り、公理（premise）と書き換え規則を設定して返す。

    rules の各要素は「記号=置き換え後の文字列」の形で書く。末尾に「:0.5」のように
    確率を付けると、同じ記号に対する複数の規則から、確率に従って 1 つが選ばれる。
    """
    lsystem = geo.createNode("lsystem", name)
    lsystem.parm("type").set("skel")  # 枝を折れ線で出力する（"tube" なら管）
    lsystem.parm("generations").set(generations)
    lsystem.parm("angleinit").set(angle)
    lsystem.parm("stepinit").set(step)
    lsystem.parm("stepscale").set(0.9)  # 記号 " で枝の長さに掛ける倍率
    lsystem.parm("premise").set(premise)
    for index in range(1, 26):  # L-System SOP は最大 25 個の規則を持てる
        lsystem.parm(f"rule{index}").set(rules[index - 1] if index <= len(rules) else "")
    return lsystem


def add_tree(geo: hou.Node, name: str = "tree") -> hou.Node:
    """3 次元で枝分かれする木の L-System SOP を作って返す。

    A は「これから枝分かれする芽」を表す。! で枝を細くし、" で枝を短くしてから、
    /(120) で軸のまわりに 120 度ずつ回しながら 3 本の枝 [B] を出す。
    B の & は、枝を既定の角度（angleinit の 22 度）だけ倒す。
    """
    return add_lsystem(geo, name, premise="FFA",
                       rules=['A=!"[B]/(120)[B]/(120)[B]', "B=&FF!A"],
                       generations=8, angle=22.0, step=0.25)


def build() -> hou.Node:
    """/obj/lsystem を作り、全部を並べたマージノードの出力を返す。"""
    geo = recreate_geo("lsystem")

    # 平面の草: F を「1 歩進んで、左右に枝を出す」形に書き換え続ける。
    plant = add_lsystem(geo, "plant", premise="F",
                        rules=["F=F[+F]F[-F]F"], generations=4, angle=25.7, step=0.05)

    # 確率付きの規則: F の書き換え方が 3 通りあり、どれになるかを乱数で決める。
    bush_rules = ["F=F[+F]F[-F]F:0.34", "F=F[+F]F:0.33", "F=F[-F]F:0.33"]
    bushes = []
    for index, seed in enumerate((1, 2, 3)):
        bush = add_lsystem(geo, f"bush_seed{seed}", premise="F",
                           rules=bush_rules, generations=5, angle=25.7, step=0.03)
        bush.parm("randseed").set(seed)
        bush.parm("tx").set(1.5 + 1.2 * index)  # 横に並べる
        bushes.append(bush)

    tree = add_tree(geo)
    tree.parm("tx").set(6.0)

    merge = geo.createNode("merge", "merge")
    for index, node in enumerate([plant, *bushes, tree]):
        merge.setInput(index, node)
    out = geo.createNode("null", "OUT_lsystem")
    out.setFirstInput(merge)
    finish(geo, out)
    return out


def main() -> None:
    out = build()
    geo = out.parent()
    check_errors(geo)
    for node in geo.children():
        if node.type().name() == "lsystem":
            print(describe(node))
    out.geometry().saveToFile(out_path("lsystem.obj").as_posix())  # 確認用に OBJ 形式でも書き出す
    print(f"保存した: {save_hip('lsystem')}")


if __name__ == "__main__":
    main()
