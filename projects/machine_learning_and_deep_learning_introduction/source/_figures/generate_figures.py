"""本文で使う図を生成する。conf.py から generate_all() が呼び出される。"""
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Ellipse, Rectangle  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

plt.rcParams['font.family'] = ['BIZ UDGothic', 'Yu Gothic', 'Meiryo', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

C0, C1, C2, C3 = '#1f77b4', '#d62728', '#2ca02c', '#ff7f0e'

FIGURES: list[Callable[[], plt.Figure]] = []


def figure(func: Callable[[], plt.Figure]) -> Callable[[], plt.Figure]:
    FIGURES.append(func)
    return func


def _boundary(ax: plt.Axes, predict: Callable[[np.ndarray], np.ndarray], x: np.ndarray, y: np.ndarray,
              title: str) -> None:
    """2 次元データの決定境界を描く。predict はクラス 1 の確率またはラベルを返す。"""
    x_min, x_max = x[:, 0].min() - 0.5, x[:, 0].max() + 0.5
    y_min, y_max = x[:, 1].min() - 0.5, x[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300), np.linspace(y_min, y_max, 300))
    zz = predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, zz, levels=np.linspace(0, 1, 11), cmap='RdBu_r', alpha=0.35)
    ax.contour(xx, yy, zz, levels=[0.5], colors='k', linewidths=1.5)
    ax.scatter(x[y == 0, 0], x[y == 0, 1], s=14, c=C0, edgecolors='w', linewidths=0.4, label='クラス 0')
    ax.scatter(x[y == 1, 0], x[y == 1, 1], s=14, c=C1, edgecolors='w', linewidths=0.4, label='クラス 1')
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)


# ---------------------------------------------------------------- 第 1 章


@figure
def ch01_ai_ml_dl() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6.5, 4))
    # (中心, 幅, 高さ, 色, ラベル, ラベルの位置)
    specs = [((0.0, 0.0), 6.0, 3.8, '#dbe9f6', '人工知能 (AI)', (0.0, 1.45)),
             ((0.55, -0.25), 4.4, 2.6, '#a9cbe8', '機械学習', (0.3, 0.6)),
             ((1.05, -0.5), 2.6, 1.4, '#5d9fd3', '深層学習', (1.05, -0.5))]
    for center, w, h, color, label, pos in specs:
        ax.add_patch(Ellipse(center, w, h, facecolor=color, edgecolor='#335', linewidth=1.2))
        ax.text(pos[0], pos[1], label, ha='center', va='center', fontsize=13)
    ax.set_xlim(-3.1, 3.1)
    ax.set_ylim(-2.0, 2.0)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig


# ---------------------------------------------------------------- 第 2 章


@figure
def ch02_derivative() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(5.5, 4))
    x = np.linspace(-0.5, 2.5, 200)
    ax.plot(x, x ** 2, color=C0, label=r'$f(x) = x^2$')
    ax.plot(x, 2 * (x - 1) + 1, '--', color=C1, label=r'$x = 1$ での接線 (傾き $f^\prime(1) = 2$)')
    h = 0.8
    ax.plot([1, 1 + h], [1, (1 + h) ** 2], 'o-', color=C2, label=r'$x = 1$ と $x = 1 + h$ を結ぶ直線')
    ax.plot(1, 1, 'ko')
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-1, 5)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$f(x)$')
    ax.legend(loc='upper left', fontsize=9)
    return fig


@figure
def ch02_gradient() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6, 4.5))
    x, y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-2, 2, 200))
    z = x ** 2 + 3 * y ** 2
    cs = ax.contour(x, y, z, levels=[0.5, 1, 2, 4, 6, 9, 12], cmap='viridis')
    ax.clabel(cs, fontsize=8)
    gx, gy = np.meshgrid(np.linspace(-2.5, 2.5, 7), np.linspace(-1.6, 1.6, 5))
    ax.quiver(gx, gy, -2 * gx, -6 * gy, color=C1, angles='xy', scale_units='xy', scale=12, width=0.004)
    ax.plot(0, 0, 'k*', markersize=12)
    ax.set_aspect('equal')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_title(r'$f(x, y) = x^2 + 3y^2$ の等高線と $-\nabla f$ (赤矢印)')
    return fig


