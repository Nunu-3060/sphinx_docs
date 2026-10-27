"""第 11 章: PyTorch による畳み込みニューラルネットワーク (CNN) の学習。

scikit-learn 付属の手書き数字データセット (8x8 画素、10 クラス、ダウンロード不要) を画像として扱い、
小さな CNN で分類する。訓練時には簡単なデータ拡張 (1 画素の平行移動) を行う。

実行方法:
    python ch11_cnn_pytorch.py
"""
import numpy as np
import torch
from numpy.typing import NDArray
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class SmallCNN(nn.Module):
    def __init__(self, n_classes: int = 10) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),   # (1, 8, 8) -> (16, 8, 8)
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),  # (16, 8, 8) -> (32, 8, 8)
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),                              # (32, 8, 8) -> (32, 4, 4)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),                                 # (32, 4, 4) -> (512,)
            nn.Dropout(0.3),
            nn.Linear(32 * 4 * 4, n_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out: torch.Tensor = self.classifier(self.features(x))
        return out


def random_shift(x: torch.Tensor) -> torch.Tensor:
    """データ拡張: ミニバッチ全体を上下左右に最大 1 画素ずらす。"""
    dy, dx = torch.randint(-1, 2, (2,)).tolist()
    return torch.roll(x, shifts=(dy, dx), dims=(2, 3))


def accuracy(model: nn.Module, x: NDArray[np.float32], y: NDArray[np.int64], device: torch.device) -> float:
    """正解率を求める。"""
    model.eval()
    with torch.no_grad():
        pred = model(torch.from_numpy(x).to(device)).argmax(dim=1)
    return float((pred == torch.from_numpy(y).to(device)).float().mean().item())


def main() -> None:
    torch.manual_seed(0)
    # 小さなモデルなので CPU で十分に速い。GPU を使うと実行のたびに結果がわずかに変わることがある
    device = torch.device("cpu")

    digits = load_digits()
    # 形状 (サンプル数, チャネル数, 高さ, 幅) に変形する
    x = (digits.images / 16.0).astype(np.float32)[:, None, :, :]
    y = digits.target.astype(np.int64)
    # 第 10 章と同じ方法で訓練・検証・テストに分割する
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=0)
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, stratify=y_train,
                                                      random_state=0)

    train_loader = DataLoader(TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train)),
                              batch_size=64, shuffle=True)

    model = SmallCNN().to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"パラメータ数 = {n_params}")

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(30):
        model.train()
        for xb, yb in train_loader:
            xb, yb = random_shift(xb.to(device)), yb.to(device)
            optimizer.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            optimizer.step()

        if epoch % 5 == 4:
            print(f"epoch {epoch + 1:2d}: 検証正解率 = {accuracy(model, x_val, y_val, device):.3f}")

    # テストデータは、すべての調整が終わった最後に一度だけ使う
    print(f"テストデータでの正解率 = {accuracy(model, x_test, y_test, device):.3f}")


if __name__ == "__main__":
    main()
