// setup() と draw() の呼ばれ方と、座標系を確かめるスケッチ

function setup() {
  createCanvas(400, 400);
  frameRate(30);  // 1 秒あたり 30 回 draw() を呼ぶ
  console.log('setup() は最初に 1 回だけ呼ばれます');
}

function draw() {
  background(240);

  // 原点（左上）から x 軸と y 軸の向きを描く
  strokeWeight(4);
  stroke(200, 0, 0);
  line(0, 0, 100, 0);  // x 軸：右向きが正
  stroke(0, 0, 200);
  line(0, 0, 0, 100);  // y 軸：下向きが正

  noStroke();
  fill(0);
  textSize(16);
  text('x →', 105, 20);
  text('y ↓', 10, 125);

  // システム変数の値を表示する
  text(`frameCount: ${frameCount}`, 20, 180);
  text(`mouseX: ${round(mouseX)}, mouseY: ${round(mouseY)}`, 20, 210);
  text(`width: ${width}, height: ${height}`, 20, 240);

  // frameCount を使って円を右へ動かす（右端まで来たら左端に戻る）
  fill(50, 150, 250);
  circle(frameCount % width, 320, 40);
}
