extends Node2D
## イージング（Tween.TransitionType）の違いを比較するサンプル。
## 4 つの四角形を、同じ時間で同じ距離だけ異なるイージングで動かす。

const DISTANCE: float = 400.0
const DURATION: float = 1.5

## 比較するイージングと表示名
const TRANSITIONS: Array[Array] = [
	[Tween.TRANS_LINEAR, "LINEAR"],
	[Tween.TRANS_SINE, "SINE"],
	[Tween.TRANS_BACK, "BACK"],
	[Tween.TRANS_BOUNCE, "BOUNCE"],
]


func _ready() -> void:
	for i in TRANSITIONS.size():
		var box := ColorRect.new()
		box.size = Vector2(32, 32)
		box.position = Vector2(0, i * 48)
		box.color = Color.from_hsv(i / 4.0, 0.6, 1.0)
		add_child(box)

		var label := Label.new()
		label.text = TRANSITIONS[i][1]
		label.position = Vector2(-100, i * 48)
		add_child(label)

		# 往復を無限に繰り返す Tween を作る。
		var transition: Tween.TransitionType = TRANSITIONS[i][0]
		var tween := create_tween().set_loops()
		tween.set_trans(transition).set_ease(Tween.EASE_OUT)
		tween.tween_property(box, "position:x", DISTANCE, DURATION)
		tween.tween_interval(0.5)
		tween.tween_property(box, "position:x", 0.0, DURATION)
		tween.tween_interval(0.5)
