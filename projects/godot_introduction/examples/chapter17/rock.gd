extends Area2D
## 画面の上から落ちてくる岩。画面の下へ出たら自分自身を削除する。

## 落下速度 [ピクセル/秒]。生成する側（main.gd）が設定する。
var speed: float = 200.0

var _spin: float = 0.0  # 回転の速さ [ラジアン/秒]


func _ready() -> void:
	_spin = randf_range(-3.0, 3.0)
	$VisibleOnScreenNotifier2D.screen_exited.connect(queue_free)


func _process(delta: float) -> void:
	position.y += speed * delta
	rotation += _spin * delta
