"""第 6 章: 過学習・正則化・交差検証・ハイパーパラメータ探索の例。

sin 関数にノイズを加えたデータに多項式回帰を当てはめ、次数と正則化の強さが
訓練誤差と検証誤差にどう影響するかを確認する。

実行方法:
    python ch06_overfitting.py
"""
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


def main() -> None:
    rng = np.random.default_rng(1)
    x = rng.uniform(0.0, 1.0, size=(40, 1))
    y = np.sin(2.0 * np.pi * x[:, 0]) + rng.normal(0.0, 0.2, size=40)
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.5, random_state=0)

    print("--- 多項式の次数と誤差 (正則化なし) ---")
    for degree in [1, 3, 9, 15]:
        model = make_pipeline(PolynomialFeatures(degree), StandardScaler(), LinearRegression())
        model.fit(x_train, y_train)
        train_mse = mean_squared_error(y_train, model.predict(x_train))
        val_mse = mean_squared_error(y_val, model.predict(x_val))
        print(f"次数 {degree:2d}: 訓練 MSE = {train_mse:.4f}, 検証 MSE = {val_mse:.4f}")

    print("--- 次数 15 に L2 正則化 (Ridge) を加える ---")
    for alpha in [1e-6, 1e-3, 1e-1, 10.0]:
        model = make_pipeline(PolynomialFeatures(15), StandardScaler(), Ridge(alpha=alpha))
        model.fit(x_train, y_train)
        val_mse = mean_squared_error(y_val, model.predict(x_val))
        print(f"alpha = {alpha:g}: 検証 MSE = {val_mse:.4f}")

    print("--- 5 分割交差検証 ---")
    cv = KFold(n_splits=5, shuffle=True, random_state=0)
    model = make_pipeline(PolynomialFeatures(3), StandardScaler(), LinearRegression())
    scores = cross_val_score(model, x, y, cv=cv, scoring="neg_mean_squared_error")
    print("各分割の MSE:", np.round(-scores, 4), " 平均:", round(float(-scores.mean()), 4))

    print("--- グリッドサーチで次数と alpha を同時に選ぶ ---")
    pipe = make_pipeline(PolynomialFeatures(), StandardScaler(), Ridge())
    grid = {
        "polynomialfeatures__degree": [1, 3, 5, 9, 15],
        "ridge__alpha": [1e-4, 1e-2, 1.0],
    }
    search = GridSearchCV(pipe, grid, cv=cv, scoring="neg_mean_squared_error")
    search.fit(x, y)
    print("最良のハイパーパラメータ:", search.best_params_)
    print(f"そのときの交差検証 MSE = {-search.best_score_:.4f}")


if __name__ == "__main__":
    main()
