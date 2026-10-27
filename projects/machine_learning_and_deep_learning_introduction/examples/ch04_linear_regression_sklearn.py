"""第 4 章: scikit-learn による線形回帰と多項式回帰。

実行方法:
    python ch04_linear_regression_sklearn.py
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def main() -> None:
    rng = np.random.default_rng(0)

    # 直線的な関係のデータ
    x = rng.uniform(0.0, 2.0, size=(100, 1))
    y = 3.0 * x[:, 0] + 2.0 + rng.normal(0.0, 0.3, size=100)

    model = LinearRegression()
    model.fit(x, y)
    print(f"切片 = {model.intercept_:.3f}, 傾き = {model.coef_[0]:.3f}")
    print("x = 1.5 での予測値:", model.predict(np.array([[1.5]])))

    # 曲線的な関係のデータには、特徴量を多項式に拡張してから線形回帰を適用する
    x2 = rng.uniform(-3.0, 3.0, size=(100, 1))
    y2 = 0.5 * x2[:, 0] ** 2 - x2[:, 0] + 1.0 + rng.normal(0.0, 0.5, size=100)

    linear = LinearRegression().fit(x2, y2)
    poly = make_pipeline(PolynomialFeatures(degree=2), LinearRegression()).fit(x2, y2)

    print(f"直線での MSE = {mean_squared_error(y2, linear.predict(x2)):.3f}")
    print(f"2 次多項式での MSE = {mean_squared_error(y2, poly.predict(x2)):.3f}")


if __name__ == "__main__":
    main()
