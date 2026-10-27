"""第 9 章: 2 層ニューラルネットワークを NumPy でスクラッチ実装する。

構成: 入力 (2) -> 全結合 -> ReLU -> 全結合 -> シグモイド -> 出力 (1)
誤差逆伝播法で勾配を求め、数値微分で求めた勾配と一致することを確認したうえで、
直線では分離できない XOR 型のデータを学習する。

実行方法:
    python ch09_two_layer_net.py
"""
import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]
Params = dict[str, FloatArray]


def make_xor_data(n: int, seed: int = 0) -> tuple[FloatArray, FloatArray]:
    """第 1 象限と第 3 象限をクラス 1、それ以外をクラス 0 とするデータ。"""
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1.0, 1.0, size=(n, 2))
    y = (x[:, 0] * x[:, 1] > 0).astype(np.float64).reshape(-1, 1)
    return x, y


def init_params(n_in: int, n_hidden: int, n_out: int, seed: int = 0) -> Params:
    """He の初期化 (ReLU 向け) で重みを初期化し、バイアスは 0 とする。"""
    rng = np.random.default_rng(seed)
    return {
        "W1": rng.normal(0.0, np.sqrt(2.0 / n_in), size=(n_in, n_hidden)),
        "b1": np.zeros(n_hidden),
        "W2": rng.normal(0.0, np.sqrt(2.0 / n_hidden), size=(n_hidden, n_out)),
        "b2": np.zeros(n_out),
    }


def forward(params: Params, x: FloatArray) -> tuple[FloatArray, dict[str, FloatArray]]:
    """順伝播。出力 (確率) と、逆伝播で使う中間値を返す。"""
    a1 = x @ params["W1"] + params["b1"]
    h1 = np.maximum(a1, 0.0)
    a2 = h1 @ params["W2"] + params["b2"]
    p: FloatArray = 1.0 / (1.0 + np.exp(-a2))
    return p, {"x": x, "a1": a1, "h1": h1}


def loss(p: FloatArray, y: FloatArray, eps: float = 1e-12) -> float:
    """2 値交差エントロピー (ミニバッチの平均)。"""
    p = np.clip(p, eps, 1.0 - eps)
    return float(-np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p)))


def backward(params: Params, p: FloatArray, y: FloatArray, cache: dict[str, FloatArray]) -> Params:
    """誤差逆伝播法で各パラメータの勾配を求める。"""
    n = y.shape[0]
    # シグモイド + 交差エントロピーの勾配は (p - y) / n にまとまる
    d_a2 = (p - y) / n
    grads = {
        "W2": cache["h1"].T @ d_a2,
        "b2": d_a2.sum(axis=0),
    }
    d_h1 = d_a2 @ params["W2"].T
    d_a1 = d_h1 * (cache["a1"] > 0.0)  # ReLU の微分は入力が正なら 1、それ以外は 0
    grads["W1"] = cache["x"].T @ d_a1
    grads["b1"] = d_a1.sum(axis=0)
    return grads


def numerical_grads(params: Params, x: FloatArray, y: FloatArray, h: float = 1e-5) -> Params:
    """中心差分で勾配を近似する (勾配確認用。遅いので学習には使わない)。"""
    grads: Params = {}
    for name, value in params.items():
        g = np.zeros_like(value)
        for idx in np.ndindex(value.shape):
            original = value[idx]
            value[idx] = original + h
            loss_plus = loss(forward(params, x)[0], y)
            value[idx] = original - h
            loss_minus = loss(forward(params, x)[0], y)
            value[idx] = original
            g[idx] = (loss_plus - loss_minus) / (2.0 * h)
        grads[name] = g
    return grads


def main() -> None:
    x, y = make_xor_data(400)
    params = init_params(2, 16, 1)

    # 勾配確認: 誤差逆伝播法と数値微分の差が十分小さいことを確かめる
    p, cache = forward(params, x[:10])
    analytic = backward(params, p, y[:10], cache)
    numeric = numerical_grads(params, x[:10], y[:10])
    for name in params:
        diff = np.max(np.abs(analytic[name] - numeric[name]))
        print(f"勾配確認 {name}: 最大誤差 = {diff:.2e}")

    # ミニバッチ確率的勾配降下法で学習する
    rng = np.random.default_rng(1)
    lr, batch_size = 0.5, 32
    for epoch in range(301):
        order = rng.permutation(len(x))
        for start in range(0, len(x), batch_size):
            batch = order[start:start + batch_size]
            p, cache = forward(params, x[batch])
            grads = backward(params, p, y[batch], cache)
            for name in params:
                params[name] -= lr * grads[name]
        if epoch % 50 == 0:
            p_all, _ = forward(params, x)
            accuracy = float(np.mean((p_all >= 0.5) == y))
            print(f"epoch {epoch:3d}: loss = {loss(p_all, y):.4f}, 正解率 = {accuracy:.3f}")


if __name__ == "__main__":
    main()
