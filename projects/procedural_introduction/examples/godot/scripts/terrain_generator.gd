extends RefCounted
## ノイズから地形のチャンクを作る（第 7 章に対応）。
##
## 世界を CHUNK_SIZE 四方の区画（チャンク）に分け、チャンクごとにメッシュを作る。
## 高さは世界座標の関数なので、どのチャンクをどの順番で作っても境目がつながる。
## generate_arrays() はノードやシーンに触れないので、ワーカースレッドから呼べる。

const CHUNK_SIZE := 64.0  ## チャンクの 1 辺の長さ [m]
const RESOLUTION := 64  ## チャンクの 1 辺のマスの数
const HEIGHT_SCALE := 40.0  ## 高さの尺度 [m]（整えたノイズの値が 1 のときの高さ）
const WATER_LEVEL := 5.0  ## 水面の高さ [m]
const SNOW_LEVEL := 26.0  ## これより高い所を雪にする [m]

var world_seed: int
var _height_noise := FastNoiseLite.new()
var _moisture_noise := FastNoiseLite.new()


func _init(seed_value: int) -> void:
	world_seed = seed_value
	# 高さ: 5 オクターブの fBm（第 3 章）
	_height_noise.seed = seed_value
	_height_noise.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	_height_noise.frequency = 0.007
	_height_noise.fractal_type = FastNoiseLite.FRACTAL_FBM
	_height_noise.fractal_octaves = 5
	_height_noise.fractal_lacunarity = 2.0
	_height_noise.fractal_gain = 0.5
	# 湿り気: 高さとは別のシードの、より滑らかなノイズ。植生の分布に使う。
	_moisture_noise.seed = seed_value + 1
	_moisture_noise.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	_moisture_noise.frequency = 0.003
	_moisture_noise.fractal_octaves = 3


## 世界座標 (x, z) の地面の高さ。
func height_at(x: float, z: float) -> float:
	var n := maxf(_height_noise.get_noise_2d(x, z) * 0.9 + 0.5, 0.0)
	# 累乗で値を再分配し、低い所を平らに、高い所を険しくする。
	return HEIGHT_SCALE * pow(n, 2.2)


## 世界座標 (x, z) の湿り気（0〜1）。
func moisture_at(x: float, z: float) -> float:
	return clampf(_moisture_noise.get_noise_2d(x, z) * 0.8 + 0.5, 0.0, 1.0)


## 世界座標 (x, z) の地面の法線。高さの中心差分から求める。
func normal_at(x: float, z: float, step := 1.0) -> Vector3:
	var dx := height_at(x - step, z) - height_at(x + step, z)
	var dz := height_at(x, z - step) - height_at(x, z + step)
	return Vector3(dx, 2.0 * step, dz).normalized()


## 高さ・湿り気・傾き（法線の y 成分）から地面の色を決める。
func ground_color(height: float, moisture: float, normal_y: float) -> Color:
	if height < WATER_LEVEL + 0.8:
		return Color(0.76, 0.7, 0.5)  # 砂浜と水の底
	if normal_y < 0.75:
		return Color(0.45, 0.42, 0.4)  # 急な斜面は岩
	if height > SNOW_LEVEL:
		return Color(0.95, 0.96, 1.0)  # 雪
	# 草地: 乾いた所は黄緑、湿った所は濃い緑。高い所ほど岩の色に近づける。
	var grass := Color(0.62, 0.66, 0.3).lerp(Color(0.2, 0.45, 0.18), moisture)
	return grass.lerp(Color(0.5, 0.47, 0.42), smoothstep(SNOW_LEVEL - 8.0, SNOW_LEVEL, height))


## チャンク (cx, cz) のメッシュの配列（頂点・法線・色・インデックス）を作る。
## 頂点の座標はチャンクの左奥の角を原点とする。
func generate_arrays(cx: int, cz: int) -> Array:
	var n := RESOLUTION + 1  # 1 辺の頂点の数
	var step := CHUNK_SIZE / RESOLUTION
	var x0 := cx * CHUNK_SIZE
	var z0 := cz * CHUNK_SIZE
	# ハイトマップ。法線の計算のため、周囲に 1 列ずつ余分に取る（隣のチャンクと法線がそろう）。
	var w := n + 2
	var heights := PackedFloat32Array()
	heights.resize(w * w)
	for j in w:
		for i in w:
			heights[j * w + i] = height_at(x0 + (i - 1) * step, z0 + (j - 1) * step)

	var vertices := PackedVector3Array()
	var normals := PackedVector3Array()
	var colors := PackedColorArray()
	vertices.resize(n * n)
	normals.resize(n * n)
	colors.resize(n * n)
	for j in n:
		for i in n:
			var k := (j + 1) * w + (i + 1)  # ハイトマップでの位置
			var h := heights[k]
			# 左右・前後の高さの差（中心差分）から法線を作る。
			var normal := (
				Vector3(
					heights[k - 1] - heights[k + 1], 2.0 * step, heights[k - w] - heights[k + w]
				)
				. normalized()
			)
			var v := j * n + i
			vertices[v] = Vector3(i * step, h, j * step)
			normals[v] = normal
			colors[v] = ground_color(h, moisture_at(x0 + i * step, z0 + j * step), normal.y)

	# 1 マスを 2 枚の三角形に分ける（mesh_builder.gd の grid と同じ並べ方）。
	var indices := PackedInt32Array()
	indices.resize(RESOLUTION * RESOLUTION * 6)
	var t := 0
	for j in RESOLUTION:
		for i in RESOLUTION:
			var a := j * n + i
			var c := a + n
			for index: int in [a, a + 1, c, a + 1, c + 1, c]:
				indices[t] = index
				t += 1

	var arrays := []
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX] = vertices
	arrays[Mesh.ARRAY_NORMAL] = normals
	arrays[Mesh.ARRAY_COLOR] = colors
	arrays[Mesh.ARRAY_INDEX] = indices
	return arrays


## 配列から ArrayMesh を作る。メッシュはエンジンのリソースなので、メインスレッドで呼ぶ。
static func build_mesh(arrays: Array) -> ArrayMesh:
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)
	return mesh


## size 四方の半透明の水面を作る。
static func create_water(size: float) -> MeshInstance3D:
	var plane := PlaneMesh.new()
	plane.size = Vector2(size, size)
	var material := StandardMaterial3D.new()
	material.albedo_color = Color(0.15, 0.4, 0.65, 0.75)
	material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	material.roughness = 0.1
	var water := MeshInstance3D.new()
	water.mesh = plane
	water.material_override = material
	return water
