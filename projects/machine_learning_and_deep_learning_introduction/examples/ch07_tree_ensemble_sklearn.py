"""第 7 章: 決定木、ランダムフォレスト、勾配ブースティングを比較する。

scikit-learn 付属の乳がん診断データセット (ダウンロード不要) を使い、5 分割交差検証で正解率を比べる。

実行方法:
    python ch07_tree_ensemble_sklearn.py
"""
from typing import Any

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier, export_text


def main() -> None:
    data = load_breast_cancer()
    x, y = data.data, data.target

    models: dict[str, Any] = {
        "決定木 (深さ制限なし)": DecisionTreeClassifier(random_state=0),
        "決定木 (深さ 3)": DecisionTreeClassifier(max_depth=3, random_state=0),
        "ランダムフォレスト": RandomForestClassifier(n_estimators=300, random_state=0),
        "勾配ブースティング": HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=0),
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    for name, model in models.items():
        scores = cross_val_score(model, x, y, cv=cv)
        print(f"{name}: 正解率 = {scores.mean():.3f} (標準偏差 {scores.std():.3f})")

    # 浅い決定木は学習結果を if-then ルールとして読める
    shallow = DecisionTreeClassifier(max_depth=2, random_state=0).fit(x, y)
    print(export_text(shallow, feature_names=list(data.feature_names)))

    # ランダムフォレストの特徴量重要度 (不純度の減少量にもとづく) の上位 5 件
    forest = RandomForestClassifier(n_estimators=300, random_state=0).fit(x, y)
    order = np.argsort(forest.feature_importances_)[::-1][:5]
    for i in order:
        print(f"{data.feature_names[i]}: {forest.feature_importances_[i]:.3f}")


if __name__ == "__main__":
    main()
