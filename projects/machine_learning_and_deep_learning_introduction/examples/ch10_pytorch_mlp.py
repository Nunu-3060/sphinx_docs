"""第 10 章: PyTorch による多層パーセプトロンの学習。

scikit-learn 付属の手書き数字データセット (8x8 画素、10 クラス、ダウンロード不要) を使い、
ミニバッチ学習、AdamW、バッチ正規化、ドロップアウト、学習率スケジューリング、早期終了を組み合わせる。

実行方法:
    python ch10_pytorch_mlp.py
"""
import copy

import numpy as np
import torch
from numpy.typing import NDArray
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def make_loaders(batch_size: int = 64) -> tuple[DataLoader[tuple[torch.Tensor, ...]], ...]:
    """訓練・検証・テスト用の DataLoader を作る。"""
    digits = load_digits()
    x = (digits.data / 16.0).astype(np.float32)  # 画素値 0〜16 を 0〜1 に収める
    y = digits.target.astype(np.int64)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=0)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, stratify=y_train,
                                                      random_state=0)

    def to_dataset(a: NDArray[np.float32], b: NDArray[np.int64]) -> TensorDataset:
        return TensorDataset(torch.from_numpy(a), torch.from_numpy(b))

    return (
        DataLoader(to_dataset(x_train, y_train), batch_size=batch_size, shuffle=True),
        DataLoader(to_dataset(x_val, y_val), batch_size=256),
        DataLoader(to_dataset(x_test, y_test), batch_size=256),
    )


def build_model() -> nn.Module:
    return nn.Sequential(
        nn.Linear(64, 128),
        nn.BatchNorm1d(128),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(128, 64),
        nn.BatchNorm1d(64),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(64, 10),  # 出力はソフトマックス前の値 (ロジット)
    )


def evaluate(model: nn.Module, loader: DataLoader[tuple[torch.Tensor, ...]], device: torch.device) -> float:
    """正解率を求める。"""
    model.eval()  # ドロップアウトを無効にし、バッチ正規化は学習済みの統計量を使う
    correct = 0
    total = 0
    with torch.no_grad():
        for x, y in loader:
            pred = model(x.to(device)).argmax(dim=1)
            correct += int((pred == y.to(device)).sum().item())
            total += len(y)
    return correct / total


def main() -> None:
    torch.manual_seed(0)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader, val_loader, test_loader = make_loaders()

    model = build_model().to(device)
    loss_fn = nn.CrossEntropyLoss()  # ソフトマックスと交差エントロピーをまとめて計算する
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

    best_acc, best_state, patience, wait = 0.0, copy.deepcopy(model.state_dict()), 10, 0
    for epoch in range(1, 101):
        model.train()
        total_loss = 0.0
        n_samples = 0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()        # 1. 前回の勾配を消す
            loss = loss_fn(model(x), y)  # 2. 順伝播して損失を求める
            loss.backward()              # 3. 誤差逆伝播法で勾配を求める
            optimizer.step()             # 4. パラメータを更新する
            total_loss += loss.item() * len(y)
            n_samples += len(y)
        scheduler.step()

        val_acc = evaluate(model, val_loader, device)
        if epoch == 1 or epoch % 10 == 0:
            print(f"epoch {epoch:3d}: 訓練損失 = {total_loss / n_samples:.4f}, 検証正解率 = {val_acc:.3f}")

        # 早期終了: 検証正解率が patience エポック改善しなければ打ち切る
        if val_acc > best_acc:
            best_acc, best_state, wait = val_acc, copy.deepcopy(model.state_dict()), 0
        else:
            wait += 1
            if wait >= patience:
                print(f"{epoch} エポック目で早期終了")
                break

    model.load_state_dict(best_state)
    print(f"最良の検証正解率 = {best_acc:.3f}")
    print(f"テストデータでの正解率 = {evaluate(model, test_loader, device):.3f}")


if __name__ == "__main__":
    main()
