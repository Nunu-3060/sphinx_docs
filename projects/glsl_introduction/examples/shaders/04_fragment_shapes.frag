#version 300 es
precision highp float;

uniform vec2 uResolution;  // キャンバスの大きさ（ピクセル）
uniform int uMode;         // 表示内容の番号

out vec4 outColor;

void main() {
    // uv：左下が (0, 0)、右上が (1, 1) になる座標
    vec2 uv = gl_FragCoord.xy / uResolution;
    // p：画面の中心が (0, 0)、短辺方向が -1 から 1 になる座標（縦横比を補正している）
    vec2 p = (gl_FragCoord.xy * 2.0 - uResolution) / min(uResolution.x, uResolution.y);
    // 1 ピクセルが p の座標系でどれだけの長さになるか
    float pixel = 2.0 / min(uResolution.x, uResolution.y);

    vec3 color = vec3(0.0);

    if (uMode == 0) {
        // グラデーション：座標をそのまま色にする（赤 = 横方向、緑 = 縦方向）
        color = vec3(uv, 0.5);
    } else if (uMode == 1) {
        // 円：中心からの距離が 0.5 以下なら白
        float d = length(p);
        color = vec3(step(d, 0.5));
    } else if (uMode == 2) {
        // 円の輪郭を 2 ピクセル分だけなめらかに変化させる（アンチエイリアス）
        float d = length(p);
        color = vec3(1.0 - smoothstep(0.5 - 2.0 * pixel, 0.5, d));
    } else if (uMode == 3) {
        // 縞模様：横方向を 10 等分し、各区間の後半を白にする
        color = vec3(step(0.5, fract(uv.x * 10.0)));
    } else if (uMode == 4) {
        // 市松模様：マス目の番号 (x, y) の和が偶数か奇数かで色を変える
        vec2 cell = floor(uv * vec2(12.0, 8.0));
        color = vec3(mod(cell.x + cell.y, 2.0));
    } else if (uMode == 5) {
        // 図形の合成：背景の上に、円とリングを mix で重ねる
        vec3 background = mix(vec3(0.10, 0.10, 0.30), vec3(0.35, 0.10, 0.25), uv.y);
        float circle = 1.0 - smoothstep(0.45 - pixel, 0.45 + pixel, length(p - vec2(-0.5, 0.0)));
        float ring = 1.0 - smoothstep(0.03 - pixel, 0.03 + pixel, abs(length(p - vec2(0.5, 0.0)) - 0.35));
        color = mix(background, vec3(1.0, 0.8, 0.2), circle);
        color = mix(color, vec3(0.3, 0.9, 1.0), ring);
    } else {
        // discard：横 6 × 縦 4 のマス目に分け、各マスの円の外側は描画しない
        vec2 cell = fract(uv * vec2(6.0, 4.0)) - 0.5;
        if (length(cell) > 0.4) {
            discard;  // このフラグメントを捨てる（背景色が見える）
        }
        color = vec3(uv, 1.0);
    }

    outColor = vec4(color, 1.0);
}
