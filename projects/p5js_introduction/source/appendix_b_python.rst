付録 B Python（py5）との対応表
==============================

Processing の考え方を Python で使えるライブラリとして、`py5 <https://py5coding.org/>`__ があります。py5 は Processing（Java 版）を Python から呼び出すライブラリで、p5.js とほぼ同じ考え方でスケッチを書けます。

py5 では、関数名や変数名が Python の命名規則に合わせてスネークケース（``mouse_x`` など）になっています。p5.js と py5 の主な対応を次の表に示します。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - p5.js
     - py5
   * - ``function setup() { }``
     - ``def setup():``
   * - ``function draw() { }``
     - ``def draw():``
   * - ``createCanvas(400, 400)``
     - ``py5.size(400, 400)``
   * - ``background(220)``
     - ``py5.background(220)``
   * - ``fill(255, 0, 0)``
     - ``py5.fill(255, 0, 0)``
   * - ``circle(x, y, d)``
     - ``py5.circle(x, y, d)``
   * - ``mouseX``、``mouseY``
     - ``py5.mouse_x``、``py5.mouse_y``
   * - ``mouseIsPressed``
     - ``py5.is_mouse_pressed``
   * - ``frameCount``
     - ``py5.frame_count``
   * - ``width``、``height``
     - ``py5.width``、``py5.height``
   * - ``function mousePressed() { }``
     - ``def mouse_pressed():``
   * - ``function keyPressed() { }``
     - ``def key_pressed():``
   * - ``push()``、``pop()``
     - ``py5.push()``、``py5.pop()``
   * - ``random(10)``
     - ``py5.random(10)``
   * - ``createVector(x, y)``
     - ``py5.Py5Vector(x, y)``
   * - スケッチは自動的に開始される。
     - 最後に ``py5.run_sketch()`` を呼んで開始する。

:doc:`02_setup` の最初のスケッチを py5 で書くと、次のようになります。

.. code-block:: python
   :linenos:

   import py5


   def setup() -> None:
       py5.size(400, 400)


   def draw() -> None:
       py5.background(220)
       py5.circle(py5.mouse_x, py5.mouse_y, 50)


   py5.run_sketch()

py5 は Java の実行環境を必要とし、作品はデスクトップのウィンドウに表示されます。一方、p5.js の作品はブラウザーで動くため、URL を共有するだけで誰でも見られます。Web で作品を公開したい場合は p5.js、Python のライブラリ（NumPy など）と組み合わせたい場合は py5 が向いています。
