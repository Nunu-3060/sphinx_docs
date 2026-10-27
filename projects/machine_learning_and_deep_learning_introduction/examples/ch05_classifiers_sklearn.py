"""第 5 章: scikit-learn で複数の分類器を比較する。

三日月形の 2 クラスデータ (make_moons) に対して、ロジスティック回帰、k 近傍法、
サポートベクターマシン (RBF カーネル) を学習し、テストデータでの正解率を比べる。

実行方法:
    python ch05_classifiers_sklearn.py
"""
from typing import Any

from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def main() -> None:
    x, y = make_moons(n_samples=400, noise=0.25, random_state=0)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

    # 距離や内積を使う手法は特徴量のスケールに敏感なので、標準化と組み合わせる
    models: dict[str, Any] = {
        "ロジスティック回帰": make_pipeline(StandardScaler(), LogisticRegression()),
        "k 近傍法 (k=15)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=15)),
        "SVM (RBF カーネル)": make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0, gamma="scale")),
    }

    for name, model in models.items():
        model.fit(x_train, y_train)
        print(f"{name}: テストデータでの正解率 = {model.score(x_test, y_test):.3f}")

    # predict_proba で各クラスの確率を得られる
    proba = models["ロジスティック回帰"].predict_proba(x_test[:3])
    print("ロジスティック回帰による先頭 3 件のクラス確率:\n", proba.round(3))


if __name__ == "__main__":
    main()
