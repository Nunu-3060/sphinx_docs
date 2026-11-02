extends Node3D
## 格子・円柱・回転体のメッシュを実行時に作って並べる（第 6 章に対応）。
## W キーでワイヤーフレーム表示を切り替える。

const MeshBuilder := preload("res://scripts/mesh_builder.gd")

var _shapes: Array[MeshInstance3D] = []

@onready var _info: Label = %Info


func _ready() -> void:
	var material := MeshBuilder.vertex_color_material()
	# 格子: 高さを波の式で、色を高さで決める。
	var ripple := func(x: float, z: float) -> float: return 0.25 * sin(2.5 * x) * cos(2.0 * z)
	var height_color := func(y: float) -> Color:
		return Color(0.2, 0.45, 0.9).lerp(Color(0.95, 0.95, 1.0), y * 2.0 + 0.5)
	var meshes: Array[Mesh] = [
		MeshBuilder.grid(2.6, 24, ripple, height_color),
		MeshBuilder.cylinder(0.8, 2.0, 12, Color(0.9, 0.55, 0.3)),
		MeshBuilder.lathe(_vase_profile(24), 32, _gradient(25)),
	]
	for i in meshes.size():
		var shape := MeshInstance3D.new()
		shape.mesh = meshes[i]
		shape.material_override = material
		shape.position = Vector3((i - 1) * 3.4, 0.0 if i == 0 else -1.0, 0.0)
		add_child(shape)
		_shapes.append(shape)
	_info.text = (
		"左から 格子・円柱・回転体　W: ワイヤーフレーム\n頂点数: %d, %d, %d"
		% [_vertex_count(meshes[0]), _vertex_count(meshes[1]), _vertex_count(meshes[2])]
	)


func _process(delta: float) -> void:
	for shape in _shapes:
		shape.rotate_y(0.4 * delta)


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_W:
		var viewport := get_viewport()
		var wireframe := viewport.debug_draw == Viewport.DEBUG_DRAW_WIREFRAME
		viewport.debug_draw = (
			Viewport.DEBUG_DRAW_DISABLED if wireframe else Viewport.DEBUG_DRAW_WIREFRAME
		)


## 回転体の断面の輪郭（壺の形）を、式から count + 1 個の点 (半径, 高さ) で作る。
func _vase_profile(count: int) -> PackedVector2Array:
	var profile: PackedVector2Array = [Vector2(0.0, 0.0)]  # 底の中心
	for k in count:
		var t := float(k) / (count - 1)  # 0（底）〜 1（口）
		var body := sin(PI * minf(t / 0.8, 1.0))  # 胴のふくらみ
		var lip := smoothstep(0.85, 1.0, t)  # 口の広がり
		profile.append(Vector2(0.35 + 0.65 * body + 0.3 * lip, 2.6 * t))
	return profile


## 輪郭の点の数だけ、下から上へ変わる色を作る。
func _gradient(count: int) -> PackedColorArray:
	var colors := PackedColorArray()
	for k in count:
		colors.append(Color(0.35, 0.2, 0.55).lerp(Color(0.95, 0.75, 0.4), float(k) / (count - 1)))
	return colors


func _vertex_count(mesh: Mesh) -> int:
	var arrays := mesh.surface_get_arrays(0)
	return (arrays[Mesh.ARRAY_VERTEX] as PackedVector3Array).size()
