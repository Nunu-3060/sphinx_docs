// 07_color.frag
// 第 7 章: 色の設計。上から順に次の 6 本の帯を表示する。
//   1. HSV の色相を 0〜1 で変化させたもの
//   2. 余弦関数によるパレット (虹色)
//   3. 余弦関数によるパレット (2 のパラメーター c と d を変えたもの)
//   4. 黄から青への補間: 表示用の値 (sRGB) のまま補間
//   5. 黄から青への補間: 線形な RGB で補間
//   6. 黄から青への補間: Oklab で補間
// 色は表示用の値 (sRGB) で指定して出力するので、最後のガンマ補正は行わない。

// ---- HSV -----------------------------------------------------------------

// HSV (色相、彩度、明度。すべて 0〜1) を RGB に変換する
vec3 hsv2rgb(vec3 c)
{
    vec3 rgb = clamp(abs(mod(6.0 * c.x + vec3(0.0, 4.0, 2.0), 6.0) - 3.0) - 1.0,
                     0.0, 1.0);
    return c.z * mix(vec3(1.0), rgb, c.y);
}

// ---- 余弦関数によるパレット ----------------------------------------------

// t (0〜1) に対して a + b cos(2π (c t + d)) を RGB ごとに計算する
vec3 cosinePalette(float t, vec3 a, vec3 b, vec3 c, vec3 d)
{
    return a + b * cos(6.2831853 * (c * t + d));
}

// ---- 色空間の変換 --------------------------------------------------------

vec3 srgbToLinear(vec3 c)
{
    return pow(c, vec3(2.2));
}

vec3 linearToSrgb(vec3 c)
{
    return pow(c, vec3(1.0 / 2.2));
}

// 線形な sRGB を Oklab (L: 明度、a: 緑〜赤、b: 青〜黄) に変換する (Ottosson, 2020)
vec3 linearToOklab(vec3 c)
{
    vec3 lms = vec3(dot(c, vec3(0.4122214708, 0.5363325363, 0.0514459929)),
                    dot(c, vec3(0.2119034982, 0.6806995451, 0.1073969566)),
                    dot(c, vec3(0.0883024619, 0.2817188376, 0.6299787005)));
    lms = pow(lms, vec3(1.0 / 3.0));
    return vec3(dot(lms, vec3(0.2104542553, 0.7936177850, -0.0040720468)),
                dot(lms, vec3(1.9779984951, -2.4285922050, 0.4505937099)),
                dot(lms, vec3(0.0259040371, 0.7827717662, -0.8086757660)));
}

// Oklab を線形な sRGB に戻す
vec3 oklabToLinear(vec3 lab)
{
    vec3 lms = vec3(dot(lab, vec3(1.0, 0.3963377774, 0.2158037573)),
                    dot(lab, vec3(1.0, -0.1055613458, -0.0638541728)),
                    dot(lab, vec3(1.0, -0.0894841775, -1.2914855480)));
    lms = lms * lms * lms;
    return vec3(dot(lms, vec3(4.0767416621, -3.3077115913, 0.2309699292)),
                dot(lms, vec3(-1.2684380046, 2.6097574011, -0.3413193965)),
                dot(lms, vec3(-0.0041960863, -0.7034186147, 1.7076147010)));
}

// ---- メイン --------------------------------------------------------------

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 uv = fragCoord / iResolution.xy;
    float t = uv.x;
    int row = int(6.0 * (1.0 - uv.y));   // 上から 0, 1, ..., 5

    // 補間の両端の色 (表示用の値)
    const vec3 yellow = vec3(1.0, 0.85, 0.1);
    const vec3 blue = vec3(0.1, 0.2, 0.9);

    vec3 col;
    if (row == 0) {
        col = hsv2rgb(vec3(t, 0.8, 0.9));
    } else if (row == 1) {
        col = cosinePalette(t, vec3(0.5), vec3(0.5), vec3(1.0),
                            vec3(0.0, 0.33, 0.67));
    } else if (row == 2) {
        col = cosinePalette(t, vec3(0.5), vec3(0.5), vec3(1.0, 1.0, 0.5),
                            vec3(0.8, 0.9, 0.3));
    } else if (row == 3) {
        col = mix(yellow, blue, t);
    } else if (row == 4) {
        col = linearToSrgb(mix(srgbToLinear(yellow), srgbToLinear(blue), t));
    } else {
        vec3 a = linearToOklab(srgbToLinear(yellow));
        vec3 b = linearToOklab(srgbToLinear(blue));
        col = linearToSrgb(max(oklabToLinear(mix(a, b, t)), 0.0));
    }

    // 帯の境界線
    col *= step(0.02, fract(6.0 * uv.y));
    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
