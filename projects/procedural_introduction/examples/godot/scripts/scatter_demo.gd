extends Node3D
## 地形の上に木と岩を散布し、MultiMesh で描く（第 10 章に対応）。
## R: 新しいシード　U: ポアソンディスクと一様乱数の切り替え
## M: MultiMesh と個別の MeshInstance3D の切り替え（描画命令の数を比べる）

const TerrainGenerator := preload("res://scripts/terrain_generator.gd")
const Scatterer := preload("res://scripts/scatterer.gd")
const MeshBuilder := preload("res://scripts/mesh_builder.gd")

const CHUNKS := 2  ## 1 辺に並べるチャンクの数

var _seed := 3
var _use_poisson := true
var _use_multimesh := true
var _material := MeshBuilder.vertex_color_material()
var _tree_mesh := Scatterer.tree_mesh()
var _rock_mesh := Scatterer.rock_mesh()
var _content := Node3D.new()
var _status := ""
var _angle := 0.0

@onready var _camera: Camera3D = $Camera3D
@onready var _info: Label = %Info


func _ready() -> void:
	add_child(_content)
	var size := TerrainGenerator.CHUNK_SIZE * CHUNKS
	var water := TerrainGenerator.create_water(size)
	water.position = Vector3(size * 0.5, TerrainGenerator.WATER_LEVEL, size * 0.5)
	add_child(water)
	_generate()


func _process(delta: float) -> void:
	_angle += 0.12 * delta
	var center := Vector3(1.0, 0.0, 1.0) * TerrainGenerator.CHUNK_SIZE * CHUNKS * 0.5
	var offset := Vector3(cos(_angle), 0.0, sin(_angle)) * 75.0 + Vector3(0.0, 55.0, 0.0)
	_camera.look_at_from_position(center + offset, center + Vector3(0.0, 8.0, 0.0))
	var draw_calls := Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)
	_info.text = _status + "\n描画命令（draw call）: %d" % draw_calls


func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed):
		return
	match (event as InputEventKey).keycode:
		KEY_R:
			_seed += 1
		KEY_U:
			_use_poisson = not _use_poisson
		KEY_M:
			_use_multimesh = not _use_multimesh
		_:
			return
	_generate()


func _generate() -> void:
	for child in _content.get_children():
		child.queue_free()
	var generator := TerrainGenerator.new(_seed)
	for cz in CHUNKS:
		for cx in CHUNKS:
			var chunk := MeshInstance3D.new()
			chunk.mesh = TerrainGenerator.build_mesh(generator.generate_arrays(cx, cz))
			chunk.material_override = _material
			chunk.position = Vector3(cx, 0, cz) * TerrainGenerator.CHUNK_SIZE
			_content.add_child(chunk)

	# 同じシードからは同じ配置になるように、散布専用の乱数をシードで初期化する。
	var rng := RandomNumberGenerator.new()
	rng.seed = _seed
	var start := Time.get_ticks_usec()
	var size := TerrainGenerator.CHUNK_SIZE * CHUNKS
	var result := Scatterer.scatter(generator, Vector2.ZERO, size, rng, _use_poisson)
	var scatter_msec := (Time.get_ticks_usec() - start) / 1000.0
	if _use_multimesh:
		_add_multimesh(_tree_mesh, result.tree_transforms, result.tree_colors)
		_add_multimesh(_rock_mesh, result.rock_transforms, result.rock_colors)
	else:
		_add_individual(_tree_mesh, result.tree_transforms, result.tree_colors)
		_add_individual(_rock_mesh, result.rock_transforms, result.rock_colors)
	_status = (
		"シード %d　木 %d 本・岩 %d 個（散布 %.0f ms）\n[U] 配置: %s　[M] 描画: %s　[R] 再生成"
		% [
			_seed,
			result.tree_transforms.size(),
			result.rock_transforms.size(),
			scatter_msec,
			"ポアソンディスク" if _use_poisson else "一様乱数",
			"MultiMesh" if _use_multimesh else "個別の MeshInstance3D"
		]
	)


## まとめて描く: 種類ごとに MultiMeshInstance3D を 1 つだけ作る。
func _add_multimesh(mesh: Mesh, transforms: Array[Transform3D], colors: PackedColorArray) -> void:
	var instance := MultiMeshInstance3D.new()
	instance.multimesh = Scatterer.create_multimesh(mesh, transforms, colors)
	instance.material_override = _material
	_content.add_child(instance)


## 比較用: 個体ごとにノードと材質を作る。個体の数だけ描画命令が増える。
func _add_individual(mesh: Mesh, transforms: Array[Transform3D], colors: PackedColorArray) -> void:
	for i in transforms.size():
		var material := MeshBuilder.vertex_color_material()
		material.albedo_color = colors[i]  # 頂点の色に掛けられる
		var instance := MeshInstance3D.new()
		instance.mesh = mesh
		instance.material_override = material
		instance.transform = transforms[i]
		_content.add_child(instance)
