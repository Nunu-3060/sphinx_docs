#version 300 es
precision highp float;

in vec3 vWorldPosition;
in vec3 vNormal;

uniform vec3 uLightDirection;  // 物体から光源へ向かう方向（ワールド座標）
uniform vec3 uCameraPosition;  // カメラの位置（ワールド座標）
uniform vec3 uBaseColor;       // 物体の色
uniform float uShininess;      // 光沢度：大きいほどハイライトが小さく鋭くなる
uniform bool uUseAmbient;
uniform bool uUseDiffuse;
uniform bool uUseSpecular;
uniform bool uUseBlinnPhong;   // true：Blinn-Phong、false：Phong
uniform bool uUseGamma;

out vec4 outColor;

const vec3 LIGHT_COLOR = vec3(1.0);    // 光源の色
const float AMBIENT_STRENGTH = 0.15;   // 環境光の強さ
const float SPECULAR_STRENGTH = 0.6;   // 鏡面反射の強さ

void main() {
    // 補間された法線は長さが 1 とは限らないので、正規化し直す
    vec3 N = normalize(vNormal);
    vec3 L = normalize(uLightDirection);
    vec3 V = normalize(uCameraPosition - vWorldPosition);  // 表面からカメラへ向かう方向

    vec3 color = vec3(0.0);

    // 環境光：周囲からの間接的な光を一定の明るさで近似する
    if (uUseAmbient) {
        color += AMBIENT_STRENGTH * uBaseColor;
    }

    // 拡散反射（Lambert）：光が当たる角度が浅いほど暗くなる
    float diffuse = max(dot(N, L), 0.0);
    if (uUseDiffuse) {
        color += diffuse * uBaseColor * LIGHT_COLOR;
    }

    // 鏡面反射：光源の反射方向とカメラの方向が近いほど明るい（光が当たっている面だけ）
    if (uUseSpecular && diffuse > 0.0) {
        float specular;
        if (uUseBlinnPhong) {
            vec3 H = normalize(L + V);                     // ハーフベクトル
            specular = pow(max(dot(N, H), 0.0), uShininess);
        } else {
            vec3 R = reflect(-L, N);                       // 光の反射方向
            specular = pow(max(dot(R, V), 0.0), uShininess);
        }
        color += SPECULAR_STRENGTH * specular * LIGHT_COLOR;
    }

    // ガンマ補正：線形な明るさを、ディスプレイ向けの値に変換する（近似）
    if (uUseGamma) {
        color = pow(color, vec3(1.0 / 2.2));
    }

    outColor = vec4(color, 1.0);
}