@figure
def ch02_normal() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6, 3.5))
    x = np.linspace(-5, 5, 400)
    for mu, sigma, color in [(0, 1, C0), (0, 2, C1), (1.5, 0.6, C2)]:
        pdf = np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / np.sqrt(2 * np.pi * sigma ** 2)
        ax.plot(x, pdf, color=color, label=rf'$\mu = {mu}, \sigma = {sigma}$')
    ax.set_xlabel('$x$')
    ax.set_ylabel('確率密度')
    ax.legend()
    return fig


# ---------------------------------------------------------------- 第 3 章


@figure
def ch03_scaling() -> plt.Figure:
    rng = np.random.default_rng(0)
    area = rng.uniform(15, 80, 100)
    age = rng.uniform(0, 40, 100)
    raw = np.c_[area, age * 0.02]  # 単位の違いを強調するため 2 列目を小さくする
    std = (raw - raw.mean(axis=0)) / raw.std(axis=0)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    axes[0].scatter(raw[:, 0], raw[:, 1], s=12, c=C0)
    axes[0].set_title('標準化前 (列ごとに値の範囲が大きく違う)')
    axes[0].set_xlabel('特徴量 1 (15〜80)')
    axes[0].set_ylabel('特徴量 2 (0〜0.8)')
    # 縦軸と横軸を同じ範囲にして、特徴量 2 の値がほとんど変化していないように見えることを示す
    axes[0].set_xlim(0, 85)
    axes[0].set_ylim(-42.5, 42.5)
    axes[1].scatter(std[:, 0], std[:, 1], s=12, c=C1)
    axes[1].set_title('標準化後 (平均 0、標準偏差 1)')
    axes[1].set_xlabel('特徴量 1')
    axes[1].set_ylabel('特徴量 2')
    axes[1].set_aspect('equal')
    axes[1].set_xlim(-2.5, 2.5)
    axes[1].set_ylim(-2.5, 2.5)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------- 第 4 章


def _linear_data() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(0)
    x = rng.uniform(0.0, 2.0, size=100)
    y = 3.0 * x + 2.0 + rng.normal(0.0, 0.3, size=100)
    return x, y


@figure
def ch04_linear_fit() -> plt.Figure:
    x, y = _linear_data()
    w1, w0 = np.polyfit(x, y, 1)
    fig, ax = plt.subplots(figsize=(6, 4))
    idx = np.arange(0, 100, 7)
    ax.vlines(x[idx], y[idx], w0 + w1 * x[idx], colors=C3, linewidth=1, label='残差 (一部)')
    ax.scatter(x, y, s=12, c=C0, label='データ')
    xs = np.linspace(0, 2, 10)
    ax.plot(xs, w0 + w1 * xs, color=C1, label=rf'回帰直線 $\hat{{y}} = {w1:.2f}x + {w0:.2f}$')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.legend()
    return fig


@figure
def ch04_learning_rate() -> plt.Figure:
    x, y = _linear_data()
    xb = np.c_[np.ones_like(x), x]
    fig, ax = plt.subplots(figsize=(6, 4))
    for lr, color in [(0.01, C0), (0.1, C2), (0.55, C1)]:
        w = np.zeros(2)
        losses = []
        for _ in range(60):
            err = xb @ w - y
            losses.append(np.mean(err ** 2))
            w -= lr * 2 / len(y) * xb.T @ err
        ax.plot(losses, color=color, label=f'学習率 {lr}')
    ax.set_yscale('log')
    ax.set_ylim(0.03, 1e4)
    ax.set_xlabel('反復回数')
    ax.set_ylabel('損失 (MSE、対数目盛)')
    ax.legend()
    return fig


@figure
def ch04_polynomial() -> plt.Figure:
    rng = np.random.default_rng(0)
    x = rng.uniform(-3.0, 3.0, 100)
    y = 0.5 * x ** 2 - x + 1.0 + rng.normal(0.0, 0.5, 100)
    xs = np.linspace(-3, 3, 200)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(x, y, s=12, c=C0, label='データ')
    ax.plot(xs, np.polyval(np.polyfit(x, y, 1), xs), color=C3, label='直線 (1 次)')
    ax.plot(xs, np.polyval(np.polyfit(x, y, 2), xs), color=C1, label='2 次多項式')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.legend()
    return fig


