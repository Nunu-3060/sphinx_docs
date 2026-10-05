"""Unicode の正規化と、コードポイント数と見た目の文字数の違いを示すサンプル。

NFC・NFD・NFKC で文字列がどう変わるかを、コードポイントの列として表示する。
また、len() が数えるコードポイント数と、人間が 1 文字と感じる単位
（書記素クラスタ）の数が異なる例を示す。書記素クラスタの判定は、
UAX #29 の規則のうち代表的なものだけを実装した簡易版である。

出力にはコードポイント（U+XXXX）だけを表示し、絵文字や結合文字そのものは
表示しない。Windows のコンソール（cp932）でもエラーにならないようにするためである。
ソースコード中の文字も、見分けにくい文字は \\N{...} の名前で書いている。

実行方法: python ch01_unicode_normalize.py
関連する章: 第 1 章「情報の表現」（Unicode の正規化と書記素クラスタ）
"""

import unicodedata

ZWJ = "\N{ZERO WIDTH JOINER}"


def codepoints(s: str) -> str:
    """文字列をコードポイントの列（U+XXXX 表記）にする。"""
    return " ".join(f"U+{ord(c):04X}" for c in s)


def is_extender(c: str) -> bool:
    """直前の文字に続けて 1 つの書記素クラスタになる文字かを判定する。"""
    cp = ord(c)
    return (
        unicodedata.category(c) in ("Mn", "Me")  # 結合文字
        or 0xFE00 <= cp <= 0xFE0F                 # 異体字セレクタ
        or 0x1F3FB <= cp <= 0x1F3FF               # 肌の色の修飾子
        or c == ZWJ
    )


def is_regional_indicator(c: str) -> bool:
    """国旗を作る地域指示記号（U+1F1E6〜U+1F1FF）かを判定する。"""
    return 0x1F1E6 <= ord(c) <= 0x1F1FF


def graphemes(s: str) -> list[str]:
    """文字列を書記素クラスタに分割する（簡易版）。"""
    clusters: list[str] = []
    for c in s:
        if clusters:
            last = clusters[-1]
            joined = last.endswith(ZWJ)  # ZWJ の後の文字は結合する
            flag = (is_regional_indicator(c) and len(last) == 1
                    and is_regional_indicator(last))  # 2 個で 1 つの国旗
            if is_extender(c) or joined or flag:
                clusters[-1] = last + c
                continue
        clusters.append(c)
    return clusters


def show_forms(label: str, s: str) -> None:
    """各正規化形式でのコードポイント列を表示する。"""
    print(f"[{label}] 元: {codepoints(s)}")
    for form in ("NFC", "NFD", "NFKC"):
        t = unicodedata.normalize(form, s)
        print(f"  {form:4}: {codepoints(t)}")


def main() -> None:
    """正規化と書記素クラスタの例を順に表示する。"""
    composed = "\N{HIRAGANA LETTER GA}"
    decomposed = ("\N{HIRAGANA LETTER KA}"
                  "\N{COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK}")
    print("== 正規化 ==")
    show_forms("が（合成済み）", composed)
    show_forms("か + 結合用濁点", decomposed)
    show_forms("半角カナのガ", "\N{HALFWIDTH KATAKANA LETTER KA}"
               "\N{HALFWIDTH KATAKANA VOICED SOUND MARK}")
    show_forms("合字 fi", "\N{LATIN SMALL LIGATURE FI}")

    print("== 比較 ==")
    print(f"  そのまま      : {composed == decomposed}")
    nfc_a = unicodedata.normalize("NFC", composed)
    nfc_b = unicodedata.normalize("NFC", decomposed)
    print(f"  NFC にそろえる: {nfc_a == nfc_b}")

    print("== len() と書記素クラスタ ==")
    samples = [
        ("e + 結合アクセント", "e\N{COMBINING ACUTE ACCENT}"),
        ("国旗（日本）",
         "\N{REGIONAL INDICATOR SYMBOL LETTER J}"
         "\N{REGIONAL INDICATOR SYMBOL LETTER P}"),
        ("親指 + 肌の色",
         "\N{THUMBS UP SIGN}\N{EMOJI MODIFIER FITZPATRICK TYPE-4}"),
        ("家族（ZWJ 結合）",
         "\N{MAN}" + ZWJ + "\N{WOMAN}" + ZWJ + "\N{GIRL}"),
    ]
    for label, s in samples:
        n_bytes = len(s.encode("utf-8"))
        n_units = len(s.encode("utf-16-le")) // 2
        print(f"  {label}: {codepoints(s)}")
        print(f"    len={len(s)} 書記素={len(graphemes(s))}"
              f" UTF-8={n_bytes} バイト UTF-16={n_units} 単位")


if __name__ == "__main__":
    main()
