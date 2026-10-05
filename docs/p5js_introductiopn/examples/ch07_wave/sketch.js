// 三角関数で周期的な動きを作るスケッチ

const AMPLITUDE = 100;  // 振幅（ピクセル）
const PERIOD = 2;       // 周期（秒）

function setup() {
  createCanvas(400, 400);
}

function draw() {
  background(255);
  const t = millis() / 1000;  // スケッチ開始からの経過時間（秒）
  const centerY = height / 2;

  // 中心線
  stroke(200);
  strokeWeight(1);
  line(0, centerY, width, centerY);

  // y = 中心 + 振幅 × sin(2π × t / 周期) で上下に振動する円
  const y = centerY + AMPLITUDE * sin((TWO_PI * t) / PERIOD);
  noStroke();
  fill(0, 120, 255);
  circle(100, y, 40);

  // 位置によって位相をずらしながら同じ式で点を並べると、波になる
  noFill();
  stroke(0, 120, 255);
  strokeWeight(2);
  beginShape();
  for (let px = 150; px <= width; px += 5) {
    const shift = (px - 150) / 100;  // 位相のずれ（周期の何倍か）
    vertex(px, centerY + AMPLITUDE * sin(TWO_PI * (t / PERIOD - shift)));
  }
  endShape();
}
