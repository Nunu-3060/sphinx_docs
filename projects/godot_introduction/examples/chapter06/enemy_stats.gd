class_name EnemyStats
extends RefCounted
## 敵の能力値を表すクラス。class_name を付けたので、どのスクリプトからも EnemyStats という名前で使える。

var enemy_name: String
var hp: int
var attack: int


## new() に渡した引数は _init() で受け取る。
func _init(new_name: String, new_hp: int, new_attack: int) -> void:
	enemy_name = new_name
	hp = new_hp
	attack = new_attack


func is_alive() -> bool:
	return hp > 0


func take_damage(amount: int) -> void:
	hp = maxi(hp - amount, 0)


## print() に渡したときの表示を決める。Python の __str__ に相当する。
func _to_string() -> String:
	return "%s (HP %d)" % [enemy_name, hp]
