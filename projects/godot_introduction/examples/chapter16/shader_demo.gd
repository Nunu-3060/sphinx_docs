extends Node2D
## 4 種類のシェーダーを試すサンプル。
## スペースキーで点滅、Enter キーで画面効果の切り替えを行う。消滅の効果は自動で繰り返す。

@onready var _flash_material: ShaderMaterial = $FlashSprite.material
@onready var _dissolve_material: ShaderMaterial = $DissolveSprite.material
@onready var _screen_effect: ColorRect = $EffectLayer/ScreenEffect


func _ready() -> void:
	# シェーダーの uniform は set_shader_parameter() で変更する。
	# Tween を使えば、時間をかけて変化させられる。
	var tween := create_tween().set_loops()
	tween.tween_method(_set_dissolve_progress, 0.0, 1.0, 2.0)
	tween.tween_interval(0.5)
	tween.tween_method(_set_dissolve_progress, 1.0, 0.0, 2.0)
	tween.tween_interval(0.5)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("jump"):
		_flash()
	elif event.is_action_pressed("ui_accept"):
		_screen_effect.visible = not _screen_effect.visible


## 白く光ってから 0.3 秒かけて元に戻る。
func _flash() -> void:
	var tween := create_tween()
	tween.tween_method(_set_flash_amount, 1.0, 0.0, 0.3)


func _set_flash_amount(value: float) -> void:
	_flash_material.set_shader_parameter("flash_amount", value)


func _set_dissolve_progress(value: float) -> void:
	_dissolve_material.set_shader_parameter("progress", value)
