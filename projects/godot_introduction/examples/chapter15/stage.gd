extends Control
## 制限時間内にアイテムのボタンを押して得点を集めるステージ。
## 終了するとスコアを JSON ファイルに書き出し、タイトル画面へ戻る。

const TITLE_SCENE := "res://chapter15/title.tscn"
const RESULT_PATH := "user://chapter15_last_result.json"

## 登場するアイテム。.tres ファイルに保存した ItemData を読み込む。
@export var items: Array[ItemData] = []

var _picked: Dictionary[String, int] = {}

@onready var _timer: Timer = $GameTimer


func _ready() -> void:
	for item in items:
		var button := Button.new()
		button.text = "%s（%d 点）" % [item.display_name, item.points]
		button.tooltip_text = item.description
		button.modulate = item.color
		button.pressed.connect(_on_item_pressed.bind(item))
		%ItemList.add_child(button)
	GameState.score_changed.connect(_on_score_changed)
	_on_score_changed(GameState.score)
	_timer.timeout.connect(_on_game_timer_timeout)
	_timer.start()


func _process(_delta: float) -> void:
	%TimeLabel.text = "残り時間: %.1f 秒" % _timer.time_left


func _on_item_pressed(item: ItemData) -> void:
	GameState.score += item.points
	_picked[item.display_name] = _picked.get(item.display_name, 0) + 1


func _on_score_changed(score: int) -> void:
	%ScoreLabel.text = "スコア: %d" % score


func _on_game_timer_timeout() -> void:
	var is_new_record := GameState.commit_score()
	_save_result(is_new_record)
	get_tree().change_scene_to_file(TITLE_SCENE)


## 今回の結果を JSON 形式で保存する。
func _save_result(is_new_record: bool) -> void:
	var result := {
		"score": GameState.score,
		"new_record": is_new_record,
		"picked": _picked,
		"time": Time.get_datetime_string_from_system(),
	}
	var file := FileAccess.open(RESULT_PATH, FileAccess.WRITE)
	if file == null:
		push_error("結果を保存できない: %s" % error_string(FileAccess.get_open_error()))
		return
	file.store_string(JSON.stringify(result, "  "))
	print("結果を保存した: ", ProjectSettings.globalize_path(RESULT_PATH))
