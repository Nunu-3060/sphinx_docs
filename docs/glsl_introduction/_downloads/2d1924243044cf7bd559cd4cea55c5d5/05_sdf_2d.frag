#version 300 es
precision highp float;

uniform vec2 uResolution;
uniform vec2 uCirclePosition;  // 円の中心（p と同じ座標系）
uniform int uOperation;        // 0：和、1：積、2：差、3：なめらかな和
uniform float uSmoothness;     // なめらかな和の k
uniform bool uShowField;       // true のとき距離の値を等高線で表示する

out vec4 outColor;

// 円の距離関数：中心が原点、半径 r
float sdCircle(vec2 p, float r) {
    return length(p) - r;
}

// 長方形の距離関数：中心が原点、幅と高さの半分が b
float sdBox(vec2 p, vec2 b) {
    vec2 d = abs(p) - b;
    return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

// なめらかな和：a と b の境目を幅 k でなめらかにつなぐ
float smoothMin(float a, float b, float k) {
    float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
    return mix(b, a, h) - k * h * (1.0 - h);
}

void main() {
    vec2 p = (gl_FragCoord.xy * 2.0 - uResolution) / min(uResolution.x, uResolution.y);
    float pixel = 2.0 / min(uResolution.x, uResolution.y);

    float a = sdBox(p, vec2(0.45, 0.30));             // 長方形（中央に固定）
    float b = sdCircle(p - uCirclePosition, 0.35);    // 円（ドラッグで移動）

    float d;
    if (uOperation == 0) {
        d = min(a, b);                  // 和：どちらかの内側
    } else if (uOperation == 1) {
        d = max(a, b);                  // 積：両方の内側
    } else if (uOperation == 2) {
        d = max(a, -b);                 // 差：a の内側かつ b の外側
    } else {
        d = smoothMin(a, b, uSmoothness);
    }

    vec3 color;
    if (uShowField) {
        // 外側（d > 0）はオレンジ、内側（d < 0）は青。境界から離れるほど明るくする
        color = (d > 0.0) ? vec3(0.9, 0.6, 0.3) : vec3(0.4, 0.7, 0.9);
        color *= 1.0 - exp(-4.0 * abs(d));
        // 距離 0.1 ごとに等高線を引く
        color *= 0.8 + 0.2 * cos(2.0 * 3.14159265 * d / 0.1);
        // 境界（d = 0）を白い線で描く
        color = mix(color, vec3(1.0), 1.0 - smoothstep(0.0, 2.0 * pixel, abs(d)));
    } else {
        // 図形の内側を塗りつぶす（境界の 1 ピクセルをなめらかにする）
        float inside = 1.0 - smoothstep(-pixel, pixel, d);
        color = mix(vec3(0.12), vec3(1.0, 0.8, 0.3), inside);
    }

    outColor = vec4(color, 1.0);
}
