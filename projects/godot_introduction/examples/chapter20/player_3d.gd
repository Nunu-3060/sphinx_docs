extends CharacterBody3D
## 3D 空間を歩くプレイヤー。2D 版（第 11 章）とほぼ同じ構造で書ける。

const SPEED: float = 5.0  # 移動速度 [メートル/秒]
const JUMP_VELOCITY: float = 4.5  # ジャンプの初速。3D では上方向が Y のプラス

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")


func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= gravity * delta

	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# 2D の入力ベクトル (x, y) を、3D の水平面 (x, z) の移動方向に変換する。
	var input := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	var direction := Vector3(input.x, 0.0, input.y)
	velocity.x = direction.x * SPEED
	velocity.z = direction.z * SPEED

	move_and_slide()
