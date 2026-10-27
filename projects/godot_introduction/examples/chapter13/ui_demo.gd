extends Control
## 設定画面風の UI。入力欄の値をまとめて、決定ボタンで表示する。

@onready var _name_edit: LineEdit = %NameEdit
@onready var _volume_slider: HSlider = %VolumeSlider
@onready var _volume_label: Label = %VolumeLabel
@onready var _difficulty: OptionButton = %DifficultyOption
@onready var _result: Label = %ResultLabel


func _ready() -> void:
	for difficulty_name: String in ["かんたん", "ふつう", "むずかしい"]:
		_difficulty.add_item(difficulty_name)
	_difficulty.select(1)
	_volume_slider.value_changed.connect(_on_volume_changed)
	%ApplyButton.pressed.connect(_on_apply_pressed)
	_on_volume_changed(_volume_slider.value)
	_name_edit.grab_focus()


func _on_volume_changed(value: float) -> void:
	_volume_label.text = "%d %%" % value


func _on_apply_pressed() -> void:
	var player_name := _name_edit.text.strip_edges()
	if player_name.is_empty():
		player_name = "名無し"
	_result.text = (
		"名前: %s / 音量: %d %% / 難易度: %s"
		% [player_name, _volume_slider.value, _difficulty.get_item_text(_difficulty.selected)]
	)
