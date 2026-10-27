"""第 11 章: 畳み込み演算とプーリングを NumPy で実装し、PyTorch の結果と比較する。

実行方法:
    python ch11_convolution_numpy.py
"""
import numpy as np
import torch
import torch.nn.functional as F
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def conv2d(image: FloatArray, kernel: FloatArray, stride: int = 1, padding: int = 0) -> FloatArray:
    """1 チャネル画像に 1 枚のフィルタを適用する (深層学習の慣習どおり、フィルタは反転しない)。"""
    if padding > 0:
        image = np.pad(image, padding)
    kh, kw = kernel.shape
    out_h = (image.shape[0] - kh) // stride + 1
    out_w = (image.shape[1] - kw) // stride + 1
    out = np.zeros((out_h, out_w))
    for i in range(out_h):
        for j in range(out_w):
            patch = image[i * stride:i * stride + kh, j * stride:j * stride + kw]
            out[i, j] = np.sum(patch * kernel)
    return out


def max_pool(x: FloatArray, size: int = 2) -> FloatArray:
    """size x size の領域ごとに最大値を取る (ストライドは size)。"""
    h, w = x.shape[0] // size, x.shape[1] // size
    result: FloatArray = x[:h * size, :w * size].reshape(h, size, w, size).max(axis=(1, 3))
    return result


def main() -> None:
    # 中央に縦線が 1 本ある 6x6 の画像
    image = np.zeros((6, 6))
    image[:, 3] = 1.0

    # 縦方向のエッジ (左右の明るさの差) に反応するフィルタ
    kernel = np.array([[1.0, 0.0, -1.0],
                       [1.0, 0.0, -1.0],
                       [1.0, 0.0, -1.0]])

    out = conv2d(image, kernel, stride=1, padding=1)
    print("入力画像:\n", image)
    print("畳み込みの出力 (特徴マップ):\n", out)
    print("2x2 最大プーリングの出力:\n", max_pool(out))

    # PyTorch の conv2d は形状 (バッチ, チャネル, 高さ, 幅) のテンソルを受け取る
    expected = F.conv2d(torch.tensor(image)[None, None], torch.tensor(kernel)[None, None], padding=1)
    print("PyTorch の結果と一致するか:", np.allclose(out, expected[0, 0].numpy()))


if __name__ == "__main__":
    main()
