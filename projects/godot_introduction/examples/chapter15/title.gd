extends Control
## タイトル画面。最高記録を表示し、ステージへ切り替える。

const STAGE_SCENE := "res://chapter15/stage.tscn"


func _ready() -> void:
	%HighScoreLabel.text = "最高記録: %d" % GameState.high_score
	%StartButton.pressed.connect(_on_start_pressed)
	%ResetButton.pressed.connect(_on_reset_pressed)
	%StartButton.grab_focus()


func _on_start_pressed() -> void:
	GameState.score = 0
	get_tree().change_scene_to_file(STAGE_SCENE)


func _on_reset_pressed() -> void:
	GameState.reset_record()
	%HighScoreLabel.text = "最高記録: %d" % GameState.high_score
