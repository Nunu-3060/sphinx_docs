extends Node2D
## 最初のスクリプト。起動時にメッセージを出力し、ラベルの文字を書き換える。


func _ready() -> void:
	print("Hello, Godot!")
	$Message.text = "Hello, Godot!"