# ---------------------------------------------------------------- 第 5 章


@figure
def ch05_sigmoid() -> plt.Figure:
    z = np.linspace(-8, 8, 300)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(z, 1 / (1 + np.exp(-z)), color=C0)
    ax.axhline(0.5, color='gray', linestyle='--', linewidth=1)
    ax.set_xlabel('$z$')
    ax.set_ylabel(r'$\sigma(z)$')
    ax.set_title(r'シグモイド関数 $\sigma(z) = 1 / (1 + e^{-z})$')
    return fig


def _two_blobs() -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(0)
    x0 = rng.normal([-1.0, -1.0], 1.0, size=(100, 2))
    x1 = rng.normal([1.5, 1.0], 1.0, size=(100, 2))
    return np.vstack([x0, x1]), np.r_[np.zeros(100), np.ones(100)].astype(int)


@figure
def ch05_logistic_boundary() -> plt.Figure:
    from sklearn.linear_model import LogisticRegression
    x, y = _two_blobs()
    model = LogisticRegression().fit(x, y)
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _boundary(ax, lambda p: model.predict_proba(p)[:, 1], x, y, '色の濃さ: クラス 1 である確率、黒線: 確率 0.5')
    ax.legend(loc='upper left')
    return fig


def _moons() -> tuple[np.ndarray, np.ndarray]:
    from sklearn.datasets import make_moons
    return make_moons(n_samples=400, noise=0.25, random_state=0)


@figure
def ch05_classifiers() -> plt.Figure:
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC
    x, y = _moons()
    models = [('ロジスティック回帰', LogisticRegression()),
              ('k 近傍法 (k=15)', KNeighborsClassifier(n_neighbors=15)),
              ('SVM (RBF カーネル)', SVC())]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    for ax, (name, clf) in zip(axes, models):
        model = make_pipeline(StandardScaler(), clf).fit(x, y)
        if hasattr(model, 'predict_proba'):
            _boundary(ax, lambda p, m=model: m.predict_proba(p)[:, 1], x, y, name)
        else:
            # SVM は確率を出力しないので、決定関数の値をシグモイド関数で 0〜1 に写して色を付ける
            _boundary(ax, lambda p, m=model: 1 / (1 + np.exp(-m.decision_function(p))), x, y, name)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------- 第 6 章


def _sin_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    from sklearn.model_selection import train_test_split
    rng = np.random.default_rng(1)
    x = rng.uniform(0.0, 1.0, 40)
    y = np.sin(2.0 * np.pi * x) + rng.normal(0.0, 0.2, 40)
    return train_test_split(x, y, test_size=0.5, random_state=0)


def _poly_model(degree: int, alpha: float | None = None):
    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler
    reg = LinearRegression() if alpha is None else Ridge(alpha=alpha)
    return make_pipeline(PolynomialFeatures(degree), StandardScaler(), reg)


@figure
def ch06_under_over() -> plt.Figure:
    x_tr, x_va, y_tr, y_va = _sin_data()
    xs = np.linspace(0, 1, 300)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), sharey=True)
    titles = {1: '次数 1 (未学習)', 3: '次数 3 (適切)', 15: '次数 15 (過学習)'}
    for ax, degree in zip(axes, [1, 3, 15]):
        model = _poly_model(degree).fit(x_tr[:, None], y_tr)
        ax.plot(xs, np.sin(2 * np.pi * xs), color='gray', linestyle='--', label='真の関数')
        ax.plot(xs, model.predict(xs[:, None]), color=C1, label='学習したモデル')
        ax.scatter(x_tr, y_tr, s=18, c=C0, label='訓練データ')
        ax.scatter(x_va, y_va, s=18, c=C3, marker='^', label='検証データ')
        ax.set_ylim(-1.8, 1.8)
        ax.set_title(titles[degree])
    axes[0].legend(fontsize=8, loc='lower left')
    fig.tight_layout()
    return fig


