extends Area2D
## 岩よけゲームのプレイヤー。上下左右に動き、岩に当たると hit シグナルを発行する。

## 岩に当たったときに発行する。
signal hit

const SPEED: float = 400.0  # 移動速度 [ピクセル/秒]
const MARGIN: float = 24.0  # 画面の端から離しておく距離

@onready var _collision: CollisionShape2D = $CollisionShape2D
@onready var _flash: ShaderMaterial = $Sprite2D.material


func _ready() -> void:
	# ゲーム開始までは表示も操作もしない。
	hide()
	set_process(false)


func _process(delta: float) -> void:
	var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	position += direction * SPEED * delta
	# 画面の外に出ないように位置を制限する。
	var screen_size := get_viewport_rect().size
	position = position.clamp(Vector2(MARGIN, MARGIN), screen_size - Vector2(MARGIN, MARGIN))


## 指定した位置からゲームを開始する。
func start(start_position: Vector2) -> void:
	position = start_position
	_flash.set_shader_parameter("flash_amount", 0.0)
	show()
	_collision.disabled = false
	set_process(true)


func _on_area_entered(_area: Area2D) -> void:
	hit.emit()
	set_process(false)
	# 同じ衝突で何度も hit を発行しないよう、当たり判定を無効にする。
	# 物理処理の最中には形状を変更できないため、set_deferred() で処理の後に変更する。
	_collision.set_deferred("disabled", true)
	# 白く光ってから消える演出（シェーダーは第 16 章の flash.gdshader と同じもの）
	var tween := create_tween()
	tween.tween_method(_set_flash_amount, 1.0, 0.0, 0.6)
	tween.tween_callback(hide)


func _set_flash_amount(amount: float) -> void:
	_flash.set_shader_parameter("flash_amount", amount)
