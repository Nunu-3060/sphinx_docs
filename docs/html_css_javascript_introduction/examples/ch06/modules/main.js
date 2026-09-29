// Python の from math_utils import TAX_RATE, with_tax に相当する
// デフォルトエクスポートは任意の名前 (ここでは formatYen) で受け取る
import formatYen, { TAX_RATE, withTax } from "./math_utils.js";

const price = 1200;
const output = document.querySelector("#output");

output.textContent =
  `税率 ${TAX_RATE * 100}%: ${formatYen(price)} → ${formatYen(withTax(price))}`;
