モデルコース
============

この章では、本書で紹介した名所を組み合わせた旅程の例を紹介する。図中の所要時間は、各章のアクセス情報にもとづく片道の目安であり、見学にかかる時間は含まない。鉄道やバスの本数は路線によって大きく異なるため、出かける前に時刻表を確認すること。

水戸・大洗コース（日帰り）
--------------------------

水戸藩ゆかりの史跡と、大洗の海を一日で巡るコースである。梅の時期（2 月から 3 月）に訪れると、偕楽園と弘道館で梅も楽しめる。

.. graphviz::
   :caption: 水戸・大洗コースの行程
   :align: center

   digraph mito_oarai {
       rankdir=TB;
       nodesep=0.3;
       node [shape=box, style="rounded,filled", fillcolor="#eef4fb", color="#3b78c2"];
       edge [color="#555555", fontsize=10];
       station [label="JR 水戸駅"];
       kodokan [label="弘道館"];
       station2 [label="JR 水戸駅"];
       kairakuen [label="偕楽園"];
       oarai [label="大洗駅"];
       aqua [label="アクアワールド\n茨城県大洗水族館"];
       jinja [label="大洗磯前神社"];
       station -> kodokan [label="徒歩 約 8 分"];
       kodokan -> kairakuen [label="バス"];
       kairakuen -> station2 [label="バス 約 20 分"];
       station2 -> oarai [label="鹿島臨海鉄道"];
       oarai -> aqua [label="バス 約 15 分"];
       aqua -> jinja [label="バス・タクシー"];
   }

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 立ち寄り先
     - ポイント
   * - 弘道館
     - 水戸駅から歩いて行ける。藩校の建物と梅林を見学する。
   * - 偕楽園
     - 好文亭と梅林、竹林を巡る。
   * - アクアワールド茨城県大洗水族館
     - サメやマンボウの展示と、イルカ・アシカのショーを楽しむ。
   * - 大洗磯前神社
     - 神磯の鳥居を見る。昼食や帰りがけに大洗の海の幸を味わうのもよい。

ひたちなか・那珂湊コース（日帰り）
----------------------------------

国営ひたち海浜公園の花畑と、那珂湊の海の幸を楽しむコースである。ネモフィラ（4 月中旬から 5 月上旬）やコキア（10 月中旬から下旬）の時期がおすすめである。

.. graphviz::
   :caption: ひたちなか・那珂湊コースの行程
   :align: center

   digraph hitachinaka {
       rankdir=TB;
       node [shape=box, style="rounded,filled", fillcolor="#eef4fb", color="#3b78c2"];
       edge [color="#555555", fontsize=10];
       katsuta [label="JR 勝田駅"];
       park [label="国営ひたち\n海浜公園"];
       katsuta2 [label="JR 勝田駅"];
       nakaminato [label="那珂湊駅"];
       market [label="那珂湊\nおさかな市場"];
       katsuta -> park [label="バス 約 15 分"];
       park -> katsuta2 [label="バス 約 15 分"];
       katsuta2 -> nakaminato [label="ひたちなか海浜鉄道湊線"];
       nakaminato -> market [label="徒歩 約 10 分"];
   }

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 立ち寄り先
     - ポイント
   * - 国営ひたち海浜公園
     - 午前中のうちに花畑を見て回る。見頃の時期は非常に混雑するため、早めの到着がよい。
   * - 那珂湊おさかな市場
     - 回転寿司や海鮮丼で昼食をとり、土産に干物などの水産加工品を買う。

つくば・筑波山コース（日帰り）
------------------------------

つくばエクスプレスを使い、宇宙開発の拠点と筑波山を巡るコースである。筑波山の紅葉（11 月）や梅（2 月から 3 月）の時期は特ににぎわう。

