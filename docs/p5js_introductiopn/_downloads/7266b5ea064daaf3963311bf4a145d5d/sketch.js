// はじめてのスケッチ：マウスに付いてくる円を描く

function setup() {
  // 幅 400 ピクセル、高さ 400 ピクセルのキャンバスを作る
  createCanvas(400, 400);
}

function draw() {
  // 毎フレーム、背景を明るい灰色で塗りつぶす
  background(220);
  // マウスの位置に直径 50 ピクセルの円を描く
  circle(mouseX, mouseY, 50);
}
