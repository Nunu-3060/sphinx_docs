#version 300 es
precision highp float;

uniform vec2 uResolution;
uniform float uTime;

out vec4 outColor;

const float PI = 3.14159265;

// イージング関数：0 から 1 に進む t を、動きの緩急を付けた値に変換する
float easeLinear(float t)  { return t; }
float easeInQuad(float t)  { return t * t; }                        // 始めはゆっくり
float easeOutQuad(float t) { return 1.0 - (1.0 - t) * (1.0 - t); }  // 終わりはゆっくり
float easeSmooth(float t)  { return t * t * (3.0 - 2.0 * t); }      // 始めと終わりがゆっくり

// コサイン関数を使ったカラーパレット：t が 1 増えるごとに色が一周する
vec3 palette(float t) {
    return 0.5 + 0.5 * cos(2.0 * PI * (t + vec3(0.0, 0.33, 0.67)));
}

void main() {
    vec2 uv = gl_FragCoord.xy / uResolution;

    // 背景：時間とともに色相が変わる暗めのグラデーション
    vec3 color = 0.25 * palette(0.1 * uTime + 0.2 * uv.x);

    // 0 → 1 → 0 と 4 秒で往復する値
    float t = 1.0 - abs(2.0 * fract(uTime / 4.0) - 1.0);

    // 画面を縦に 4 段に分け、上の段から順に 0, 1, 2, 3 と番号を付ける
    float rowHeight = uResolution.y / 4.0;
    int row = 3 - int(gl_FragCoord.y / rowHeight);

    float e;
    if (row == 0) {
        e = easeLinear(t);
    } else if (row == 1) {
        e = easeInQuad(t);
    } else if (row == 2) {
        e = easeOutQuad(t);
    } else {
        e = easeSmooth(t);
    }

    // 円の中心：横方向は e に応じて左端から右端まで動く
    float margin = 40.0;
    vec2 center = vec2(mix(margin, uResolution.x - margin, e), (3.5 - float(row)) * rowHeight);

    // 円の通り道を示す線
    float line = 1.0 - smoothstep(0.5, 1.5, abs(gl_FragCoord.y - center.y));
    color += 0.15 * line;

    // 円（半径 20 ピクセル、輪郭を 1 ピクセルなめらかにする）
    float circle = 1.0 - smoothstep(19.0, 21.0, length(gl_FragCoord.xy - center));
    color = mix(color, palette(float(row) * 0.25), circle);

    outColor = vec4(color, 1.0);
}
