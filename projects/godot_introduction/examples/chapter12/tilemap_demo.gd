extends Node2D
## 文字で書いたステージの配置図から TileMapLayer にタイルを並べるサンプル。
## エディターで手作業でタイルを塗る代わりに、コードで配置する方法を示す。

## ステージの配置図。# は地面、B はレンガ、それ以外は空白。1 文字が 1 タイル（32 x 32 ピクセル）。
const LEVEL: Array[String] = [
	"B                                                          B",
	"B                                                          B",
	"B                                                          B",
	"B                                                          B",
	"B                                                          B",
	"B                                                          B",
	"B                                                          B",
	"B                                       BBBB               B",
	"B                                                          B",
	"B                           BBBB                           B",
	"B                                                  BBB     B",
	"B                  BBBB                                    B",
	"B                                         ###              B",
	"B          BBBB                                            B",
	"B                                ####                      B",
	"B                                                          B",
	"B                                                          B",
	"############################################################",
	"############################################################",
	"############################################################",
]
const SOURCE_ID: int = 0  # タイルセット内のアトラスの番号
## 文字とアトラス内のタイル座標の対応
const TILES: Dictionary[String, Vector2i] = {
	"#": Vector2i(0, 0),
	"B": Vector2i(1, 0),
}

@onready var _ground: TileMapLayer = $Ground
@onready var _camera: Camera2D = $Player/Camera2D


func _ready() -> void:
	for row in LEVEL.size():
		var line := LEVEL[row]
		for column in line.length():
			var symbol := line[column]
			if TILES.has(symbol):
				_ground.set_cell(Vector2i(column, row), SOURCE_ID, TILES[symbol])

	# カメラがステージの外を映さないように、移動範囲を制限する。
	var used := _ground.get_used_rect()
	var tile_size := _ground.tile_set.tile_size
	_camera.limit_left = used.position.x * tile_size.x
	_camera.limit_top = used.position.y * tile_size.y
	_camera.limit_right = used.end.x * tile_size.x
	_camera.limit_bottom = used.end.y * tile_size.y
