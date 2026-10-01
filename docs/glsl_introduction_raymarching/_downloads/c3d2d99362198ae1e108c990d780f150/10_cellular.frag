// 10_cellular.frag
// 第 10 章: セルラーノイズ (Worley ノイズ) とミンコフスキー距離。画面を 6 つに分け、次の順に表示する。
//   上段: F1 (最も近い点までの距離)、F2 (2 番目に近い点までの距離)、F2 - F1
//   下段: ボロノイの境界までの距離、マンハッタン距離 (p = 1) のセル、チェビシェフ距離 (p = ∞) のセル
// 各セルの点は、時間とともにゆっくり動かしている。

// ---- ハッシュ (第 10 章) -------------------------------------------------

uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

// 整数の格子点 p に、0 以上 1 未満の乱数を 2 つ割り当てる
vec2 hash22(vec2 p)
{
    uvec2 q = uvec2(ivec2(p));
    uint h = pcgHash(q.x + pcgHash(q.y));
    return vec2(float(h), float(pcgHash(h))) / 4294967296.0;
}

// ---- 距離の測り方 --------------------------------------------------------

const int METRIC_EUCLIDEAN = 0;   // p = 2 (ユークリッド距離)
const int METRIC_MANHATTAN = 1;   // p = 1 (マンハッタン距離)
const int METRIC_CHEBYSHEV = 2;   // p = ∞ (チェビシェフ距離)

// ミンコフスキー距離の代表的な 3 つ
float distanceOf(vec2 d, int metric)
{
    if (metric == METRIC_MANHATTAN) {
        return abs(d.x) + abs(d.y);
    }
    if (metric == METRIC_CHEBYSHEV) {
        return max(abs(d.x), abs(d.y));
    }
    return length(d);
}

// ---- セルラーノイズ ------------------------------------------------------

// 格子のセル cell に置く点の位置 (セル内の座標 0〜1)。時間とともに動かす
vec2 featurePoint(vec2 cell)
{
    vec2 h = hash22(cell);
    return 0.5 + 0.4 * sin(0.5 * iTime + 6.2831853 * h);
}

// 点 x のまわり 3 × 3 のセルの点を調べ、(F1, F2, 最も近い点のセルの乱数) を返す
vec3 cellular(vec2 x, int metric)
{
    vec2 n = floor(x);
    vec2 f = fract(x);
    float f1 = 8.0;
    float f2 = 8.0;
    float id = 0.0;
    for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
            vec2 g = vec2(float(i), float(j));
            vec2 r = g + featurePoint(n + g) - f;   // x から点へのベクトル
            float d = distanceOf(r, metric);
            if (d < f1) {
                f2 = f1;
                f1 = d;
                id = hash22(n + g + 31.0).x;
            } else if (d < f2) {
                f2 = d;
            }
        }
    }
    return vec3(f1, f2, id);
}

// ボロノイの境界までのユークリッド距離 (Quilez の方法)。
// 1 回目の探索で最も近い点を求め、2 回目の探索でその点と他の点の垂直二等分線までの距離の最小値をとる
float voronoiBorder(vec2 x)
{
    vec2 n = floor(x);
    vec2 f = fract(x);

    // 1 回目: 最も近い点
    vec2 nearestCell = vec2(0.0);
    vec2 nearest = vec2(0.0);   // x から最も近い点へのベクトル
    float best = 8.0;
    for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
            vec2 g = vec2(float(i), float(j));
            vec2 r = g + featurePoint(n + g) - f;
            float d = dot(r, r);
            if (d < best) {
                best = d;
                nearest = r;
                nearestCell = g;
            }
        }
    }

    // 2 回目: 最も近い点と、その周囲 5 × 5 の点との境界までの距離
    float border = 8.0;
    for (int j = -2; j <= 2; j++) {
        for (int i = -2; i <= 2; i++) {
            vec2 g = nearestCell + vec2(float(i), float(j));
            vec2 r = g + featurePoint(n + g) - f;
            vec2 diff = r - nearest;
            if (dot(diff, diff) > 1e-6) {
                // 2 点の中点から、2 点を結ぶ方向に測った距離
                border = min(border, dot(0.5 * (nearest + r), normalize(diff)));
            }
        }
    }
    return border;
}

// ---- メイン --------------------------------------------------------------

vec3 cellColor(float id)
{
    return 0.55 + 0.4 * cos(6.2831853 * (id + vec3(0.0, 0.33, 0.67)));
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 grid = vec2(3.0, 2.0);
    vec2 uv = fragCoord / iResolution.xy;
    vec2 cell = floor(uv * grid);
    int index = int(cell.x) + 3 * int(1.0 - cell.y);   // 左上から 0, 1, 2, ...

    vec2 local = fract(uv * grid);
    float aspect = (iResolution.x / grid.x) / (iResolution.y / grid.y);
    vec2 p = 5.0 * local * vec2(aspect, 1.0);   // 縦方向に格子 5 個分

    vec3 col;
    if (index == 0) {
        col = vec3(cellular(p, METRIC_EUCLIDEAN).x);
    } else if (index == 1) {
        col = vec3(0.7 * cellular(p, METRIC_EUCLIDEAN).y);
    } else if (index == 2) {
        vec3 c = cellular(p, METRIC_EUCLIDEAN);
        col = vec3(2.0 * (c.y - c.x));
    } else if (index == 3) {
        // 境界までの距離: 等間隔の縞と、幅一定の境界線
        float d = voronoiBorder(p);
        col = vec3(0.3 + 0.2 * cos(40.0 * d));
        col = mix(vec3(1.0, 0.8, 0.3), col, smoothstep(0.02, 0.04, d));
    } else {
        // ミンコフスキー距離を変えたセル。境界線は F2 - F1 で近似する
        int metric = (index == 4) ? METRIC_MANHATTAN : METRIC_CHEBYSHEV;
        vec3 c = cellular(p, metric);
        col = cellColor(c.z) * (0.6 + 0.4 * (1.0 - c.x));
        col *= smoothstep(0.02, 0.06, c.y - c.x);
    }

    // 領域の境界線
    vec2 border = step(vec2(0.005), local) * step(local, vec2(0.995));
    col *= border.x * border.y;
    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
