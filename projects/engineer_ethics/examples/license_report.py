"""インストール済みパッケージのライセンスを一覧表示するサンプルです。

OSS を利用するときは、ライセンスが定める義務（著作権表示の掲載、
ソースコードの開示など）を守る必要があります。まずは自分のプロジェクトが
どのライセンスのパッケージに依存しているかを把握することが第一歩です。

パッケージのメタデータに記載されたライセンス情報は自己申告であり、
誤りや記載漏れがあり得ます。重要な判断をする前には、
各パッケージに同梱されているライセンス文書を必ず確認してください。

実行方法::

    python license_report.py
"""

from importlib import metadata

UNKNOWN = "（記載なし）"


def first_value(dist: metadata.Distribution, field: str) -> str | None:
    """メタデータの指定したフィールドの最初の値を返します。"""
    values = dist.metadata.get_all(field)
    if not values:
        return None
    value = str(values[0]).strip()
    return value or None


def license_of(dist: metadata.Distribution) -> str:
    """パッケージのライセンスを、信頼できる情報源から順に調べて返します。"""
    # 1. PEP 639 で定められた SPDX 形式のライセンス表記
    expression = first_value(dist, "License-Expression")
    if expression:
        return expression

    # 2. 「License :: OSI Approved :: MIT License」のような分類子
    classifiers = dist.metadata.get_all("Classifier") or []
    licenses = [str(c).split(" :: ")[-1] for c in classifiers
                if str(c).startswith("License ::")]
    if licenses:
        return ", ".join(licenses)

    # 3. 自由記述の License フィールド（全文が入っていることがあるため 1 行目のみ）
    text = first_value(dist, "License")
    if text:
        return text.splitlines()[0]

    return UNKNOWN


def main() -> None:
    """パッケージ名、バージョン、ライセンスを表形式で表示します。"""
    rows = sorted(
        (
            (first_value(dist, "Name") or UNKNOWN, dist.version,
             license_of(dist))
            for dist in metadata.distributions()
        ),
        key=lambda row: row[0].lower(),
    )

    print(f"{'パッケージ':<27}{'バージョン':<11}ライセンス")
    for name, version, license_name in rows:
        print(f"{name:<32}{version:<16}{license_name}")


if __name__ == "__main__":
    main()
