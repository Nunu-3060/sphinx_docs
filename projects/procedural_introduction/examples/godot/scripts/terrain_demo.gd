extends Node3D
## 3 × 3 個のチャンクから成る地形を作り、周りを回りながら見る（第 7 章に対応）。
## R キーで新しいシードの地形を作る。

const TerrainGenerator := preload("res://scripts/terrain_generator.gd")
const MeshBuilder := preload("res://scripts/mesh_builder.gd")

const CHUNKS := 3  ## 1 辺に並べるチャンクの数

var _seed := 1
var _material := MeshBuilder.vertex_color_material()
var _terrain := Node3D.new()
var _angle := 0.0

@onready var _camera: Camera3D = $Camera3D
@onready var _info: Label = %Info


func _ready() -> void:
	add_child(_terrain)
	var size := TerrainGenerator.CHUNK_SIZE * CHUNKS
	var water := TerrainGenerator.create_water(size)
	water.position = Vector3(size * 0.5, TerrainGenerator.WATER_LEVEL, size * 0.5)
	add_child(water)
	_generate()


func _process(delta: float) -> void:
	# 地形の中心の周りを回る。
	_angle += 0.15 * delta
	var center := Vector3(1.0, 0.0, 1.0) * TerrainGenerator.CHUNK_SIZE * CHUNKS * 0.5
	var offset := Vector3(cos(_angle), 0.0, sin(_angle)) * 190.0 + Vector3(0.0, 140.0, 0.0)
	_camera.look_at_from_position(center + offset, center)


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_R:
		_seed += 1
		_generate()


## チャンクを 1 つずつ作り、かかった時間を計る。
func _generate() -> void:
	for child in _terrain.get_children():
		child.queue_free()
	var generator := TerrainGenerator.new(_seed)
	var start := Time.get_ticks_usec()
	for cz in CHUNKS:
		for cx in CHUNKS:
			var chunk := MeshInstance3D.new()
			chunk.mesh = TerrainGenerator.build_mesh(generator.generate_arrays(cx, cz))
			chunk.material_override = _material
			chunk.position = Vector3(cx, 0, cz) * TerrainGenerator.CHUNK_SIZE
			_terrain.add_child(chunk)
	var msec := (Time.get_ticks_usec() - start) / 1000.0
	var count := CHUNKS * CHUNKS
	_info.text = (
		"シード %d　R: 再生成\nチャンク %d 個（%d × %d マス）の生成: %.0f ms（1 個あたり %.1f ms）"
		% [
			_seed,
			count,
			TerrainGenerator.RESOLUTION,
			TerrainGenerator.RESOLUTION,
			msec,
			msec / count
		]
	)
