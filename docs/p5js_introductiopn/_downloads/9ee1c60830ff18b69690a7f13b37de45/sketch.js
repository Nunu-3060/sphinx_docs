// マウスで線を描くお絵かきツール
//   ドラッグ      ：線を描く
//   上部のボタン  ：色を切り替える
//   ↑ / ↓ キー   ：線の太さを変える
//   c キー        ：消去する
//   s キー        ：PNG 画像として保存する

const COLORS = ['black', 'red', 'blue', 'green'];
const BUTTON_SIZE = 30;
const PALETTE_HEIGHT = 50;  // ボタンを置く上部の領域の高さ
let currentColor = 'black';
let weight = 4;

function setup() {
  createCanvas(400, 400);
  background(255);
}

function draw() {
  drawPalette();

  // マウスボタンが押されている間、前のフレームの位置から現在の位置まで線を引く
  if (mouseIsPressed && mouseY > PALETTE_HEIGHT && pmouseY > PALETTE_HEIGHT) {
    stroke(currentColor);
    strokeWeight(weight);
    line(pmouseX, pmouseY, mouseX, mouseY);
  }
}

// 画面上部に色のボタンと線の太さを描く
function drawPalette() {
  // 上部の領域だけを毎フレーム描き直す
  noStroke();
  fill(230);
  rect(0, 0, width, PALETTE_HEIGHT);

  for (let i = 0; i < COLORS.length; i++) {
    // 選択中の色のボタンは太い枠で囲む
    stroke(120);
    strokeWeight(COLORS[i] === currentColor ? 4 : 1);
    fill(COLORS[i]);
    rect(buttonX(i), 10, BUTTON_SIZE, BUTTON_SIZE);
  }

  noStroke();
  fill(0);
  textSize(14);
  text(`太さ: ${weight}`, 200, 30);
}

// i 番目のボタンの左端の x 座標を返す
function buttonX(i) {
  return 10 + i * (BUTTON_SIZE + 10);
}

// マウスボタンを押した瞬間に 1 回だけ呼ばれる
function mousePressed() {
  for (let i = 0; i < COLORS.length; i++) {
    const x = buttonX(i);
    // マウスの位置がボタンの範囲内にあるかを判定する
    const insideX = mouseX >= x && mouseX <= x + BUTTON_SIZE;
    const insideY = mouseY >= 10 && mouseY <= 10 + BUTTON_SIZE;
    if (insideX && insideY) {
      currentColor = COLORS[i];
    }
  }
}

// キーを押した瞬間に 1 回だけ呼ばれる
function keyPressed() {
  if (key === 'c') {
    background(255);
  } else if (key === 's') {
    saveCanvas('drawing', 'png');
  } else if (key === 'ArrowUp') {
    weight = min(weight + 1, 20);
  } else if (key === 'ArrowDown') {
    weight = max(weight - 1, 1);
  }
}
