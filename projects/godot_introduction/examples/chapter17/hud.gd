extends CanvasLayer
## スコア、メッセージ、開始ボタンを表示する画面。一時停止の切り替えも受け持つ。

## 開始ボタンが押されたときに発行する。
signal start_game

## ゲーム中だけ一時停止できるようにするためのフラグ。main.gd が設定する。
var can_pause: bool = false

@onready var _score_label: Label = $ScoreLabel
@onready var _message: Label = $Message
@onready var _start_button: Button = $StartButton
@onready var _pause_label: Label = $PauseLabel


func _ready() -> void:
	_start_button.pressed.connect(_on_start_button_pressed)
	_pause_label.hide()


func _unhandled_input(event: InputEvent) -> void:
	# この CanvasLayer は Process Mode が Always なので、一時停止中も入力を受け取れる。
	if can_pause and event.is_action_pressed("pause"):
		get_tree().paused = not get_tree().paused
		_pause_label.visible = get_tree().paused


func show_title(high_score: int) -> void:
	show_message("岩をよけろ！\n最高記録: %d" % high_score)
	_start_button.show()
	_start_button.grab_focus()


func show_message(text: String) -> void:
	_message.text = text
	_message.show()


func hide_message() -> void:
	_message.hide()


func update_score(score: int) -> void:
	_score_label.text = str(score)


func show_game_over(high_score: int, is_new_record: bool) -> void:
	show_message("新記録！" if is_new_record else "ゲームオーバー")
	# 2 秒待ってからタイトル表示に戻す。
	await get_tree().create_timer(2.0).timeout
	show_title(high_score)


func _on_start_button_pressed() -> void:
	_start_button.hide()
	start_game.emit()
