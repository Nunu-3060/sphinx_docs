"""第 6 章: 分類の評価指標 (混同行列、適合率、再現率、F1 値、ROC AUC) の例。

scikit-learn 付属の乳がん診断データセット (ダウンロード不要) を使う。

実行方法:
    python ch06_metrics.py
"""
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score, precision_score, recall_score,
                             roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def main() -> None:
    data = load_breast_cancer()
    # このデータセットでは 0 が悪性、1 が良性である。悪性を「陽性」として扱うためにラベルを反転する
    x = data.data
    y = 1 - data.target
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y, random_state=0)

    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    model.fit(x_train, y_train)
    proba = model.predict_proba(x_test)[:, 1]

    for threshold in [0.5, 0.2]:
        y_pred = (proba >= threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        print(f"--- しきい値 {threshold} ---")
        print(f"TP = {tp}, FP = {fp}, FN = {fn}, TN = {tn}")
        print(f"正解率 = {accuracy_score(y_test, y_pred):.3f}")
        print(f"適合率 = {precision_score(y_test, y_pred):.3f}")
        print(f"再現率 = {recall_score(y_test, y_pred):.3f}")
        print(f"F1 値 = {f1_score(y_test, y_pred):.3f}")

    print(f"ROC AUC = {roc_auc_score(y_test, proba):.4f}")

    # 陽性の割合が極端に少ないと、すべて陰性と答えるだけで正解率が高くなる
    y_rare = np.zeros(1000, dtype=int)
    y_rare[:10] = 1
    print(f"陽性 1 % のデータを常に陰性と予測した場合の正解率 = {accuracy_score(y_rare, np.zeros(1000, dtype=int)):.3f}")


if __name__ == "__main__":
    main()
