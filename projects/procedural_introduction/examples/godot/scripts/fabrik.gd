extends RefCounted
## FABRIK（Forward And Backward Reaching Inverse Kinematics）。第 12 章に対応する。
##
## 関節の列 joints の先端を target に近づける。各区間の長さは lengths に従う。
## 「先端を目標に合わせて根元へ」「根元を元の位置に戻して先端へ」の 2 回のなぞりを繰り返す。


static func solve(
	joints: PackedVector2Array,
	lengths: PackedFloat32Array,
	target: Vector2,
	iterations := 10,
	tolerance := 0.5
) -> PackedVector2Array:
	var n := joints.size()
	var root := joints[0]
	var total := 0.0
	for length in lengths:
		total += length
	if root.distance_to(target) >= total:
		# 届かないときは、目標の方向にまっすぐ伸ばす。
		for i in n - 1:
			joints[i + 1] = joints[i] + joints[i].direction_to(target) * lengths[i]
		return joints
	for _iteration in iterations:
		# 後ろ向き: 先端を目標に置き、根元の方へ、区間の長さを保って引き寄せる。
		joints[n - 1] = target
		for i in range(n - 2, -1, -1):
			joints[i] = joints[i + 1] + joints[i + 1].direction_to(joints[i]) * lengths[i]
		# 前向き: 根元を元の位置に戻し、先端の方へ同じことをする。
		joints[0] = root
		for i in range(1, n):
			joints[i] = joints[i - 1] + joints[i - 1].direction_to(joints[i]) * lengths[i - 1]
		if joints[n - 1].distance_to(target) < tolerance:
			break
	return joints
