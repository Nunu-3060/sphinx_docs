extends RefCounted
## SurfaceTool で基本的な形のメッシュを作る関数集（第 6 章に対応）。
##
## Godot の三角形は、表から見て頂点が時計回りに並ぶ面を表とする。
## 裏の面は描かれない（バックフェースカリング）ので、頂点の順番に注意する。


## 平面の格子。size × size の正方形を divisions × divisions のマスに分け、
## 各頂点の高さを height_func(x, z) で、色を color_func(高さ) で決める。
static func grid(
	size: float, divisions: int, height_func: Callable, color_func: Callable
) -> ArrayMesh:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var step := size / divisions
	var half := size * 0.5
	for j in divisions + 1:
		for i in divisions + 1:
			var x := i * step - half
			var z := j * step - half
			var y: float = height_func.call(x, z)
			st.set_uv(Vector2(float(i) / divisions, float(j) / divisions))
			st.set_color(color_func.call(y))
			st.add_vertex(Vector3(x, y, z))
	# 1 マスを 2 枚の三角形に分ける。上から見て時計回りに並べる。
	for j in divisions:
		for i in divisions:
			var a := j * (divisions + 1) + i  # 左奥
			var b := a + 1  # 右奥
			var c := a + divisions + 1  # 左手前
			var d := c + 1  # 右手前
			for index: int in [a, b, c, b, d, c]:
				st.add_index(index)
	# 頂点を共有する面の法線を平均して、滑らかな法線を作る。
	st.generate_normals()
	return st.commit()


## 円柱。側面と上下のふたを作る。法線は自分で計算して与える。
static func cylinder(radius: float, height: float, segments: int, color: Color) -> ArrayMesh:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	st.set_color(color)
	for s in segments:
		var a0 := TAU * s / segments
		var a1 := TAU * (s + 1) / segments
		var d0 := Vector3(cos(a0), 0.0, sin(a0))  # 外向きの方向 = 側面の法線
		var d1 := Vector3(cos(a1), 0.0, sin(a1))
		var top := Vector3(0.0, height, 0.0)
		# 側面の四角形（三角形 2 枚）。角で法線を共有しない（ふたとの境目を鋭くする）。
		var quad := [
			[d0, Vector3.ZERO],
			[d1, Vector3.ZERO],
			[d0, top],
			[d1, Vector3.ZERO],
			[d1, top],
			[d0, top]
		]
		for vertex: Array in quad:
			st.set_normal(vertex[0])
			st.add_vertex(vertex[0] * radius + vertex[1])
		# 上のふた（上向き）と下のふた（下向き）
		st.set_normal(Vector3.UP)
		for p: Vector3 in [top, top + d0 * radius, top + d1 * radius]:
			st.add_vertex(p)
		st.set_normal(Vector3.DOWN)
		for p: Vector3 in [Vector3.ZERO, d1 * radius, d0 * radius]:
			st.add_vertex(p)
	return st.commit()


## 回転体。断面の輪郭 profile（各点は (半径, 高さ)）を y 軸の周りに回して作る。
## colors を与えると、輪郭の点ごとに頂点の色を変える。
static func lathe(
	profile: PackedVector2Array, segments: int, colors := PackedColorArray()
) -> ArrayMesh:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	for k in profile.size():
		for s in segments:
			var angle := TAU * s / segments
			var r := profile[k].x
			if not colors.is_empty():
				st.set_color(colors[k])
			st.add_vertex(Vector3(r * cos(angle), profile[k].y, r * sin(angle)))
	# 輪郭の k 番目と k + 1 番目の輪の間を四角形でつなぐ。
	# 最後の列は最初の列とつなぐ（s + 1 を segments で割った余り）ので、継ぎ目ができない。
	for k in profile.size() - 1:
		for s in segments:
			var a := k * segments + s
			var b := k * segments + (s + 1) % segments
			var c := a + segments
			var d := b + segments
			for index: int in [a, b, c, b, d, c]:
				st.add_index(index)
	st.generate_normals()
	return st.commit()


## 頂点の色をそのまま表面の色に使う材質。
static func vertex_color_material() -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.vertex_color_use_as_albedo = true
	material.vertex_color_is_srgb = true  # 色は sRGB の値で指定している
	material.roughness = 0.85
	return material
