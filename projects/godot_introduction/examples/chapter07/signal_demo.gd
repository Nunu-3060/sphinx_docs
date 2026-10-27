extends Control
## シグナル、await、enum、ラムダ式の例。

## キャラクターの状態
enum State { ALIVE, DEAD }

const RESPAWN_SECONDS: float = 2.0

var state: State = State.ALIVE

@onready var _health: Health = $Health
@onready var _bar: ProgressBar = %HealthBar
@onready var _status: Label = %StatusLabel


func _ready() -> void:
	# コードでシグナルを接続する。接続先には関数そのもの（Callable）を渡す。
	_health.health_changed.connect(_on_health_changed)
	_health.died.connect(_on_died)
	# 小さな処理はラムダ式（名前のない関数）で書ける。
	%DamageButton.pressed.connect(func() -> void: _health.take_damage(30))
	%HealButton.pressed.connect(func() -> void: _health.heal(20))
	_on_health_changed(_health.max_health, _health.max_health)


func _on_health_changed(current: int, maximum: int) -> void:
	_bar.max_value = maximum
	_bar.value = current
	_status.text = "HP %d / %d" % [current, maximum]


func _on_died() -> void:
	state = State.DEAD
	_status.text = "倒れた。%d 秒後に復活する..." % RESPAWN_SECONDS
	# await はシグナルが発行されるまで、この関数の実行を一時停止する。
	# その間もゲーム全体は止まらない。
	await get_tree().create_timer(RESPAWN_SECONDS).timeout
	state = State.ALIVE
	_health.heal(_health.max_health)
	print("復活した。状態: ", State.keys()[state])
