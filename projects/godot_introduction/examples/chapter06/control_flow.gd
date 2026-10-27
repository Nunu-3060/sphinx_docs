extends Node
## if、for、while、match の例。


func _ready() -> void:
	print("--- 制御構文 ---")
	var score: int = 75
	if score >= 80:
		print("評価 A")
	elif score >= 60:
		print("評価 B")
	else:
		print("評価 C")

	# range() は Python と同じく終端を含まない。
	for i in range(3):
		print("for: ", i)

	# 数値を直接書くと range() と同じ意味になる。
	for i in 3:
		print("for (省略形): ", i)

	for fruit: String in ["りんご", "みかん"]:
		print("果物: ", fruit)

	var count: int = 0
	while count < 3:
		count += 1
	print("while の結果: ", count)

	# match は他言語の switch 文に相当する。
	for command: String in ["jump", "attack", "dance"]:
		match command:
			"jump":
				print("ジャンプする")
			"attack", "shoot":
				print("攻撃する")
			_:
				print("知らないコマンド: ", command)
