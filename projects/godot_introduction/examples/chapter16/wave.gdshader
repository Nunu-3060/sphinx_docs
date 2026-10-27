// 画像を横方向に波打たせるシェーダー。旗や水面の揺らぎを表現する。
shader_type canvas_item;

uniform float amplitude = 0.05;  // 揺れ幅（UV 座標の単位。画像の幅に対する割合）
uniform float frequency = 12.0;  // 縦方向に並ぶ波の細かさ
uniform float speed = 4.0;  // 波が流れる速さ

void fragment() {
	vec2 uv = UV;
	// 行（y）ごとに、時間とともに変化する量だけ横にずらして読み取る。
	uv.x += sin(uv.y * frequency + TIME * speed) * amplitude;
	COLOR = texture(TEXTURE, uv);
}
