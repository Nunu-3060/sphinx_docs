"""第 3 章: 前処理 (欠損値の補完・標準化・one-hot 符号化・データ分割) の例。

scikit-learn の ColumnTransformer を使い、数値列とカテゴリ列に別々の前処理を適用する。
前処理の統計量 (平均・標準偏差など) は訓練データだけから求める点に注意する。

実行方法:
    python ch03_preprocessing.py
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def make_dataset(n: int, seed: int = 0) -> pd.DataFrame:
    """家賃を予測する架空の表形式データを作る。"""
    rng = np.random.default_rng(seed)
    area = rng.uniform(15.0, 80.0, n)
    age = rng.integers(0, 40, n).astype(float)
    station = rng.choice(["A駅", "B駅", "C駅"], n)
    rent = 2.0 + 0.12 * area - 0.05 * age + np.where(station == "A駅", 1.5, 0.0) + rng.normal(0.0, 0.5, n)

    df = pd.DataFrame({"area": area, "age": age, "station": station, "rent": rent})
    # 一部の築年数を欠損させる
    df.loc[rng.random(n) < 0.1, "age"] = np.nan
    return df


def main() -> None:
    df = make_dataset(200)
    print(df.head())
    print("欠損値の数:\n", df.isna().sum())

    x = df[["area", "age", "station"]]
    y = df["rent"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    numeric = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    preprocess = ColumnTransformer([
        ("num", numeric, ["area", "age"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["station"]),
    ])

    # fit は訓練データだけで行い、テストデータには transform のみを適用する
    z_train = preprocess.fit_transform(x_train)
    z_test = preprocess.transform(x_test)

    print("前処理後の列名:", list(preprocess.get_feature_names_out()))
    print("訓練データの形状:", z_train.shape, " テストデータの形状:", z_test.shape)
    print("標準化後の訓練データの平均 (ほぼ 0):", np.round(z_train[:, :2].mean(axis=0), 3))
    print("標準化後の訓練データの標準偏差 (ほぼ 1):", np.round(z_train[:, :2].std(axis=0), 3))
    print("y_train の件数:", len(y_train), " y_test の件数:", len(y_test))


if __name__ == "__main__":
    main()
