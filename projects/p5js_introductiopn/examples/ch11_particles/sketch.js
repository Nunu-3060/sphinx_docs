// p5.Vector とクラスを使ったパーティクル（粒子）の噴水
// マウスボタンを押している間は、マウスの位置から粒子が出る

const particles = [];
let gravity;  // 重力を表すベクトル（createVector() は setup() 以降で使う）

class Particle {
  constructor(x, y) {
    this.position = createVector(x, y);
    // 上向きを基本に、ランダムな向きと速さを与える
    this.velocity = createVector(random(-1, 1), random(-5, -3));
    this.life = 255;  // 残りの寿命（透明度としても使う）
  }

  // 速度に重力を加え、位置に速度を加える
  update() {
    this.velocity.add(gravity);
    this.position.add(this.velocity);
    this.life -= 3;
  }

  show() {
    noStroke();
    fill(255, 150, 0, this.life);
    circle(this.position.x, this.position.y, 10);
  }

  isDead() {
    return this.life <= 0;
  }
}

function setup() {
  createCanvas(400, 400);
  gravity = createVector(0, 0.1);
}

function draw() {
  background(20);

  // 粒子の発生位置（マウスボタンを押している間はマウスの位置）
  let originX = width / 2;
  let originY = height - 80;
  if (mouseIsPressed) {
    originX = mouseX;
    originY = mouseY;
  }

  // 毎フレーム、新しい粒子を 3 個追加する
  for (let i = 0; i < 3; i++) {
    particles.push(new Particle(originX, originY));
  }

  // 後ろから順に処理すると、途中で要素を削除しても添字がずれない
  for (let i = particles.length - 1; i >= 0; i--) {
    const particle = particles[i];
    particle.update();
    particle.show();
    if (particle.isDead()) {
      particles.splice(i, 1);  // 配列から i 番目の要素を削除する
    }
  }

  fill(255);
  textSize(14);
  text(`粒子の数: ${particles.length}`, 10, 20);
}
