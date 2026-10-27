extends CharacterBody2D
## 横スクロールアクションの基本的なプレイヤー操作。
## 左右移動、重力、ジャンプを行い、ぶつかった木箱を押す。

const SPEED: float = 300.0  # 左右の移動速度 [ピクセル/秒]
const JUMP_VELOCITY: float = -500.0  # ジャンプの初速。画面の上方向は Y がマイナス
const PUSH_FORCE: float = 40.0  # 木箱を押す強さ

# プロジェクト設定の重力（既定値は 980 ピクセル/秒²）を使う。
var gravity: float = ProjectSettings.get_setting("physics/2d/default_gravity")


func _physics_process(delta: float) -> void:
	# 空中にいる間は重力で下向きに加速する。
	if not is_on_floor():
		velocity.y += gravity * delta

	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	var direction := Input.get_axis("move_left", "move_right")
	velocity.x = direction * SPEED

	# velocity に従って移動し、壁や床に当たったら沿うように滑らせる。
	move_and_slide()
	_push_rigid_bodies()


## 移動中にぶつかった RigidBody2D に力を加えて押す。
func _push_rigid_bodies() -> void:
	for i in get_slide_collision_count():
		var collision := get_slide_collision(i)
		var body := collision.get_collider() as RigidBody2D
		if body != null:
			body.apply_central_impulse(-collision.get_normal() * PUSH_FORCE)
