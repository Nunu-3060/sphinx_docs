// JavaScript の基本文法を試すスケッチ
// 結果はキャンバスと開発者ツールのコンソールの両方に表示する

// const は再代入できない定数、let は再代入できる変数
const TITLE = 'JavaScript の基本';
const lines = [];

// 関数宣言（Python の def に相当）
// 名前を square にすると p5.js の square() と衝突してエラーになるため注意
function squared(x) {
  return x * x;
}

// アロー関数（Python の lambda に近いが、複数行の処理も書ける）
const cubed = (x) => x * x * x;

// クラス（Python の class に相当）
class Counter {
  // コンストラクター（Python の __init__ に相当）
  constructor(start) {
    this.count = start;  // Python の self は JavaScript では this
  }

  increment() {
    this.count += 1;
  }
}

function setup() {
  createCanvas(400, 400);
  noLoop();  // 静止画なので draw() は 1 回だけ実行する

  // 配列（Python のリストに相当）
  const numbers = [1, 2, 3];
  numbers.push(4);  // Python の append に相当

  // for...of で要素を順に取り出す（Python の for n in numbers に相当）
  for (const n of numbers) {
    // テンプレートリテラル（Python の f 文字列に相当）
    lines.push(`${n} の 2 乗は ${squared(n)}、3 乗は ${cubed(n)}`);
  }

  // オブジェクト（Python の辞書に相当）
  const point = { x: 10, y: 20 };
  lines.push(`point.x = ${point.x}, point['y'] = ${point['y']}`);

  // === は型も含めて比較し、== は型を変換してから比較する
  lines.push(`1 === '1' の結果: ${1 === '1'}`);
  lines.push(`1 == '1' の結果: ${1 == '1'}`);

  // new でインスタンスを作る
  const counter = new Counter(0);
  counter.increment();
  counter.increment();
  lines.push(`counter.count = ${counter.count}`);

  // 開発者ツールのコンソールに出力する（Python の print に相当）
  for (const line of lines) {
    console.log(line);
  }
}

function draw() {
  background(255);
  fill(0);
  textSize(18);
  text(TITLE, 20, 35);

  textSize(14);
  // 要素と番号を同時に取り出す（Python の enumerate に相当）
  lines.forEach((line, i) => {
    text(line, 20, 75 + i * 26);
  });
}