@figure
def ch06_error_vs_complexity() -> plt.Figure:
    x_tr, x_va, y_tr, y_va = _sin_data()
    degrees = list(range(1, 16))
    tr, va = [], []
    for d in degrees:
        model = _poly_model(d).fit(x_tr[:, None], y_tr)
        tr.append(np.mean((model.predict(x_tr[:, None]) - y_tr) ** 2))
        va.append(np.mean((model.predict(x_va[:, None]) - y_va) ** 2))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(degrees, tr, 'o-', color=C0, label='訓練誤差')
    ax.plot(degrees, va, 's-', color=C3, label='検証誤差')
    ax.set_yscale('log')
    ax.set_xlabel('多項式の次数 (モデルの複雑さ)')
    ax.set_ylabel('MSE (対数目盛)')
    ax.legend()
    return fig


@figure
def ch06_kfold() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7.5, 2.8))
    k = 5
    for i in range(k):
        for j in range(k):
            color = C3 if i == j else '#a9cbe8'
            ax.add_patch(Rectangle((j, k - 1 - i), 0.95, 0.8, facecolor=color, edgecolor='#335'))
        ax.text(-0.15, k - 1 - i + 0.4, f'{i + 1} 回目', ha='right', va='center')
        ax.text(k + 0.1, k - 1 - i + 0.4, f'スコア {i + 1}', ha='left', va='center')
    ax.add_patch(Rectangle((0.0, -1.0), 0.4, 0.5, facecolor='#a9cbe8', edgecolor='#335'))
    ax.text(0.5, -0.75, '学習に使う', va='center')
    ax.add_patch(Rectangle((2.2, -1.0), 0.4, 0.5, facecolor=C3, edgecolor='#335'))
    ax.text(2.7, -0.75, '評価に使う', va='center')
    ax.set_xlim(-1.2, 6.3)
    ax.set_ylim(-1.2, k)
    ax.axis('off')
    return fig


@figure
def ch06_roc() -> plt.Figure:
    from sklearn.datasets import load_breast_cancer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score, roc_curve
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    data = load_breast_cancer()
    x, y = data.data, 1 - data.target
    x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.3, stratify=y, random_state=0)
    fig, ax = plt.subplots(figsize=(5, 4.5))
    for cols, name, color in [(slice(None), '全特徴量', C0), ([0], '特徴量 1 個 (mean radius)', C3)]:
        model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(x_tr[:, cols], y_tr)
        p = model.predict_proba(x_te[:, cols])[:, 1]
        fpr, tpr, _ = roc_curve(y_te, p)
        ax.plot(fpr, tpr, color=color, label=f'{name} (AUC = {roc_auc_score(y_te, p):.3f})')
    ax.plot([0, 1], [0, 1], '--', color='gray', label='ランダム (AUC = 0.5)')
    ax.set_xlabel('偽陽性率 (FPR)')
    ax.set_ylabel('真陽性率 (TPR、再現率)')
    ax.legend(loc='lower right', fontsize=9)
    ax.set_aspect('equal')
    return fig


# ---------------------------------------------------------------- 第 7 章


@figure
def ch07_tree_boundary() -> plt.Figure:
    from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier
    x, y = _moons()
    models = [('決定木 (深さ 3)', DecisionTreeClassifier(max_depth=3, random_state=0)),
              ('決定木 (深さ制限なし)', DecisionTreeClassifier(random_state=0)),
              ('ランダムフォレスト', RandomForestClassifier(n_estimators=300, random_state=0)),
              ('勾配ブースティング', HistGradientBoostingClassifier(random_state=0))]
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.6))
    for ax, (name, model) in zip(axes, models):
        model.fit(x, y)
        _boundary(ax, lambda p, m=model: m.predict_proba(p)[:, 1], x, y, name)
    fig.tight_layout()
    return fig


