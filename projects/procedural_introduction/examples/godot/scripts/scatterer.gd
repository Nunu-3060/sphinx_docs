extends RefCounted
## 地形の上に木と岩を散布する（第 10 章に対応）。
##
## ポアソンディスクで候補の点を作り、高さ・傾き・湿り気の条件で、置く物を選ぶ。
## 個体ごとに大きさ・向き・色を少しずつ変える。
## scatter() はノードを作らないので、ワーカースレッドから呼べる。

const PoissonDisk := preload("res://scripts/poisson_disk.gd")
const MeshBuilder := preload("res://scripts/mesh_builder.gd")
const TerrainGenerator := preload("res://scripts/terrain_generator.gd")

const SPACING := 4.5  ## 木や岩どうしの最小の間隔 [m]


## 散布の結果。種類ごとに、各個体の変換（位置・回転・拡大率）と色を持つ。
class Result:
	var tree_transforms: Array[Transform3D] = []
	var tree_colors := PackedColorArray()
	var rock_transforms: Array[Transform3D] = []
	var rock_colors := PackedColorArray()


## 世界座標 origin = (x, z) から size 四方の範囲に散布する。
## 座標はこの範囲の左奥の角を原点として返す。
## use_poisson が false のときは、比較のため同じ個数の点を一様乱数で置く。
static func scatter(
	generator: TerrainGenerator,
	origin: Vector2,
	size: float,
	rng: RandomNumberGenerator,
	use_poisson := true
) -> Result:
	var points := PoissonDisk.sample(size, size, SPACING, rng)
	if not use_poisson:
		points = PoissonDisk.uniform(size, size, points.size(), rng)
	var result := Result.new()
	for p in points:
		var h := generator.height_at(origin.x + p.x, origin.y + p.y)
		var slope := generator.normal_at(origin.x + p.x, origin.y + p.y).y  # 1 なら平ら
		var moisture := generator.moisture_at(origin.x + p.x, origin.y + p.y)
		var position := Vector3(p.x, h, p.y)
		var r := rng.randf()
		if h < TerrainGenerator.WATER_LEVEL + 1.0 or h > TerrainGenerator.SNOW_LEVEL:
			continue  # 水辺と雪の上には置かない
		if slope < 0.8:
			if r < 0.4:  # 急な斜面には岩だけを置く
				_add_rock(result, position, rng)
		elif r < moisture * 0.9:  # 湿った所ほど木が多い
			_add_tree(result, position, moisture, rng)
		elif r > 0.95:
			_add_rock(result, position, rng)
	return result


static func _add_tree(
	result: Result, position: Vector3, moisture: float, rng: RandomNumberGenerator
) -> void:
	# y 軸周りの向きと大きさを変える。高さだけ別に変えると、形にも個体差が出る。
	var s := rng.randf_range(0.7, 1.4)
	var basis := Basis(Vector3.UP, rng.randf() * TAU).scaled(
		Vector3(s, s * rng.randf_range(0.8, 1.3), s)
	)
	result.tree_transforms.append(Transform3D(basis, position))
	# 色相・彩度・明度を少しずらす。湿った所ほど濃い緑にする。
	var hue := rng.randf_range(0.24, 0.34)
	result.tree_colors.append(
		Color.from_hsv(hue, 0.5 + 0.25 * moisture, rng.randf_range(0.45, 0.7) - 0.15 * moisture)
	)


static func _add_rock(result: Result, position: Vector3, rng: RandomNumberGenerator) -> void:
	# 任意の向きに傾け、軸ごとに違う倍率で伸ばして、同じメッシュを違う形に見せる。
	var axis := Vector3(rng.randf() - 0.5, rng.randf() - 0.5, rng.randf() - 0.5).normalized()
	var scale := Vector3(
		rng.randf_range(0.6, 1.6), rng.randf_range(0.4, 1.0), rng.randf_range(0.6, 1.6)
	)
	var basis := (
		Basis(axis, rng.randf_range(-0.4, 0.4)) * Basis(Vector3.UP, rng.randf() * TAU).scaled(scale)
	)
	result.rock_transforms.append(Transform3D(basis, position))
	var v := rng.randf_range(0.4, 0.65)
	result.rock_colors.append(Color(v, v * 0.97, v * 0.93))


## 木のメッシュ。針葉樹の輪郭を回転させて作る。葉は白にして、個体ごとの色を掛けて使う。
static func tree_mesh() -> ArrayMesh:
	var profile: PackedVector2Array = [
		Vector2(0.25, -0.5),
		Vector2(0.2, 1.0),
		Vector2(1.6, 1.0),
		Vector2(0.7, 2.6),
		Vector2(1.25, 2.6),
		Vector2(0.0, 5.0),
	]
	var brown := Color(0.55, 0.4, 0.3)
	var colors: PackedColorArray = [
		brown, brown, Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE
	]
	return MeshBuilder.lathe(profile, 7, colors)


## 岩のメッシュ。角の多い低い回転体を、個体ごとに伸ばしたり傾けたりして使う。
static func rock_mesh() -> ArrayMesh:
	var profile: PackedVector2Array = [
		Vector2(1.0, -0.5), Vector2(1.1, 0.2), Vector2(0.7, 0.8), Vector2(0.0, 1.0)
	]
	var colors: PackedColorArray = [Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE]
	return MeshBuilder.lathe(profile, 6, colors)


## 同じメッシュの多数の個体を、1 つの MultiMesh にまとめる。
## MultiMesh は全個体を 1 回の描画命令（draw call）で描く。
static func create_multimesh(
	mesh: Mesh, transforms: Array[Transform3D], colors: PackedColorArray
) -> MultiMesh:
	var multimesh := MultiMesh.new()
	multimesh.transform_format = MultiMesh.TRANSFORM_3D
	multimesh.use_colors = true  # 個体ごとの色を使う（instance_count より先に設定する）
	multimesh.mesh = mesh
	multimesh.instance_count = transforms.size()
	for i in transforms.size():
		multimesh.set_instance_transform(i, transforms[i])
		multimesh.set_instance_color(i, colors[i])
	return multimesh
