"""認証局（CA）とサーバーの証明書を生成し、証明書チェーンを検証する。

cryptography ライブラリで次の処理を行う。

1. 自己署名のルート CA 証明書を作る。
2. ルート CA の秘密鍵でサーバー証明書に署名する。
3. サーバー証明書の内容を表示し、ルート CA が発行したものであることを検証する。

実行方法::

    pip install cryptography
    python inspect_cert.py
"""

import datetime

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID


def make_name(common_name: str) -> x509.Name:
    """CN（コモンネーム）と O（組織名）からなる識別名を作る。"""
    return x509.Name([
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Example Org"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])


def make_ca() -> tuple[ec.EllipticCurvePrivateKey, x509.Certificate]:
    """自己署名のルート CA 証明書を作る。"""
    key = ec.generate_private_key(ec.SECP256R1())
    name = make_name("Example Root CA")
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)  # 自己署名なので発行者と主体が同じ
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(key, hashes.SHA256())
    )
    return key, cert


def make_server_cert(ca_key: ec.EllipticCurvePrivateKey, ca_cert: x509.Certificate) -> x509.Certificate:
    """CA の秘密鍵で www.example.com のサーバー証明書に署名する。"""
    server_key = ec.generate_private_key(ec.SECP256R1())
    now = datetime.datetime.now(datetime.timezone.utc)
    return (
        x509.CertificateBuilder()
        .subject_name(make_name("www.example.com"))
        .issuer_name(ca_cert.subject)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=90))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName("www.example.com")]), critical=False)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256())
    )


def main() -> None:
    ca_key, ca_cert = make_ca()
    server_cert = make_server_cert(ca_key, ca_cert)

    print(f"主体（Subject）  : {server_cert.subject.rfc4514_string()}")
    print(f"発行者（Issuer）  : {server_cert.issuer.rfc4514_string()}")
    print(f"シリアル番号      : {server_cert.serial_number:x}")
    print(f"有効期間          : {server_cert.not_valid_before_utc} 〜 {server_cert.not_valid_after_utc}")
    san = server_cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    print(f"SAN（DNS 名）     : {san.value.get_values_for_type(x509.DNSName)}")
    hash_algorithm = server_cert.signature_hash_algorithm
    print(f"署名のハッシュ関数: {hash_algorithm.name if hash_algorithm else 'なし'}")

    # サーバー証明書の署名を CA の公開鍵で検証する（失敗すると例外が送出される）
    server_cert.verify_directly_issued_by(ca_cert)
    print("サーバー証明書は Example Root CA によって発行されたことを確認した")


if __name__ == "__main__":
    main()
