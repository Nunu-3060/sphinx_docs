"""cryptography ライブラリによるデジタル署名（RSA-PSS / ECDSA / Ed25519）。

実行方法::

    pip install cryptography
    python signatures_demo.py
"""

from collections.abc import Callable

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

MESSAGE = b"I will pay Bob 100 yen."
TAMPERED = b"I will pay Bob 900 yen."
PSS = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH)


def check(name: str, message: bytes, verify: Callable[[bytes], None]) -> None:
    """verify(message) を呼び、検証結果を表示する。"""
    try:
        verify(message)
        print(f"  {name}: 検証成功")
    except InvalidSignature:
        print(f"  {name}: 検証失敗")


def demo_rsa_pss() -> None:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    signature = private_key.sign(MESSAGE, PSS, hashes.SHA256())
    public_key = private_key.public_key()
    print(f"RSA-PSS（署名 {len(signature)} バイト）")
    for label, message in [("正しいメッセージ", MESSAGE), ("改ざんされたメッセージ", TAMPERED)]:
        check(label, message, lambda m: public_key.verify(signature, m, PSS, hashes.SHA256()))


def demo_ecdsa() -> None:
    private_key = ec.generate_private_key(ec.SECP256R1())
    signature = private_key.sign(MESSAGE, ec.ECDSA(hashes.SHA256()))
    public_key = private_key.public_key()
    print(f"ECDSA P-256（署名 {len(signature)} バイト、DER 形式）")
    for label, message in [("正しいメッセージ", MESSAGE), ("改ざんされたメッセージ", TAMPERED)]:
        check(label, message, lambda m: public_key.verify(signature, m, ec.ECDSA(hashes.SHA256())))


def demo_ed25519() -> None:
    private_key = Ed25519PrivateKey.generate()
    signature = private_key.sign(MESSAGE)
    public_key = private_key.public_key()
    print(f"Ed25519（署名 {len(signature)} バイト）")
    print(f"  同じメッセージの署名は同じか: {signature == private_key.sign(MESSAGE)}（決定的）")
    for label, message in [("正しいメッセージ", MESSAGE), ("改ざんされたメッセージ", TAMPERED)]:
        check(label, message, lambda m: public_key.verify(signature, m))


def main() -> None:
    demo_rsa_pss()
    demo_ecdsa()
    demo_ed25519()


if __name__ == "__main__":
    main()
