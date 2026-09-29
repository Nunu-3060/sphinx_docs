CSS によるレイアウト
====================

display プロパティ
------------------

``display`` プロパティは、要素をどのように配置するかを指定する。第 2 章で説明したブロック要素とインライン要素の違いも、ブラウザが既定で指定している ``display`` プロパティの値によるものである。

.. list-table:: display プロパティの主な値
   :header-rows: 1
   :widths: 20 80

   * - 値
     - 配置のされ方
   * - ``block``
     - ブロック要素として配置する。新しい行から始まり、横幅いっぱいに広がる。``width`` や ``height`` を指定できる。
   * - ``inline``
     - インライン要素として配置する。文章の流れの中に並ぶ。``width`` や ``height`` を指定しても無視される。
   * - ``inline-block``
     - 文章の流れの中に並びつつ、``width`` や ``height`` を指定できる。
   * - ``none``
     - 表示しない。その要素が無いものとして配置される。
   * - ``flex``
     - 子要素を Flexbox で配置する（後述）。
   * - ``grid``
     - 子要素を Grid で配置する（後述）。

position プロパティ
-------------------

``position`` プロパティは、要素を通常の配置から移動させる方法を指定する。移動量は ``top``、``right``、``bottom``、``left`` プロパティで指定する。

.. list-table:: position プロパティの値
   :header-rows: 1
   :widths: 20 80

   * - 値
     - 配置のされ方
   * - ``static``
     - 通常の配置（既定値）。``top`` などは無視される。
   * - ``relative``
     - 通常の位置を基準に、指定した量だけずらす。元の位置の領域は確保されたままになる。
   * - ``absolute``
     - 通常の配置から外し、``static`` 以外の ``position`` を持つ最も近い祖先要素を基準に配置する。そのような祖先要素が無い場合は、ページの先頭を基準にする。
   * - ``fixed``
     - 通常の配置から外し、ブラウザの表示領域を基準に配置する。スクロールしても画面上の同じ位置に留まる。
   * - ``sticky``
     - 通常は ``static`` と同様に配置されるが、スクロールによって指定した位置に達すると、そこに貼り付いたように留まる。表の見出し行などに使う。

``absolute`` は、親要素に ``position: relative;`` を指定し、その親を基準に子要素を配置する組み合わせでよく使われる。

Flexbox
-------

Flexbox は、要素を 1 方向（横または縦）に並べるための仕組みである。親要素に ``display: flex;`` を指定すると、その直接の子要素が横一列に並ぶ。``display: flex;`` を指定した親要素をフレックスコンテナー、その子要素をフレックスアイテムと呼ぶ。

Flexbox では、並べる方向を主軸、それと直交する方向を交差軸と呼ぶ。既定では主軸が横方向、交差軸が縦方向である。

.. list-table:: フレックスコンテナーに指定する主なプロパティ
   :header-rows: 1
   :widths: 25 75

   * - プロパティ
     - 意味
   * - ``flex-direction``
     - 主軸の方向。``row`` （横、既定値）、``column`` （縦）などを指定する。
   * - ``justify-content``
     - 主軸方向の配置。``flex-start`` （先頭に寄せる、既定値）、``center`` （中央）、``space-between`` （両端に揃えて均等に配置）などを指定する。
   * - ``align-items``
     - 交差軸方向の配置。``stretch`` （いっぱいに伸ばす、既定値）、``center`` （中央）などを指定する。
   * - ``flex-wrap``
     - 幅が足りないときに折り返すかどうか。``nowrap`` （折り返さない、既定値）、``wrap`` （折り返す）を指定する。
   * - ``gap``
     - アイテムどうしの間隔。

.. list-table:: フレックスアイテムに指定する主なプロパティ
   :header-rows: 1
   :widths: 25 75

   * - プロパティ
     - 意味
   * - ``flex-grow``
     - コンテナーの幅に余りがあるとき、それを分け合う比率。既定値は 0（伸びない）である。
   * - ``flex-shrink``
     - コンテナーの幅が足りないとき、縮む比率。既定値は 1 である。
   * - ``flex-basis``
     - 伸び縮みする前の基準の大きさ。既定値は ``auto`` （内容や ``width`` に従う）である。

.. literalinclude:: ../examples/ch05/flexbox.html
   :language: html
   :caption: examples/ch05/flexbox.html

:download:`flexbox.html をダウンロード <../examples/ch05/flexbox.html>` ／ `ブラウザで表示 <examples/ch05/flexbox.html>`__

Grid
----

Grid は、要素を行と列の 2 方向で格子状に並べるための仕組みである。親要素に ``display: grid;`` を指定し、``grid-template-columns`` プロパティで列の幅を、``grid-template-rows`` プロパティで行の高さを指定する。

