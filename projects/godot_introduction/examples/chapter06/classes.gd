extends Node
## クラスの利用例。class_name を付けたクラスと内部クラスを使う。


## 内部クラス。このスクリプトの中でだけ使う小さなクラスを定義できる。
class Counter:
	var value: int = 0

	func increment() -> void:
		value += 1


func _ready() -> void:
	print("--- クラス ---")
	var slime := EnemyStats.new("スライム", 10, 2)
	slime.take_damage(4)
	print(slime, " 生存: ", slime.is_alive())
	slime.take_damage(100)
	print(slime, " 生存: ", slime.is_alive())

	var counter := Counter.new()
	counter.increment()
	counter.increment()
	print("カウンター: ", counter.value)
