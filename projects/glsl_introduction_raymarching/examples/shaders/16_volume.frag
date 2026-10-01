// 16_volume.frag
// 第 16 章: ボリュームレンダリング。雲の形を SDF とノイズで定義し、
// 一定の歩幅で進みながら光の吸収と散乱を積分する。

const int   VOLUME_STEPS = 96;     // 視線方向の分割数
const int   LIGHT_STEPS  = 6;      // 光源に向かう方向の分割数
const float STEP_SIZE    = 0.06;   // 雲の内部での歩幅
const float SIGMA        = 6.0;    // 消散係数 (密度 1 あたり)

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.5, -0.4));
const vec3 SUN_COLOR = vec3(1.4, 1.25, 1.0);
const vec3 AMBIENT   = vec3(0.25, 0.32, 0.45);

// ---- ノイズ (第 10 章) ---------------------------------------------------

// PCG ハッシュ (Jarzynski and Olano, 2020)
uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

// 3 次元の整数の格子点 p に 0 以上 1 未満の乱数を割り当てる
float hash31(vec3 p)
{
    uvec3 q = uvec3(ivec3(p));
    return float(pcgHash(q.x + pcgHash(q.y + pcgHash(q.z)))) / 4294967296.0;
}

// 3 次元の値ノイズ: 立方体の 8 頂点の乱数を 3 次のエルミート補間でつなぐ
float valueNoise(vec3 x)
{
    vec3 i = floor(x);
    vec3 f = fract(x);
    vec3 u = f * f * (3.0 - 2.0 * f);
    vec2 e = vec2(1.0, 0.0);
    return mix(mix(mix(hash31(i + e.yyy), hash31(i + e.xyy), u.x),
                   mix(hash31(i + e.yxy), hash31(i + e.xxy), u.x), u.y),
               mix(mix(hash31(i + e.yyx), hash31(i + e.xyx), u.x),
                   mix(hash31(i + e.yxx), hash31(i + e.xxx), u.x), u.y),
               u.z);
}

// フラクタルブラウン運動: 周波数を 2 倍、振幅を半分にしながらノイズを重ねる
float fbm(vec3 p)
{
    float value = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < 5; i++) {
        value += amplitude * valueNoise(p);
        p *= 2.02;
        amplitude *= 0.5;
    }
    return value;
}

// ---- 雲の形 --------------------------------------------------------------

float sdSphere(vec3 p, float r)
{
    return length(p) - r;
}

float smin(float a, float b, float k)
{
    float h = max(k - abs(a - b), 0.0) / k;
    return min(a, b) - h * h * k * 0.25;
}

// 雲の大まかな形 (3 つの球を滑らかにつないだもの)
float sdCloudShape(vec3 p)
{
    float d = sdSphere(p - vec3(0.0, 0.0, 0.0), 1.0);
    d = smin(d, sdSphere(p - vec3(1.1, -0.2, 0.2), 0.75), 0.6);
    d = smin(d, sdSphere(p - vec3(-1.1, -0.3, -0.1), 0.7), 0.6);
    return d;
}

// ノイズで削る量の最大値。SDF がこれより大きい場所には雲が無い
const float EROSION = 0.5;

// 位置 p での密度 (0 以上)
float density(vec3 p)
{
    vec3 q = p + vec3(0.15 * iTime, 0.0, 0.0);  // ノイズを流して形を変化させる
    float d = sdCloudShape(p) + EROSION * (fbm(3.0 * q) - 0.5) * 2.0;
    return clamp(-d * 2.0, 0.0, 1.0);
}

// 点 p から光源の方向に進み、途中の密度から光の透過率を求める
float lightTransmittance(vec3 p)
{
    float sum = 0.0;
    const float stepSize = 0.15;
    for (int i = 1; i <= LIGHT_STEPS; i++) {
        sum += density(p + LIGHT_DIR * stepSize * float(i));
    }
    return exp(-SIGMA * sum * stepSize);
}

// ---- レンダリング --------------------------------------------------------

vec3 skyColor(vec3 rd)
{
    vec3 col = mix(vec3(0.7, 0.78, 0.88), vec3(0.25, 0.42, 0.72),
                   sqrt(clamp(rd.y, 0.0, 1.0)));
    float sun = max(dot(rd, LIGHT_DIR), 0.0);
    col += SUN_COLOR * (pow(sun, 512.0) * 4.0 + pow(sun, 8.0) * 0.2);
    return col;
}

vec3 render(vec3 ro, vec3 rd, float jitter)
{
    vec3 col = vec3(0.0);        // 雲から視点に届く光の合計
    float transmittance = 1.0;   // 視点から現在位置までの透過率

    // 光が進行方向の前方に散乱しやすいことを近似する位相関数
    float mu = dot(rd, LIGHT_DIR);
    float phase = 0.6 + 0.8 * pow(max(mu, 0.0), 4.0);

    float t = jitter * STEP_SIZE;
    for (int i = 0; i < VOLUME_STEPS; i++) {
        vec3 p = ro + t * rd;
        float shape = sdCloudShape(p);
        if (shape > EROSION) {
            // 雲の外: SDF を使って空の空間を一気に飛ばす
            t += max(shape - EROSION, STEP_SIZE);
        } else {
            float dens = density(p);
            if (dens > 0.0) {
                // この区間で吸収・散乱される割合
                float absorbed = 1.0 - exp(-SIGMA * dens * STEP_SIZE);
                vec3 light = SUN_COLOR * lightTransmittance(p) * phase +
                             AMBIENT;
                col += transmittance * absorbed * light;
                transmittance *= 1.0 - absorbed;
                if (transmittance < 0.01) {
                    break;   // ほとんど光が届かないので打ち切る
                }
            }
            t += STEP_SIZE;
        }
        if (t > 20.0) {
            break;
        }
    }
    // 雲を透過した分だけ背景の空が見える
    return col + transmittance * skyColor(rd);
}

mat3 setCamera(vec3 ro, vec3 ta)
{
    vec3 cw = normalize(ta - ro);
    vec3 cu = normalize(cross(cw, vec3(0.0, 1.0, 0.0)));
    vec3 cv = cross(cu, cw);
    return mat3(cu, cv, cw);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    vec3 ro = vec3(0.0, 0.8, 5.0);
    vec3 ta = vec3(0.0, 0.0, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.0));

    // ピクセルごとに開始位置をずらし、縞模様をノイズに置き換える
    float jitter = hash31(vec3(fragCoord, float(iFrame)));
    vec3 col = render(ro, rd, jitter);

    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
