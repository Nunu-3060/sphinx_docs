extends Node2D
## 手続き的に歩く生き物（第 12 章に対応）。上から見た 4 本足のトカゲ。
##
## 胴は頭を追いかける点の列、脚は FABRIK で解く関節の列、尾はばねでつないだ点の列で表す。
## アニメーションのデータは持たず、足を置く位置の規則だけで歩き方が決まる。
## マウスの左ボタンを押している間はマウスを追う。D: 補助線の表示を切り替える

const Fabrik := preload("res://scripts/fabrik.gd")

const SPEED := 200.0  ## 頭の速さ [px/s]
const TURN_RATE := 2.5  ## 向きを変える速さの上限 [rad/s]
const SPINE_SPACING := 30.0  ## 胴の点の間隔 [px]
const BODY_RADII: Array[float] = [22.0, 28.0, 31.0, 29.0, 25.0, 20.0]  ## 胴の各点の太さ [px]
const TAIL_COUNT := 14  ## 尾の点の数
const TAIL_SPACING := 18.0  ## 尾の点の間隔 [px]
const TAIL_STIFFNESS := 900.0  ## 尾をまっすぐに戻すばねの強さ
const TAIL_DAMPING := 0.85  ## 尾の速度の減衰（1 フレームあたりに残る割合）
const LEG_LENGTHS: PackedFloat32Array = [42.0, 40.0, 20.0]  ## 脚の各区間の長さ [px]
const STEP_DISTANCE := 48.0  ## 足が休みの位置からこれだけ離れたら踏み出す [px]
const STEP_TIME := 0.16  ## 1 歩にかける時間 [s]

var _heading := 0.0
var _spine := PackedVector2Array()
var _tail := PackedVector2Array()
var _tail_previous := PackedVector2Array()  ## 1 フレーム前の尾の位置（速度の計算用）
var _legs: Array[Leg] = []
var _time := 0.0
var _show_guides := true


## 脚 1 本の状態。
class Leg:
	var spine_index: int  ## 付け根の胴の点の番号
	var side: float  ## -1 なら左、1 なら右
	var reach: Vector2  ## 休みの位置（前方向・横方向の距離）
	var group: int  ## 対角の脚どうしを同じ組にする（0 か 1）
	var foot := Vector2()  ## 足先の位置
	var rest := Vector2()  ## 足を置きたい位置（体に対して決まる）
	var step_from := Vector2()
	var step_to := Vector2()
	var step_t := 1.0  ## 踏み出しの進み具合。1 以上なら接地している
	var joints := PackedVector2Array()

	func _init(index: int, side_sign: float, reach_offset: Vector2, group_id: int) -> void:
		spine_index = index
		side = side_sign
		reach = reach_offset
		group = group_id

	func is_stepping() -> bool:
		return step_t < 1.0


func _ready() -> void:
	var start := get_viewport_rect().size * 0.5
	for i in BODY_RADII.size():
		_spine.append(start - Vector2(i * SPINE_SPACING, 0.0))
	for i in TAIL_COUNT:
		_tail.append(_spine[-1] - Vector2((i + 1) * TAIL_SPACING, 0.0))
	_tail_previous = _tail.duplicate()
	# 前脚は胴の 1 番目、後ろ脚は 4 番目の点に付ける。左前と右後ろ、右前と左後ろを組にする。
	_legs = [
		Leg.new(1, -1.0, Vector2(36.0, 72.0), 0),
		Leg.new(1, 1.0, Vector2(36.0, 72.0), 1),
		Leg.new(4, -1.0, Vector2(6.0, 70.0), 1),
		Leg.new(4, 1.0, Vector2(6.0, 70.0), 0),
	]
	for leg in _legs:
		_update_rest(leg)
		leg.foot = leg.rest


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_D:
		_show_guides = not _show_guides


func _process(delta: float) -> void:
	_time += delta
	_move_head(delta)
	_follow_spine()
	_update_tail(delta)
	for leg in _legs:
		_update_leg(leg, delta)
	queue_redraw()


## 頭を目標に向けて進める。向きを変える速さに上限を設け、急に曲がらないようにする。
func _move_head(delta: float) -> void:
	var target: Vector2
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		target = get_global_mouse_position()
	else:
		# リサジュー曲線の上を動く点を追いかけ、画面の中を歩き回る。
		var size := get_viewport_rect().size
		target = (
			size * 0.5
			+ Vector2(sin(0.23 * _time) * size.x * 0.36, sin(0.37 * _time + 1.0) * size.y * 0.33)
		)
	var wanted := (target - _spine[0]).angle()
	_heading += clampf(angle_difference(_heading, wanted), -TURN_RATE * delta, TURN_RATE * delta)
	if _spine[0].distance_to(target) > 10.0:
		_spine[0] += Vector2.from_angle(_heading) * SPEED * delta


## 胴の各点は、1 つ前の点から一定の距離を保つように引っ張られる（鎖のように頭に従う）。
func _follow_spine() -> void:
	for i in range(1, _spine.size()):
		_spine[i] = _spine[i - 1] + _spine[i - 1].direction_to(_spine[i]) * SPINE_SPACING


