extends Node
## ライフサイクル関数が呼ばれる順番を確認するスクリプト。
## 親ノードと子ノードの両方にこのスクリプトを付けて実行する。

var _frame_count: int = 0


func _init() -> void:
	# この時点ではまだシーンツリーに入っていないので、名前も決まっていない。
	print("_init")


func _enter_tree() -> void:
	print(name, ": _enter_tree")


func _ready() -> void:
	print(name, ": _ready")


func _process(delta: float) -> void:
	# 毎フレーム呼ばれる。出力が多くなりすぎないよう最初の 3 回だけ表示する。
	if _frame_count < 3:
		print(name, ": _process delta=%.4f" % delta)
	_frame_count += 1


func _physics_process(delta: float) -> void:
	if _frame_count < 3:
		print(name, ": _physics_process delta=%.4f" % delta)


func _exit_tree() -> void:
	print(name, ": _exit_tree")
