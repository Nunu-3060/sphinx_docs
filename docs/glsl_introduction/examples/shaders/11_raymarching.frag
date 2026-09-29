#version 300 es
precision highp float;

uniform vec2 uResolution;
uniform float uTime;
uniform int uMaxSteps;   // レイを進める回数の上限
uniform bool uUseShadow;
uniform bool uShowSteps;

out vec4 outColor;

const float MAX_DISTANCE = 20.0;      // これより遠くへ進んだら「何にも当たらない」とする
const float SURFACE_DISTANCE = 0.001; // 距離がこれより小さくなったら「表面に当たった」とする

// ---- 距離関数 ----
float sdSphere(vec3 p, float r) {
    return length(p) - r;
}

float sdBox(vec3 p, vec3 b) {
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// y = 0 の平面（床）
float sdPlane(vec3 p) {
    return p.y;
}

float smoothMin(float a, float b, float k) {
    float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
    return mix(b, a, h) - k * h * (1.0 - h);
}

// シーン全体の距離関数：点 p から最も近い物体の表面までの距離
float map(vec3 p) {
    vec3 spherePosition = vec3(0.9 * sin(uTime), 0.7 + 0.2 * sin(2.0 * uTime), 0.0);
    float sphere = sdSphere(p - spherePosition, 0.45);
    float box = sdBox(p - vec3(0.0, 0.35, 0.0), vec3(0.35));
    float objects = smoothMin(sphere, box, 0.25);
    return min(objects, sdPlane(p));
}
// ---- 距離関数ここまで ----

// ---- レイマーチング ----
// 始点 ro から方向 rd へレイを進める。表面に当たれば true を返す。
// t には進んだ距離、steps には繰り返した回数を書き込む。
bool rayMarch(vec3 ro, vec3 rd, out float t, out int steps) {
    t = 0.0;
    steps = 0;
    for (int i = 0; i < 1000; i++) {
        if (i >= uMaxSteps) {
            break;
        }
        steps = i + 1;
        float d = map(ro + rd * t);
        if (d < SURFACE_DISTANCE) {
            return true;
        }
        t += d;  // 最も近い表面までの距離だけ進んでも、何かを突き抜けることはない
        if (t > MAX_DISTANCE) {
            break;
        }
    }
    return false;
}
// ---- レイマーチングここまで ----

// ---- 法線と影 ----
// 法線：距離関数の勾配（各軸方向の変化量）を中心差分で近似する
vec3 calcNormal(vec3 p) {
    const float h = 0.0005;
    return normalize(vec3(
        map(p + vec3(h, 0.0, 0.0)) - map(p - vec3(h, 0.0, 0.0)),
        map(p + vec3(0.0, h, 0.0)) - map(p - vec3(0.0, h, 0.0)),
        map(p + vec3(0.0, 0.0, h)) - map(p - vec3(0.0, 0.0, h))));
}

// ソフトシャドウ：表面から光源へレイを進め、物体の近くを通るほど暗くする
float softShadow(vec3 ro, vec3 rd, float k) {
    float result = 1.0;
    float t = 0.02;
    for (int i = 0; i < 64; i++) {
        float d = map(ro + rd * t);
        if (d < SURFACE_DISTANCE) {
            return 0.0;  // 光源との間に物体がある
        }
        result = min(result, k * d / t);
        t += d;
        if (t > MAX_DISTANCE) {
            break;
        }
    }
    return clamp(result, 0.0, 1.0);
}
// ---- 法線と影ここまで ----

// ステップ数の可視化用：0 → 黒、赤、黄、1 → 白
vec3 heatColor(float s) {
    return clamp(vec3(3.0 * s, 3.0 * s - 1.0, 3.0 * s - 2.0), 0.0, 1.0);
}

void main() {
    // ---- カメラとレイの生成 ----
    // 画面の中心を原点とし、縦方向が -1 から 1 になる座標
    vec2 p = (gl_FragCoord.xy * 2.0 - uResolution) / uResolution.y;

    vec3 ro = vec3(0.0, 1.2, 3.0);           // カメラの位置（レイの始点）
    vec3 target = vec3(0.0, 0.4, 0.0);       // カメラが見る点
    vec3 forward = normalize(target - ro);
    vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0)));
    vec3 up = cross(right, forward);
    const float FOCAL_LENGTH = 1.5;          // 大きいほど視野が狭くなる
    vec3 rd = normalize(p.x * right + p.y * up + FOCAL_LENGTH * forward);  // レイの方向
    // ---- カメラとレイの生成ここまで ----

    float t;
    int steps;
    bool hit = rayMarch(ro, rd, t, steps);

    if (uShowSteps) {
        outColor = vec4(heatColor(float(steps) / float(uMaxSteps)), 1.0);
        return;
    }

    vec3 sky = vec3(0.55, 0.7, 0.9);
    vec3 color = sky;

    if (hit) {
        vec3 position = ro + rd * t;
        vec3 normal = calcNormal(position);
        vec3 lightDirection = normalize(vec3(0.6, 0.8, 0.4));

        // 床は市松模様、物体はオレンジ色
        vec3 albedo;
        if (position.y < 0.002) {
            float checker = mod(floor(position.x * 2.0) + floor(position.z * 2.0), 2.0);
            albedo = mix(vec3(0.3), vec3(0.8), checker);
        } else {
            albedo = vec3(0.9, 0.45, 0.2);
        }

        // 影：表面から少し浮かせた位置から光源へ向かってレイを進める
        float shadow = uUseShadow ? softShadow(position + normal * 0.01, lightDirection, 8.0) : 1.0;

        // Blinn-Phong（第 10 章と同じ考え方）
        float diffuse = max(dot(normal, lightDirection), 0.0);
        vec3 halfVector = normalize(lightDirection - rd);
        float specular = (diffuse > 0.0) ? pow(max(dot(normal, halfVector), 0.0), 32.0) : 0.0;
        color = albedo * (0.15 + 0.85 * diffuse * shadow) + 0.3 * specular * shadow;

        // フォグ：遠くの物ほど空の色に近づける
        color = mix(color, sky, 1.0 - exp(-0.01 * t * t));
    }

    // ガンマ補正
    color = pow(color, vec3(1.0 / 2.2));
    outColor = vec4(color, 1.0);
}
