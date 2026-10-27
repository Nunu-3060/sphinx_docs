// ノイズ画像を使って、画像が燃え尽きるように消えていくシェーダー。
shader_type canvas_item;

uniform sampler2D noise_texture;  // 消える順番を決めるノイズ画像
uniform float progress : hint_range(0.0, 1.0) = 0.0;  // 0.0 で元の画像、1.0 で完全に消える
uniform vec4 edge_color : source_color = vec4(1.0, 0.5, 0.1, 1.0);  // 消える境目の色
uniform float edge_width = 0.05;  // 境目の太さ

void fragment() {
	float noise = texture(noise_texture, UV).r;
	// ノイズの値が progress より小さい部分は描画しない。
	if (noise < progress) {
		discard;
	}
	// 消える直前の部分を edge_color で塗り、燃えているように見せる。
	if (noise < progress + edge_width && progress > 0.0) {
		COLOR.rgb = edge_color.rgb;
	}
}
