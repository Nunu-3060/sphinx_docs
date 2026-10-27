extends Node2D
## デバッグ用の出力関数と、性能の監視（モニター）を試すサンプル。
## スペースキーでノードを 100 個作り、Enter キーでまとめて削除する。
## デバッガーの「モニター」タブで、オブジェクト数の変化を確認できる。

const BATCH_SIZE: int = 100

var _spawned: Array[Node2D] = []

@onready var _info: Label = $Info
@onready var _container: Node2D = $Spawned


func _ready() -> void:
	print("通常の出力")
	print_rich("[color=green][b]色付き[/b][/color]の出力")
	# 呼び出し元のファイル名と行番号も一緒に出力する。
	print_debug("print_debug() の出力")
	# 警告とエラーはデバッガーの「エラー」タブにも表示される。実行は止まらない。
	push_warning("これは警告の例")
	push_error("これはエラーの例（実際には問題は起きていない）")
	# 独自の値をデバッガーの「モニター」タブに表示する。
	Performance.add_custom_monitor("sample/spawned_nodes", _get_spawned_count)


func _exit_tree() -> void:
	Performance.remove_custom_monitor("sample/spawned_nodes")


func _process(_delta: float) -> void:
	_info.text = (
		"FPS: %d  オブジェクト数: %d  作成したノード: %d"
		% [
			Engine.get_frames_per_second(),
			Performance.get_monitor(Performance.OBJECT_COUNT),
			_spawned.size(),
		]
	)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("jump"):
		_spawn_batch()
	elif event.is_action_pressed("ui_accept"):
		_clear()


func _spawn_batch() -> void:
	# assert() は条件が偽のとき、デバッグ実行中だけ実行を止める（エクスポートしたゲームでは無視される）。
	assert(_spawned.size() < 10000, "ノードを作りすぎている。Enter キーで削除すること")
	for i in BATCH_SIZE:
		var dot := Polygon2D.new()
		dot.polygon = PackedVector2Array([Vector2(-4, -4), Vector2(4, -4), Vector2(4, 4), Vector2(-4, 4)])
		dot.position = Vector2(randf_range(40, 1100), randf_range(140, 620))
		dot.color = Color.from_hsv(randf(), 0.7, 1.0)
		_container.add_child(dot)
		_spawned.append(dot)


func _clear() -> void:
	for dot in _spawned:
		dot.queue_free()
	_spawned.clear()


func _get_spawned_count() -> int:
	return _spawned.size()