.. list-table:: Grid で使う主な値とプロパティ
   :header-rows: 1
   :widths: 35 65

   * - 記述
     - 意味
   * - ``fr``
     - 残りの領域を分ける比率を表す単位。``1fr 2fr`` と書くと、残りの幅を 1 : 2 に分ける。
   * - ``repeat(3, 1fr)``
     - ``1fr 1fr 1fr`` と同じ意味。同じ指定を繰り返す。
   * - ``gap``
     - 行と列の間隔。
   * - ``grid-template-areas``
     - 領域に名前を付けて、配置を図のように記述する。
   * - ``grid-area``
     - 子要素を、``grid-template-areas`` で名前を付けた領域に配置する。

子要素は、特に指定しなければ左上から順に 1 つずつセルに配置される。列の数を超えると次の行に折り返す。

.. literalinclude:: ../examples/ch05/grid.html
   :language: html
   :caption: examples/ch05/grid.html

:download:`grid.html をダウンロード <../examples/ch05/grid.html>` ／ `ブラウザで表示 <examples/ch05/grid.html>`__

Flexbox と Grid の使い分け
~~~~~~~~~~~~~~~~~~~~~~~~~~

Flexbox はメニューやボタンの並びなど、1 方向に並べる場合に向いている。Grid はカードの一覧やページ全体の骨組みなど、行と列の両方を揃えたい場合に向いている。両者は組み合わせて使える。たとえば、ページ全体を Grid で分割し、ヘッダーの中のメニューを Flexbox で並べる、といった使い方をする。

レスポンシブデザイン
--------------------

レスポンシブデザインとは、1 つの HTML で、PC からスマートフォンまで、さまざまな画面の幅に合わせて表示を切り替える手法である。次の 2 つを組み合わせて実現する。

* ``head`` 要素に ``<meta name="viewport" content="width=device-width, initial-scale=1">`` を書く（第 3 章を参照）。
* CSS のメディアクエリを使い、画面の幅に応じて異なるスタイルを適用する。

メディアクエリは ``@media`` で始まるブロックであり、条件を満たすときだけ中のルールが適用される。

.. code-block:: css

   /* 画面の幅が 600px 以上のときだけ適用される */
   @media (min-width: 600px) {
     .cards {
       grid-template-columns: repeat(2, 1fr);
     }
   }

まず狭い画面向けのスタイルを書き、``min-width`` の条件で広い画面向けのスタイルを追加していく書き方をモバイルファーストと呼ぶ。狭い画面向けの単純なレイアウトを基本にできるため、CSS が整理しやすい。

CSS 変数
--------

CSS 変数（カスタムプロパティ）を使うと、色や余白などの値に名前を付けて、複数の場所で再利用できる。``--`` で始まる名前で定義し、``var()`` で参照する。

.. code-block:: css

   :root {
     --main-color: steelblue;
   }

   header {
     background-color: var(--main-color);
   }

``:root`` はルート要素（``html`` 要素）を表す疑似クラスである。CSS 変数は継承されるため、``:root`` に定義した変数はページ全体で使える。テーマの色を変更したいときは、定義を 1 か所書き換えるだけで済む。

トランジションとアニメーション
------------------------------

トランジション
~~~~~~~~~~~~~~

``transition`` プロパティを指定すると、プロパティの値が変化したとき（``:hover`` になったときなど）に、瞬時に切り替えるのではなく、指定した時間をかけて滑らかに変化させる。

.. code-block:: css

   .card {
     transition: transform 0.3s;
   }

   .card:hover {
     transform: translateY(-4px); /* 上に 4px 移動する */
   }

アニメーション
~~~~~~~~~~~~~~

``@keyframes`` で動きの途中経過を定義し、``animation`` プロパティで要素に適用すると、利用者の操作が無くても動くアニメーションを作れる。

.. code-block:: css

   @keyframes blink {
     from { opacity: 1; }
     to   { opacity: 0.3; }
   }

   .badge {
     /* 名前 所要時間 変化の仕方 繰り返し回数 方向 */
     animation: blink 1s ease-in-out infinite alternate;
   }

次のサンプルは、メディアクエリ・CSS 変数・トランジション・アニメーションを使った例である。ブラウザの幅を変えて、カードの列数が変わることを確認すること。開発者ツールのデバイスツールバー（Chrome と Edge では Ctrl + Shift + M キー）を使うと、スマートフォンの画面幅を再現できる。

.. literalinclude:: ../examples/ch05/responsive.html
   :language: html
   :caption: examples/ch05/responsive.html

:download:`responsive.html をダウンロード <../examples/ch05/responsive.html>` ／ `ブラウザで表示 <examples/ch05/responsive.html>`__
