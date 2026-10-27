extends Area2D
## 回転し続けるコイン。プレイヤーが触れると消える。

## 1 秒あたりの回転量 [ラジアン]
@export var spin_speed: float = 3.0

var _angle: float = 0.0


func _process(delta: float) -> void:
	# 画像の横幅を cos で伸び縮みさせて、縦の軸で回っているように見せる。
	_angle += spin_speed * delta
	$Sprite2D.scale.x = cos(_angle)


func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		queue_free()
