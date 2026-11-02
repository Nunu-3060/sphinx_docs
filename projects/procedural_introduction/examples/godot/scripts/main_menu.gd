extends Control
## サンプルのシーンを選んで起動するメニュー。

## 一覧に表示するシーン。[表示名, シーンのパス] の組で並べる。
const SCENES: Array[Array] = [
	["メッシュの生成（第 6 章）", "res://mesh_primitives.tscn"],
	["地形のチャンク（第 7 章）", "res://terrain.tscn"],
	["配置と散布（第 10 章）", "res://scatter.tscn"],
	["BSP によるダンジョン（第 11 章）", "res://dungeon.tscn"],
	["手続き的な歩行（第 12 章）", "res://procedural_walk.tscn"],
	["ボイド（第 13 章）", "res://boids.tscn"],
	["統合例：生成される世界の飛行", "res://world.tscn"],
]

@onready var _list: VBoxContainer = %SceneList


func _ready() -> void:
	for entry: Array in SCENES:
		var button := Button.new()
		button.text = entry[0]
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.add_theme_font_size_override("font_size", 22)
		var path: String = entry[1]
		button.pressed.connect(func() -> void: get_tree().change_scene_to_file(path))
		_list.add_child(button)
	# キーボードでも選べるように、最初のボタンにフォーカスを当てる。
	(_list.get_child(0) as Button).grab_focus()
