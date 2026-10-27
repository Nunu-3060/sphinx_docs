// 画面全体を白黒にし、周囲を暗くするシェーダー。画面全体を覆う ColorRect に設定する。
shader_type canvas_item;

// 描画済みの画面の内容を読み取るためのテクスチャ
uniform sampler2D screen_texture : hint_screen_texture, filter_linear_mipmap;
uniform float grayscale : hint_range(0.0, 1.0) = 1.0;  // 白黒の度合い
uniform float vignette : hint_range(0.0, 2.0) = 0.8;  // 周辺を暗くする強さ

void fragment() {
	vec3 color = textureLod(screen_texture, SCREEN_UV, 0.0).rgb;
	// 人の目の感度に合わせた重みで明るさ（輝度）を求める。
	float luminance = dot(color, vec3(0.299, 0.587, 0.114));
	color = mix(color, vec3(luminance), grayscale);
	// 画面の中心からの距離が大きいほど暗くする。
	float distance_from_center = distance(SCREEN_UV, vec2(0.5));
	color *= 1.0 - vignette * distance_from_center * distance_from_center;
	COLOR = vec4(color, 1.0);
}
