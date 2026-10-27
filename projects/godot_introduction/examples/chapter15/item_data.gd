class_name ItemData
extends Resource
## アイテムの定義データ。インスペクターで値を入力して .tres ファイルとして保存する。

@export var display_name: String = ""
@export var points: int = 0
@export var color: Color = Color.WHITE
@export_multiline var description: String = ""