## 尾: 各点を、まっすぐ伸びた位置へばねで引き、速度を減衰させる（ベルレ積分）。
func _update_tail(delta: float) -> void:
	var previous := _spine[-1]
	var direction := _spine[-2].direction_to(_spine[-1])
	for i in TAIL_COUNT:
		var velocity := (_tail[i] - _tail_previous[i]) * TAIL_DAMPING
		_tail_previous[i] = _tail[i]
		var straight := previous + direction * TAIL_SPACING  # 尾がまっすぐなら来る位置
		var p := _tail[i] + velocity + (straight - _tail[i]) * TAIL_STIFFNESS * delta * delta
		# 長さを一定に保つ（距離の拘束）。
		p = previous + previous.direction_to(p) * TAIL_SPACING
		direction = previous.direction_to(p)
		_tail[i] = p
		previous = p


## 体の向きに対して、足を置きたい位置を決める。
func _update_rest(leg: Leg) -> void:
	var forward := _body_direction(leg.spine_index)
	var outward := forward.orthogonal() * -leg.side  # 体の外側
	leg.rest = _spine[leg.spine_index] + forward * leg.reach.x + outward * leg.reach.y


func _update_leg(leg: Leg, delta: float) -> void:
	_update_rest(leg)
	if leg.is_stepping():
		leg.step_t = minf(leg.step_t + delta / STEP_TIME, 1.0)
		leg.foot = leg.step_from.lerp(leg.step_to, smoothstep(0.0, 1.0, leg.step_t))
	elif leg.foot.distance_to(leg.rest) > STEP_DISTANCE and not _other_group_stepping(leg.group):
		# 踏み出す。体の進みを見越して、休みの位置より少し前に足を置く。
		leg.step_from = leg.foot
		leg.step_to = leg.rest + _body_direction(leg.spine_index) * STEP_DISTANCE * 0.5
		leg.step_t = 0.0
	# 付け根から足先までの関節を FABRIK で解く。初期値の膝を外側に置き、曲がる向きをそろえる。
	var hip := _spine[leg.spine_index]
	var outward := _body_direction(leg.spine_index).orthogonal() * -leg.side
	var joints: PackedVector2Array = [
		hip,
		hip.lerp(leg.foot, 0.4) + outward * 28.0,
		hip.lerp(leg.foot, 0.8) + outward * 8.0,
		leg.foot
	]
	leg.joints = Fabrik.solve(joints, LEG_LENGTHS, leg.foot)


## 反対の組の脚が踏み出している最中か。対角の脚を交互に動かすために使う。
func _other_group_stepping(group: int) -> bool:
	for leg in _legs:
		if leg.group != group and leg.is_stepping():
			return true
	return false


## 胴の i 番目の点での前向きの方向。
func _body_direction(i: int) -> Vector2:
	if i == 0:
		return Vector2.from_angle(_heading)
	return _spine[i].direction_to(_spine[i - 1])


func _draw() -> void:
	draw_rect(get_viewport_rect(), Color(0.2, 0.24, 0.2))
	# 地面の目印の点（足が地面に止まっていることが分かるように）
	var size := get_viewport_rect().size
	for y in range(32, int(size.y), 64):
		for x in range(32, int(size.x), 64):
			draw_circle(Vector2(x, y), 2.0, Color(0.32, 0.37, 0.3))
	var skin := Color(0.45, 0.68, 0.38)
	var dark := Color(0.28, 0.45, 0.25)
	# 尾（根元から先へ細くする）
	var tail_points := PackedVector2Array([_spine[-1]]) + _tail
	for i in range(tail_points.size() - 1):
		var width := lerpf(BODY_RADII[-1] * 1.6, 2.0, float(i) / TAIL_COUNT)
		draw_line(tail_points[i], tail_points[i + 1], skin, width)
		draw_circle(tail_points[i + 1], width * 0.5, skin)
	# 脚
	for leg in _legs:
		if leg.joints.size() < 2:
			continue  # まだ一度も解いていない
		draw_polyline(leg.joints, dark, 10.0)
		for joint in leg.joints:
			draw_circle(joint, 6.0, dark)
		# 踏み出している間は、足を持ち上げたように大きく描く。
		var lift := sin(PI * leg.step_t) if leg.is_stepping() else 0.0
		draw_circle(leg.foot, 10.0 * (1.0 + 0.6 * lift), skin.darkened(0.2))
	# 胴と頭
	for i in range(_spine.size() - 1, -1, -1):
		draw_circle(_spine[i], BODY_RADII[i], skin)
	var forward := Vector2.from_angle(_heading)
	for side: float in [-1.0, 1.0]:
		draw_circle(
			_spine[0] + forward * 11.0 + forward.orthogonal() * side * 12.0,
			5.0,
			Color(0.1, 0.1, 0.1)
		)
	if _show_guides:
		# 補助線: 足を置きたい位置（×）と、体の中心線
		draw_polyline(_spine, Color(1, 1, 1, 0.4), 1.5)
		for leg in _legs:
			var c := Color(1.0, 0.85, 0.3, 0.9)
			draw_line(leg.rest - Vector2(5, 5), leg.rest + Vector2(5, 5), c, 2.0)
			draw_line(leg.rest - Vector2(5, -5), leg.rest + Vector2(5, -5), c, 2.0)
