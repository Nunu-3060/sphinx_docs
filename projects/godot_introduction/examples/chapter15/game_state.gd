extends Node
## シーンをまたいで保持するゲームの状態。プロジェクト設定でオートロードに登録して使う。
## どのスクリプトからも GameState という名前でアクセスできる。

signal score_changed(score: int)

const SAVE_PATH := "user://chapter15_save.cfg"

var score: int = 0:
	set(value):
		score = value
		score_changed.emit(score)
var high_score: int = 0


func _ready() -> void:
	load_game()


## 今回のスコアが最高記録を超えていたら更新して保存する。更新したら true を返す。
func commit_score() -> bool:
	if score <= high_score:
		return false
	high_score = score
	save_game()
	return true


func save_game() -> void:
	var config := ConfigFile.new()
	config.set_value("record", "high_score", high_score)
	var error := config.save(SAVE_PATH)
	if error != OK:
		push_error("セーブに失敗した: %s" % error_string(error))


func load_game() -> void:
	var config := ConfigFile.new()
	# 初回起動時はファイルがないので、読み込みに失敗しても既定値のまま進める。
	if config.load(SAVE_PATH) != OK:
		return
	high_score = config.get_value("record", "high_score", 0)


func reset_record() -> void:
	high_score = 0
	save_game()
