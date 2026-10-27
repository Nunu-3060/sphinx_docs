"""第 13 章: 実務を意識した学習パイプラインの例。

* 乱数シードを固定して再現性を確保する
* 前処理とモデルを Pipeline にまとめ、交差検証の中で前処理を学習させる (データリークの防止)
* 学習済みパイプラインをファイルに保存し、読み込んで予測する
* 順列重要度 (permutation importance) で、どの特徴量が予測に効いているかを確認する

実行方法:
    python ch13_pipeline.py
"""
import tempfile
from pathlib import Path

import joblib
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SEED = 0


def main() -> None:
    data = load_diabetes()
    x_train, x_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2,
                                                        random_state=SEED)

    # ベースライン: 訓練データの平均値を常に答える
    baseline = mean_absolute_error(y_test, np.full_like(y_test, y_train.mean()))
    print(f"ベースライン (平均値) の MAE = {baseline:.1f}")

    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    candidates = {
        "Ridge": GridSearchCV(
            Pipeline([("scale", StandardScaler()), ("model", Ridge())]),
            {"model__alpha": [0.1, 1.0, 10.0]},
            cv=cv, scoring="neg_mean_absolute_error",
        ),
        "勾配ブースティング": GridSearchCV(
            HistGradientBoostingRegressor(random_state=SEED),
            {"max_depth": [2, 3], "learning_rate": [0.03, 0.1]},
            cv=cv, scoring="neg_mean_absolute_error",
        ),
    }
    for name, search in candidates.items():
        search.fit(x_train, y_train)
        print(f"{name}: 交差検証 MAE = {-search.best_score_:.1f}, 最良の設定 = {search.best_params_}")

    # 交差検証の結果が最も良かったモデルを選び、最後に一度だけテストデータで評価する
    best_name = max(candidates, key=lambda name: candidates[name].best_score_)
    best = candidates[best_name].best_estimator_
    print(f"{best_name} のテストデータでの MAE = {mean_absolute_error(y_test, best.predict(x_test)):.1f}")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "model.joblib"
        joblib.dump(best, path)
        loaded = joblib.load(path)
        same = np.allclose(loaded.predict(x_test), best.predict(x_test))
        print("保存・読み込み後も同じ予測になるか:", same)

    result = permutation_importance(best, x_test, y_test, n_repeats=20, random_state=SEED,
                                    scoring="neg_mean_absolute_error")
    order = np.argsort(result.importances_mean)[::-1][:3]
    for i in order:
        print(f"特徴量 {data.feature_names[i]}: 重要度 = {result.importances_mean[i]:.2f}")


if __name__ == "__main__":
    main()
