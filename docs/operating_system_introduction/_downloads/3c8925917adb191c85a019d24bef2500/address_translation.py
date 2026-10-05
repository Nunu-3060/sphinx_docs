"""ページテーブルによるアドレス変換のサンプル。

ページサイズを 4 KiB とし、仮想アドレスを

* ページ番号 (上位ビット)
* ページ内オフセット (下位 12 ビット)

に分けて、ページテーブルで物理アドレスに変換します。
ページテーブルに載っていないページを参照するとページフォールトになります。

実行方法::

    python address_translation.py
"""

PAGE_SIZE = 4096  # 4 KiB
OFFSET_BITS = 12  # 4096 = 2 ** 12

# ページテーブル: ページ番号 → フレーム番号
# 載っていないページは物理メモリに割り当てられていない
PAGE_TABLE: dict[int, int] = {
    0: 5,
    1: 2,
    2: 7,
    4: 1,
}


class PageFault(Exception):
    """ページテーブルにないページを参照したときの例外。"""


def translate(virtual: int) -> int:
    """仮想アドレスを物理アドレスに変換する。"""
    page = virtual >> OFFSET_BITS  # 上位ビットがページ番号
    offset = virtual & (PAGE_SIZE - 1)  # 下位 12 ビットがオフセット
    if page not in PAGE_TABLE:
        raise PageFault(f"ページ {page} は物理メモリにありません")
    frame = PAGE_TABLE[page]
    return (frame << OFFSET_BITS) | offset


def main() -> None:
    addresses = [0x0000, 0x0ABC, 0x1004, 0x2FFF, 0x3000, 0x4010]
    print("仮想アドレス  ページ  オフセット  物理アドレス")
    for virtual in addresses:
        page = virtual >> OFFSET_BITS
        offset = virtual & (PAGE_SIZE - 1)
        try:
            physical = f"0x{translate(virtual):05X}"
        except PageFault as e:
            physical = f"ページフォールト ({e})"
        print(f"     0x{virtual:05X}  {page:>6}  0x{offset:03X}"
              f"       {physical}")


if __name__ == "__main__":
    main()
