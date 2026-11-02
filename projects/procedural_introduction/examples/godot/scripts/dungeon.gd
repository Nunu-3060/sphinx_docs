extends Node2D
## 空間の 2 分割（BSP）で部屋と通路を作るダンジョン（第 11 章に対応）。
## Space または R: 新しいシードで作り直す　B: 分割の境界線の表示を切り替える

enum Tile { WALL, ROOM, CORRIDOR }

const MAP_SIZE := Vector2i(80, 45)  ## マップの大きさ [マス]
const CELL := 16.0  ## 1 マスの大きさ [px]
const MIN_LEAF := 8  ## 分割した区画の 1 辺の最小値 [マス]
const MAX_DEPTH := 5  ## 分割の深さの上限（区画は最大 2^5 = 32 個）
const MIN_ROOM := 4  ## 部屋の 1 辺の最小値 [マス]

var _seed := 1
var _rng := RandomNumberGenerator.new()
var _tiles := PackedByteArray()
var _leaves: Array[Rect2i] = []  ## 分割の末端の区画（境界線の表示用）
var _room_count := 0
var _show_partitions := true

@onready var _info: Label = %Info


## BSP の木の節。末端（葉）の節だけが部屋を持つ。
class Leaf:
	var rect: Rect2i
	var left: Leaf
	var right: Leaf
	var room := Rect2i()

	func _init(area: Rect2i) -> void:
		rect = area


func _ready() -> void:
	_generate()


func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed):
		return
	match (event as InputEventKey).keycode:
		KEY_SPACE, KEY_R:
			_seed += 1
			_generate()
		KEY_B:
			_show_partitions = not _show_partitions
			queue_redraw()


func _generate() -> void:
	var start := Time.get_ticks_usec()
	_rng.seed = _seed
	_tiles.resize(MAP_SIZE.x * MAP_SIZE.y)
	_tiles.fill(Tile.WALL)
	_leaves.clear()
	_room_count = 0
	# 外周の 1 マスを壁として残し、その内側を分割する。
	var root := Leaf.new(Rect2i(Vector2i.ONE, MAP_SIZE - Vector2i(2, 2)))
	_split(root, 0)
	_connect(root)
	var usec := Time.get_ticks_usec() - start
	_info.text = (
		"シード %d　部屋 %d 個　生成 %.2f ms\n[Space] 再生成　[B] 分割の表示" % [_seed, _room_count, usec / 1000.0]
	)
	queue_redraw()


## 区画を再帰的に 2 つに分ける。分けられなくなったら部屋を作る。
func _split(leaf: Leaf, depth: int) -> void:
	var size := leaf.rect.size
	# 横長なら縦の線で、縦長なら横の線で切る。正方形に近ければ乱数で決める。
	var vertical := size.x > size.y
	if maxf(size.x, size.y) < 1.25 * minf(size.x, size.y):
		vertical = _rng.randf() < 0.5
	var length := size.x if vertical else size.y
	if depth >= MAX_DEPTH or length < MIN_LEAF * 2:
		_make_room(leaf)
		return
	# 両側が MIN_LEAF 以上残る範囲で、切る位置を選ぶ。
	var cut := _rng.randi_range(MIN_LEAF, length - MIN_LEAF)
	var r := leaf.rect
	if vertical:
		leaf.left = Leaf.new(Rect2i(r.position.x, r.position.y, cut, r.size.y))
		leaf.right = Leaf.new(Rect2i(r.position.x + cut, r.position.y, r.size.x - cut, r.size.y))
	else:
		leaf.left = Leaf.new(Rect2i(r.position.x, r.position.y, r.size.x, cut))
		leaf.right = Leaf.new(Rect2i(r.position.x, r.position.y + cut, r.size.x, r.size.y - cut))
	_split(leaf.left, depth + 1)
	_split(leaf.right, depth + 1)


## 区画の内側に、大きさと位置が乱数の部屋を作る。区画の境界から 1 マス離す。
func _make_room(leaf: Leaf) -> void:
	_leaves.append(leaf.rect)
	var w := _rng.randi_range(MIN_ROOM, leaf.rect.size.x - 2)
	var h := _rng.randi_range(MIN_ROOM, leaf.rect.size.y - 2)
	var x := _rng.randi_range(leaf.rect.position.x + 1, leaf.rect.end.x - 1 - w)
	var y := _rng.randi_range(leaf.rect.position.y + 1, leaf.rect.end.y - 1 - h)
	leaf.room = Rect2i(x, y, w, h)
	_fill(leaf.room, Tile.ROOM)
	_room_count += 1


## 木の各節で、左右の部分木の部屋どうしを通路でつなぐ。これで全部屋がつながる。
func _connect(leaf: Leaf) -> void:
	if leaf.left == null:
		return
	_connect(leaf.left)
	_connect(leaf.right)
	var a := _pick_room(leaf.left).get_center()
	var b := _pick_room(leaf.right).get_center()
	# L 字の通路。先に横へ進むか縦へ進むかを乱数で決める。
	var corner := Vector2i(b.x, a.y) if _rng.randf() < 0.5 else Vector2i(a.x, b.y)
	_carve_line(a, corner)
	_carve_line(corner, b)


## 部分木の中の部屋を 1 つ乱数で選ぶ。
func _pick_room(leaf: Leaf) -> Rect2i:
	if leaf.left == null:
		return leaf.room
	return _pick_room(leaf.left if _rng.randf() < 0.5 else leaf.right)


## 縦か横の直線の通路を掘る。部屋の床は通路で上書きしない。
func _carve_line(from: Vector2i, to: Vector2i) -> void:
	var step := (to - from).sign()
	var p := from
	while true:
		var index := p.y * MAP_SIZE.x + p.x
		if _tiles[index] == Tile.WALL:
			_tiles[index] = Tile.CORRIDOR
		if p == to:
			break
		p += step


func _fill(rect: Rect2i, tile: Tile) -> void:
	for y in range(rect.position.y, rect.end.y):
		for x in range(rect.position.x, rect.end.x):
			_tiles[y * MAP_SIZE.x + x] = tile


func _draw() -> void:
	# 全体を壁の色で塗り、床のマスだけを描く。
	draw_rect(Rect2(Vector2.ZERO, Vector2(MAP_SIZE) * CELL), Color(0.12, 0.12, 0.16))
	var colors := {Tile.ROOM: Color(0.86, 0.8, 0.66), Tile.CORRIDOR: Color(0.62, 0.55, 0.42)}
	for y in MAP_SIZE.y:
		for x in MAP_SIZE.x:
			var tile := _tiles[y * MAP_SIZE.x + x]
			if tile != Tile.WALL:
				draw_rect(Rect2(Vector2(x, y) * CELL, Vector2(CELL, CELL)).grow(-0.5), colors[tile])
	if _show_partitions:
		for leaf in _leaves:
			draw_rect(
				Rect2(Vector2(leaf.position) * CELL, Vector2(leaf.size) * CELL),
				Color(0.3, 0.75, 1.0, 0.8),
				false,
				2.0
			)
