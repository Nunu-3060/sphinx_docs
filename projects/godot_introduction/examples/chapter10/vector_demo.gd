extends Node2D
## ベクトルの基本演算を可視化するサンプル。
## 矢印はマウスの方向を向き、追跡者（オレンジの円）はマウスに向かって一定の速さで進む。

const CHASER_SPEED: float = 150.0

var _chaser_position := Vector2(100, 500)

@onready var _arrow: Node2D = $Arrow
@onready var _info: Label = $Info


func _process(delta: float) -> void:
	var mouse := get_global_mouse_position()

	# 矢印をマウスの方向へ向ける。look_at() はノードの +X 方向を目標へ向ける。
	_arrow.look_at(mouse)

	# 追跡者からマウスへのベクトル = 目標の位置 - 自分の位置
	var to_mouse := mouse - _chaser_position
	if to_mouse.length() > 5.0:
		# normalized() で長さを 1 にしてから速さを掛ける。
		_chaser_position += to_mouse.normalized() * CHASER_SPEED * delta

	# 矢印の正面の向きと「矢印から追跡者への向き」の内積で、追跡者が矢印の前にいるかを判定する。
	var forward := Vector2.RIGHT.rotated(_arrow.rotation)
	var dot := forward.dot(_arrow.position.direction_to(_chaser_position))
	var side := "前" if dot > 0.0 else "後ろ"
	_info.text = (
		"矢印の角度: %.1f 度  追跡者とマウスの距離: %.1f  内積: %.2f（追跡者は矢印の%s）"
		% [rad_to_deg(_arrow.rotation), to_mouse.length(), dot, side]
	)
	queue_redraw()


func _draw() -> void:
	draw_line(_chaser_position, get_global_mouse_position(), Color(1, 1, 1, 0.3), 2.0)
	draw_circle(_chaser_position, 16.0, Color.ORANGE)
