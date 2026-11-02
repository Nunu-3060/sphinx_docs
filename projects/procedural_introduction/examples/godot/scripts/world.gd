extends Node3D
## 統合例: カメラが飛ぶにつれて、周りのチャンク（地形と木・岩）を別スレッドで生成する。
## R: 新しいシードで世界を作り直す　左右キー: 向きを変える　上下キー: 速さを変える

const TerrainGenerator := preload("res://scripts/terrain_generator.gd")
const Scatterer := preload("res://scripts/scatterer.gd")
const MeshBuilder := preload("res://scripts/mesh_builder.gd")
const ChunkJob := preload("res://scripts/chunk_job.gd")

const VIEW_RADIUS := 3  ## カメラの周り何チャンクまで作るか（7 × 7 個）
const MAX_JOBS := 6  ## 同時に実行する生成の仕事の数の上限
const MAX_UPLOADS_PER_FRAME := 1  ## 1 フレームにシーンへ加えるチャンクの数の上限
const FLY_HEIGHT := 30.0  ## 地面からの高さ [m]

var _seed := 7
var _generation := 0  ## シードを変えるたびに増やす。古い仕事の結果を見分けるのに使う。
var _generator := TerrainGenerator.new(_seed)
var _chunks: Dictionary[Vector2i, Node3D] = {}  ## 作り終えたチャンク
var _jobs: Array[ChunkJob] = []  ## 実行中の仕事
var _requested: Dictionary[Vector2i, bool] = {}  ## 今の世代で生成を頼んだチャンク
var _material := MeshBuilder.vertex_color_material()
var _tree_mesh := Scatterer.tree_mesh()
var _rock_mesh := Scatterer.rock_mesh()
var _heading := 0.6  ## 進む向き [rad]
var _speed := 24.0  ## 進む速さ [m/s]
var _compute_msec: Array[float] = []  ## 最近のチャンクの生成時間（ワーカー）
var _upload_msec: Array[float] = []  ## 最近のチャンクのノード作成時間（メインスレッド）
## カメラについて動く水面
var _water := TerrainGenerator.create_water(TerrainGenerator.CHUNK_SIZE * (VIEW_RADIUS * 2 + 2))

@onready var _camera: Camera3D = $Camera3D
@onready var _info: Label = %Info


func _ready() -> void:
	add_child(_water)
	_camera.position = Vector3(0.0, _generator.height_at(0.0, 0.0) + FLY_HEIGHT, 0.0)


func _process(delta: float) -> void:
	_fly(delta)
	var center := Vector2i(
		(Vector2(_camera.position.x, _camera.position.z) / TerrainGenerator.CHUNK_SIZE).floor()
	)
	_request_chunks(center)
	_collect_finished_jobs()
	_unload_far_chunks(center)
	_water.position = Vector3(_camera.position.x, TerrainGenerator.WATER_LEVEL, _camera.position.z)
	_update_info()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_R:
		_regenerate(_seed + 1)


func _exit_tree() -> void:
	# WorkerThreadPool に渡した仕事は、必ず完了を待ってから終える。
	for job in _jobs:
		WorkerThreadPool.wait_for_task_completion(job.task_id)


## カメラを前に進め、地面の高さに合わせて上下させる。
func _fly(delta: float) -> void:
	_heading += Input.get_axis("ui_left", "ui_right") * 0.8 * delta
	_speed = clampf(_speed + Input.get_axis("ui_down", "ui_up") * 20.0 * delta, 0.0, 80.0)
	var forward := Vector3(sin(_heading), 0.0, -cos(_heading))
	var p := _camera.position + forward * _speed * delta
	# 少し先の地面の高さも見て、山にぶつからないようにする。
	var ahead := p + forward * 40.0
	var ground := maxf(_generator.height_at(p.x, p.z), _generator.height_at(ahead.x, ahead.z))
	var target_y := maxf(ground, TerrainGenerator.WATER_LEVEL) + FLY_HEIGHT
	p.y = lerpf(p.y, target_y, 1.0 - exp(-3.0 * delta))
	_camera.position = p
	_camera.look_at(p + forward * 60.0 + Vector3(0.0, -22.0, 0.0))


## カメラの周りで、まだ無いチャンクの生成を、近い順に WorkerThreadPool に頼む。
func _request_chunks(center: Vector2i) -> void:
	var missing: Array[Vector2i] = []
	for dz in range(-VIEW_RADIUS, VIEW_RADIUS + 1):
		for dx in range(-VIEW_RADIUS, VIEW_RADIUS + 1):
			var coord := center + Vector2i(dx, dz)
			if not _chunks.has(coord) and not _requested.has(coord):
				missing.append(coord)
	missing.sort_custom(
		func(a: Vector2i, b: Vector2i) -> bool:
			return (a - center).length_squared() < (b - center).length_squared()
	)
	for coord in missing:
		if _jobs.size() >= MAX_JOBS:
			break
		var job := ChunkJob.new(coord, _generation, _generator)
		job.task_id = WorkerThreadPool.add_task(job.compute)
		_jobs.append(job)
		_requested[coord] = true


## 終わった仕事を受け取り、メインスレッドでノードを作ってシーンに加える。
func _collect_finished_jobs() -> void:
	var uploads := 0
	for job: ChunkJob in _jobs.duplicate():
		if uploads >= MAX_UPLOADS_PER_FRAME:
			break
		if not WorkerThreadPool.is_task_completed(job.task_id):
			continue
		WorkerThreadPool.wait_for_task_completion(job.task_id)  # 仕事の後始末（すぐ戻る）
		_jobs.erase(job)
		if job.generation != _generation:
			continue  # シードを変える前に頼んだ仕事の結果は捨てる
		var start := Time.get_ticks_usec()
		var chunk := job.create_node(_material, _tree_mesh, _rock_mesh)
		add_child(chunk)
		_record(_upload_msec, (Time.get_ticks_usec() - start) / 1000.0)
		_record(_compute_msec, job.elapsed_msec)
		_chunks[job.coord] = chunk
		uploads += 1


## 見える範囲から外れたチャンクを消す。必要になればまた同じ形で作られる。
func _unload_far_chunks(center: Vector2i) -> void:
	for coord: Vector2i in _chunks.keys():
		var d := (coord - center).abs()
		if maxi(d.x, d.y) > VIEW_RADIUS + 1:
			_chunks[coord].queue_free()
			_chunks.erase(coord)
			_requested.erase(coord)


## 新しいシードで世界を作り直す。実行中の仕事は待たず、終わったときに結果を捨てる。
func _regenerate(seed_value: int) -> void:
	_seed = seed_value
	_generation += 1
	_generator = TerrainGenerator.new(_seed)
	for chunk: Node3D in _chunks.values():
		chunk.queue_free()
	_chunks.clear()
	_requested.clear()


func _record(samples: Array[float], value: float) -> void:
	samples.append(value)
	if samples.size() > 30:
		samples.pop_front()


func _average(samples: Array[float]) -> float:
	if samples.is_empty():
		return 0.0
	var total := 0.0
	for value in samples:
		total += value
	return total / samples.size()


func _update_info() -> void:
	var draw_calls := Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)
	_info.text = "シード %d　[R] 再生成　[左右キー] 向き　[上下キー] 速さ\n" % _seed
	_info.text += "チャンク %d 個（生成中 %d）　描画命令 %d\n" % [_chunks.size(), _jobs.size(), draw_calls]
	_info.text += (
		"1 チャンクの生成 %.1f ms（ワーカー）、ノード作成 %.1f ms（メイン）"
		% [_average(_compute_msec), _average(_upload_msec)]
	)
