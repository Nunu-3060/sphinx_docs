"""L-system (Lindenmayer system) による再帰的図形の生成。

L-system は、文字列の書き換え規則（production rule）を繰り返し適用して
複雑な文字列を作り、それをタートルグラフィックスとして解釈することで
樹木状の分岐構造やコッホ曲線のような再帰的フラクタルを描く手法。

書き換え自体は単純な文字列置換の繰り返しであり、意味を持つのは
``draw_l_system`` 側の解釈規則である。本実装では以下の記号を使う。

- ``F`` / ``G``: 現在の向きに ``step`` だけ前進しながら線を引く
- ``+`` / ``-``: 向きを ``angle_deg`` だけ左/右に回転する
- ``[`` / ``]``: 現在の位置と向きをスタックに退避/復帰する（分岐の起点）
- それ以外の文字（``X`` など）: 書き換え規則を駆動するだけで、
  タートル側では無視される

どの文字を「前進して線を引く」記号として扱うかは ``draw_l_system``
の ``draw_chars`` 引数で切り替えられる。専用の終端記号 ``F`` を
使わず、非終端記号そのもの（例えばペンローズタイルの ``M/N/O/P``）を
前進の合図として使う流儀の規則にも対応するためである。
"""

import math

from PIL import Image, ImageDraw


def generate(axiom: str, rules: dict[str, str], iterations: int) -> str:
    """axiom に production rules を iterations 回適用した文字列を返す。

    各文字を ``rules`` に従って並列に置換する処理を ``iterations`` 回
    繰り返す。``rules`` に登録のない文字はそのまま残る。
    """
    current: str = axiom
    for _ in range(iterations):
        rewritten: list[str] = [rules.get(ch, ch) for ch in current]
        current = "".join(rewritten)
    return current


def draw_l_system(
    instructions: str,
    angle_deg: float,
    step: float,
    start_pos: tuple[float, float],
    start_angle_deg: float,
    image_size: tuple[int, int],
    line_color: tuple[int, int, int] = (30, 120, 40),
    background: tuple[int, int, int] = (255, 255, 255),
    draw_chars: str = "FG",
) -> Image.Image:
    """L-systemの文字列をタートルグラフィックスとして解釈し描画する。

    ``draw_chars`` に含まれる文字が現れるたびに、現在の向きへ
    ``step`` だけ前進しながら線を引く。既定の ``"FG"`` は専用の
    終端記号を使う流儀向けで、非終端記号自体を前進の合図として
    使う規則（例えばペンローズタイル）では、その記号を渡す。
    """
    image: Image.Image = Image.new("RGB", image_size, background)
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)

    x: float
    y: float
    x, y = start_pos
    angle: float = start_angle_deg
    stack: list[tuple[float, float, float]] = []

    for command in instructions:
        if command in draw_chars:
            rad: float = math.radians(angle)
            next_x: float = x + step * math.cos(rad)
            next_y: float = y + step * math.sin(rad)
            draw.line([(x, y), (next_x, next_y)], fill=line_color)
            x, y = next_x, next_y
        elif command == "+":
            angle += angle_deg
        elif command == "-":
            angle -= angle_deg
        elif command == "[":
            stack.append((x, y, angle))
        elif command == "]":
            x, y, angle = stack.pop()

    return image


def main() -> None:
    # 古典的な植物風フラクタル（Prusinkiewicz & Lindenmayer,
    # "The Algorithmic Beauty of Plants" に載る規則の一つ）。
    # X はダミー記号で、分岐の骨組みを増やすためだけに使う。
    plant_rules: dict[str, str] = {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}
    plant_str: str = generate("X", plant_rules, iterations=5)
    plant_image: Image.Image = draw_l_system(
        plant_str,
        angle_deg=25.0,
        step=5.0,
        start_pos=(210.0, 505.0),
        start_angle_deg=-90.0,
        image_size=(350, 520),
    )
    plant_image.save("l_system_tree.png")

    # コッホ雪片: 正三角形を初期形とし、各辺をコッホ曲線の生成規則
    # F -> F+F--F+F (角度60度) で置き換える。
    koch_rules: dict[str, str] = {"F": "F+F--F+F"}
    koch_str: str = generate("F--F--F", koch_rules, iterations=4)
    koch_image: Image.Image = draw_l_system(
        koch_str,
        angle_deg=60.0,
        step=6.0,
        start_pos=(60.0, 450.0),
        start_angle_deg=0.0,
        image_size=(600, 620),
        line_color=(30, 90, 160),
    )
    koch_image.save("koch_snowflake.png")

    # ペンローズタイル: 専用の終端記号を使わず、非終端記号 M/N/O/P
    # 自体を前進の合図として使う流儀の規則。A は使い切りの前進命令
    # で、次の世代では空文字列に置き換わって消える。角度36度は
    # 5回対称に対応する。
    penrose_rules: dict[str, str] = {
        "M": "OA++PA----NA[-OA----MA]++",
        "N": "+OA--PA[---MA--NA]+",
        "O": "-MA++NA[+++OA++PA]-",
        "P": "--OA++++MA[+PA++++NA]--NA",
        "A": "",
    }
    penrose_str: str = generate(
        "[N]++[N]++[N]++[N]++[N]", penrose_rules, iterations=5
    )
    penrose_image: Image.Image = draw_l_system(
        penrose_str,
        angle_deg=36.0,
        step=10.5,
        start_pos=(300.0, 300.0),
        start_angle_deg=0.0,
        image_size=(600, 600),
        line_color=(120, 50, 130),
        draw_chars="MNOPA",
    )
    penrose_image.save("penrose_lsystem.png")


if __name__ == "__main__":
    main()
