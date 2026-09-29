// 第 8 章：テクスチャーを貼り、UV 座標を時間とともにずらしてスクロールさせるシェーダー。
Shader "Introduction/Chapter08/TextureScroll"
{
    Properties
    {
        // [MainTexture] を付けると、
        // C# の Material.mainTexture でこのテクスチャーを読み書きできる
        [MainTexture] _BaseMap ("Base Map", 2D) = "white" {}
        [MainColor] _BaseColor ("Base Color", Color) = (1, 1, 1, 1)
        // 1 秒あたりに UV 座標をずらす量（x：横方向、y：縦方向）
        _ScrollSpeed ("Scroll Speed", Vector) = (0.1, 0, 0, 0)
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
            Name "Unlit"
            Tags { "LightMode" = "UniversalForward" }

            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment Frag

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float2 uv : TEXCOORD0; // メッシュの UV 座標
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float2 uv : TEXCOORD0;
            };

            // テクスチャーとサンプラーは定数バッファーの外で宣言する
            TEXTURE2D(_BaseMap);
            SAMPLER(sampler_BaseMap);

            CBUFFER_START(UnityPerMaterial)
                // テクスチャー名 + _ST には、
                // Inspector の Tiling（xy）と Offset（zw）が入る
                float4 _BaseMap_ST;
                half4 _BaseColor;
                float4 _ScrollSpeed;
            CBUFFER_END

            Varyings Vert(Attributes input)
            {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                // Tiling と Offset を適用したあと、
                // 経過時間（_Time.y、単位は秒）に比例して UV をずらす
                output.uv = TRANSFORM_TEX(input.uv, _BaseMap) + _ScrollSpeed.xy * _Time.y;
                return output;
            }

            half4 Frag(Varyings input) : SV_Target
            {
                half4 texColor = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, input.uv);
                return texColor * _BaseColor;
            }
            ENDHLSL
        }
    }
}
