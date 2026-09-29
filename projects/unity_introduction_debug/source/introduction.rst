.. _introduction:

はじめに
========

本資料の目的
------------

Unity で作ったゲームが思ったとおりに動かない、あるいは動作が重いという問題には、開発の中で必ず直面します。本資料では、こうした問題に対処するための「デバッグ」と「最適化」について、基本的な考え方と Unity が提供するツールの使い方を解説します。

本資料は、大きく次の 3 つの部分で構成されています。

.. list-table::
   :header-rows: 1
   :widths: 15 20 65

   * - 部分
     - 章
     - 内容
   * - デバッグ
     - 第 2 章〜第 5 章
     - 不具合の原因を調べる手順と、ログ、デバッガー、可視化などの手法
   * - 計測
     - 第 6 章〜第 7 章
     - 最適化の考え方と、Profiler による処理負荷の計測方法
   * - 最適化
     - 第 8 章〜第 11 章
     - CPU、GPU、メモリ、物理演算、UI の各分野における代表的な改善手法

最後の第 12 章では、本資料の内容をチェックリストとしてまとめます。

対象読者と前提知識
------------------

本資料は、次のような知識を持つ方を対象としています。

* Unity エディターの基本操作（シーンの作成、GameObject の配置、コンポーネントの追加）
* C# による簡単なスクリプトの作成と、GameObject に追加して実行する方法
* クラス、メソッド、変数など、プログラミングの基本的な用語

想定する環境
------------

本資料は、次の環境を想定して説明します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 内容
   * - Unity のバージョン
     - Unity 6（6000.0 LTS）
   * - レンダーパイプライン
     - Universal Render Pipeline（URP）
   * - コードエディター
     - Visual Studio 2022、JetBrains Rider、Visual Studio Code のいずれか

Unity のバージョンによっては、メニューの位置や API の名前が本資料の説明と異なる場合があります。その場合は、使用しているバージョンの公式マニュアルを参照してください（:ref:`references`）。

.. _sample-code:

サンプルコードの使い方
----------------------

本資料のサンプルコードは、すべて C# のスクリプトファイルです。各章の本文に掲載しているほか、次の表のリンクからダウンロードできます。

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - ファイル
     - 解説している章
     - 内容
   * - :download:`LogExample.cs <../examples/LogExample.cs>`
     - :ref:`debug-basics`
     - Debug クラスによるログ出力
   * - :download:`DebugLogger.cs <../examples/DebugLogger.cs>`
     - :ref:`debug-basics`
     - リリースビルドでログ出力を取り除くラッパークラス
   * - :download:`GizmosExample.cs <../examples/GizmosExample.cs>`
     - :ref:`debug-tools`
     - Gizmos と Debug.DrawRay による可視化
   * - :download:`FpsCounter.cs <../examples/FpsCounter.cs>`
     - :ref:`debug-tools`
     - 画面上へのフレームレートの表示
   * - :download:`NullCheckExample.cs <../examples/NullCheckExample.cs>`
     - :ref:`common-bugs`
     - 破棄されたオブジェクトと null の比較
   * - :download:`ExecutionOrderExample.cs <../examples/ExecutionOrderExample.cs>`
     - :ref:`common-bugs`
     - イベント関数の実行順序の確認
   * - :download:`ProfilerMarkerExample.cs <../examples/ProfilerMarkerExample.cs>`
     - :ref:`profiling`
     - ProfilerMarker による処理区間の計測
   * - :download:`GcAllocationExample.cs <../examples/GcAllocationExample.cs>`
     - :ref:`cpu-optimization`
     - GC アロケーションが発生するコードと改善後のコードの比較
   * - :download:`ComponentCacheExample.cs <../examples/ComponentCacheExample.cs>`
     - :ref:`cpu-optimization`
     - GetComponent の結果のキャッシュ
   * - :download:`BulletPool.cs <../examples/BulletPool.cs>`
     - :ref:`cpu-optimization`
     - ObjectPool<T> による弾の再利用
   * - :download:`RaycastNonAllocExample.cs <../examples/RaycastNonAllocExample.cs>`
     - :ref:`cpu-optimization`
     - Physics.RaycastNonAlloc による GC アロケーションの回避

サンプルコードは、次の手順で使用します。

#. ファイルをダウンロードし、Unity プロジェクトの Assets フォルダー内に配置します。
#. シーンに GameObject を作成し、Inspector ウィンドウの :guilabel:`Add Component` ボタンからスクリプトを追加します。
#. 必要に応じて Inspector ウィンドウで設定値を変更し、再生します。

.. note::

   Unity では、MonoBehaviour を継承したクラスの名前とファイル名が一致していないと、そのスクリプトを GameObject に追加できません。ファイル名は変更せずに使用してください。
