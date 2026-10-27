extends Node2D
## 物理と衝突のサンプルの画面表示を更新する。

@onready var _player: CharacterBody2D = $Player
@onready var _info: Label = $Info


func _process(_delta: float) -> void:
	var coins_left := get_tree().get_nodes_in_group("coins").size()
	_info.text = (
		"速度: (%.0f, %.0f)  床の上: %s  残りのコイン: %d"
		% [_player.velocity.x, _player.velocity.y, _player.is_on_floor(), coins_left]
	)
