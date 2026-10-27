extends Control
## サンプルの一覧を表示し、選んだシーンを起動するランチャー。
##
## 各サンプルの実行中に Esc キーを押すと、この画面に戻る
## （example_navigator.gd を参照）。

## 一覧に表示するサンプル。[表示名, シーンのパス] の組で並べる。
const EXAMPLES: Array[Array] = [
	["第 3 章 Hello, Godot!", "res://chapter03/hello.tscn"],
	["第 5 章 シーンのインスタンス化", "res://chapter05/level.tscn"],
	["第 6 章 GDScript の基礎（出力パネルを見る）", "res://chapter06/basics.tscn"],
	["第 6 章 ライフサイクル関数", "res://chapter06/lifecycle.tscn"],
	["第 7 章 シグナルと await", "res://chapter07/signal_demo.tscn"],
	["第 8 章 delta とタイマー", "res://chapter08/delta_demo.tscn"],
	["第 9 章 入力", "res://chapter09/input_demo.tscn"],
	["第 10 章 ベクトル", "res://chapter10/vector_demo.tscn"],
	["第 11 章 物理と衝突", "res://chapter11/platformer.tscn"],
	["第 12 章 アニメーション", "res://chapter12/animation_demo.tscn"],
	["第 12 章 タイルマップとカメラ", "res://chapter12/tilemap_demo.tscn"],
	["第 13 章 UI", "res://chapter13/ui_demo.tscn"],
	["第 14 章 サウンド", "res://chapter14/audio_demo.tscn"],
	["第 15 章 シーン切り替えとセーブ", "res://chapter15/title.tscn"],
	["第 16 章 シェーダー", "res://chapter16/shader_demo.tscn"],
	["第 17 章 チュートリアル：岩よけゲーム", "res://chapter17/main.tscn"],
	["第 18 章 デバッグ", "res://chapter18/debug_demo.tscn"],
	["第 20 章 3D の入り口", "res://chapter20/world_3d.tscn"],
]

@onready var _list: VBoxContainer = %ExampleList


func _ready() -> void:
	for example: Array in EXAMPLES:
		var button := Button.new()
		button.text = example[0]
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		var path: String = example[1]
		button.pressed.connect(func() -> void: get_tree().change_scene_to_file(path))
		_list.add_child(button)
	# 最初のボタンにフォーカスを当て、キーボードやゲームパッドでも選べるようにする。
	if _list.get_child_count() > 0:
		(_list.get_child(0) as Button).grab_focus()