@figure
def ch07_boosting_steps() -> plt.Figure:
    from sklearn.tree import DecisionTreeRegressor
    rng = np.random.default_rng(0)
    x = np.sort(rng.uniform(0, 1, 80))
    y = np.sin(2 * np.pi * x) + rng.normal(0, 0.15, 80)
    xs = np.linspace(0, 1, 400)
    pred = np.full_like(y, y.mean())
    pred_s = np.full_like(xs, y.mean())
    lr = 0.5
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), sharey=True)
    shown = {1: axes[0], 5: axes[1], 50: axes[2]}
    for m in range(1, 51):
        tree = DecisionTreeRegressor(max_depth=2).fit(x[:, None], y - pred)
        pred += lr * tree.predict(x[:, None])
        pred_s += lr * tree.predict(xs[:, None])
        if m in shown:
            ax = shown[m]
            ax.scatter(x, y, s=10, c=C0)
            ax.plot(xs, pred_s, color=C1)
            ax.set_title(f'木を {m} 本足した時点')
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------- 第 8 章


@figure
def ch08_kmeans() -> plt.Figure:
    rng = np.random.default_rng(0)
    true_centers = np.array([[0.0, 0.0], [4.0, 4.0], [0.0, 5.0]])
    x = np.vstack([rng.normal(c, 0.8, size=(100, 2)) for c in true_centers])
    centers = np.array([[1.0, 1.0], [1.5, 1.2], [2.0, 0.8]])
    colors = np.array([C0, C1, C2])
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.6), sharey=True)
    for step, ax in enumerate(axes):
        labels = np.argmin(np.linalg.norm(x[:, None] - centers[None], axis=2), axis=1)
        ax.scatter(x[:, 0], x[:, 1], s=8, c=colors[labels], alpha=0.6)
        ax.scatter(centers[:, 0], centers[:, 1], s=180, c='k', marker='X')
        ax.set_title('初期状態' if step == 0 else f'{step} 回更新後')
        centers = np.array([x[labels == c].mean(axis=0) for c in range(3)])
    fig.tight_layout()
    return fig


@figure
def ch08_pca_digits() -> plt.Figure:
    from sklearn.datasets import load_digits
    from sklearn.decomposition import PCA
    digits = load_digits()
    z = PCA(n_components=2).fit_transform(digits.data)
    fig, ax = plt.subplots(figsize=(6.5, 5))
    sc = ax.scatter(z[:, 0], z[:, 1], c=digits.target, cmap='tab10', s=8)
    cbar = fig.colorbar(sc, ax=ax, ticks=range(10))
    cbar.set_label('数字 (正解ラベル。PCA 自体はラベルを使わない)')
    ax.set_xlabel('第 1 主成分')
    ax.set_ylabel('第 2 主成分')
    return fig


# ---------------------------------------------------------------- 第 9 章


@figure
def ch09_activations() -> plt.Figure:
    z = np.linspace(-4, 4, 400)
    sig = 1 / (1 + np.exp(-z))
    funcs = [('シグモイド', sig, sig * (1 - sig)),
             ('tanh', np.tanh(z), 1 - np.tanh(z) ** 2),
             ('ReLU', np.maximum(z, 0), (z > 0).astype(float))]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))
    for ax, (name, f, df) in zip(axes, funcs):
        ax.plot(z, f, color=C0, label='関数')
        ax.plot(z, df, '--', color=C1, label='導関数')
        ax.set_title(name)
        ax.set_ylim(-1.2, 2.0)
        ax.legend(loc='upper left', fontsize=9)
    fig.tight_layout()
    return fig


