extends Node
## 変数、定数、型、文字列の書式指定の例。

const MAX_HP: int = 100  # 定数。値を変更できない

var player_name: String = "ゴドー"  # 型を明示した変数
var speed := 200.0  # := で右辺から型を推論する（float になる）
var target: Node = null  # オブジェクト型は null を代入できる


func _ready() -> void:
	print("--- 変数と型 ---")
	var hp: int = MAX_HP
	hp -= 30
	print(player_name, " の HP: ", hp, " / ", MAX_HP)
	print("speed の型: ", type_string(typeof(speed)))
	print("target は null か: ", target == null)

	# 整数どうしの割り算は整数になる（小数点以下は 0 の方向へ切り捨て）。
	# エディターは警告を出すが、ここでは結果を確かめるために @warning_ignore で抑えている。
	@warning_ignore("integer_division")
	print("7 / 2 = ", 7 / 2, "、7.0 / 2 = ", 7.0 / 2)
	@warning_ignore("integer_division")
	print("-7 / 2 = ", -7 / 2, "（Python の -7 // 2 は -4）")
	print("-7 % 3 = ", -7 % 3, "、posmod(-7, 3) = ", posmod(-7, 3))

	# 文字列の書式指定
	print("%s のスコアは %05d 点" % [player_name, 420])
	print("{name} は {x}, {y} にいる".format({"name": player_name, "x": 10, "y": 20}))
	print("円周率は約 %.2f" % PI)
