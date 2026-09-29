.. _checklist:

まとめとチェックリスト
======================

本資料で解説した内容を、チェックリストとしてまとめます。不具合の調査や最適化を行う際の確認に使ってください。

デバッグのチェックリスト
------------------------

.. list-table::
   :header-rows: 1
   :widths: 70 30

   * - 確認項目
     - 参照先
   * - 不具合を確実に再現する手順が分かっているか。
     - :ref:`debug-steps`
   * - Console ウィンドウのスタックトレースで、例外が発生した場所を確認したか。
     - :ref:`debug-basics`
   * - ログに context を渡して、どのオブジェクトのログかを特定できるようにしているか。
     - :ref:`debug-basics`
   * - 毎フレーム実行されるログが、リリースビルドに残っていないか。
     - :ref:`debug-basics`
   * - ログで追いきれない場合に、IDE のデバッガーや条件付きブレークポイントを使っているか。
     - :ref:`ide-debugger`
   * - 当たり判定や Ray など目に見えない情報を、Gizmos などで可視化したか。
     - :ref:`gizmos`
   * - Inspector ウィンドウでの設定忘れや、``GetComponent`` の失敗による null を疑ったか。
     - :ref:`null-reference`
   * - ``UnityEngine.Object`` の null チェックに ``?.`` や ``is null`` を使っていないか。
     - :ref:`missing-reference`
   * - ``Awake`` と ``Start`` の役割を分け、初期化の順序に依存した不具合を防いでいるか。
     - :ref:`execution-order`
   * - 移動量に ``Time.deltaTime`` を掛け、物理演算の処理を ``FixedUpdate`` で行っているか。
     - :ref:`update-fixedupdate`
   * - 実機でしか発生しない不具合を、Development Build とログファイルで調査したか。
     - :ref:`device-debug`

最適化のチェックリスト
----------------------

.. list-table::
   :header-rows: 1
   :widths: 70 30

   * - 確認項目
     - 参照先
   * - 対象の端末と、目標のフレームレートを決めているか。
     - :ref:`frame-budget`
   * - 推測ではなく、実機での計測に基づいてボトルネックを特定したか。
     - :ref:`optimization-basics`
   * - CPU バウンドか GPU バウンドかを見分けたか。
     - :ref:`cpu-gpu-bound`
   * - 改善の前後で、同じ条件で計測して効果を確認したか。
     - :ref:`profiling`
   * - 毎フレーム実行される処理で、GC アロケーションが発生していないか。
     - :ref:`gc-allocation`
   * - ``GetComponent`` や ``Find`` の結果をキャッシュしているか。
     - :ref:`cpu-optimization`
   * - 生成と破棄を繰り返すオブジェクトに、オブジェクトプールを使っているか。
     - :ref:`object-pool`
   * - SetPass コールの数を確認し、バッチングが効いているかを Frame Debugger で確認したか。
     - :ref:`gpu-optimization`
   * - 半透明のオブジェクトやパーティクルによるオーバードローが多すぎないか。
     - :ref:`gpu-optimization`
   * - テクスチャの最大サイズ、圧縮形式、ミップマップ、Read/Write の設定は適切か。
     - :ref:`memory-optimization`
   * - オーディオの Load Type は、音声の長さに合っているか。
     - :ref:`memory-optimization`
   * - Layer Collision Matrix で、不要な衝突の判定を無効にしているか。
     - :ref:`physics-ui`
   * - 頻繁に変化する UI を別の Canvas に分けているか。
     - :ref:`physics-ui`

おわりに
--------

デバッグと最適化は、どちらも「観察し、仮説を立て、検証する」という同じ考え方に基づいています。やみくもにコードを書き換えるのではなく、ツールを使って事実を確かめながら進めることが、問題を早く確実に解決する近道です。本資料で紹介したツールと手法を、日々の開発に役立ててください。
