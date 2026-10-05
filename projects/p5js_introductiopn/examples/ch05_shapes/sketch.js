// 基本的な図形を並べて描くスケッチ

function setup() {
  createCanvas(400, 400);
  noLoop();  // 静止画なので draw() は 1 回だけ実行する
}

function draw() {
  background(255);

  // 点（線の太さを大きくしないと見えにくい）
  strokeWeight(8);
  point(50, 50);

  // 線（始点の座標、終点の座標）
  strokeWeight(2);
  line(80, 30, 160, 70);

  // 長方形（左上の座標、幅、高さ）
  rect(200, 30, 80, 50);
  // 5 番目の引数で角を丸める
  rect(300, 30, 80, 50, 10);

  // 円（中心の座標、直径）と楕円（中心の座標、幅、高さ）
  circle(60, 160, 60);
  ellipse(170, 160, 100, 50);

  // 円弧（中心の座標、幅、高さ、開始角、終了角、描き方）
  arc(300, 160, 80, 80, 0, PI + HALF_PI, PIE);

  // 三角形と四角形（頂点の座標を順に指定する）
  triangle(30, 280, 90, 220, 110, 290);
  quad(150, 230, 230, 220, 250, 290, 140, 280);

  // rectMode(CENTER) にすると、長方形を中心の座標で指定できる
  rectMode(CENTER);
  rect(330, 255, 60, 60);
  rectMode(CORNER);  // 既定値に戻す

  // 頂点を自由に並べた図形（星形）
  beginShape();
  for (let i = 0; i < 10; i++) {
    const angle = -HALF_PI + (i * TWO_PI) / 10;
    const r = i % 2 === 0 ? 40 : 18;  // 外側と内側の頂点を交互に置く
    vertex(200 + r * cos(angle), 350 + r * sin(angle));
  }
  endShape(CLOSE);  // CLOSE で最後の頂点と最初の頂点をつなぐ
}
