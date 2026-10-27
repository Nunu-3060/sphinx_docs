extends Node2D
## delta を使う移動と使わない移動の違いを確かめるサンプル。
## 上下キーで最大フレームレートを切り替えると、delta を使わない四角形だけ速さが変わる。

const SPEED: float = 200.0  # 1 秒あたりの移動量 [ピクセル]
const FPS_CHOICES: Array[int] = [30, 60, 144]

var _fps_index: int = 1
var _x_with_delta: float = 0.0
var _x_without_delta: float = 0.0
var _tick_count: int = 0

@onready var _info: Label = $Info


func _ready() -> void:
	Engine.max_fps = FPS_CHOICES[_fps_index]
	# Timer ノードの timeout シグナルで、一定間隔の処理を行う。
	$TickTimer.timeout.connect(_on_tick_timer_timeout)


func _process(delta: float) -> void:
	# 正しい書き方：速さ × 経過時間。フレームレートが変わっても 1 秒で 200 ピクセル進む。
	_x_with_delta = wrapf(_x_with_delta + SPEED * delta, 0.0, 1000.0)
	# 誤った書き方：1 フレームごとに一定量進む。フレームレートが高いほど速くなる。
	_x_without_delta = wrapf(_x_without_delta + SPEED / 60.0, 0.0, 1000.0)
	var info_format := "最大 FPS: %d（上下キーで変更）  実測 FPS: %d  タイマーの発火回数: %d"
	_info.text = info_format % [Engine.max_fps, Engine.get_frames_per_second(), _tick_count]
	# _draw() を呼び直して、四角形を新しい位置に描き直す。
	queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("move_up"):
		_fps_index = mini(_fps_index + 1, FPS_CHOICES.size() - 1)
	elif event.is_action_pressed("move_down"):
		_fps_index = maxi(_fps_index - 1, 0)
	else:
		return
	Engine.max_fps = FPS_CHOICES[_fps_index]


func _exit_tree() -> void:
	# 他のサンプルに影響しないよう、制限を解除する（0 は無制限）。
	Engine.max_fps = 0


func _draw() -> void:
	var font := ThemeDB.fallback_font
	draw_string(font, Vector2(50, 140), "delta を使う")
	draw_rect(Rect2(50.0 + _x_with_delta, 150.0, 40.0, 40.0), Color.SKY_BLUE)
	draw_string(font, Vector2(50, 290), "delta を使わない")
	draw_rect(Rect2(50.0 + _x_without_delta, 300.0, 40.0, 40.0), Color.SALMON)


func _on_tick_timer_timeout() -> void:
	_tick_count += 1
