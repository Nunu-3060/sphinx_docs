// 10_quadtree_pattern.frag
// 第 10 章: 手続き的な四分木による模様。正方形を、ハッシュ関数で選んだ場所だけ
// 4 つに分割することを繰り返し、大小の正方形のタイルを敷き詰める。
// 分割の判定に使う乱数を一定時間ごとに変え、模様を切り替える。

const float ROOT_SIZE = 1.0;   // 分割前の正方形の 1 辺 (縦方向の画面の 1/2)
const int   MAX_DEPTH = 5;     // 分割の最大の深さ

// ---- ハッシュ (第 10 章) -------------------------------------------------

uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

// セルの位置 (整数) と深さ、模様の番号から乱数を作る
float hashCell(vec2 cell, int depth, float pattern)
{
    uvec2 q = uvec2(ivec2(cell));
    uint h = pcgHash(q.x + pcgHash(q.y + pcgHash(uint(depth) +
                                                 pcgHash(uint(pattern)))));
    return float(h) / 4294967296.0;
}

// ---- 四分木 --------------------------------------------------------------

// 点 p を含む葉のセルを、根から順に分割の判定をたどって求める。
// cellMin にはセルの左下の角、size には 1 辺の長さ、戻り値には深さを返す
int quadtreeLeaf(vec2 p, float pattern, out vec2 cellMin, out float size)
{
    size = ROOT_SIZE;
    cellMin = floor(p / size) * size;
    int depth = 0;
    for (; depth < MAX_DEPTH; depth++) {
        // 深いほど分割しにくくする。セルの位置は最小のセルの大きさを単位とする整数
        vec2 key = cellMin / (ROOT_SIZE / exp2(float(MAX_DEPTH)));
        float splitProbability = 0.85 - 0.12 * float(depth);
        if (hashCell(key, depth, pattern) > splitProbability) {
            break;
        }
        // 4 つの子のうち、p を含む子に進む
        size *= 0.5;
        cellMin += step(cellMin + size, p) * size;
    }
    return depth;
}

// ---- メイン --------------------------------------------------------------

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 p = 2.0 * fragCoord / iResolution.y;   // 縦方向が 0〜2
    float pattern = floor(0.25 * iTime);         // 4 秒ごとに模様を変える

    vec2 cellMin;
    float size;
    int depth = quadtreeLeaf(p, pattern, cellMin, size);

    // セルの中の局所座標 (-1〜1)。深さに応じて色を変え、角の丸い正方形を描く
    vec2 local = (p - cellMin) / size * 2.0 - 1.0;
    float t = float(depth) / float(MAX_DEPTH);
    vec3 col = 0.55 + 0.4 * cos(6.2831853 * (0.6 * t + vec3(0.0, 0.33, 0.67)));
    vec2 q = abs(local) - (0.8 - 0.2);
    float box = length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - 0.2;
    // 境界の幅を画面上で一定にするため、局所座標での幅をセルの大きさで割る
    float edge = 2.0 / (size * iResolution.y);
    col *= smoothstep(0.0, 2.0 * edge, -box);
    col = mix(vec3(0.05), col, smoothstep(0.0, edge, -box));

    fragColor = vec4(col, 1.0);
}