@figure
def ch09_xor() -> plt.Figure:
    rng = np.random.default_rng(0)
    x = rng.uniform(-1.0, 1.0, size=(400, 2))
    y = (x[:, 0] * x[:, 1] > 0).astype(int)
    # 2 層ニューラルネットワーク (examples/ch09_two_layer_net.py と同じ構成) を学習する
    w1 = rng.normal(0, np.sqrt(2 / 2), (2, 16))
    b1 = np.zeros(16)
    w2 = rng.normal(0, np.sqrt(2 / 16), (16, 1))
    b2 = np.zeros(1)
    t = y[:, None].astype(float)

    def forward(p: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        a1 = p @ w1 + b1
        h1 = np.maximum(a1, 0)
        return 1 / (1 + np.exp(-(h1 @ w2 + b2))), a1, h1

    for _ in range(3000):
        out, a1, h1 = forward(x)
        d2 = (out - t) / len(x)
        d1 = (d2 @ w2.T) * (a1 > 0)
        w2 -= 0.5 * h1.T @ d2
        b2 -= 0.5 * d2.sum(0)
        w1 -= 0.5 * x.T @ d1
        b1 -= 0.5 * d1.sum(0)

    from sklearn.linear_model import LogisticRegression
    lin = LogisticRegression().fit(x, y)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    _boundary(axes[0], lambda p: lin.predict_proba(p)[:, 1], x, y, 'ロジスティック回帰 (直線の境界)')
    _boundary(axes[1], lambda p: forward(p)[0][:, 0], x, y, '2 層ニューラルネットワーク')
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------- 第 10 章


@figure
def ch10_optimizers() -> plt.Figure:
    def grad(p: np.ndarray) -> np.ndarray:
        return np.array([0.1 * p[0], 4.0 * p[1]])

    def sgd(lr: float) -> np.ndarray:
        p, path = np.array([-8.0, 2.0]), []
        for _ in range(60):
            path.append(p.copy())
            p = p - lr * grad(p)
        return np.array(path)

    def momentum(lr: float, beta: float = 0.9) -> np.ndarray:
        p, v, path = np.array([-8.0, 2.0]), np.zeros(2), []
        for _ in range(60):
            path.append(p.copy())
            v = beta * v - lr * grad(p)
            p = p + v
        return np.array(path)

    def adam(lr: float, b1: float = 0.9, b2: float = 0.999) -> np.ndarray:
        p, m, v, path = np.array([-8.0, 2.0]), np.zeros(2), np.zeros(2), []
        for t in range(1, 61):
            path.append(p.copy())
            g = grad(p)
            m = b1 * m + (1 - b1) * g
            v = b2 * v + (1 - b2) * g ** 2
            p = p - lr * (m / (1 - b1 ** t)) / (np.sqrt(v / (1 - b2 ** t)) + 1e-8)
        return np.array(path)

    xx, yy = np.meshgrid(np.linspace(-9, 3, 300), np.linspace(-2.5, 2.5, 300))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.contour(xx, yy, 0.05 * xx ** 2 + 2 * yy ** 2, levels=15, cmap='Greys', linewidths=0.7)
    for path, name, color in [(sgd(0.4), 'SGD (学習率 0.4)', C0), (momentum(0.1), 'モメンタム (学習率 0.1)', C2),
                              (adam(0.5), 'Adam (学習率 0.5)', C1)]:
        ax.plot(path[:, 0], path[:, 1], 'o-', markersize=3, linewidth=1, color=color, label=name)
    ax.plot(0, 0, 'k*', markersize=12)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_title(r'$f(x, y) = 0.05x^2 + 2y^2$ 上の 60 ステップの軌跡')
    ax.legend(loc='lower right', fontsize=9)
    return fig


@figure
def ch10_lr_schedule() -> plt.Figure:
    epochs = np.arange(100)
    step = 0.1 * 0.1 ** (epochs // 40)
    cosine = 0.05 * (1 + np.cos(np.pi * epochs / 100))
    warm = np.where(epochs < 10, 0.1 * (epochs + 1) / 10, 0.05 * (1 + np.cos(np.pi * (epochs - 10) / 90)))
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    ax.plot(epochs, step, color=C0, label='ステップ減衰')
    ax.plot(epochs, cosine, color=C2, label='コサイン減衰')
    ax.plot(epochs, warm, color=C1, label='ウォームアップ + コサイン減衰')
    ax.set_xlabel('エポック')
    ax.set_ylabel('学習率')
    ax.legend()
    return fig


# ---------------------------------------------------------------- 第 11 章


def _sample_image() -> np.ndarray:
    """Pillow で図形を描いた 64x64 のグレースケール画像を作る。"""
    img = Image.new('L', (64, 64), 0)
    draw = ImageDraw.Draw(img)
    draw.rectangle((8, 10, 30, 54), fill=255)
    draw.ellipse((34, 14, 58, 38), fill=180)
    draw.line((34, 56, 58, 44), fill=255, width=3)
    return np.asarray(img, dtype=float) / 255.0


def _conv2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    kh, kw = kernel.shape
    padded = np.pad(image, ((kh // 2, kh // 2), (kw // 2, kw // 2)))
    out = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            out[i, j] = np.sum(padded[i:i + kh, j:j + kw] * kernel)
    return out


@figure
def ch11_convolution() -> plt.Figure:
    image = _sample_image()
    kernels = [('縦エッジ検出', np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype=float)),
               ('横エッジ検出', np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=float)),
               ('ぼかし (平均)', np.full((5, 5), 1 / 25))]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.6))
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('入力画像')
    for ax, (name, k) in zip(axes[1:], kernels):
        out = _conv2d(image, k)
        lim = np.abs(out).max()
        ax.imshow(out, cmap='RdBu_r' if out.min() < 0 else 'gray', vmin=-lim if out.min() < 0 else 0, vmax=lim)
        ax.set_title(name)
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
    fig.tight_layout()
    return fig


@figure
def ch11_conv_operation() -> plt.Figure:
    image = np.array([[1, 2, 0, 1, 3],
                      [0, 1, 3, 1, 0],
                      [2, 1, 0, 2, 1],
                      [1, 0, 1, 3, 2],
                      [0, 2, 1, 0, 1]])
    kernel = np.array([[1, 0, -1],
                       [1, 0, -1],
                       [1, 0, -1]])
    out = np.array([[np.sum(image[i:i + 3, j:j + 3] * kernel) for j in range(3)] for i in range(3)])
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), gridspec_kw={'width_ratios': [5, 3, 3]})
    for ax, mat, title in [(axes[0], image, '入力 (5×5)'), (axes[1], kernel, 'フィルタ (3×3)'),
                           (axes[2], out, '出力 (3×3)')]:
        n_r, n_c = mat.shape
        for i in range(n_r):
            for j in range(n_c):
                hl = (mat is image and i < 3 and j < 3) or (mat is out and i == 0 and j == 0)
                ax.add_patch(Rectangle((j, n_r - 1 - i), 1, 1, facecolor='#ffd27f' if hl else 'white',
                                       edgecolor='#335'))
                ax.text(j + 0.5, n_r - 0.5 - i, str(mat[i, j]), ha='center', va='center', fontsize=13)
        ax.set_xlim(-0.1, n_c + 0.1)
        ax.set_ylim(-0.1, n_r + 0.1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------- 第 12 章


@figure
def ch12_positional_encoding() -> plt.Figure:
    seq_len, d_model = 50, 64
    pos = np.arange(seq_len)[:, None]
    i = np.arange(0, d_model, 2)[None, :]
    angle = pos / 10000 ** (i / d_model)
    pe = np.zeros((seq_len, d_model))
    pe[:, 0::2] = np.sin(angle)
    pe[:, 1::2] = np.cos(angle)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    im = ax.imshow(pe, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
    fig.colorbar(im, ax=ax)
    ax.set_xlabel('埋め込みベクトルの次元')
    ax.set_ylabel('位置 (トークンの番号)')
    ax.grid(False)
    return fig


@figure
def ch12_causal_mask() -> plt.Figure:
    rng = np.random.default_rng(3)
    n = 6
    scores = rng.normal(0, 1, (n, n))
    full = np.exp(scores) / np.exp(scores).sum(1, keepdims=True)
    masked_scores = np.where(np.triu(np.ones((n, n), bool), 1), -np.inf, scores)
    causal = np.exp(masked_scores) / np.exp(masked_scores).sum(1, keepdims=True)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, w, title in [(axes[0], full, 'マスクなし (エンコーダ)'), (axes[1], causal, '因果マスクあり (デコーダ)')]:
        ax.imshow(w, cmap='Blues', vmin=0, vmax=1)
        for r in range(n):
            for c in range(n):
                ax.text(c, r, f'{w[r, c]:.2f}', ha='center', va='center', fontsize=8,
                        color='w' if w[r, c] > 0.6 else 'k')
        ax.set_xlabel('参照されるトークン (キー)')
        ax.set_ylabel('注目するトークン (クエリ)')
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_title(title)
        ax.grid(False)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------- 生成処理


def generate_all(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    for func in FIGURES:
        fig = func()
        fig.savefig(outdir / f'{func.__name__}.png')
        plt.close(fig)


if __name__ == '__main__':
    generate_all(Path(__file__).resolve().parent.parent / '_generated')
