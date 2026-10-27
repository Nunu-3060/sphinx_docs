// 画像と JSON を読み込んで表示するスケッチ
// 外部ファイルを読み込むため、ローカルサーバー経由で開くこと

let img;
let data;

// setup() を async 関数にすると、中で await が使える
async function setup() {
  createCanvas(400, 400);
  // await を付けると、読み込みが終わるまで次の行に進まない
  img = await loadImage('image.png');
  data = await loadJSON('data.json');
}

function draw() {
  background(255);

  // 画像を表示する（左上の座標、幅、高さ）
  image(img, 20, 20, 120, 120);

  // tint() で色をかけて、もう 1 枚表示する
  tint(255, 120, 120);
  image(img, 160, 20, 120, 120);
  noTint();

  // JSON のデータから横棒グラフを描く
  noStroke();
  fill(0);
  textSize(16);
  textAlign(LEFT, BASELINE);
  text(data.title, 20, 180);

  textSize(14);
  textAlign(LEFT, CENTER);
  data.items.forEach((item, i) => {
    const y = 200 + i * 45;
    const barWidth = item.value * 5;
    fill(0);
    text(item.name, 20, y + 15);
    fill(80, 160, 240);
    rect(90, y, barWidth, 30);
    fill(0);
    text(item.value, 100 + barWidth, y + 15);
  });
}
