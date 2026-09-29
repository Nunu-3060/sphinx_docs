// 第 14 章：ノイズを使って、
// オブジェクトが燃え尽きるように消えていく（ディゾルブ）シェーダー。
Shader "Introduction/Chapter14/Dissolve"
{
    Properties
    {
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
        // 0 で消えている部分なし、1 ですべて消える
        _Threshold ("Threshold", Range(0, 1)) = 0.3
        // 消える境目を光らせる幅
        _EdgeWidth ("Edge Width", Range(0, 0.2)) = 0.05
        [HDR] _EdgeColor ("Edge Color", Color) = (4, 1.5, 0.3, 1)
        // ノイズの細かさ（UV 座標に掛ける値）
        _NoiseScale ("Noise Scale", Float) = 10
    }

    SubShader
    {
        Tags
        {
            "RenderType" = "TransparentCutout"
            "Queue" = "AlphaTest"
            "RenderPipeline" = "UniversalPipeline"
        }

        Pass
        {
            Name "Dissolve"
            Tags { "LightMode" = "UniversalForward" }

            // 消えた部分から内側（裏面）が見えるため、裏面も描画する
            Cull Off

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
                float2 uv : TEXCOORD0;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 normalWS : TEXCOORD0;
                float2 uv : TEXCOORD1;
            };

            CBUFFER_START(UnityPerMaterial)
                half4 _BaseColor;
                half _Threshold;
                half _EdgeWidth;
                half4 _EdgeColor;
                float _NoiseScale;
            CBUFFER_END

            // 2 次元の座標から、0 ～ 1 の疑似乱数を作る
            float Hash(float2 p)
            {
                return frac(sin(dot(p, float2(12.9898, 78.233))) * 43758.5453);
            }

            // バリューノイズ：格子点ごとの乱数を、滑らかに補間したノイズ
            float ValueNoise(float2 uv)
            {
                float2 cell = floor(uv); // 格子の番号
                float2 local = frac(uv); // 格子の中での位置（0 ～ 1）

                // 格子の四隅の乱数
                float a = Hash(cell);
                float b = Hash(cell + float2(1.0, 0.0));
                float c = Hash(cell + float2(0.0, 1.0));
                float d = Hash(cell + float2(1.0, 1.0));

                // 3t^2 - 2t^3 で補間の重みを滑らかにし、格子の境目が目立たないようにする
                float2 t = local * local * (3.0 - 2.0 * local);
                return lerp(lerp(a, b, t.x), lerp(c, d, t.x), t.y);
            }

            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                output.normalWS = TransformObjectToWorldNormal(input.normalOS);
                output.uv = input.uv;
                return output;
            }

            half4 Frag(Varyings input, bool isFrontFace : SV_IsFrontFace) : SV_Target
            {
                float noise = ValueNoise(input.uv * _NoiseScale);

                // ノイズの値がしきい値より小さいピクセルを破棄する
                clip(noise - _Threshold);

                // 裏面では法線を反転し、内側にもライティングが正しく当たるようにする
                float3 normalWS = normalize(input.normalWS) * (isFrontFace ? 1.0 : -1.0);
                Light mainLight = GetMainLight();
                half3 ambient = SampleSH(normalWS) * _BaseColor.rgb;
                half nDotL = saturate(dot(normalWS, mainLight.direction));
                half3 diffuse = _BaseColor.rgb * mainLight.color * nDotL;

                // しきい値のすぐ上（消える境目）ほど edge が 1 に近づく。
                // しきい値が 0 のときは何も消えていないため、境目も光らせない。
                half edge = 1.0 - smoothstep(0.0, _EdgeWidth, noise - _Threshold);
                edge *= step(0.001, _Threshold);

                half3 color = lerp(ambient + diffuse, _EdgeColor.rgb, edge);
                return half4(color, 1.0);
            }
            ENDHLSL
        }
    }
}
