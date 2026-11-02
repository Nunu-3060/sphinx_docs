extends RefCounted
## ポアソンディスク・サンプリング（Bridson の方法）。第 10 章に対応する。
##
## どの 2 点も radius 以上離れ、かつ隙間なく点を並べる。
## 半径 radius / √2 の格子を使い、近くの点だけを調べて距離を確かめる。


## width × height の長方形に点を並べる。k は 1 つの点の周りで候補を試す回数。
static func sample(
	width: float, height: float, radius: float, rng: RandomNumberGenerator, k := 30
) -> PackedVector2Array:
	# 格子の 1 マスの対角線が radius になるので、1 マスには点が高々 1 個しか入らない。
	var cell := radius / sqrt(2.0)
	var cols := ceili(width / cell)
	var rows := ceili(height / cell)
	var grid := PackedInt32Array()
	grid.resize(cols * rows)
	grid.fill(-1)  # -1 は「点が無い」

	var points := PackedVector2Array()
	var active: Array[int] = []  # まだ周りに点を置けるかもしれない点の番号
	var first := Vector2(rng.randf() * width, rng.randf() * height)
	points.append(first)
	active.append(0)
	grid[int(first.y / cell) * cols + int(first.x / cell)] = 0

	while not active.is_empty():
		var a := rng.randi_range(0, active.size() - 1)
		var center := points[active[a]]
		var found := false
		for _try in k:
			# 中心から radius〜2 radius の円環の中に候補を作る。
			var candidate := (
				center + Vector2.from_angle(rng.randf() * TAU) * radius * (1.0 + rng.randf())
			)
			if (
				candidate.x < 0.0
				or candidate.y < 0.0
				or candidate.x >= width
				or candidate.y >= height
			):
				continue
			var gx := int(candidate.x / cell)
			var gy := int(candidate.y / cell)
			if _is_far_enough(candidate, gx, gy, points, grid, cols, rows, radius):
				grid[gy * cols + gx] = points.size()
				active.append(points.size())
				points.append(candidate)
				found = true
				break
		if not found:
			# k 回試して置けなければ、この点の周りは埋まったとみなす。
			active[a] = active[active.size() - 1]
			active.pop_back()
	return points


## 候補の周り 5 × 5 マスにある点が、すべて radius 以上離れているか。
static func _is_far_enough(
	p: Vector2,
	gx: int,
	gy: int,
	points: PackedVector2Array,
	grid: PackedInt32Array,
	cols: int,
	rows: int,
	radius: float
) -> bool:
	for y in range(maxi(gy - 2, 0), mini(gy + 3, rows)):
		for x in range(maxi(gx - 2, 0), mini(gx + 3, cols)):
			var index := grid[y * cols + x]
			if index >= 0 and points[index].distance_squared_to(p) < radius * radius:
				return false
	return true


## 比較用: 一様乱数で count 個の点を置く。点どうしが近づいたり重なったりする。
static func uniform(
	width: float, height: float, count: int, rng: RandomNumberGenerator
) -> PackedVector2Array:
	var points := PackedVector2Array()
	for i in count:
		points.append(Vector2(rng.randf() * width, rng.randf() * height))
	return points
