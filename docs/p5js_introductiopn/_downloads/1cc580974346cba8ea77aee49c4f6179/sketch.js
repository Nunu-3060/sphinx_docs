// インスタンスモードで書いたスケッチ
// p5.js の関数や変数は、すべて引数 p を通して使う

const sketch = (p) => {
  let x = 0;  // このスケッチ専用の変数（グローバル変数にならない）

  p.setup = () => {
    p.createCanvas(400, 400);
  };

  p.draw = () => {
    p.background(240);
    p.noStroke();
    p.fill(50, 150, 250);
    p.circle(x, p.height / 2, 40);
    x = (x + 2) % p.width;
  };
};

// スケッチを表す関数を渡して、p5 のインスタンスを作る
new p5(sketch);
