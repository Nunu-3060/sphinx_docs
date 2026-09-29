// 第 13 章：頂点シェーダーで頂点を上下に動かし、波打つ表面を作るシェーダー。
// 頂点の多いメッシュ（Plane など）に使う。
Shader "Introduction/Chapter13/Wave"
{
    Properties
    {
        [MainColor] _BaseColor ("Base Color", Color) = (0.2, 0.5, 1, 1)
        // 波の高さ（オブジェクト空間の単位）
        _Amplitude ("Amplitude", Float) = 0.3
        // 1 単位の距離あたりの波の数（値が大きいほど波が細かくなる）
        _Frequency ("Frequency", Float) = 2
        // 波の進む速さ
        _Speed ("Speed", Float) = 2
    }

    SubShader
    {
        Tags
        {
            "RenderType" = "Opaque"
            "Queue" = "Geometry"
            "RenderPipeline" = "UniversalPipeline"
        }

        Pass
        {
            Name "Wave"
            Tags { "LightMode" = "UniversalForward" }

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 normalWS : TEXCOORD0;
            };

            CBUFFER_START(UnityPerMaterial)
                half4 _BaseColor;
                float _Amplitude;
                float _Frequency;
                float _Speed;
            CBUFFER_END

            Varyings Vert(Attributes input)
            {
                Varyings output;
                float3 positionOS = input.positionOS.xyz;

                // x 座標と時間から、正弦波（sin）で y 方向の変位を求める
                float phase = positionOS.x * _Frequency + _Time.y * _Speed;
                positionOS.y += sin(phase) * _Amplitude;

                // 頂点を動かすと元の法線は使えなくなるため、
                // 波の傾きから法線を計算し直す。
                // y = A sin(fx + st) の x での微分は A f cos(fx + st) なので、
                // 接線は (1, A f cos, 0)、法線はそれに垂直な (-A f cos, 1, 0) になる。
                float slope = _Amplitude * _Frequency * cos(phase);
                float3 normalOS = normalize(float3(-slope, 1.0, 0.0));

                output.positionCS = TransformObjectToHClip(positionOS);
                output.normalWS = TransformObjectToWorldNormal(normalOS);
                return output;
            }

            half4 Frag(Varyings input) : SV_Target
            {
                float3 normalWS = normalize(input.normalWS);
                Light mainLight = GetMainLight();

                half3 ambient = SampleSH(normalWS) * _BaseColor.rgb;
                half nDotL = saturate(dot(normalWS, mainLight.direction));
                half3 diffuse = _BaseColor.rgb * mainLight.color * nDotL;

                return half4(ambient + diffuse, 1.0);
            }
            ENDHLSL
        }
    }
}
