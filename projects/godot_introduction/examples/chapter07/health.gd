class_name Health
extends Node
## 体力を管理するコンポーネント。体力が変化したときと 0 になったときにシグナルを発行する。

## 体力が変化したときに発行する。
signal health_changed(current: int, maximum: int)
## 体力が 0 になったときに発行する。
signal died

@export var max_health: int = 100

var current_health: int


func _ready() -> void:
	current_health = max_health


func take_damage(amount: int) -> void:
	if current_health <= 0:
		return
	current_health = maxi(current_health - amount, 0)
	health_changed.emit(current_health, max_health)
	if current_health == 0:
		died.emit()


func heal(amount: int) -> void:
	current_health = mini(current_health + amount, max_health)
	health_changed.emit(current_health, max_health)
