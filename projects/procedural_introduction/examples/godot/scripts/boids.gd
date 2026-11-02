extends Node2D
## ボイド（第 13 章に対応）。分離・整列・結合の 3 つの規則で群れを動かす。
## 近くの個体を探すのに、空間を格子に分けて、近くのマスだけを調べる。
## G: 格子と総当たりの切り替え　上下キー: 個体の数を変える　R: 新しいシード

const VIEW_RADIUS := 48.0  ## これより近い個体を「近く」とみなす [px]
const SEPARATION_RADIUS := 20.0  ## これより近い個体から離れる [px]
const MIN_SPEED := 90.0
const MAX_SPEED := 180.0
const MAX_FORCE := 260.0  ## 1 秒あたりの速度の変化の上限 [px/s²]
const SEPARATION_WEIGHT := 1.8
const ALIGNMENT_WEIGHT := 1.0
const COHESION_WEIGHT := 0.7
const EDGE_MARGIN := 60.0  ## 画面の端からこの距離に入ったら内側へ曲がる [px]

var _seed := 1
var _count := 400
var _use_grid := true
var _positions := PackedVector2Array()
var _velocities := PackedVector2Array()
var _grid: Dictionary[Vector2i, PackedInt32Array] = {}  ## マス → そのマスにいる個体の番号
var _step_msec := 0.0

@onready var _info: Label = %Info


func _ready() -> void:
	_spawn()


func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed):
		return
	match (event as InputEventKey).keycode:
		KEY_G:
			_use_grid = not _use_grid
		KEY_UP:
			_count += 200
			_spawn()
		KEY_DOWN:
			_count = maxi(_count - 200, 100)
			_spawn()
		KEY_R:
			_seed += 1
			_spawn()


func _spawn() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = _seed
	var size := get_viewport_rect().size
	_positions.resize(_count)
	_velocities.resize(_count)
	for i in _count:
		_positions[i] = Vector2(rng.randf() * size.x, rng.randf() * size.y)
		_velocities[i] = Vector2.from_angle(rng.randf() * TAU) * MIN_SPEED


func _process(delta: float) -> void:
	var start := Time.get_ticks_usec()
	if _use_grid:
		_build_grid()
	var new_velocities := _velocities.duplicate()
	for i in _count:
		var neighbors := _neighbors_grid(i) if _use_grid else _neighbors_brute_force(i)
		var steer := _steer(i, neighbors) + _avoid_edges(_positions[i])
		var v := _velocities[i] + steer.limit_length(MAX_FORCE) * delta
		new_velocities[i] = v.normalized() * clampf(v.length(), MIN_SPEED, MAX_SPEED)
	# 全員の新しい速度を計算してから、まとめて動かす（計算の順番で結果が変わらないように）。
	_velocities = new_velocities
	for i in _count:
		_positions[i] += _velocities[i] * delta
	# 時間を平滑化して表示する。
	_step_msec = lerpf(_step_msec, (Time.get_ticks_usec() - start) / 1000.0, 0.1)
	_info.text = (
		"個体 %d　近傍探索: %s　1 ステップ %.1f ms\n[G] 格子／総当たり　[上下キー] 個体数　[R] 再配置"
		% [_count, "格子" if _use_grid else "総当たり", _step_msec]
	)
	queue_redraw()


## 各個体を、VIEW_RADIUS 四方のマスに振り分ける。
func _build_grid() -> void:
	_grid.clear()
	for i in _count:
		var cell := Vector2i((_positions[i] / VIEW_RADIUS).floor())
		var members: PackedInt32Array = _grid.get(cell, PackedInt32Array())
		members.append(i)
		_grid[cell] = members


## 格子による近傍探索: 自分のマスと周りの 8 マスだけを調べる。
func _neighbors_grid(i: int) -> PackedInt32Array:
	var result := PackedInt32Array()
	var cell := Vector2i((_positions[i] / VIEW_RADIUS).floor())
	for dy in range(-1, 2):
		for dx in range(-1, 2):
			for j in _grid.get(cell + Vector2i(dx, dy), PackedInt32Array()):
				if (
					j != i
					and _positions[i].distance_squared_to(_positions[j]) < VIEW_RADIUS * VIEW_RADIUS
				):
					result.append(j)
	return result


## 比較用: 全個体との距離を調べる。個体数の 2 乗に比例して時間がかかる。
func _neighbors_brute_force(i: int) -> PackedInt32Array:
	var result := PackedInt32Array()
	for j in _count:
		if j != i and _positions[i].distance_squared_to(_positions[j]) < VIEW_RADIUS * VIEW_RADIUS:
			result.append(j)
	return result


## 分離・整列・結合の 3 つの力を合わせる。
func _steer(i: int, neighbors: PackedInt32Array) -> Vector2:
	if neighbors.is_empty():
		return Vector2.ZERO
	var separation := Vector2.ZERO
	var average_velocity := Vector2.ZERO
	var center := Vector2.ZERO
	for j in neighbors:
		var offset := _positions[i] - _positions[j]
		var d := offset.length()
		if d < SEPARATION_RADIUS and d > 0.0:
			separation += offset / (d * d) * SEPARATION_RADIUS  # 近いほど強く離れる
		average_velocity += _velocities[j]
		center += _positions[j]
	average_velocity /= neighbors.size()
	center /= neighbors.size()
	# 「望む速度 − 今の速度」を操舵の力とする（Reynolds の操舵行動）。
	var alignment := average_velocity.normalized() * MAX_SPEED - _velocities[i]
	var cohesion := (center - _positions[i]).normalized() * MAX_SPEED - _velocities[i]
	var separation_force := (
		separation.normalized() * MAX_SPEED - _velocities[i]
		if separation != Vector2.ZERO
		else Vector2.ZERO
	)
	return (
		separation_force * SEPARATION_WEIGHT
		+ alignment * ALIGNMENT_WEIGHT
		+ cohesion * COHESION_WEIGHT
	)


## 画面の端に近づいたら内側へ向ける。
func _avoid_edges(p: Vector2) -> Vector2:
	var size := get_viewport_rect().size
	var force := Vector2.ZERO
	if p.x < EDGE_MARGIN:
		force.x += 1.0
	elif p.x > size.x - EDGE_MARGIN:
		force.x -= 1.0
	if p.y < EDGE_MARGIN:
		force.y += 1.0
	elif p.y > size.y - EDGE_MARGIN:
		force.y -= 1.0
	return force * MAX_FORCE * 2.0


func _draw() -> void:
	draw_rect(get_viewport_rect(), Color(0.08, 0.1, 0.16))
	for i in _count:
		var forward := _velocities[i].normalized()
		var side := forward.orthogonal() * 4.0
		var p := _positions[i]
		var color := Color.from_hsv(fposmod(forward.angle() / TAU, 1.0), 0.55, 0.95)
		draw_colored_polygon(
			PackedVector2Array(
				[p + forward * 9.0, p - forward * 5.0 + side, p - forward * 5.0 - side]
			),
			color
		)
