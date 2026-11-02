extends RefCounted
## 1 つのチャンクの生成を表す仕事。
##
## compute() はワーカースレッドで実行し、地形の配列と散布の結果だけを作る。
## ノードやメッシュはメインスレッドで create_node() を呼んで作る。
## 計算とエンジンへの登録を分けると、重い計算の間もゲームが止まらない。

const TerrainGenerator := preload("res://scripts/terrain_generator.gd")
const Scatterer := preload("res://scripts/scatterer.gd")

var coord: Vector2i  ## チャンクの番号 (cx, cz)
var generation: int  ## どのシードの世界のための仕事か
var task_id := -1  ## WorkerThreadPool の仕事の番号
var elapsed_msec := 0.0  ## compute() にかかった時間 [ms]

var _generator: TerrainGenerator
var _terrain_arrays: Array
var _scatter: Scatterer.Result


func _init(chunk_coord: Vector2i, generation_id: int, generator: TerrainGenerator) -> void:
	coord = chunk_coord
	generation = generation_id
	_generator = generator


## ワーカースレッドで実行する部分。
func compute() -> void:
	var start := Time.get_ticks_usec()
	_terrain_arrays = _generator.generate_arrays(coord.x, coord.y)
	# チャンクごとの乱数のシードを、世界のシードとチャンクの番号から決める。
	# こうすると、チャンクを作る順番が変わっても同じ配置になる（第 2 章のハッシュの考え方）。
	var rng := RandomNumberGenerator.new()
	rng.seed = hash([_generator.world_seed, coord.x, coord.y])
	var origin := Vector2(coord) * TerrainGenerator.CHUNK_SIZE
	_scatter = Scatterer.scatter(_generator, origin, TerrainGenerator.CHUNK_SIZE, rng)
	elapsed_msec = (Time.get_ticks_usec() - start) / 1000.0


## メインスレッドで実行する部分。地形と木・岩のノードを作る。
func create_node(material: Material, tree_mesh: Mesh, rock_mesh: Mesh) -> Node3D:
	var chunk := Node3D.new()
	chunk.name = "Chunk_%d_%d" % [coord.x, coord.y]
	chunk.position = Vector3(coord.x, 0, coord.y) * TerrainGenerator.CHUNK_SIZE
	var terrain := MeshInstance3D.new()
	terrain.mesh = TerrainGenerator.build_mesh(_terrain_arrays)
	terrain.material_override = material
	chunk.add_child(terrain)
	# 木と岩は、種類ごとに MultiMeshInstance3D を 1 つずつ作る。
	for item: Array in [
		[tree_mesh, _scatter.tree_transforms, _scatter.tree_colors],
		[rock_mesh, _scatter.rock_transforms, _scatter.rock_colors],
	]:
		var instances := MultiMeshInstance3D.new()
		instances.multimesh = Scatterer.create_multimesh(item[0], item[1], item[2])
		instances.material_override = material
		chunk.add_child(instances)
	return chunk
