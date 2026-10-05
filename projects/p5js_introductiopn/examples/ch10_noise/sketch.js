// random() と noise() の違いを比べるスケッチ
// クリックするたびに種を変えて描き直す

let seed = 1;

function setup() {
  createCanvas(400, 400);
  noLoop();  // クリックされたときだけ描き直す
}

function draw() {
  // 種を固定すると、毎回同じ乱数列とノイズが得られる
  randomSeed(seed);
  noiseSeed(seed);

  background(255);
  noFill();
  strokeWeight(2);

  // 上段：random() の値をつないだ折れ線（隣り合う値に関係がない）
  stroke(220, 0, 0);
  beginShape();
  for (let x = 0; x <= width; x += 4) {
    vertex(x, random(40, 170));
  }
  endShape();

  // 下段：noise() の値をつないだ折れ線（隣り合う値が滑らかにつながる）
  stroke(0, 0, 220);
  beginShape();
  for (let x = 0; x <= width; x += 4) {
    const n = noise(x * 0.01);  // 0〜1 の値が返る
    vertex(x, map(n, 0, 1, 230, 390));
  }
  endShape();

  noStroke();
  fill(0);
  textSize(14);
  text(`random()  seed = ${seed}`, 10, 20);
  text('noise()', 10, 215);
}

function mousePressed() {
  seed += 1;
  redraw();  // noLoop() の状態で draw() を 1 回だけ実行する
}
