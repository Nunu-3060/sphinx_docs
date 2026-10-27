extends Node
## 関数の定義と呼び出しの例。


func _ready() -> void:
	print("--- 関数 ---")
	print("合計: ", add(3, 4))
	print("挨拶: ", greet("ゴドー"))
	print("挨拶: ", greet("ゴドー", "こんばんは"))
	print("2 点間の距離: ", distance(Vector2(0, 0), Vector2(3, 4)))


## 2 つの整数の和を返す。
func add(a: int, b: int) -> int:
	return a + b


## 既定値を持つ引数は、呼び出し時に省略できる。
func greet(target_name: String, message: String = "こんにちは") -> String:
	return "%s、%s" % [message, target_name]


## static を付けた関数は、インスタンスを作らずに呼び出せる。
static func distance(from: Vector2, to: Vector2) -> float:
	return from.distance_to(to)
