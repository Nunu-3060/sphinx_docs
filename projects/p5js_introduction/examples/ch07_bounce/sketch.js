// 壁で跳ね返るボール

const DIAMETER = 40;  // ボールの直径
let x = 200;          // ボールの位置
let y = 100;
let vx = 3;           // ボールの速度（1 フレームあたりの移動量）
let vy = 2;

function setup() {
  createCanvas(400, 400);
}

function draw() {
  background(30);

  // 位置に速度を加えて動かす
  x += vx;
  y += vy;

  const r = DIAMETER / 2;
  // 左右の壁に当たったら、x 方向の速度の符号を反転する
  if (x < r || x > width - r) {
    vx = -vx;
  }
  // 上下の壁に当たったら、y 方向の速度の符号を反転する
  if (y < r || y > height - r) {
    vy = -vy;
  }

  noStroke();
  fill(255, 200, 0);
  circle(x, y, DIAMETER);
}
