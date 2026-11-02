extends Node
## どのシーンからでも Esc キーでメニュー（main.tscn）に戻れるようにするオートロード。

const MENU_SCENE := "res://main.tscn"


func _unhandled_input(event: InputEvent) -> void:
	if not event.is_action_pressed("ui_cancel"):
		return
	var current := get_tree().current_scene
	if current != null and current.scene_file_path != MENU_SCENE:
		get_tree().change_scene_to_file(MENU_SCENE)
