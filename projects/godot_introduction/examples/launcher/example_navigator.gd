extends Node
## どのサンプルからでも Esc キーでランチャーに戻れるようにするオートロード。

const LAUNCHER_SCENE := "res://launcher/launcher.tscn"


func _ready() -> void:
	# ゲームが一時停止中でも入力を受け付けるようにする。
	process_mode = Node.PROCESS_MODE_ALWAYS


func _unhandled_input(event: InputEvent) -> void:
	if not event.is_action_pressed("back_to_launcher"):
		return
	var current := get_tree().current_scene
	if current != null and current.scene_file_path == LAUNCHER_SCENE:
		return
	get_tree().paused = false
	get_tree().change_scene_to_file(LAUNCHER_SCENE)
