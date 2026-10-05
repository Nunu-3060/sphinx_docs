// RGB、HSB、透明度を試すスケッチ

function setup() {
  createCanvas(400, 400);
  noLoop();
}

function draw() {
  background(255);
  noStroke();

  // RGB：赤・緑・青の強さを 0〜255 で指定する
  fill(255, 0, 0);
  rect(20, 20, 100, 60);
  fill(0, 255, 0);
  rect(150, 20, 100, 60);
  fill(0, 0, 255);
  rect(280, 20, 100, 60);

  // HSB：色相を 0〜360、彩度と明度を 0〜100 で指定する
  colorMode(HSB, 360, 100, 100);
  for (let h = 0; h < 360; h += 10) {
    fill(h, 80, 100);  // 彩度と明度は固定し、色相だけを変える
    rect(20 + h, 110, 10, 60);
  }
  colorMode(RGB, 255);  // RGB に戻す

  // 4 番目の引数は透明度（アルファ値）。重なった部分の色が混ざる
  fill(255, 0, 0, 120);
  circle(160, 270, 120);
  fill(0, 0, 255, 120);
  circle(240, 270, 120);

  // 線の色と太さ
  noFill();
  stroke(0);
  strokeWeight(6);
  rect(20, 350, 360, 30);
}
