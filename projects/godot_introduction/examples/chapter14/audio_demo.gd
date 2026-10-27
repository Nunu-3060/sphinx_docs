extends Control
## 効果音と BGM を鳴らし、オーディオバスごとに音量を変えるサンプル。

@onready var _bgm_player: AudioStreamPlayer = $BGMPlayer
@onready var _se_player: AudioStreamPlayer = $SEPlayer


func _ready() -> void:
	%JumpButton.pressed.connect(_play_se.bind(preload("res://assets/jump.wav")))
	%CoinButton.pressed.connect(_play_se.bind(preload("res://assets/coin.wav")))
	%HitButton.pressed.connect(_play_se.bind(preload("res://assets/hit.wav")))
	%BGMButton.toggled.connect(_on_bgm_toggled)
	%BGMVolume.value_changed.connect(_set_bus_volume.bind("BGM"))
	%SEVolume.value_changed.connect(_set_bus_volume.bind("SE"))
	# BGM の素材はループしない設定で読み込まれるので、再生が終わったら最初から流し直す。
	_bgm_player.finished.connect(_bgm_player.play)


func _play_se(stream: AudioStream) -> void:
	_se_player.stream = stream
	_se_player.play()


func _on_bgm_toggled(enabled: bool) -> void:
	if enabled:
		_bgm_player.play()
	else:
		_bgm_player.stop()


## スライダーの値（0 から 1 の割合）をデシベルに変換してバスの音量に設定する。
func _set_bus_volume(ratio: float, bus_name: String) -> void:
	var bus_index := AudioServer.get_bus_index(bus_name)
	AudioServer.set_bus_volume_db(bus_index, linear_to_db(ratio))
	AudioServer.set_bus_mute(bus_index, ratio <= 0.0)
