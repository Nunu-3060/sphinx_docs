// 名前付きエクスポート: 複数の値を公開できる
export const TAX_RATE = 0.1;

export function withTax(price) {
  return Math.round(price * (1 + TAX_RATE));
}

// デフォルトエクスポート: モジュールごとに 1 つだけ
export default function formatYen(value) {
  return `${value.toLocaleString("ja-JP")} 円`;
}
