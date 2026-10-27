// 画像を指定した色で塗りつぶす（被弾時の点滅などに使う）シェーダー。
shader_type canvas_item;

// 塗りつぶす色。source_color を付けるとインスペクターでカラーピッカーが使える。
uniform vec4 flash_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
// 塗りつぶしの度合い。0.0 で元の画像、1.0 で flash_color 一色になる。
uniform float flash_amount : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	// COLOR には、テクスチャの色に頂点色（modulate など）を掛けた値が入っている。
	// 透明度はそのままにして、RGB だけを flash_color へ近づける。
	COLOR.rgb = mix(COLOR.rgb, flash_color.rgb, flash_amount);
}
