extends Node2D
## 入力の 2 つの受け取り方（ポーリングとイベント）を試すサンプル。

const SPEED: float = 300.0

var _jump_count: int = 0

@onready var _player: Sprite2D = $Player
@onready var _info: Label = $Info


func _process(delta: float) -> void:
	# ポーリング：毎フレーム「今どのキーが押されているか」を問い合わせる。
	# get_vector() は 4 つのアクションから長さ 1 以下の方向ベクトルを作る。
	var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	_player.position += direction * SPEED * delta
	_info.text = "方向: %s  ジャンプ回数: %d" % [direction, _jump_count]


func _unhandled_input(event: InputEvent) -> void:
	# イベント：入力が発生したときに 1 回だけ呼ばれる。
	if event.is_action_pressed("jump"):
		_jump_count += 1
		get_viewport().set_input_as_handled()
	elif event is InputEventMouseButton and event.is_pressed():
		# アクションを介さず、イベントの種類を直接調べることもできる。
		_player.position = (event as InputEventMouseButton).position
