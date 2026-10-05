"""2 段ページテーブルと TLB によるアドレス変換のシミュレーター。

RISC-V の Sv32 と同じく、32 ビットの仮想アドレスを VPN[1]（10 ビット）、
VPN[0]（10 ビット）、ページ内オフセット（12 ビット）に分け、4 KiB の
ページ単位で物理アドレスに変換します。TLB は 4 エントリのフル
アソシアティブで、LRU で置換します。各アクセスについて、TLB のヒット
／ミス、ページフォールトの有無、物理アドレスを表示します。

実行方法: python tlb_sim.py
"""

import unicodedata
from collections import OrderedDict
from dataclasses import dataclass

PAGE_BITS = 12  # ページの大きさは 2^12 = 4096 バイト
TLB_ENTRIES = 4


@dataclass
class PTE:
    """ページテーブルエントリ（必要な項目だけ）。"""

    frame: int  # 物理ページ番号（ページフレーム番号）
    valid: bool = True  # 有効ビット
    writable: bool = True  # 書き込みを許すか（保護ビット）
    accessed: bool = False  # 参照ビット
    dirty: bool = False  # ダーティビット


class MMU:
    """ページテーブルウォークを行う MMU と TLB。"""

    def __init__(self) -> None:
        # 1 段目の表: VPN[1] -> 2 段目の表（VPN[0] -> PTE）
        self.root: dict[int, dict[int, PTE]] = {}
        self.tlb: OrderedDict[int, PTE] = OrderedDict()  # VPN -> PTE
        self.next_frame = 0x80  # OS が次に割り当てるページフレーム
        self.walk_reads = 0  # ページテーブルウォークでのメモリ読み出し回数

    def map(self, vpn: int, frame: int, writable: bool = True) -> None:
        """OS の役割: 仮想ページ vpn をページフレーム frame に対応させる。"""
        table = self.root.setdefault(vpn >> 10, {})
        table[vpn & 0x3FF] = PTE(frame, writable=writable)

    def walk(self, vpn: int) -> PTE | None:
        """ページテーブルを 2 段たどって PTE を探す（ハードウェアの役割）。"""
        self.walk_reads += 1  # 1 段目のエントリを読む
        table = self.root.get(vpn >> 10)
        if table is None:
            return None
        self.walk_reads += 1  # 2 段目のエントリを読む
        pte = table.get(vpn & 0x3FF)
        return pte if pte is not None and pte.valid else None

    def translate(self, va: int, write: bool) -> tuple[str, str, str]:
        """仮想アドレス va を変換し、(TLB, 例外, 物理アドレス) を返す。"""
        vpn, offset = va >> PAGE_BITS, va & ((1 << PAGE_BITS) - 1)
        fault = "-"
        pte = self.tlb.get(vpn)
        if pte is not None:
            tlb = "ヒット"
            self.tlb.move_to_end(vpn)
        else:
            tlb = "ミス"
            pte = self.walk(vpn)
            if pte is None:
                # ページフォールト: OS が空きフレームを割り当てて再実行する
                fault = "ページフォールト"
                self.map(vpn, self.next_frame)
                self.next_frame += 1
                pte = self.walk(vpn)
                assert pte is not None
            if len(self.tlb) >= TLB_ENTRIES:
                self.tlb.popitem(last=False)  # LRU のエントリを追い出す
            self.tlb[vpn] = pte
        if write and not pte.writable:
            return tlb, "保護違反", "-"
        pte.accessed = True
        pte.dirty = pte.dirty or write
        return tlb, fault, f"0x{(pte.frame << PAGE_BITS) | offset:08x}"


def pad(text: str, width: int) -> str:
    """全角文字を幅 2 として、text の右に空白を足して幅 width にする。"""
    w = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1
            for c in text)
    return text + " " * max(width - w, 0)


def main() -> None:
    """仮想アドレス列を変換し、結果を 1 行ずつ表示する。"""
    mmu = MMU()
    mmu.map(0x00010, 0x20, writable=False)  # コード（読み出し専用）
    mmu.map(0x00011, 0x21, writable=False)
    mmu.map(0x10000, 0x35)  # データ
    mmu.map(0x10001, 0x36)
    accesses = [
        (0x00010004, False), (0x00010008, False), (0x10000010, True),
        (0x10001ff0, False), (0x00011000, False), (0x10000014, False),
        (0x20000000, True), (0x00010010, False), (0x10001ff4, True),
        (0x00010020, True),
    ]
    print("仮想アドレス  VPN[1]  VPN[0]  オフセット  操作  "
          "TLB     例外              物理アドレス")
    for va, write in accesses:
        tlb, fault, pa = mmu.translate(va, write)
        op = "W" if write else "R"
        print(f"0x{va:08x}  {va >> 22:>8x}{(va >> 12) & 0x3FF:>8x}"
              f"{va & 0xFFF:>12x}{op:>6}  {pad(tlb, 8)}{pad(fault, 18)}{pa}")
    print(f"ページテーブルウォークのメモリ読み出し: {mmu.walk_reads} 回")


if __name__ == "__main__":
    main()
