"""第 12 章: PyTorch の Transformer エンコーダで系列を分類する。

課題: 長さ 8 のトークン列 (0〜9 の整数) について、先頭のトークンが 2 番目以降にもう一度
現れるかどうかを判定する。答えるには離れた位置どうしを比較する必要があり、Attention が役に立つ。

実行方法:
    python ch12_transformer_pytorch.py
"""
import torch
from torch import nn

SEQ_LEN = 8
VOCAB = 10


def make_batch(n: int, generator: torch.Generator) -> tuple[torch.Tensor, torch.Tensor]:
    """ランダムなトークン列とラベル (先頭のトークンが再出現すれば 1) を作る。"""
    x = torch.randint(0, VOCAB, (n, SEQ_LEN), generator=generator)
    y = (x[:, 1:] == x[:, :1]).any(dim=1).long()
    return x, y


class TinyTransformer(nn.Module):
    def __init__(self, d_model: int = 32, n_heads: int = 4, n_layers: int = 2) -> None:
        super().__init__()
        self.token_emb = nn.Embedding(VOCAB, d_model)
        # 位置ごとに学習可能なベクトルを足して、トークンの順序の情報を与える
        self.pos_emb = nn.Parameter(torch.zeros(1, SEQ_LEN, d_model))
        layer = nn.TransformerEncoderLayer(d_model, n_heads, dim_feedforward=64, dropout=0.0, batch_first=True)
        self.encoder = nn.TransformerEncoder(layer, n_layers)
        self.head = nn.Linear(d_model, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.token_emb(x) + self.pos_emb  # (バッチ, 系列長, d_model)
        h = self.encoder(h)
        out: torch.Tensor = self.head(h[:, 0])  # 先頭位置の出力ベクトルで分類する
        return out


def main() -> None:
    torch.manual_seed(0)
    gen = torch.Generator().manual_seed(0)
    x_val, y_val = make_batch(2000, gen)
    print(f"検証データで正例 (再出現する) の割合 = {y_val.float().mean().item():.3f}")

    model = TinyTransformer()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    for step in range(1, 2001):
        model.train()
        x, y = make_batch(128, gen)
        optimizer.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        optimizer.step()

        if step % 400 == 0:
            model.eval()
            with torch.no_grad():
                acc = (model(x_val).argmax(dim=1) == y_val).float().mean().item()
            print(f"step {step:4d}: loss = {loss.item():.4f}, 検証正解率 = {acc:.3f}")


if __name__ == "__main__":
    main()
