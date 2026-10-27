extends AnimatedSprite2D
## 左右に往復しながら歩くキャラクター。進む向きに合わせて画像を反転する。

const SPEED: float = 120.0
const LEFT_END: float = 100.0
const RIGHT_END: float = 500.0

var _direction: float = 1.0


func _ready() -> void:
	play("walk")


func _process(delta: float) -> void:
	position.x += _direction * SPEED * delta
	if position.x > RIGHT_END or position.x < LEFT_END:
		_direction = -_direction
	# 元の画像は右向き。左へ進むときは左右反転して表示する。
	flip_h = _direction < 0.0
