『宝石と見張り』 - 総合演習のサンプル

■ 必要なもの
  Python 3.10 以上、pygame-ce、matplotlib（ヒートマップを描く場合のみ）
    python -m pip install pygame-ce matplotlib

■ 遊ぶ
  final_project フォルダに移動して実行する。
    python main.py

  操作: 矢印キー（または WASD）で移動、Space で待つ、Z で 1 手戻す、R でやり直し、Esc で終了

■ ファイル
  game_logic.py  ルール（画面表示を含まない部分）
  solver.py      幅優先探索でレベルを解き、最短手数を求める
  main.py        pygame-ce による画面表示と操作
  levels/        レベルのテキストファイル（ファイル名の順に遊ぶ）

■ レベルを作る
  levels フォルダに level5.txt などを追加し、solver.py で解けることを確かめる。
    python solver.py levels/level5.txt

■ プレイログを分析する
  main.py は遊んだ記録を playlog.csv に追記する。
  zip を展開したフォルダ（playtest_heatmap.py がある場所）で次のように実行すると、
  レベル「二つの通り道」で移動した位置のヒートマップを表示する。
    python playtest_heatmap.py --input final_project/playlog.csv --event move --level 二つの通り道 --grid
