extends Node
## 岩よけゲームの進行を管理する。岩の生成、スコアの計算、ゲームオーバーの処理を行う。

const Player := preload("res://chapter17/player.gd")
const Rock := preload("res://chapter17/rock.gd")
const Hud := preload("res://chapter17/hud.gd")
const SAVE_PATH := "user://rock_dodge.cfg"

## 生成する岩のシーン。インスペクターで rock.tscn を指定する。
@export var rock_scene: PackedScene

var score: int = 0
var high_score: int = 0

@onready var _player: Player = $Player
@onready var _hud: Hud = $HUD
@onready var _start_position: Marker2D = $StartPosition
@onready var _rock_timer: Timer = $RockTimer
@onready var _score_timer: Timer = $ScoreTimer
@onready var _start_timer: Timer = $StartTimer
@onready var _music: AudioStreamPlayer = $Music
@onready var _hit_sound: AudioStreamPlayer = $HitSound


func _ready() -> void:
	_load_high_score()
	_player.hit.connect(game_over)
	_hud.start_game.connect(new_game)
	_start_timer.timeout.connect(_on_start_timer_timeout)
	_score_timer.timeout.connect(_on_score_timer_timeout)
	_rock_timer.timeout.connect(_on_rock_timer_timeout)
	_music.finished.connect(_music.play)
	_hud.show_title(high_score)


func new_game() -> void:
	score = 0
	_rock_timer.wait_time = 0.6
	# 前のゲームで残っている岩をすべて削除する。
	get_tree().call_group("rocks", "queue_free")
	_player.start(_start_position.position)
	_hud.update_score(score)
	_hud.show_message("用意...")
	_start_timer.start()
	_music.play()


func game_over() -> void:
	_rock_timer.stop()
	_score_timer.stop()
	_music.stop()
	_hit_sound.play()
	_hud.can_pause = false
	var is_new_record := score > high_score
	if is_new_record:
		high_score = score
		_save_high_score()
	_hud.show_game_over(high_score, is_new_record)


func _on_start_timer_timeout() -> void:
	_hud.hide_message()
	_hud.can_pause = true
	_rock_timer.start()
	_score_timer.start()


func _on_score_timer_timeout() -> void:
	score += 1
	_hud.update_score(score)
	# 時間がたつほど岩の出現間隔を短くして、難しくする。
	_rock_timer.wait_time = maxf(0.6 - score * 0.01, 0.2)


func _on_rock_timer_timeout() -> void:
	var rock: Rock = rock_scene.instantiate()
	var screen_width := get_viewport().get_visible_rect().size.x
	rock.position = Vector2(randf_range(24.0, screen_width - 24.0), -32.0)
	rock.speed = randf_range(150.0, 250.0) + score * 5.0
	add_child(rock)


func _load_high_score() -> void:
	var config := ConfigFile.new()
	if config.load(SAVE_PATH) == OK:
		high_score = config.get_value("record", "high_score", 0)


func _save_high_score() -> void:
	var config := ConfigFile.new()
	config.set_value("record", "high_score", high_score)
	config.save(SAVE_PATH)
