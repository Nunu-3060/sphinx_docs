"""第 12 章: Scaled Dot-Product Attention を NumPy で実装し、PyTorch の結果と比較する。

実行方法:
    python ch12_attention.py
"""
import numpy as np
import torch
import torch.nn.functional as F
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def softmax(z: FloatArray, axis: int = -1) -> FloatArray:
    """数値的に安定なソフトマックス (最大値を引いてから exp を取る)。"""
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    result: FloatArray = e / e.sum(axis=axis, keepdims=True)
    return result


def scaled_dot_product_attention(q: FloatArray, k: FloatArray, v: FloatArray,
                                 causal: bool = False) -> tuple[FloatArray, FloatArray]:
    """Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V を計算し、出力と重みを返す。"""
    d_k = q.shape[-1]
    scores = q @ k.swapaxes(-1, -2) / np.sqrt(d_k)
    if causal:
        # 未来の位置を参照しないよう、対角より上を -inf にする
        n = scores.shape[-1]
        scores = np.where(np.triu(np.ones((n, n), dtype=bool), k=1), -np.inf, scores)
    weights = softmax(scores)
    return weights @ v, weights


def main() -> None:
    rng = np.random.default_rng(0)
    seq_len, d_model = 4, 8
    x = rng.normal(size=(seq_len, d_model))  # 4 個のトークンの埋め込みベクトル

    # 学習可能な行列で入力をクエリ・キー・バリューに変換する (ここでは乱数で代用する)
    w_q, w_k, w_v = (rng.normal(size=(d_model, d_model)) / np.sqrt(d_model) for _ in range(3))
    q, k, v = x @ w_q, x @ w_k, x @ w_v

    out, weights = scaled_dot_product_attention(q, k, v)
    np.set_printoptions(precision=3, suppress=True)
    print("Attention の重み (各行の和は 1):\n", weights)
    print("出力の形状:", out.shape)

    _, causal_weights = scaled_dot_product_attention(q, k, v, causal=True)
    print("因果マスク付きの重み (上三角が 0):\n", causal_weights)

    expected = F.scaled_dot_product_attention(torch.tensor(q), torch.tensor(k), torch.tensor(v))
    print("PyTorch の結果と一致するか:", np.allclose(out, expected.numpy()))


if __name__ == "__main__":
    main()
