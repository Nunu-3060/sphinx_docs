# Dodge Lab: 落ちてくるブロックを左右に動いて避けるゲーム。
# Main ノードを選択すると、下の @export の値をインスペクターで変えられる。
# 1 回遊ぶごとに、そのときの値と生存時間を CSV ファイルに追記する。
extends Node2D

@export_group("Player (game feel)")
## 左右に動く最高速度 [px/s]
@export var max_speed: float = 300.0
## キーを押している間の加速度 [px/s^2]。大きいほど素早く最高速度に達する
@export var acceleration: float = 1500.0
## キーを離したときの減速度 [px/s^2]。小さいほど滑る
@export var deceleration: float = 2000.0

@export_group("Blocks (difficulty)")
## ブロックが落ちる加速度（重力）[px/s^2]
@export var fall_gravity: float = 400.0
## ブロックが出現する間隔 [s]。短いほど難しい
@export var spawn_interval: float = 0.9
## ブロックの 1 辺の長さ [px]
@export var block_size: float = 32.0

@export_group("Record")
## この時間だけ生き残ればクリア [s]
@export var time_limit: float = 60.0
## 記録を書き出すファイル
@export var log_path: String = "user://dodge_lab_log.csv"

const PLAYER_SIZE: Vector2 = Vector2(32.0, 32.0)
const GROUND_HEIGHT: float = 40.0

var _player_x: float = 0.0
var _player_vx: float = 0.0
var _blocks: Array[Vector2] = []        # ブロックの中心の位置
var _block_speeds: Array[float] = []    # ブロックの落ちる速さ
var _spawn_timer: float = 0.0
var _elapsed: float = 0.0
var _playing: bool = true
var _message: String = ""
var _rng: RandomNumberGenerator = RandomNumberGenerator.new()


func _ready() -> void:
	_rng.randomize()
	print("Log file: ", ProjectSettings.globalize_path(log_path))
	_restart()


func _restart() -> void:
	var size: Vector2 = get_viewport_rect().size
	_player_x = size.x / 2.0
	_player_vx = 0.0
	_blocks.clear()
	_block_speeds.clear()
	_spawn_timer = 0.0
	_elapsed = 0.0
	_playing = true
	_message = ""


func _process(delta: float) -> void:
	if _playing:
		_update_player(delta)
		_update_blocks(delta)
		_elapsed += delta
		if _hits_block():
			_finish("HIT!")
		elif _elapsed >= time_limit:
			_elapsed = time_limit
			_finish("CLEAR!")
	elif Input.is_action_just_pressed("ui_accept"):
		_restart()
	queue_redraw()


# 入力に応じて、速度を目標の速度へ少しずつ近づける
func _update_player(delta: float) -> void:
	var axis: float = Input.get_axis("ui_left", "ui_right")
	if Input.is_key_pressed(KEY_A):
		axis -= 1.0
	if Input.is_key_pressed(KEY_D):
		axis += 1.0
	axis = clampf(axis, -1.0, 1.0)
	if axis != 0.0:
		_player_vx = move_toward(_player_vx, axis * max_speed, acceleration * delta)
	else:
		_player_vx = move_toward(_player_vx, 0.0, deceleration * delta)
	var width: float = get_viewport_rect().size.x
	var half: float = PLAYER_SIZE.x / 2.0
	_player_x += _player_vx * delta
	if _player_x < half or _player_x > width - half:
		_player_x = clampf(_player_x, half, width - half)
		_player_vx = 0.0


# 一定の間隔でブロックを出し、重力で加速させながら落とす
func _update_blocks(delta: float) -> void:
	var size: Vector2 = get_viewport_rect().size
	_spawn_timer -= delta
	if _spawn_timer <= 0.0:
		_spawn_timer += spawn_interval
		var x: float = _rng.randf_range(block_size / 2.0, size.x - block_size / 2.0)
		_blocks.append(Vector2(x, -block_size))
		_block_speeds.append(0.0)
	for i: int in range(_blocks.size() - 1, -1, -1):
		_block_speeds[i] += fall_gravity * delta
		var center: Vector2 = _blocks[i]
		center.y += _block_speeds[i] * delta
		_blocks[i] = center
		if center.y > size.y + block_size:
			_blocks.remove_at(i)
			_block_speeds.remove_at(i)


func _player_rect() -> Rect2:
	var ground_y: float = get_viewport_rect().size.y - GROUND_HEIGHT
	return Rect2(Vector2(_player_x - PLAYER_SIZE.x / 2.0, ground_y - PLAYER_SIZE.y), PLAYER_SIZE)


func _block_rect(center: Vector2) -> Rect2:
	return Rect2(center - Vector2(block_size, block_size) / 2.0, Vector2(block_size, block_size))


func _hits_block() -> bool:
	var player: Rect2 = _player_rect()
	for center: Vector2 in _blocks:
		if player.intersects(_block_rect(center)):
			return true
	return false


func _finish(result: String) -> void:
	_playing = false
	var saved: bool = _append_log()
	_message = "%s  %.2f s\nPress Enter or Space to retry" % [result, _elapsed]
	if saved:
		_message += "\nSaved: " + ProjectSettings.globalize_path(log_path)


# 設定値と生存時間を CSV に 1 行追記する。初めて書くときは見出しの行も書く
func _append_log() -> bool:
	var exists: bool = FileAccess.file_exists(log_path)
	var file: FileAccess = FileAccess.open(log_path, FileAccess.READ_WRITE if exists else FileAccess.WRITE)
	if file == null:
		push_error("Cannot open %s" % log_path)
		return false
	if exists:
		file.seek_end()
	else:
		file.store_line("date_time,max_speed,acceleration,deceleration,fall_gravity,spawn_interval,survival_time")
	var values: PackedStringArray = [
		Time.get_datetime_string_from_system(),
		str(max_speed), str(acceleration), str(deceleration),
		str(fall_gravity), str(spawn_interval), "%.2f" % _elapsed,
	]
	file.store_line(",".join(values))
	file.close()
	print("Saved: ", ProjectSettings.globalize_path(log_path))
	return true


func _draw() -> void:
	var size: Vector2 = get_viewport_rect().size
	draw_rect(Rect2(Vector2.ZERO, size), Color(0.10, 0.11, 0.14))
	draw_rect(Rect2(0.0, size.y - GROUND_HEIGHT, size.x, GROUND_HEIGHT), Color(0.25, 0.27, 0.30))
	for center: Vector2 in _blocks:
		draw_rect(_block_rect(center), Color(0.90, 0.35, 0.30))
	draw_rect(_player_rect(), Color(0.35, 0.75, 0.95))
	var font: Font = ThemeDB.fallback_font
	draw_string(font, Vector2(12.0, 28.0), "TIME %.1f / %.0f" % [_elapsed, time_limit],
			HORIZONTAL_ALIGNMENT_LEFT, -1.0, 20)
	if not _playing:
		draw_multiline_string(font, Vector2(12.0, size.y / 2.0 - 30.0), _message,
				HORIZONTAL_ALIGNMENT_LEFT, size.x - 24.0, 20)
