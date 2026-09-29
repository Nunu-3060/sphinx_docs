#version 300 es
precision highp float;

in vec2 vTexCoord;

uniform sampler2D uScene;  // 1 パス目で描いたシーン
uniform vec2 uTexelSize;   // 1 テクセルの大きさ（1 / 幅, 1 / 高さ）
uniform int uEffect;
uniform int uBlurRadius;

out vec4 outColor;

// 輝度：人の目の感度に合わせて、緑を重く、青を軽く重み付けする
float luminance(vec3 color) {
    return dot(color, vec3(0.2126, 0.7152, 0.0722));
}

// 周囲のテクセルを読み出す
vec3 sampleScene(vec2 offset) {
    return texture(uScene, vTexCoord + offset * uTexelSize).rgb;
}

// ボックスブラー：半径 r の正方形の範囲の平均を取る
vec3 boxBlur(int r) {
    vec3 sum = vec3(0.0);
    for (int y = -r; y <= r; y++) {
        for (int x = -r; x <= r; x++) {
            sum += sampleScene(vec2(x, y));
        }
    }
    float count = float((2 * r + 1) * (2 * r + 1));
    return sum / count;
}

// Sobel フィルター：輝度の横方向と縦方向の変化量（勾配）の大きさを求める
float sobel() {
    float tl = luminance(sampleScene(vec2(-1.0,  1.0)));  // 左上
    float t  = luminance(sampleScene(vec2( 0.0,  1.0)));  // 上
    float tr = luminance(sampleScene(vec2( 1.0,  1.0)));  // 右上
    float l  = luminance(sampleScene(vec2(-1.0,  0.0)));  // 左
    float r  = luminance(sampleScene(vec2( 1.0,  0.0)));  // 右
    float bl = luminance(sampleScene(vec2(-1.0, -1.0)));  // 左下
    float b  = luminance(sampleScene(vec2( 0.0, -1.0)));  // 下
    float br = luminance(sampleScene(vec2( 1.0, -1.0)));  // 右下
    float gx = (tr + 2.0 * r + br) - (tl + 2.0 * l + bl);
    float gy = (tl + 2.0 * t + tr) - (bl + 2.0 * b + br);
    return length(vec2(gx, gy));
}

void main() {
    vec3 color = sampleScene(vec2(0.0));

    if (uEffect == 1) {
        // グレースケール
        color = vec3(luminance(color));
    } else if (uEffect == 2) {
        // セピア：RGB を行列で変換する
        color = vec3(
            dot(color, vec3(0.393, 0.769, 0.189)),
            dot(color, vec3(0.349, 0.686, 0.168)),
            dot(color, vec3(0.272, 0.534, 0.131)));
        color = min(color, vec3(1.0));
    } else if (uEffect == 3) {
        // 色の反転
        color = 1.0 - color;
    } else if (uEffect == 4) {
        color = boxBlur(uBlurRadius);
    } else if (uEffect == 5) {
        // 勾配が大きい所（輪郭）を白く表示する
        color = vec3(clamp(sobel(), 0.0, 1.0));
    } else if (uEffect == 6) {
        // 周辺減光：画面の中心から離れるほど暗くする
        float d = distance(vTexCoord, vec2(0.5));
        color *= 1.0 - smoothstep(0.3, 0.75, d);
    }

    outColor = vec4(color, 1.0);
}