.. graphviz::
   :caption: つくば・筑波山コースの行程
   :align: center

   digraph tsukuba {
       rankdir=TB;
       node [shape=box, style="rounded,filled", fillcolor="#eef4fb", color="#3b78c2"];
       edge [color="#555555", fontsize=10];
       akiba [label="秋葉原駅"];
       tsukuba [label="つくば駅"];
       jaxa [label="JAXA\n筑波宇宙センター"];
       tsukuba2 [label="つくば駅"];
       mountain [label="筑波山\n筑波山神社"];
       akiba -> tsukuba [label="つくばエクスプレス"];
       tsukuba -> jaxa [label="バス"];
       jaxa -> tsukuba2 [label="バス"];
       tsukuba2 -> mountain [label="シャトルバス 約 40 分"];
   }

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 立ち寄り先
     - ポイント
   * - JAXA 筑波宇宙センター
     - 展示館スペースドームで人工衛星やロケットエンジンを見学する。
   * - 筑波山・筑波山神社
     - 筑波山神社に参拝し、ロープウェイで女体山に上って関東平野を眺める。ケーブルカーの運行状況は事前に確認すること（:doc:`kennan`\ を参照）。

県北の自然コース（1 泊 2 日）
-----------------------------

袋田の滝や竜神大吊橋など、県北の山あいの自然を巡るコースである。紅葉が見頃となる 11 月がおすすめである。県北の山間部は鉄道やバスの本数が少ないため、車で回ると効率がよい。

.. graphviz::
   :caption: 県北の自然コースの行程
   :align: center

   digraph kenpoku {
       rankdir=TB;
       node [shape=box, style="rounded,filled", fillcolor="#eef4fb", color="#3b78c2"];
       edge [color="#555555", fontsize=10];
       subgraph cluster_day1 {
           label="1 日目";
           color="#bbbbbb";
           mito [label="JR 水戸駅"];
           fukuroda_st [label="袋田駅"];
           fukuroda [label="袋田の滝\n（大子町に宿泊）"];
       }
       subgraph cluster_day2 {
           label="2 日目";
           color="#bbbbbb";
           ohta [label="常陸太田駅"];
           ryujin [label="竜神大吊橋"];
           seizan [label="西山御殿"];
       }
       mito -> fukuroda_st [label="JR 水郡線"];
       fukuroda_st -> fukuroda [label="バス 約 10 分"];
       fukuroda -> ohta [label="JR 水郡線"];
       ohta -> ryujin [label="バス 約 40 分"];
       ryujin -> seizan [label="バス・タクシー"];
   }

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 立ち寄り先
     - ポイント
   * - 袋田の滝
     - 二つの観瀑台から滝を眺める。大子町の温泉宿に泊まり、奥久慈しゃもや常陸秋そばを味わう。
   * - 竜神大吊橋
     - 長さ 375 m の吊り橋を渡り、竜神峡の渓谷を見下ろす。
   * - 西山御殿
     - 徳川光圀が晩年を過ごした隠居所と庭園を見学する。

鹿島・潮来の水郷コース（日帰り）
--------------------------------

鹿島神宮と息栖神社に参拝し、潮来の水郷を巡るコースである。あやめが咲く 6 月が特におすすめである。千葉県の香取神宮とあわせて東国三社を巡るのもよい。

.. graphviz::
   :caption: 鹿島・潮来の水郷コースの行程
   :align: center

   digraph kashima_itako {
       rankdir=TB;
       node [shape=box, style="rounded,filled", fillcolor="#eef4fb", color="#3b78c2"];
       edge [color="#555555", fontsize=10];
       tokyo [label="東京駅"];
       kashima [label="鹿島神宮"];
       ikisu [label="息栖神社"];
       itako [label="水郷潮来\nあやめ園"];
       tokyo -> kashima [label="高速バス 約 2 時間"];
       kashima -> ikisu [label="バス"];
       ikisu -> itako [label="バス・タクシー"];
   }

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 立ち寄り先
     - ポイント
   * - 鹿島神宮
     - 楼門と社殿を見た後、森の中の奥参道を歩いて奥宮、要石、御手洗池を巡る。
   * - 息栖神社
     - 一の鳥居の脇にある忍潮井を見る。
   * - 水郷潮来あやめ園
     - あやめを眺め、ろ舟で前川を巡る。潮来駅からは JR 鹿島線で帰ることもできる。
