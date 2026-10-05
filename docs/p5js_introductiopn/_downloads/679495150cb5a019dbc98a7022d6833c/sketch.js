// translate()、rotate()、push()、pop() で描くアナログ時計

function setup() {
  createCanvas(400, 400);
  angleMode(DEGREES);  // 角度を度数法で指定する
}

function draw() {
  background(255);
  translate(width / 2, height / 2);  // 原点をキャンバスの中心に移す

  // 文字盤の外周
  noFill();
  stroke(0);
  strokeWeight(4);
  circle(0, 0, 360);

  // 目盛り：30 度ずつ回転しながら 12 本描く
  for (let i = 0; i < 12; i++) {
    push();
    rotate(i * 30);
    strokeWeight(i % 3 === 0 ? 6 : 2);  // 3 時間ごとの目盛りは太くする
    line(0, -170, 0, -150);
    pop();
  }

  // 現在時刻から各針の角度を求める（真上が 0 度、時計回りが正）
  const s = second();
  const m = minute() + s / 60;
  const h = (hour() % 12) + m / 60;

  stroke(0);
  drawHand(h * 30, 90, 8);  // 時針：1 時間で 30 度進む
  drawHand(m * 6, 130, 4);  // 分針：1 分で 6 度進む
  stroke(220, 0, 0);
  drawHand(s * 6, 150, 2);  // 秒針：1 秒で 6 度進む
}

// 指定した角度・長さ・太さで針を 1 本描く
function drawHand(angle, length, weight) {
  push();  // 現在の座標系とスタイルを保存する
  rotate(angle);
  strokeWeight(weight);
  line(0, 0, 0, -length);
  pop();  // 保存した状態に戻す
}
